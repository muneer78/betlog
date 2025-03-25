import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials file for Google Sheets
scope_sheets = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
sheets_credentials = ServiceAccountCredentials.from_json_keyfile_name('laghezza-e6374719f2f8.json', scope_sheets)

# Authenticate with Google Sheets
gc_sheets = gspread.authorize(sheets_credentials)

# Open the Google Sheet by its title or URL
sheet = gc_sheets.open_by_url('https://docs.google.com/spreadsheets/d/1sjfqRGZxpQ9xkwpc6WrPMdsJgcIOfFHWGNgnkW0ebCc/')

# List of sheet names you want to extract
desired_sheets = ['TEAM O L8', 'TEAM O L4', 'DEFENSE L8', 'DEFENSE L4', 'PASSING L8', 'PASSING L4', 'RECEIVING L8', 'RECEIVING L4', 'RUSHING L8', 'RUSHING L4']

# Create an empty list to store dataframes
dataframes_list = []

# Iterate through each sheet and convert it to a dataframe
for sheet_name in sheet.worksheets():
    if sheet_name.title in desired_sheets:
        worksheet = sheet.worksheet(sheet_name.title)
        data = worksheet.get_all_values()

        # Convert the data into a Pandas DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Append the dataframe to the list
        dataframes_list.append(df)

# Define a function to remove newlines from dataframe column names
def remove_newlines(df_list):
    for df in df_list:
        df.columns = df.columns.str.replace('\n', ' ')

# Call the function to remove newlines from column names
remove_newlines(dataframes_list)

# Define a function to join fields based on 'Pos'
def join_fields(df, l4_df, l8_df, pos, output_file, title):
    if pos in df['Pos'].unique():
        # Merge L4 and L8 dataframes based on a common column (e.g., 'Player')
        merged_df = df.merge(l4_df, on='Player').merge(l8_df, on='Player', suffixes=('_L4', '_L8'))

        # Sort the merged dataframe by "Fantasy Pts" column
        merged_df = merged_df.sort_values(by="Fantasy Pts_L8", ascending=False)

        # Write the merged data to a CSV file with a title
        with open(output_file, "a", newline="") as csvfile:
            # Write title
            csvfile.write(title + '\n')
            # Write headers
            csvfile.write(','.join(merged_df.columns) + "\n")
            # Write data
            for _, row in merged_df.head(10).iterrows():
                csvfile.write(','.join(map(str, row.values)) + "\n")

# Define the output file for saving data
output_file = "fbpickups.csv"

# Define L4 and L8 dataframes for each category
l4_passing_df = dataframes_list[5]  # PASSING L4
l8_passing_df = dataframes_list[4]  # PASSING L8
l4_rushing_df = dataframes_list[10]  # RUSHING L4
l8_rushing_df = dataframes_list[9]  # RUSHING L8
l4_receiving_df = dataframes_list[8]  # receiving L4
l8_receiving_df = dataframes_list[7]  # receiving L8

# Iterate through each dataframe in the list and filter/save data based on 'Pos'
for df in dataframes_list:
    if 'Player' in df.columns and 'Fantasy Pts' in df.columns:
        if 'QB' in df['Pos'].unique():
            join_fields(df, l4_passing_df, l8_passing_df, 'QB', output_file, "QBs")
        elif df['Pos'].isin(['WR', 'TE']).all():
            join_fields(df, l4_receiving_df, l8_receiving_df, 'WR', output_file, "WR/TE")
        elif 'RB' in df['Pos'].unique():
            join_fields(df, l4_rushing_df, l8_rushing_df, 'RB', output_file, "RB")
