import os

# MAIN FOLDER
main_folder = os.path.dirname(__file__)

# SUB FOLDER
dataframes_folder = os.path.join(main_folder, 'dataframes')

# DATAFRAMES
sendedmails_csv = os.path.join(dataframes_folder, 'sendedmails.csv')
