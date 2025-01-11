import pandas as pd
import os
from dotenv import load_dotenv


current_file_path = os.getenv('LOCAL_FILE_PATH')


class AppendCleanData():


    def append_all_clean_data(self):
        # Define the path to clean_data


        clean_data_spend_file_path = os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'clean_data_spend')
        all_transaction_path = os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'clean_data_spend')


        os.chdir(clean_data_spend_file_path)
        file_list = os.listdir()


        output_file_name = "all_clean_data_spend.csv"
        file_path = os.path.join(all_transaction_path, output_file_name)


        # Read the existing concatenated data if it exists
        if os.path.exists(output_file_name):
            df = pd.read_csv(output_file_name)
        else:
            df = pd.DataFrame()


        for file in file_list:
            if file != output_file_name:  # Skip the output file
                new_file_path = os.path.join(clean_data_spend_file_path, file)
                new_df = pd.read_csv(new_file_path)


                concat_file = pd.concat([df, new_df])
                concat_file = concat_file.drop_duplicates()  # Drop duplicates based on all columns
                concat_file.to_csv(file_path, index=False)
                df = concat_file  # Update df for the next iteration


        print(f"All Clean Data files were appended successfully to {output_file_name}")