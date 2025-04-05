import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reference environment variables
current_file_path = os.getenv('LOCAL_FILE_PATH')

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
        finance_table_name = 'raw__finance'


        rhythm_file_name = f'{rhythm_table_name}.csv'
        gym_file_name = f'{gym_table_name}.csv'
        professional_file_name = f'{professional_table_name}.csv'
        finance_file_name = 'all_clean_data_spend.csv'


        # Connect to PostgreSQL
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        engine.connect()

        # Path to the rhythm files
        src_dir = os.path.abspath(os.path.join(current_file_path, 'data', 'raw_data', 'raw_rhythm_data'))

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


        # Path to the finance files
        finance_dir = os.path.abspath(os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'clean_data_spend'))

        # Load finance data
        finance_file_path = os.path.join(finance_dir, finance_file_name)
        finance_df = pd.read_csv(finance_file_path, low_memory=False)
        finance_df.to_sql(name=finance_table_name, con=engine, if_exists='replace')

        print(f'Finance data replaced in PostgreSQL')