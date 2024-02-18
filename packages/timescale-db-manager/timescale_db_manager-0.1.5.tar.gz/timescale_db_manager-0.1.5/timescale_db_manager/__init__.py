import os
import sys
import glob
import time
import boto3
import shutil
import logging
import psycopg2
import subprocess
import pandas as pd
from typing import List
from pathlib import Path
from typing import Literal
from urllib.parse import unquote_plus
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone, timedelta
from timescale_db_manager.utilities import time_it

logger = logging.getLogger(__name__)


class TimeScaleDBManager:
    def __init__(
            self,
            db_name: str,
            environment: str,
            root_folder: Path = Path('/tmp/data-archives').absolute(),
            app_name: str = 'tickerdax-data-api',
            user: str | None = None,
            password: str | None = None,
            host: str | None = None,
            port: str | None = None,
            aws_region: str | None = None,
            use_private_ips: bool = False,
            ignore_tables: list | None = None
        ) -> None:
        self.db_name = db_name
        self.environment = environment.lower()
        self.root_folder = root_folder
        self.app_name = app_name
        self._ignore_tables = ignore_tables
        if not self._ignore_tables:
            self._ignore_tables = []

        self.local_folder = self.root_folder / 'db_backups'
        self.csv_folder = self.local_folder / 'csv' / self.db_name / self.environment
        self.raw_folder = self.local_folder / 'raw' / self.db_name / self.environment
        self.bucket_folder = f"s3://{self.app_name}-{self.environment}-backups/"


        self._user = user or os.environ[f'{self.db_name.upper()}_DB_{self.environment.upper()}_USER']
        self._password = password or os.environ[f'{self.db_name.upper()}_DB_{self.environment.upper()}_PASSWORD']
        self._host = host or os.environ[f'{self.db_name.upper()}_DB_{self.environment.upper()}_HOST']
        self._port = port or '5432'

        self._use_private_ips = use_private_ips
        self._temp_prefix = 'tmp_import_'
        self._aws_region = aws_region or os.environ['AWS_REGION']
        self._start_of_data = datetime(year=2023, month=1, day=1, tzinfo=timezone.utc)
        self._date_format = '%Y-%m-%d %H:%M:%S'
        self._file_date_format = '%Y-%m-%d_%H_%M_%S'

        self._aws_session = boto3.Session(region_name=self._aws_region)
        self._ec2_client = self._aws_session.client('ec2', self._aws_region)
        self._s3_client = self._aws_session.client('s3', self._aws_region)

        self._s3_data = {}
        self._private_ips = {}
        if self._use_private_ips:
            self._private_ips = self.get_private_ips()

        # metrics
        self.total_csv_backup_size = {}
        self.total_zip_backup_size = {}
        self.start_export_csv = None 
        self.end_export_csv = None
        self.start_import_csv = None 
        self.end_import_csv = None
        self.start_compress = None
        self.end_compress = None
        self.start_sync_to_s3 = None
        self.end_sync_to_s3 = None
        self.start_sync_from_s3 = None
        self.end_sync_from_s3 = None

        # calculate the max number of s3 files
        self._tables = self.get_all_tables()
        self._max_keys = len(self._tables) * 24 * (datetime.now(tz=timezone.utc) - self._start_of_data).days
        self._existing_s3_data = self.get_existing_s3_data()

        # create the database if it does not already exist
        self._create_database()


    def _post_actions(
            self,
            sync_to_s3: bool,
            clean_up_disk_location: str | None,
        ):
        # sync the files to s3
        if sync_to_s3:
            _, folder_size_string = self.get_size_on_disk(self.csv_folder, unit='GB')
            logger.info(f'Uploading {folder_size_string} to S3')
            self.sync_to_s3()

        # remove all the local files
        if clean_up_disk_location:
            self.clean_up_disk(location=clean_up_disk_location)

    def _create_database(self):
        with self.db_cursor(database=False) as cursor:
            try:
                cursor.execute(f"CREATE DATABASE {self.db_name};")
            except psycopg2.errors.DuplicateDatabase as error:
                logger.warning(error)
            cursor.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")

    def create_table(
            self, 
            table_name: str,
            schema: str,
            retention_policy_days: int = 60,
            compression_interval_days: int = 7
        ):
        with self.db_cursor() as cursor:
            logger.info(f'Creating table "{table_name}"...')

            create_table_command = f'CREATE TABLE IF NOT EXISTS public.{table_name} {schema}'

            cursor.execute(
                f"{create_table_command};\n"
                # make it a hypertable
                f"SELECT create_hypertable('{table_name}', 'timestamp', if_not_exists => TRUE);\n"
                # add a retention policy so it does not fill up data indefinitely
                f"SELECT add_retention_policy('{table_name}', INTERVAL '{retention_policy_days} days', if_not_exists => TRUE);\n"
                # TODO add a compression policy after the first week
                f"ALTER TABLE {table_name} SET (timescaledb.compress);\n"
                f"SELECT add_compression_policy('{table_name}', INTERVAL '{compression_interval_days} days');"
            )
            if table_name not in self._tables:
                self._tables.append(table_name)


    def db_cursor(
            self,
            database: str | None | bool = None,
            user: str | None = None,
            password: str | None = None,
            host: str | None = None,
            port: str | None = None
        ):
        database = database or self.db_name
        user = user or self._user
        password = password or self._password
        host = host or self._host
        port = port or self._port

        # convert to private ip if available
        host = self._private_ips.get(host, host)

        kwargs = {
            'database': database,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        if database is False:
            kwargs.pop('database')

        postgres_connection = psycopg2.connect(**kwargs)
        postgres_connection.autocommit = True

        # Creating a cursor object using the cursor() method
        return postgres_connection.cursor(cursor_factory=RealDictCursor)

    def get_all_tables(self) -> List:
        with self.db_cursor() as cursor:
            # run sql query
            logger.info('starting sql query...')
            start = time.time()
            cursor.execute(
                """
                SELECT * FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                """
            )
            end = time.time()
            logger.info(f'sql query finished in {round(end - start, 2)} secs')
            return [i['table_name'] for i in cursor.fetchall() if not i['table_name'].startswith(self._temp_prefix) and i['table_name'] not in self._ignore_tables]

    def get_table_hourly_time_ranges(
            self,
            start: datetime,
            end: datetime,
    ) -> list:
        truncated_start = datetime(
            year=start.year,
            month=start.month,
            day=start.day,
            hour=start.hour,
            tzinfo=timezone.utc
        )
        truncated_end = datetime(
            year=end.year,
            month=end.month,
            day=end.day,
            hour=end.hour,
            tzinfo=timezone.utc
        )
        table_time_ranges = []

        for table_name in self._tables:
            for hour_timestamp in pd.period_range(
                start=truncated_start,
                end=truncated_end,
                freq='h'
            ).to_timestamp().tz_localize('utc'):
                hour_start = hour_timestamp.to_pydatetime()

                if hour_start == truncated_end:
                    break

                table_time_ranges.append((table_name, hour_start, hour_start + timedelta(hours=1)))

        return table_time_ranges

    @staticmethod
    def get_size_on_disk(path, unit: Literal['MB', 'GB'] = 'MB'):
        if unit == 'GB':
            size = os.stat(path).st_size / 1024 / 1024 / 1024
            return size, f'{round(size, 4)} GB'
        if unit == 'MB':
            size = os.stat(path).st_size / 1024 / 1024
            return size, f'{round(size, 4)} MB'

    @staticmethod
    def shell(
            command: str, 
            error_message: str, 
            **kwargs
        ):
        process = subprocess.Popen(
            command,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kwargs
        )

        output = []
        for line in iter(process.stdout.readline, ""):  # type: ignore
            output += [line.rstrip()]
            sys.stdout.write(line)

        process.wait()
        sys.stdout.flush()

        if process.returncode != 0:
            raise OSError(f"{error_message}\n" + "\n".join(output))
        
    @time_it
    def compress(
            self, 
            file_path: Path
        ) -> Path:
        table_name = file_path.parent.parent.name

        zip_folder = os.path.dirname(file_path)
        zip_file_path = f'{zip_folder}.zip'
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)

        logger.info(f'Compressing "{file_path}" to zip "{zip_file_path}"')
        zip_file_path = shutil.make_archive(
            base_name=zip_folder, 
            format='zip', 
            root_dir=zip_folder,
            base_dir='.'
        )
        csv_size, csv_size_string = self.get_size_on_disk(file_path, unit='MB')
        zip_size, zip_size_string = self.get_size_on_disk(zip_file_path, unit='MB')

        self.total_csv_backup_size[table_name] = self.total_csv_backup_size.get(table_name, 0)
        self.total_csv_backup_size[table_name] += csv_size

        self.total_zip_backup_size[table_name] = self.total_zip_backup_size.get(table_name, 0)
        self.total_zip_backup_size[table_name] += zip_size

        percent = round((1 - (zip_size / csv_size)) * 100)
        logger.info(f'The csv file size is {csv_size_string} and zip file size is {zip_size_string}. Size was reduced by {percent}%.')
        logger.info(f'Removing "{zip_folder}" to save disk space.')
        shutil.rmtree(zip_folder)
        return Path(zip_file_path).absolute()

    def clean_up_disk(self, location: Literal['csv', 'raw']):
        if location == 'csv':
            logger.info(f'Removing local csv files from "{self.csv_folder}" to save disk space.')
            shutil.rmtree(self.csv_folder)

        elif location == 'raw':
            # remove all the local csv files
            logger.info(f'Removing local dump files from "{self.raw_folder}" to save disk space.')
            shutil.rmtree(self.raw_folder)

    @time_it
    def export_csv(
            self,
            table_name: str,
            start: datetime,
            end: datetime,
            server_folder_path: str,
            compress: bool = True
    ):
        # convert datetime to string
        start_string = start.strftime(self._date_format)
        end_string = end.strftime(self._date_format)

        file_name = start_string.replace(' ', '_').replace(':', '_')
        file_path = os.path.join(server_folder_path, table_name, file_name, f"{file_name}.csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # convert to private ip if available
        host = self._private_ips.get(self._host, self._host)

        cli_commands = f'PGPASSWORD={self._password} psql -h {host} -U {self._user} -d {self.db_name} -c '
        sql_commands = f"\copy (SELECT * FROM public.{table_name} WHERE timestamp BETWEEN '{start_string}' AND '{end_string}') TO '{file_path}' csv header;"

        self.shell(
            f'{cli_commands} "{sql_commands}"',
            error_message=f'Failed to export {table_name} data from {start_string} to {end_string}'
        )

        if compress:
            return self.compress(Path(file_path))
        
        return file_path

    @time_it
    def import_csv(
            self,
            file_path: str,
            table_name: str,
            db_name: str | None = None,
            user: str | None = None,
            password: str | None = None,
            host: str | None = None,
            port: str | None = None
    ):
        _db_name = db_name or self.db_name
        _user = user or self._user
        _host = host or self._host
        _password = password or self._password
        _port = port or self._port

        # convert to private ip if available
        _host = self._private_ips.get(_host, _host)

        cli_commands = f'PGPASSWORD="{_password}" psql -h {_host} -p {_port} -U {_user} -d {_db_name} -c '
        tmp_table_name = f'{self._temp_prefix}{table_name}'

        # use the correct copy command, depending on if this is copying to a local server or a remote server
        copy_command = 'COPY'
        if _host != self._host:
            copy_command = r'\copy'

        with self.db_cursor(
            database=_db_name,
            user=_user,
            host=_host,
            password=_password,
            port=_port
        ) as cursor:
            # create a temp table like the one we will import to
            cursor.execute(
                f"""
                DROP TABLE IF EXISTS {tmp_table_name};
                CREATE TABLE {tmp_table_name} (LIKE public.{table_name} INCLUDING ALL);
                """
            )

            # copy the csv into the temp table
            sql_commands = f"{copy_command} {tmp_table_name} FROM '{file_path}' WITH CSV HEADER;"
            self.shell(
                f'{cli_commands} "{sql_commands}"',
                error_message=f'Failed to import "{file_path}" into table "{table_name}".'
            )

            # then insert the temp table into the main table and remove the temp table
            cursor.execute(
                f"""
                INSERT INTO public.{table_name} SELECT * FROM {tmp_table_name} ON CONFLICT (timestamp) DO NOTHING;
                DROP TABLE {tmp_table_name};
                """
            )

    @time_it
    def sync_to_s3(self):
        _, size_string = self.get_size_on_disk(self.local_folder, unit='GB')
        logger.info(f'Starting sync of {size_string} from "{self.local_folder}" to "{self.bucket_folder}"...')

        chunks = self.bucket_folder.replace('s3://', '').split('/')
        bucket_name = chunks[0]
        local_file_paths = [Path(i) for i in glob.glob(f'{self.local_folder}/**/*', recursive=True) if Path(i).is_file()]


        for local_file in local_file_paths:
            # convert the local path to an s3 path
            parts = [i for i in local_file.parts if i not in self.local_folder.parts]
            bucket_path = '/'.join(parts)

            _, size_string = self.get_size_on_disk(local_file, unit='MB')
            logger.info(f'Uploading {size_string} "{local_file}" to "s3://{bucket_name}/{bucket_path}"...')
            with open(local_file, 'rb') as file:
                self._s3_client.upload_fileobj(
                    file,
                    bucket_name,
                    bucket_path
                )

        # self.shell(
        #     f"aws s3 --region {self._aws_region} sync {self.local_folder} {self.bucket_folder}",
        #     error_message=f'Failed to sync folder path {self.local_folder} to bucket path {self.bucket_folder}'
        # )

    def get_existing_s3_data(self):
        mapping = {}
        chunks = self.bucket_folder.replace('s3://', '').split('/')
        bucket_name = chunks[0]
        folder_root = Path(*[part for part in self.local_folder.parts if part not in chunks[1:]])

        response = self._s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=self._max_keys)
        for s3_object in response['Contents']:
            file_path = folder_root / s3_object['Key'].replace(' ', '_').replace(':', '-')
            table_name = file_path.parent.name
            
            try:
                timestamp = datetime.strptime(file_path.with_suffix('').name, self._file_date_format)
            except ValueError:
                timestamp = None

            if timestamp and file_path.suffix == '.zip':
                mapping[table_name] = mapping.get(table_name, {})
                mapping[table_name][timestamp.strftime(self._date_format)] = {
                    'bucket_name': bucket_name,
                    'bucket_folder': unquote_plus(s3_object['Key']),
                    'table_name': file_path.parent.name,
                    'timestamp': timestamp,
                    'file_path': file_path
                }

        return mapping


    def sync_from_s3(self):
        logger.info(f'Syncing from {self.bucket_folder} to {self.local_folder}')
        for data in self._existing_s3_data.values():
            file_path = data['file_path']
            bucket_name = data['bucket_name']
            bucket_folder = data['bucket_folder']

            if not file_path.exists():
                logger.info(f'Downloading "s3://{bucket_name}/{bucket_folder}" to "{file_path}"')
                self._s3_client.download_file(
                    data['bucket_name'], 
                    data['bucket_folder'], 
                    str(file_path)
                )

    # Todo make sure this still works
    def backup(self):
        for table_name in self.get_all_tables():
            today_string = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
            file_path = os.path.join(self.raw_folder, table_name, f'{today_string}.dump')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            logger.info(f"Saving table {table_name}")
            self.shell(
                command=' '.join([
                "pg_dump",
                "--no-owner",
                f"--dbname=postgresql://{self._user}:{self._password}@{self._host}:5432/{self.db_name}",
                "--table",
                f"public.{table_name}",
                "--format",
                "custom",
                "--verbose",
                "--file",
                file_path
                ]),
                error_message=f'Failed to backup table {table_name}'
            )
            logger.info(f"Finished saving table to {file_path}")

        # sync the dump files to s3
        self.sync_to_s3()

    def backup_csv_files(
            self,
            start: datetime,
            end: datetime,
            sync_to_s3: bool = True,
            clean_up_disk: bool = True
        ) -> dict:
        back_ups = {}

        hourly_time_ranges = self.get_table_hourly_time_ranges(
            start=start,
            end=end
        )
        total = len(hourly_time_ranges)

        for index, (table_name, start_hour, end_hour) in enumerate(hourly_time_ranges):
            hour_string = start_hour.strftime(self._date_format)
            if not self._existing_s3_data.get(table_name, {}).get(hour_string):
                logger.info(f"Saving ({index+1}/{total}) table {table_name} for hour {hour_string}")
                file_path = self.export_csv(
                    table_name=table_name,
                    start=start_hour,
                    end=end_hour,
                    server_folder_path=self.csv_folder,
                    compress=True
                )
                logger.info(f"Finished saving hour {hour_string} for table {table_name} to {file_path}")
                back_ups[table_name] = back_ups.get(table_name, [])
                back_ups[table_name].append(file_path)
            else:
                logger.info(f'Skipping backup of ({index+1}/{total}) table {table_name} for hour {hour_string}, since it already exists.')

        self._post_actions(
            sync_to_s3=sync_to_s3,
            clean_up_disk_location= 'csv' if clean_up_disk else None
        )
        
        return back_ups

    def synchronize_and_backup_csv_files(
            self,
            start: datetime,
            end: datetime,
            to_db_name: str,
            to_environment: str,
            to_user: str | None = None,
            to_password: str | None = None,
            to_host: str | None = None,
            to_port: str | None = None,
            sync_to_s3: bool = True,
            clean_up_disk: bool = True
        ):
        back_ups = {}
        user = to_user or os.environ[f'{to_db_name.upper()}_DB_{to_environment.upper()}_USER']
        password = to_password or os.environ[f'{to_db_name.upper()}_DB_{to_environment.upper()}_PASSWORD']
        host = to_host or os.environ[f'{to_db_name.upper()}_DB_{to_environment.upper()}_HOST']
        port = to_port or '5432'

        hourly_time_ranges = self.get_table_hourly_time_ranges(
            start=start,
            end=end
        )
        total = len(hourly_time_ranges)

        for index, (table_name, start_hour, end_hour) in enumerate(hourly_time_ranges):
            hour_string = start_hour.strftime(self._date_format)
            if not self._existing_s3_data.get(table_name, {}).get(hour_string):
                logger.info(f"Saving ({index+1}/{total}) table {table_name} for hour {hour_string}")

                # export as a csv from current database
                file_path = self.export_csv(
                    table_name=table_name,
                    start=start_hour,
                    end=end_hour,
                    server_folder_path=self.csv_folder,
                    compress=False
                )
                logger.info(f"Finished saving hour {hour_string} for table {table_name} to {file_path}")

                # import into the next database from a the csv
                logger.info(f"Importing hour {hour_string} for table {table_name} to database {to_db_name} {to_environment}")
                self.import_csv(
                    file_path=file_path,
                    table_name=table_name,
                    db_name=to_db_name,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )

                back_ups[table_name] = back_ups.get(table_name, [])
                back_ups[table_name].append(file_path)
            else:
                logger.info(f'Skipping sync and backup of ({index+1}/{total}) table {table_name} for hour {hour_string}, since it already exists.')

        # now compress all tables
        zip_backups = {}
        for table_name, csv_files in back_ups.items():
            zip_backups[table_name] = zip_backups.get(table_name, [])

            for csv_file in csv_files:
                zip_file = self.compress(Path(csv_file))
                zip_backups[table_name].append(zip_file)

        # sync them to s3 and clean up
        self._post_actions(
            sync_to_s3=sync_to_s3,
            clean_up_disk_location= 'csv' if clean_up_disk else None
        )

        return zip_backups

    
    def get_private_ips(self):
        instances = {}
        response = self._ec2_client.describe_instances(MaxResults=500)
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if instance['State']['Name'] == 'running':
                    public_ip = instance.get('PublicIpAddress')
                    if public_ip:
                        instances[public_ip] = instance['PrivateIpAddress']
        return instances
    
    def create_read_only_users(
            self, 
            user_logins: dict[str, str]
        ):
        commands = []
        with self.db_cursor() as cursor:
            for user_name, password in user_logins.items():
                commands.append(
                    f"""
                    DO
                    $do$
                    BEGIN
                       IF EXISTS (
                          SELECT FROM pg_catalog.pg_roles
                          WHERE  rolname = '{user_name}') THEN
                    
                          RAISE NOTICE 'Role "{user_name}" already exists. Skipping.';
                       ELSE
                          CREATE USER "{user_name}" WITH PASSWORD '{password}';
                       END IF;
                    END
                    $do$;
                    """
                )
                for table_name in self._tables:
                    commands.append(f'GRANT SELECT ON TABLE public.{table_name} TO "{user_name}";')
                    logger.info(f'Granting user "{user_name}" read permissions to table "{table_name}"...')

                cursor.execute('\n'.join(commands))
                logger.info(f'Permissions granted to user {user_name} successfully!')

    def print_summary(self, backups):
        total_files = 0
        total_tables = 0
        total_uncompressed_size = 0
        total_compressed_size = 0
        for _, files in backups.items():
            total_files += len(files)
            total_tables += 1

        print('-'*100)
        print('Uncompressed:')
        for table_name, size in self.total_csv_backup_size.items():
            total_uncompressed_size += size 
            print(f'{table_name} {round(size, 2)} MB')
        print('-'*100)
        print('Compressed:')
        for table_name, size in self.total_zip_backup_size.items():
            total_compressed_size += size 
            print(f'{table_name} {round(size, 2)} MB')
        print('-'*100)

        print(f'Backed Up: {total_tables} tables to {total_files} files.')
        print(f'Compression reduced the total backup size of {round(total_uncompressed_size / 1024, 2)} GB to {round(total_compressed_size / 1024, 2)} GB by: {round((1 - (total_compressed_size / total_uncompressed_size)) * 100)}%')

        print('-'*100)
        print('Timing:')
        if self.start_export_csv:
            print(f'Exporting CSVs from tables took: {round(self.end_export_csv-self.start_export_csv, 2)} seconds')

        if self.start_import_csv:
            print(f'Importing CSVs to tables took: {round(self.end_import_csv-self.start_import_csv, 2)} seconds')

        if self.start_compress:
            print(f'Compressing CSVs took: {round(self.end_compress-self.start_compress, 2)} seconds')

        if self.start_sync_to_s3:
            print(f'The sync to S3 took: {round(self.end_sync_to_s3-self.start_sync_to_s3, 2)} seconds')

        if self.start_sync_from_s3:
            print(f'The sync from S3 took: {round(self.end_sync_from_s3-self.start_sync_from_s3, 2)} seconds')
            
        print('-'*100)
        