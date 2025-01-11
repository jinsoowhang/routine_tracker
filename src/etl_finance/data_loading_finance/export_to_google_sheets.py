# Importing libraries
import gspread
import pandas as pd
import os
from oauth2client.service_account import ServiceAccountCredentials


# Reference environment variables
json_key_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')


class ExportGoogleSheets():

        # UDF
        def export_to_google_sheets(self, tab_name, csv_path):


            # define the scope
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


            # add credentials to the account
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
            gc = gspread.authorize(credentials)
            spreadsheet_key = '14L4DYapAqELkeTxC59y-iUNyg5dU4on7PUOVo9llvJg'
            book = gc.open_by_key(spreadsheet_key)


            # Read CSV file
            new_df_name = pd.read_csv(csv_path)


            # Convert out-of-range float values to strings
            new_df_name = new_df_name.astype(str)
           
            # Export to Google Sheets
            worksheet = book.worksheet(tab_name)
            worksheet.update([new_df_name.columns.values.tolist()] + new_df_name.values.tolist())
           
            print(f'Data exported to New Beginnings Finance Google Sheets tab name: {tab_name}')
            return new_df_name