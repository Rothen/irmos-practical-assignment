import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Float
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TIMESTAMP

postgresql_url = 'postgresql://irmos:pwd123@localhost:5432/actual_bridge'
engine = create_engine(postgresql_url)
connection = engine.connect()

csv_data = pd.read_csv('midspan_data.csv', parse_dates=['time'])

csv_data['time'] = pd.to_datetime(csv_data['time'], utc=True, format='ISO8601')

csv_data.to_sql(
    'midspan',
    con=engine,
    if_exists='replace',
    index=False,
    dtype={
        'ts': PG_TIMESTAMP(timezone=True),
        'Fat_cycle_bot': Float,
        'Pos_na': Float
    }
)
