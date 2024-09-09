from src.data_extraction.import_google_sheets import ImportGoogleSheets
import argparse

def main():

    import_google_sheets = ImportGoogleSheets()

    ####################################################################
    ######################### EXTRACT RAW DATA #########################
    ####################################################################

    # Extract raw rhythm data
    import_google_sheets.import_raw_data()

if __name__ == '__main__':
    main()