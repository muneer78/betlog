import pandas as pd

# Load draftsheet.csv as a dataframe
df = pd.read_csv('draftsheet.csv')

# Ask how many players to lookup in the Name value for Side A
num_players_side_a = int(input("How many players to lookup in Side A? "))

# Input strings and match them to values in the Name column
side_a_players = []
for i in range(num_players_side_a):
    player = input(f"Enter name of player {i+1}: ")
    side_a_players.append(player)

# Lookup values in the Total Z-Score column and add them for Side A
side_a_df = df[df['Name'].str.contains('|'.join(side_a_players), na=False)]
side_a_total = side_a_df['Total Z-Score'].sum()

# Print the value for Side A
print(f"The value for Side A is {side_a_total}")
print("Players found in Side A:")
for index, row in side_a_df.iterrows():
    print(f"{row['Name']}: {row['Total Z-Score']}")

# Ask how many players to lookup in the Name value for Side B
num_players_side_b = int(input("How many players to lookup in Side B? "))

# Input strings and match them to values in the Name column for Side B
side_b_players = []
for i in range(num_players_side_b):
    player = input(f"Enter name of player {i+1}: ")
    side_b_players.append(player)

# Lookup values in the Total Z-Score column and add them for Side B
side_b_df = df[df['Name'].str.contains('|'.join(side_b_players), na=False)]
side_b_total = side_b_df['Total Z-Score'].sum()

# Print the value for Side B
print(f"The value for Side B is {side_b_total}")
print("Players found in Side B:")
for index, row in side_b_df.iterrows():
    print(f"{row['Name']}: {row['Total Z-Score']}")
