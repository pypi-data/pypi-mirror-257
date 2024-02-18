# TimeScale DB Manger

[![CI](https://github.com/Algo-Trading-Tools/timescale-db-manager/actions/workflows/ci.yaml/badge.svg)](https://github.com/Algo-Trading-Tools/timescale-db-manager/actions/workflows/ci.yaml)


A python package that manages timescale db interactions.

Things Like:
* Export to CSV
* Import from CSV
* Compress and backup to S3
* Sync from one database to another

There are also specific database types implemented:
* `cryptofeed`

These handle creating and initializing these database types with their tables.