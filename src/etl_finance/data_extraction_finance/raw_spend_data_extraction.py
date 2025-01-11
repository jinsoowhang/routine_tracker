import pandas as pd
import os
from dotenv import load_dotenv


current_file_path = os.getenv('LOCAL_FILE_PATH')


class DataExtraction():


    def extract_raw_spend_data(self, bank_file_path, file_name):


        all_transaction_path = os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'raw_spend')


        os.chdir(bank_file_path)
        file_list = os.listdir()


       
        file_path = os.path.join(all_transaction_path, file_name)


        # Read the existing concatenated data if it exists
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame()


        for file in file_list:
            if file != file_name:  # Skip the output file
                new_file_path = os.path.join(bank_file_path, file)
                new_df = pd.read_csv(new_file_path)


                concat_file = pd.concat([df, new_df])
                concat_file = concat_file.drop_duplicates()  # Drop duplicates based on all columns
                concat_file.to_csv(file_path, index=False)
                df = concat_file  # Update df for the next iteration


        print(f"Data appended successfully for {file_name}")