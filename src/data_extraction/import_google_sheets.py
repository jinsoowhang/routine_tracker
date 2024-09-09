#importing the required libraries
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Reference environment variables
json_key_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
historical_spreadsheet_key = os.getenv('HISTORICAL_SPREADSHEET_KEY')
spreadsheet_key = os.getenv('SPREADSHEET_KEY')
local_file_path = os.getenv('LOCAL_FILE_PATH')
tab_name = os.getenv('TAB_NAME')

class ImportGoogleSheets():

    def import_raw_data(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        # Add credentials to the account
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
        gc = gspread.authorize(credentials)

        # Open the spreadsheets
        book_historical = gc.open_by_key(historical_spreadsheet_key)
        book = gc.open_by_key(spreadsheet_key)

        # Import from Google Sheets
        worksheet_historical = book_historical.worksheet(tab_name)
        worksheet = book.worksheet(tab_name)

        values_historical = worksheet_historical.get_all_values()
        values = worksheet.get_all_values()

        # Convert to pandas DataFrame
        raw_historical_df = pd.DataFrame(values_historical[1:], columns=values_historical[0])
        raw_df = pd.DataFrame(values[1:], columns=values[0])

        # Ignore this placeholder data
        raw_df = raw_df[raw_df['date'] != '1/1/1900']

        # Define the desired data types for the columns
        desired_dtypes = {
            'weekday': 'str', 'day_num': 'str', 'date': 'str', 'hour': 'str', 'activity': 'str', 
            'attribute_1': 'str', 'attribute_2': 'str', 'attribute_3': 'str', 'attribute_4': 'str', 
            'places': 'str', 'people': 'str', 'notes': 'str', 'adj_day': 'str', 'adj_day_num': 'str', 
            'adj_date': 'str', 'adj_hour': 'str'
        }

        # Change data types of specified columns
        raw_historical_df = raw_historical_df.astype(desired_dtypes)
        raw_df = raw_df.astype(desired_dtypes)

        # Append raw_df to raw_historical_df using pd.concat
        combined_df = pd.concat([raw_historical_df, raw_df], ignore_index=True)


        # Save raw data to CSV
        all_clean_data_path = os.path.join(local_file_path, "data", "raw_data", "raw_rhythm.csv")
        combined_df.to_csv(all_clean_data_path, index=False)

        return combined_df