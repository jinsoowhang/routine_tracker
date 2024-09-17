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
tab_life = os.getenv('TAB_LIFE')
tab_gym = os.getenv('TAB_GYM')

class ImportGoogleSheets():

    def __init__(self):
        # Set the scope and authorize the Google Sheets client
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
        self.gc = gspread.authorize(credentials)

    def fetch_sheet_data(self, spreadsheet_key, tab_name):
        """Fetches data from a Google Sheets worksheet and returns it as a pandas DataFrame."""
        try:
            book = self.gc.open_by_key(spreadsheet_key)
            worksheet = book.worksheet(tab_name)
            values = worksheet.get_all_values()
            return pd.DataFrame(values[1:], columns=values[0])
        except Exception as e:
            print(f"Error fetching data from {tab_name}: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error


    def import_raw_data(self):
        # Fetch data from historical and current sheets
        raw_historical_df = self.fetch_sheet_data(historical_spreadsheet_key, tab_life)
        raw_df = self.fetch_sheet_data(spreadsheet_key, tab_life)
        gym_df = self.fetch_sheet_data(spreadsheet_key, tab_gym)

        # Ignore placeholder data in raw_df
        raw_df = raw_df[raw_df['date'] != '1/1/1900']

        # Ensure data types are consistent
        raw_historical_df = raw_historical_df.astype(str)
        raw_df = raw_df.astype(str)
        gym_df = gym_df.astype(str)

        # Concatenate historical and new data (check for empty DataFrames to avoid issues)
        if not raw_historical_df.empty and not raw_df.empty:
            combined_df = pd.concat([raw_historical_df, raw_df], ignore_index=True)
        else:
            combined_df = pd.DataFrame()  # Handle the case when no data is fetched

        # Save the combined DataFrame and gym DataFrame to CSV
        if not combined_df.empty:
            all_clean_data_path = os.path.join(local_file_path, "data", "raw_data", "raw_rhythm.csv")
            combined_df.to_csv(all_clean_data_path, index=False)
        else:
            print("No data to save for raw_rhythm.csv")

        if not gym_df.empty:
            gym_data_path = os.path.join(local_file_path, "data", "raw_data", "raw_gym.csv")
            gym_df.to_csv(gym_data_path, index=False)
        else:
            print("No data to save for raw_gym.csv")

        return combined_df, gym_df