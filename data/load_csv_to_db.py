import pandas as pd
from sqlalchemy import create_engine

postgresql_url = 'postgresql://irmos:pwd123@db:5432/actual_bridge'
engine = create_engine(postgresql_url)
connection = engine.connect()

csv_data = pd.read_csv('midspan_data.csv')
