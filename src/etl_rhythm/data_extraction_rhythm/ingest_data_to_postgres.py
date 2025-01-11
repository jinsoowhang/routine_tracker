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


        rhythm_table_name = 'raw__rhythm'
        gym_table_name = 'raw__gym'
        professional_table_name = 'raw__professional'


        rhythm_file_name = f'{rhythm_table_name}.csv'
        gym_file_name = f'{gym_table_name}.csv'
        professional_file_name = f'{professional_table_name}.csv'


        # download the csv


        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


        engine.raw_connection()


        # Get the absolute path to the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))


        # Path to the source directory
        src_dir = os.path.abspath(os.path.join(script_dir, '..', '..', '..', 'data', 'raw_data', 'raw_rhythm_data'))


        # Load rhythm data
        rhythm_file_path = os.path.join(src_dir, rhythm_file_name)
        rhythm_df = pd.read_csv(rhythm_file_path, low_memory=False)
        rhythm_df.to_sql(name=rhythm_table_name, con=engine, if_exists='replace')


        # Load gym data
        gym_file_path = os.path.join(src_dir, gym_file_name)
        gym_df = pd.read_csv(gym_file_path, low_memory=False)
        gym_df.to_sql(name=gym_table_name, con=engine, if_exists='replace')


        # Load professional data
        professional_file_path = os.path.join(src_dir, professional_file_name)
        professional_df = pd.read_csv(professional_file_path, low_memory=False)
        professional_df.to_sql(name=professional_table_name, con=engine, if_exists='replace')


        print(f'Rhythm data replaced in PostgreSQL')