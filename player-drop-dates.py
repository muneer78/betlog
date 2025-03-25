import pandas as pd

# Step 1: Create a dataframe from the list
data = pd.read_csv

# Define column names
columns = ['Round', 'Player', 'Position', 'Time Frame', 'When To Drop']

# Create the dataframe
df = pd.DataFrame(data, columns=columns)

# Step 2: Set the season start date for MLB season to 4/1/24
season_start_date = pd.to_datetime('2024-04-01')

# Step 3: Add values in Time Frame column to Season Start Date variable
df['When To Drop'] = season_start_date + pd.to_timedelta(df['Time Frame'], unit='D')

# Display the updated dataframe
print(df)
