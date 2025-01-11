# Import Rhythm Packages
from src.etl_rhythm.data_extraction_rhythm.import_google_sheets import ImportGoogleSheets
from src.etl_rhythm.data_extraction_rhythm.ingest_data_to_postgres import IngestDataToPostgres

# Import Finance Packages
from src.etl_finance.data_extraction_finance.raw_spend_data_extraction import DataExtraction

# Import other Packages
import argparse
import sys
import os
from dotenv import load_dotenv

def main(args):


    ############################################################################
    ######################### EXTRACT RAW FINANCE DATA #########################
    ############################################################################


    current_file_path = os.getenv('LOCAL_FILE_PATH')


    # Initialize Finance Data
    data_extraction = DataExtraction()

    # Concatenate all americanExpress_jinsoo raw spend data
    americanExpress_jinsoo_file_path = os.path.join(current_file_path, "data", "raw_data", "raw_personal_finance_data", "bank_statements", "credit_card_statements", "americanExpress_jinsoo")
    americanExpress_jinsoo_file_name = "americanExpress_jinsoo_raw_spend.csv"
    data_extraction.extract_raw_spend_data(bank_file_path=americanExpress_jinsoo_file_path, file_name=americanExpress_jinsoo_file_name)


    # Concatenate all boa_jinsoo raw spend data
    boa_jinsoo_file_path = os.path.join(current_file_path, "data", "raw_data", "raw_personal_finance_data", "bank_statements", "credit_card_statements", "boa_jinsoo")
    boa_jinsoo_file_name = "boa_jinsoo_raw_spend.csv"
    data_extraction.extract_raw_spend_data(bank_file_path=boa_jinsoo_file_path, file_name=boa_jinsoo_file_name)


    # Concatenate all chase_jinsoo raw spend data
    chase_jinsoo_file_path = os.path.join(current_file_path, "data", "raw_data", "raw_personal_finance_data", "bank_statements", "credit_card_statements", "chase_jinsoo")
    chase_jinsoo_file_name = "chase_jinsoo_raw_spend.csv"
    data_extraction.extract_raw_spend_data(bank_file_path=chase_jinsoo_file_path, file_name=chase_jinsoo_file_name)


    # Concatenate all chase_nicole raw spend data
    chase_nicole_file_path = os.path.join(current_file_path, "data", "raw_data", "raw_personal_finance_data", "bank_statements", "credit_card_statements", "chase_nicole")
    chase_nicole_file_name = "chase_nicole_raw_spend.csv"
    data_extraction.extract_raw_spend_data(bank_file_path=chase_nicole_file_path, file_name=chase_nicole_file_name)


    ###########################################################################
    ######################### EXTRACT RAW RHYTHM DATA #########################
    ###########################################################################


    # Initialize Rhythm Data
    import_google_sheets = ImportGoogleSheets()
    ingest_data_to_postgres = IngestDataToPostgres()


    # Extract raw rhythm rhythm data
    import_google_sheets.import_raw_data()
   
    # Ingest raw rhythm data into Postgres
    ingest_data_to_postgres.ingest_data_to_postgres(args)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')

    args = parser.parse_args()

    main(args)