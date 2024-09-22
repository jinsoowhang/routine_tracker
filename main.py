from src.data_extraction.import_google_sheets import ImportGoogleSheets
from src.data_extraction.ingest_data_to_postgres import IngestDataToPostgres
import argparse

def main():

    import_google_sheets = ImportGoogleSheets()
    ingest_data_to_postgres = IngestDataToPostgres()

    ####################################################################
    ######################### EXTRACT RAW DATA #########################
    ####################################################################

    # Extract raw rhythm data
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
    parser.add_argument('--table_name', help='name of the table where we will write the results to')

    args = parser.parse_args()

    main(args)