import csv

def map_rows_to_csv(csv_file, rows_to_map):
    """
    Add multiple rows to a CSV file.

    Args:
    - csv_file (str): File path of the CSV file.
    - new_rows_data (list of dicts): Data for the new rows, each dict representing one row.

    Format for adds: # {'Date': 'value1', 'Sportsbook': 'value3', 'Sport': 'value', 'System': 'value', 'Pick': 'value3', 'FreeBet': 'value3', 'Amount': 'value', 'Odds': 'value', 'Result': 'value', 'bet_group': 'Value'},
    """
    # Open the existing CSV file in read mode
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        existing_rows = list(reader)

    # Extract column names from the existing CSV file
    column_names = reader.fieldnames

    # Append new rows to existing rows
    for new_row in rows_to_map:
        existing_rows.append(new_row)

    # Write the combined rows to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)

        # Write the header
        writer.writeheader()

        # Write the combined rows
        writer.writerows(existing_rows)

    print("New rows added to the CSV file.")

# Define the data for the new rows
rows_to_map = [
{'Date': '2024-04-20', 'Sportsbook': 'DraftKings', 'Sport': 'Golf', 'System': 'Sportsline', 'Pick': '2024 PGA Championship Winner- Scottie Scheffler', 'FreeBet': 'N', 'Amount': '0.10', 'Odds': '+400', 'Result': 'P', 'bet_group': '2024 PGA Championship Winner'},
    {'Date' : '2024-04-20' , 'Sportsbook' : 'DraftKings' , 'Sport' : 'Golf' , 'System' : 'Sportsline' ,
     'Pick' : '2024 PGA Championship Winner- Collin Morikawa' , 'FreeBet' : 'N' , 'Amount' : '0.10' ,
     'Odds' : '+2200' , 'Result' : 'P' , 'bet_group' : '2024 PGA Championship Winner'} ,
    {'Date' : '2024-04-20' , 'Sportsbook' : 'DraftKings' , 'Sport' : 'Golf' , 'System' : 'Sportsline' ,
     'Pick' : '2024 PGA Championship Winner- Ludvig Aberg' , 'FreeBet' : 'N' , 'Amount' : '0.10' ,
     'Odds' : '+1800' , 'Result' : 'P' , 'bet_group' : '2024 PGA Championship Winner'} ,
    {'Date' : '2024-04-20' , 'Sportsbook' : 'DraftKings' , 'Sport' : 'Golf' , 'System' : 'Sportsline' ,
     'Pick' : '2024 PGA Championship Winner- Rory McIlroy' , 'FreeBet' : 'N' , 'Amount' : '0.10' ,
     'Odds' : '+900' , 'Result' : 'P' , 'bet_group' : '2024 PGA Championship Winner'} ,
    {'Date' : '2024-04-20' , 'Sportsbook' : 'DraftKings' , 'Sport' : 'Golf' , 'System' : 'Sportsline' ,
     'Pick' : '2024 PGA Championship Winner- Jon Rahm' , 'FreeBet' : 'N' , 'Amount' : '0.10' ,
     'Odds' : '+1000' , 'Result' : 'P' , 'bet_group' : '2024 PGA Championship Winner'} ,

    # Add more rows as needed
]

# Specify the file path of the existing CSV
existing_csv_file = 'futures.csv'

# Map rows to the existing CSV file
map_rows_to_csv(existing_csv_file, rows_to_map)
