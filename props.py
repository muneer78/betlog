"""
Provides some arithmetic functions and ability to use regex
"""

import re
import pandas as pd
from skimpy import skim

'''
Code to show today's plays
'''''

dfschedtoday = pd.read_excel("roster-resource-download.xlsx", usecols=[0, 1])
dfpropstoday = pd.read_csv("fangraphs-leaderboards.csv")

dfpropstoday['K/GS'] = dfpropstoday['SO'] / dfpropstoday['GS']
dfpropstoday ['K/GS' ] = dfpropstoday['K/GS'].round(2)
dfpropstoday['BB/GS'] = dfpropstoday['BB'] / dfpropstoday['GS']
dfpropstoday['BB/GS'] = dfpropstoday['BB/GS'].round(2)
dfpropstoday['IP/G'] = dfpropstoday['IP'] / dfpropstoday['GS']
dfpropstoday['IP/G'] = dfpropstoday['IP/G'].round(0)

# Filter rows where GS > 1
dfpropstoday = dfpropstoday.loc[(dfpropstoday['GS'] > 1) & (dfpropstoday['IP/G'] >= 5) & (dfpropstoday['IP/G'] < 8) & (dfpropstoday['K/GS'] <= 9) & (dfpropstoday['BB/GS'] <= 6)]

dfschedtoday.rename(columns={dfschedtoday.columns[1]: "Name"}, inplace=True)
dfschedtoday = dfschedtoday.fillna(0)

dfopponentstoday = pd.read_csv(
    "fangraphs-leaderboards (1).csv", usecols=[ "Team", "K%", "BB%" ]
)

dfopponentstoday.sort_values("K%", ascending=False, ignore_index=True, inplace=True)
# Add a new column called "KRank"
dfopponentstoday["KRank"] = range(1, len(dfopponentstoday) + 1)


dfopponentstoday.sort_values("BB%", ascending=True, ignore_index=True, inplace=True)
dfopponentstoday["BBRank"] = range(1, len(dfopponentstoday) + 1)

dfschedtoday["Name"] = dfschedtoday["Name"].str.strip()
opposing_teamstoday = dfschedtoday.iloc[:, 1].str.split("\n").str[0]
dfschedtoday["OpposingTeam"] = opposing_teamstoday
dfschedtoday["OpposingTeam"] = dfschedtoday["OpposingTeam"].str.replace("@ ", "")

"""
Deletes first line in cell from roster resource file
"""
def delete_first_line(cell_value):
    lines = cell_value.split("\n")
    if len(lines) > 1:
        lines.pop(0)
    return "\n".join(lines)

"""
Applies delete_first_line function
"""
dfschedtoday = dfschedtoday.applymap(delete_first_line)

"""
Remove the R or L from after pitcher name
"""
def remove_text(cell_value):
    pattern = r"\s*\(R\)|\s*\(L\)"
    return re.sub(pattern, "", cell_value)


dfschedtoday = dfschedtoday.applymap(remove_text)

# Generate dfopponents again
dfopponentstoday = pd.read_csv( "fangraphs-leaderboards (1).csv", usecols=[ "Team", "K%", "BB%" ] )

# Sort and add ranking columns
dfopponentstoday.sort_values("K%", ascending=False, ignore_index=True, inplace=True)
dfopponentstoday["KRank"] = range(1, len(dfopponentstoday) + 1)
dfopponentstoday.sort_values("BB%", ascending=True, ignore_index=True, inplace=True)
dfopponentstoday["BBRank"] = range(1, len(dfopponentstoday) + 1)

# Update merged_merged_dfschedtoday with opponent data again
dfschedtoday = pd.merge(dfschedtoday, dfopponentstoday[["Team", "KRank", "BBRank"]], on="Team", how="left")

dfsortedBBtoday = dfpropstoday.sort_values("BB%+", ascending=True)
dfbbtop25today = dfsortedBBtoday.head(25).fillna(0)

dfsortedKtoday = dfpropstoday.sort_values("K%+", ascending=False)
dfktop25today = dfsortedKtoday.head(25).fillna(0)

matching_dfbbtop25today = dfschedtoday[dfschedtoday["Name"].isin(dfbbtop25today["Name"])]
matching_dfktop25today = dfschedtoday[dfschedtoday["Name"].isin(dfktop25today["Name"])]

matching_dfbbtop25today = dfschedtoday[
    (dfschedtoday["Name"].isin(dfbbtop25today["Name"])) & ((dfschedtoday["BBRank"] <= 10))
]
matching_dfktop25today = dfschedtoday[
    (dfschedtoday["Name"].isin(dfktop25today["Name"])) & ((dfschedtoday["KRank"] <= 10))
]

matching_dfktop25today = pd.merge(
    matching_dfktop25today, dfktop25today[["Name", "K%+", "BB%+", "xFIP", "K/GS"]], on="Name", how="left"
)
matching_dfbbtop25today = pd.merge(
    matching_dfbbtop25today, dfbbtop25today[["Name", "K%+", "BB%+", "xFIP", "BB/GS"]], on="Name", how="left"
)

matching_dfktop25today = matching_dfktop25today.sort_values(by="K%+", ascending=False)
matching_dfbbtop25today = matching_dfbbtop25today.sort_values(by="BB%+", ascending=True)


'''
Code to show tomorrow's plays
'''''

dfschedtmr = pd.read_excel("roster-resource-download.xlsx", usecols=[0, 1, 2])
dfpropstmr = pd.read_csv("fangraphs-leaderboards.csv")
skim(dfpropstmr)


