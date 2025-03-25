'''
Steps to get create the CSVs
1. Update Preseason Hitter Report on Fangraphs
2. Download as hitter.csv
3. Update Preseason Pitcher Report on Fangraphs
4. Downlaod as hitter.csv
5. Go to Draft Rankings on Fantasy Pros. Download rankings file as csv. Update name of reference in script.
6. Request csv file from John Laghezza
'''

import pandas as pd
from scipy import stats
import numpy as np
from unidecode import unidecode

# Function to create keys from player names
def create_key(player_name):
    return "".join([i[:3] for i in player_name.strip().split(" ")])

# Function to remove accents
def remove_accents(text):
    if isinstance(text, str):  # Check if the value is a string
        return unidecode(text)
    else:
        return text  # Retu

# Read the preseason pitchers data
df_pitchers = pd.read_csv("pitcher.csv", index_col=["PlayerId"])

# Calculate EstimatedQS
expr1 = (df_pitchers["GS"] / (df_pitchers["ER"] * (df_pitchers["GS"] / df_pitchers["G"]))).fillna(0).replace([np.inf, -np.inf], 0)
expr2 = (df_pitchers["IP"] * (df_pitchers["GS"] / df_pitchers["G"])).fillna(0)
expr3 = (((df_pitchers["GS"] + df_pitchers["G"]) / (2 * df_pitchers["G"])) ** 2).fillna(0)
df_pitchers["EstimatedQS"] = expr1 * expr2 * expr3

# Drop unnecessary columns
df_pitchers.drop(["ER", "GS", "G"], axis=1, inplace=True)

# Sum the numerical columns
numerical_columns = df_pitchers.select_dtypes(include="number").columns
df_pitchers["Total Numerical Sum"] = df_pitchers[numerical_columns].sum(axis=1)

# Apply z-score to numerical columns (excluding the new "Total Numerical Sum" column)
df_pitchers[numerical_columns] = df_pitchers[numerical_columns].apply(stats.zscore)

# Modify specific columns
df_pitchers["SV"] *= 1.5
df_pitchers["Barrel%"] *= 1.5
df_pitchers["xFIP-"] *= 1.5
df_pitchers["SwStr%"] *= 1.5
df_pitchers["F-Strike%"] *= 1.5
df_pitchers["CSW%"] *= 1.5
df_pitchers["K%+"] *= 5
df_pitchers["BB%+"] *= 5
df_pitchers["EstimatedQS"] *= 5

# Calculate Total Z-Score
df_pitchers["Total Z-Score_Pitcher"] = df_pitchers[numerical_columns].sum(axis=1)

# Drop the intermediate "Total Numerical Sum" column if needed
df_pitchers.drop("Total Numerical Sum", axis=1, inplace=True)

# Round the dataframe and save to CSV
rounded_df_pitchers = df_pitchers.round(decimals=2).sort_values(by="Total Z-Score_Pitcher", ascending=False)
rounded_df_pitchers.to_csv("ZPitchers.csv")

# Read the preseason hitters data
df_hitters = pd.read_csv("hitter.csv", index_col=["PlayerId"])

# Filter the hitters dataframe
filter1 = df_hitters[(df_hitters["PA"] > 250) & (df_hitters["HR"] > 5)]

# Apply z-score to numerical columns
numerical_columns1 = df_hitters.select_dtypes(include="number").columns

# Sum the numerical columns
df_hitters["Total Numerical Sum"] = df_hitters[numerical_columns1].sum(axis=1)

df_hitters[numerical_columns1] = df_hitters[numerical_columns1].apply(stats.zscore)

# Calculate Total Z-Score
df_hitters["Total Z-Score_Hitter"] = df_hitters[numerical_columns1].sum(axis=1)

# Drop the intermediate "Total Numerical Sum" column if needed
df_hitters.drop("Total Numerical Sum", axis=1, inplace=True)

# Round the dataframe and save to CSV
rounded_df_hitters = df_hitters.round(decimals=2).sort_values(by="Total Z-Score_Hitter", ascending=False)
rounded_df_hitters.to_csv("ZHitters.csv")

# Read the additional dataframes
df_adp = pd.read_csv("FantasyPros_Fantasy_Baseball_Rankings_ALL.csv")
df_zpit = pd.read_csv("ZPitchers.csv")
df_zhit = pd.read_csv("ZHitters.csv")
df_laghezza = pd.read_csv("laghezza.csv")

df_adp = df_adp.rename(columns={"Player": "Name"})

dataframes_to_clean = [df_adp, df_zpit, df_zhit, df_laghezza]  # List of DataFrames to clean
for df in dataframes_to_clean:
    df['Name'] = df['Name'].apply(remove_accents)  # Remove accents
    df['Name'] = df['Name'].str.replace(r"[^\w\s]|_\*|\.|,", "")  # Remove special characters, '.', and ','
    df['Name'] = df['Name'].str.replace(" Jr.", "")  # Remove "Jr"
    df['Name'] = df['Name'].str.replace(" II", "")  # Remove "II"

# Convert df_adp to string
df_adp = df_adp.astype(str)

# Rename the "Rank" column to "ADP"
df_laghezza = df_laghezza.rename(columns={"Rank": "LRank"})

# Apply the create_key function to add the "Key" column
df_adp["Key"] = df_adp["Name"].apply(create_key)
df_zpit["Key"] = df_zpit["Name"].apply(create_key)
df_zhit["Key"] = df_zhit["Name"].apply(create_key)
df_laghezza["Key"] = df_laghezza["Name"].apply(create_key)

# Create a list of dataframes for merging
dflist = [df_zpit, df_zhit, df_adp, df_laghezza]

# Merge the dataframes with suffixes to handle duplicate columns
df1 = df_adp.merge(df_zpit[["Key", "Total Z-Score_Pitcher"]], on=["Key"], how="left")\
    .merge(df_zhit[["Key", "Total Z-Score_Hitter"]], on=["Key"], how="left")\
    .merge(df_laghezza[["Key", "LRank"]], on=["Key"], how="left")

# Fill NaN values with zeros
df1 = df1.fillna(0)

# Convert specific columns to numeric
cols = ["Rank"]
df1[cols] = df1[cols].apply(pd.to_numeric, errors="coerce", axis=1)

# Drop duplicates based on "Player" and "Rank" columns
df1 = df1.drop_duplicates(subset=["Name", "Rank"], keep="last")

# Calculate the "Total Z-Score" column
df1["Total Z-Score"] = df1["Total Z-Score_Pitcher"].mask(df1["Total Z-Score_Pitcher"].eq(0), df1["Total Z-Score_Hitter"])

# Create the "CombinedRank" column
df1["CombinedRank"] = df1["LRank"].mask(df1["LRank"].eq(0), df1["Rank"])
df1.loc[df1.LRank.isnull(), "LRank"] = df1["Rank"]

# Calculate the "RankDiff" column
df1["RankDiff"] = df1["Rank"] - df1["LRank"].mask(df1["LRank"].eq(0), df1["Rank"])

# Select and rename columns
columns = ["Name", "Team", "Total Z-Score", "RankDiff", "LRank", "ADP"]
df1 = df1[columns]

# Sort the "ADP" column
df1["ADP"] = sorted(df1["ADP"], key=float)

# Save the second dataframe to CSV
df1.to_csv("draftsheet.csv")
