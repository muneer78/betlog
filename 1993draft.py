import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('1993DraftList.csv')

# Initialize the rounds and teams
rounds = 10  # Number of rounds in the draft
num_teams = 10  # Number of teams participating
teams = {f'Team {i}': [] for i in range(1, num_teams + 1)}  # Dictionary to track drafted players by team

# Function to get the next available player with the highest WAR
def get_next_pick(round_num):
    available_players = df[~df['Taken?'].notna() & ~df['Name'].isin([p for players in teams.values() for p in players])]
    available_players = available_players.sort_values(by='WAR', ascending=False)
    if not available_players.empty:
        next_pick = available_players.iloc[0]
        return next_pick
    else:
        return None

# Function to return the next 5 players with the most WAR
def get_next_5_players():
    available_players = df[~df['Taken?'].notna() & ~df['Name'].isin([p for players in teams.values() for p in players])]
    available_players = available_players.sort_values(by='WAR', ascending=False)
    next_5_players = available_players.head(5)
    return next_5_players

# Draft loop
for round_num in range(1, rounds + 1):
    print(f"\nRound {round_num}")
    for team_name in teams.keys():
        print(f"\n{team_name}'s Pick:")
        next_pick = get_next_pick(round_num)
        if next_pick:
            player_name = next_pick['Name']
            print(f"Picked: {player_name}")
            teams[team_name].append(player_name)
            next_5 = get_next_5_players()
            print("\nNext 5 Players with the Most WAR:")
            print(next_5)
        else:
            print("No available players left. The draft is complete.")
            break