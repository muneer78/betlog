import pandas as pd
from io import StringIO

# Your data as a list of strings
data = pd.read_csv('2023batters.csv')

# Create a DataFrame from the data
df = pd.read_csv(StringIO('\n'.join(data)), sep='\t')

# Remove special characters from all columns
df = df.apply(lambda x: x.str.replace('[^A-Za-z0-9\s]+', '', regex=True))

# Delete the first column
df = df.iloc[:, 1:]

# Split the team name from the Name column and create a new 'Team' column
df['Team'] = df[0].str.extract(r'([A-Z]{3})')

# Display the resulting DataFrame
print(df)