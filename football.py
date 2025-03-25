import pandas as pd

def convert_column_headers_to_lower_case(df):
    df.columns = [column.lower() for column in df.columns]

def load_and_convert_data(file, columns):
    df = pd.read_csv(file, usecols=columns)
    convert_column_headers_to_lower_case(df)
    return df

def map_team_names(df, teammap):
    df["team"] = df["team"].map(lambda x: teammap.get(x, x))

def clean_player_data(df):
    df.replace(r"[^\w\s]|_\*| jr| ii", "", regex=True, inplace=True)

def calculate_average_rank(df, columns, new_column):
    df[new_column] = df.iloc[:, columns].mean(axis=1, numeric_only=True)

def merge_and_fill_na(df1, df2, on_column, how_type):
    merged_df = df1.merge(df2, on=[on_column], how=how_type)
    return merged_df.fillna(value=0)

def convert_floats_to_ints(df):
    float_cols = df.select_dtypes(include=['float64']).columns
    df[float_cols] = df[float_cols].astype(int)

# Load the team mapping
teammap = pd.read_csv("TeamDict.csv", index_col=0).squeeze().to_dict()

# Load and process dataframes
dfpff = load_and_convert_data("PFFOLine.csv", ["Team", "PFFRank"])
dfcbsoline = load_and_convert_data("CBSOLine.csv", ["Team", "CBSOLineRank"])
dfpfn = load_and_convert_data("PFNOLine.csv", ["Team", "Rank"])
dfcbs = load_and_convert_data("CBSSportsSOS.csv", ["Team", "CBSRank"])
dffbs = load_and_convert_data("FBSchedulesSOS.csv", ["Team", "FBRank"])
dfpfnsos = load_and_convert_data("PFNSOS.csv", ["Team", "PFNSOSRank"])
dfdk = load_and_convert_data("DKSOS.csv", ["Team", "DKRank"])
dfplayer = load_and_convert_data("Player List.csv", ["Rank", "Name", "Team", "Pos"])

# Apply transformations before merging
dataframes = [dfpff, dfpfn, dfcbs, dfcbsoline, dffbs, dfpfnsos, dfdk, dfplayer]
for df in dataframes:
    map_team_names(df, teammap)
    convert_column_headers_to_lower_case(df)
    convert_floats_to_ints(df)  # Convert floats to ints before merging

# Clean player data
clean_player_data(dfplayer)

# Perform merges and calculations
df_oline = merge_and_fill_na(dfpfn, dfpff[["team", "pffrank"]], "team", "left")
df_oline = merge_and_fill_na(df_oline, dfcbsoline[["team", "cbsolinerank"]], "team", "left")
convert_floats_to_ints(df_oline)
calculate_average_rank(df_oline, [2, 3], "olinerank")
convert_floats_to_ints(df_oline)

df_sos = merge_and_fill_na(dfcbs, dffbs[["team", "fbrank"]], "team", "left")
df_sos = merge_and_fill_na(df_sos, dfdk[["team", "dkrank"]], "team", "left")
convert_floats_to_ints(df_sos)
calculate_average_rank(df_sos, [2, 3], "sosrank")
convert_floats_to_ints(df_sos)

df_players = merge_and_fill_na(dfplayer, df_oline[["team", "olinerank"]], "team", "left")
df_players = merge_and_fill_na(df_players, df_sos[["team", "sosrank"]], "team", "left")
convert_floats_to_ints(df_players)

df_players = df_players.rename(columns={"rank": "adp", "pos": "position"})
convert_floats_to_ints(df_players)

# Calculate playerscore as the sum of adp, olinerank, and sosrank
df_players["playerscore"] = df_players["adp"] + df_players["olinerank"] + df_players["sosrank"]

# Filter out rows where playerscore = 0
df_players_filtered = df_players.query("playerscore != 0")

# Sort and organize the columns
sorted_df = df_players_filtered.sort_values(by=["playerscore"])
new_order = ["name", "team", "position", "adp", "olinerank", "sosrank", "playerscore"]
sorted_df = sorted_df[new_order]

print(sorted_df)

sorted_df.to_csv("2024FantasyFootballRanks.csv", index=False)