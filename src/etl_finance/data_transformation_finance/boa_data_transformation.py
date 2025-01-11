import pandas as pd
import os
from dotenv import load_dotenv


current_file_path = os.getenv('LOCAL_FILE_PATH')


class cleanBankofamericaData():


    def cleaning_bank_of_america_credit_card_data(self, file_name, card_owner, output_file_name):


        # Define the path to concatenated files
       
        all_transaction_path = os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'raw_spend')


        os.chdir(all_transaction_path)
        # file_list = os.listdir()


       
        file_path = os.path.join(all_transaction_path, file_name)


        # Open BOA
        boa_df = pd.read_csv(file_path)




        ##############################################################################################################################
        ######################################################### Clean Data #########################################################
        ##############################################################################################################################


        clean_data = boa_df.copy()


        # Column name change
        clean_data.columns = ['Date', 'Reference', 'Supplier', 'Address', 'Amount']


        # Change data type
        clean_data['Date'] = clean_data['Date'].str.replace(',','/')
        clean_data['Date'] = pd.to_datetime(clean_data['Date'], format='%m/%d/%Y')


        # Only keep relevant columns
        clean_data = clean_data[['Date', 'Supplier', 'Amount']]




        ###############################################################################################################################
        ######################################################### Modify Data #########################################################
        ###############################################################################################################################


        modify_data = clean_data.copy()


        ###################################################################
        #### Who's credit card account is this and what bank account? #####
        ###################################################################


        modify_data['Card Owner'] = card_owner
        modify_data['Bank Name'] = 'Bank of America'


        ################################################################################
        ### Reverse amount, so positive is purchase and negative is refund/returns #####
        ################################################################################


        modify_data['Amount'] = modify_data['Amount']*-1


        ###################################################################
        #### Categorize if transaction was a card payment or purchase #####
        ###################################################################


        # list of card payment values
        list_card_payment = ['payment - thank you', 'online payment from',
                            'payment thank you']


        # list of card adjustment
        list_card_adjustment = ['your cash reward/refund is', 'cash back',
                                'statement credit', 'redemption credit']


        # default transaction_type to purchase
        modify_data['Type'] = 'Sale'


        # card payment if Supplier contains list of card payment values
        modify_data.loc[modify_data['Supplier'].str.strip().str.lower()
                                            .str.contains('|'.join(list_card_payment)), 'Type'] = 'Payment'


        # card adjustment if Supplier contains list of card adjustment
        modify_data.loc[modify_data['Supplier'].str.strip().str.lower()
                                            .str.contains('|'.join(list_card_adjustment)), 'Type'] = 'Adjustment'




        # return if transaction is not a card payment and amount below 0
        modify_data.loc[(modify_data['Type'] != 'Payment') &
                        (modify_data['Type'] != 'Adjustment') &
                        (modify_data['Amount'] < 0), 'Type'] = 'Return'


        ##############################################################################################################################
        ######################################################### Clean Data II #########################################################
        ##############################################################################################################################


        clean_data_ii = modify_data.copy()


        # Initialize empty columns
        clean_data_ii['Category'] = ''
        clean_data_ii['Memo'] = ''


        # reorder columns
        clean_data_ii = clean_data_ii[['Date', 'Supplier', 'Category', 'Card Owner',
                                    'Bank Name', 'Type', 'Amount', 'Memo']]


        # rename df name for analysis_df and final_df
        final_clean_df = clean_data_ii.copy()


        ###############################################################################################################################
        ######################################################### analysis df #########################################################
        ###############################################################################################################################






        ############################################################################################################################
        ######################################################### final df #########################################################
        ############################################################################################################################


        final_df = final_clean_df.copy()


        # print(final_df[final_df['Type'] == 'purchase'])
        # print(final_df)


        clean_data_path = os.path.join(current_file_path, 'data', 'raw_data', 'raw_personal_finance_data', 'concatenated_data', 'clean_data_spend')


        clean_data_file_path = os.path.join(clean_data_path, output_file_name)


        final_df.to_csv(clean_data_file_path, index=False)
        print(f'Clean data file has been successfully saved as {output_file_name}')