dfpropstmr['K/GS'] = dfpropstmr['SO'] / dfpropstmr['GS']
dfpropstmr['K/GS'] = dfpropstmr['K/GS'].round(2)
dfpropstmr['BB/GS'] = dfpropstmr['BB'] / dfpropstmr['GS']
dfpropstmr['BB/GS'] = dfpropstmr['BB/GS'].round(2)
dfpropstmr['IP/G'] = dfpropstmr['IP'] / dfpropstmr['GS']
dfpropstmr['IP/G'] = dfpropstmr['IP/G'].round(0)
dfpropstmr.fillna(0)

# Filter rows where GS > 1
dfpropstmr = dfpropstmr.loc[(dfpropstmr['GS'] > 1) & (dfpropstmr['IP/G'] >= 5) & (dfpropstmr['IP/G'] < 8) & (dfpropstmr['K/GS'] <= 9) & (dfpropstmr['BB/GS'] <= 6)]

dfschedtmr.rename(columns={dfschedtmr.columns[2]: "Name"}, inplace=True)
dfschedtmr = dfschedtmr.fillna(0)

# Delete the second column from dfschedtmr
dfschedtmr = dfschedtmr.drop(dfschedtmr.columns[1], axis=1)

dfopponentstmr = pd.read_csv("fangraphs-leaderboards (1).csv", usecols=[ "Team", "K%", "BB%" ]
)

dfopponentstmr.sort_values("K%", ascending=False, ignore_index=True, inplace=True)

# Add a new column called "KRank"
dfopponentstmr["KRank"] = range(1, len(dfopponentstmr) + 1)


dfopponentstmr.sort_values("BB%", ascending=True, ignore_index=True, inplace=True)
dfopponentstmr["BBRank"] = range(1, len(dfopponentstmr) + 1)

dfschedtmr["Name"] = dfschedtmr["Name"].str.strip()
opposing_teamstmr = dfschedtmr.iloc[:, 1].str.split("\n").str[0]
dfschedtmr["OpposingTeam"] = opposing_teamstmr
dfschedtmr["OpposingTeam"] = dfschedtmr["OpposingTeam"].str.replace("@ ", "")

"""
Deletes first line in cell from roster resource file
"""
def delete_first_line(cell_value):
    lines = cell_value.split("\n")
    if len(lines) > 1:
        lines.pop(0)
    return "\n".join(lines)

"""
Applies delete_first_line function
"""
dfschedtmr = dfschedtmr.applymap(delete_first_line)

"""
Remove the R or L from after pitcher name
"""
def remove_text(cell_value):
    pattern = r"\s*\(R\)|\s*\(L\)"
    return re.sub(pattern, "", cell_value)


dfschedtmr = dfschedtmr.applymap(remove_text)

merged_dfschedtmr = pd.merge(dfschedtmr, dfopponentstmr[["Team", "KRank", "BBRank"]], on="Team", how="left")

dfsortedBBtmr = dfpropstmr.sort_values("BB%+", ascending=True)
dfbbtop25tmr = dfsortedBBtmr.head(25).fillna(0)
skim(dfsortedBBtmr)

dfsortedKtmr = dfpropstmr.sort_values("K%+", ascending=False)
dfktop25tmr = dfsortedKtmr.head(25).fillna(0)

matching_dfbbtop25tmr = merged_dfschedtmr[merged_dfschedtmr["Name"].isin(dfbbtop25tmr["Name"])]
matching_dfktop25tmr = merged_dfschedtmr[merged_dfschedtmr["Name"].isin(dfktop25tmr["Name"])]

matching_dfbbtop25tmr = merged_dfschedtmr[
    (merged_dfschedtmr["Name"].isin(dfbbtop25tmr["Name"])) & ((merged_dfschedtmr["BBRank"] <= 10))
]
matching_dfktop25tmr = merged_dfschedtmr[
    (merged_dfschedtmr["Name"].isin(dfktop25tmr["Name"])) & ((merged_dfschedtmr["KRank"] <= 10))
]

matching_dfktop25tmr = pd.merge(
    matching_dfktop25tmr, dfktop25tmr[["Name", "K%+", "BB%+", "xFIP", "K/GS"]], on="Name", how="left"
)
matching_dfbbtop25tmr = pd.merge(
    matching_dfbbtop25tmr, dfbbtop25tmr[["Name", "K%+", "BB%+", "xFIP", "BB/GS"]], on="Name", how="left"
)

matching_dfktop25tmr = matching_dfktop25tmr.sort_values(by="K%+", ascending=False)
matching_dfbbtop25tmr = matching_dfbbtop25tmr.sort_values(by="BB%+", ascending=True)

list_of_dfs = [matching_dfktop25today, matching_dfbbtop25today, matching_dfktop25tmr, matching_dfbbtop25tmr]

titles = [
    "Pitcher High Strikeout Props Today",
    "Pitcher Low BB Props Today",
    "Pitcher High Strikeout Props Tomorrow",
    "Pitcher Low BB Props Tomorrow",
]

with open("props.csv", "w+", encoding="utf8") as f:
    for i, df in enumerate(list_of_dfs):
        if not df.empty:  # Check if the dataframe is not empty
            f.write(titles[i] + "\n")  # Write the title
            df.round(2).to_csv(f, index=False)  # Round numbers to 2 digits
            f.write("\n")
