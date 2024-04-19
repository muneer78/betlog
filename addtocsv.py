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
    {'Date': '2024-04-18', 'Sportsbook': 'FanDuel', 'Sport': 'Basketball', 'System': 'Sportsline', 'Pick': 'Series Win- Knicks', 'FreeBet': 'N', 'Amount': '0.10', 'Odds': '-108', 'Result': 'P'},
    {'Date': '2024-04-18', 'Sportsbook': 'FanDuel', 'Sport': 'Basketball', 'System': 'Sportsline', 'Pick': 'Series Win- Pacers', 'FreeBet': 'N', 'Amount': '0.10', 'Odds': '+100', 'Result': 'P'    },
    # Add more rows as needed
]

# Specify the file path of the existing CSV
existing_csv_file = 'futures.csv'

# Map rows to the existing CSV file
map_rows_to_csv(existing_csv_file, rows_to_map)
