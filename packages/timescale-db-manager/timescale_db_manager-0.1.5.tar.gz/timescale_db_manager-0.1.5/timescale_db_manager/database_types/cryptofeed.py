import logging
from timescale_db_manager import TimeScaleDBManager

logger = logging.getLogger(__name__)


L2_BOOK = 'l2_book'
TRADES = 'trades'
TICKER = 'ticker'
FUNDING = 'funding'
OPEN_INTEREST = 'open_interest'
LIQUIDATIONS = 'liquidations'
CANDLES = 'candles'



class CryptofeedDBManager(TimeScaleDBManager):
    def __init__(
            self, 
            *args, 
            symbols: list[str],
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)

        self._table_types = []

        for symbol in symbols:
            self._table_types.extend([
                (FUNDING, f'{FUNDING}_futures_{symbol}'.lower().replace("-", "_")),
                (LIQUIDATIONS, f'{LIQUIDATIONS}_futures_{symbol}'.lower().replace("-", "_")),
                (OPEN_INTEREST, f'{OPEN_INTEREST}_futures_{symbol}'.lower().replace("-", "_")),

                (TICKER, f'{TICKER}_futures_{symbol}'.lower().replace("-", "_")),
                (TICKER, f'{TICKER}_spot_{symbol}'.lower().replace("-", "_")),
                (CANDLES, f'{CANDLES}_futures_{symbol}'.lower().replace("-", "_")),
                (CANDLES, f'{CANDLES}_spot_{symbol}'.lower().replace("-", "_")),
                (TRADES, f'{TRADES}_futures_{symbol}'.lower().replace("-", "_")),
                (TRADES, f'{TRADES}_spot_{symbol}'.lower().replace("-", "_")),
                (L2_BOOK, f'{L2_BOOK}_delta_spot_{symbol}'.lower().replace("-", "_")),
                (L2_BOOK, f'{L2_BOOK}_snapshot_spot_{symbol}'.lower().replace("-", "_")),
                (L2_BOOK, f'{L2_BOOK}_delta_futures_{symbol}'.lower().replace("-", "_")),
                (L2_BOOK, f'{L2_BOOK}_snapshot_futures_{symbol}'.lower().replace("-", "_")),
            ])

    def create_tables(
            self, 
            retention_policy_days: int = 60,
            compression_interval_days: int = 7
        ):
        for table_type, table_name in self._table_types:
            schema = None
            if table_type == L2_BOOK:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), data JSONB)'
            elif table_type == TRADES:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), side VARCHAR(8), amount NUMERIC(64, 32), price NUMERIC(64, 32), trade_id VARCHAR(64), order_type VARCHAR(32))'
            elif table_type == OPEN_INTEREST:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), open_interest INTEGER)'
            elif table_type == LIQUIDATIONS:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), side VARCHAR(8), quantity NUMERIC(64, 32), price NUMERIC(64, 32), trade_id VARCHAR(64), status VARCHAR(16))'
            elif table_type == FUNDING:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), mark_price DOUBLE PRECISION, rate DOUBLE PRECISION, next_funding_time TIMESTAMP, predicted_rate DOUBLE PRECISION)'
            elif table_type == CANDLES:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), candle_start TIMESTAMP, candle_stop TIMESTAMP, interval VARCHAR(4), trades INTEGER, open NUMERIC(64, 32), close NUMERIC(64, 32), high NUMERIC(64, 32), low NUMERIC(64, 32), volume NUMERIC(64, 32), closed BOOLEAN)'
            elif table_type == TICKER:
                schema = '(timestamp TIMESTAMP PRIMARY KEY, receipt_timestamp TIMESTAMP, exchange VARCHAR(32), symbol VARCHAR(32), bid NUMERIC(64, 32), ask NUMERIC(64, 32))'

            if schema:
                self.create_table(
                    table_name=table_name,
                    schema=schema,
                    retention_policy_days=retention_policy_days,
                    compression_interval_days=compression_interval_days
                )
            self._tables