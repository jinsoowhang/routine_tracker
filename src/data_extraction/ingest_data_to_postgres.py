import os 
import pandas as pd
from sqlalchemy import create_engine

class IngestDataToPostgres():

    def ingest_data_to_postgres(self, params):
        user = params.user 
        password = params.password
        host = params.host 
        port = params.port
        db = params.db
        table_name = params.table_name

        csv_name = 'raw_rhythm.csv'

        # download the csv

        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

        engine.connect()

        # Get the absolute path to the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Path to the source directory
        src_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'data', 'raw_data', csv_name))

        df = pd.read_csv(src_dir, low_memory=False)

        df.to_sql(name=table_name, con=engine, if_exists='replace')

