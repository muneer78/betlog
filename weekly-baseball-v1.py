import pandas as pd
from datetime import date, datetime, timedelta
import os
from scipy import stats

# # define dictionary
comp_dict = {
    "FanGraphs Leaderboard.csv": "fgl_pitchers_10_ip.csv",
    "FanGraphs Leaderboard (1).csv": "fgl_pitchers_30_ip.csv",
    "FanGraphs Leaderboard (2).csv": "fgl_hitters_40_pa.csv",
    "FanGraphs Leaderboard (3).csv": "fgl_hitters_last_14.csv",
    "FanGraphs Leaderboard (4).csv": "fgl_hitters_last_7.csv",
    "FanGraphs Leaderboard (5).csv": "fgl_pitchers_last_14.csv",
    "FanGraphs Leaderboard (6).csv": "fgl_pitchers_last_30.csv",
    "FanGraphs Leaderboard (7).csv": "hitter.csv",
    "FanGraphs Leaderboard (8).csv": "pitcher.csv",
}

for newname, oldname in comp_dict.items():
    os.replace(newname, oldname)

excluded = pd.read_csv("excluded.csv")

dfhitter = pd.read_csv('hitter.csv')
dfhitter['Barrel%'] = dfhitter['Barrel%'] = dfhitter['Barrel%'].str.rstrip('%').astype('float64')
temp_df = dfhitter[['Name', 'playerid']]
dfhitter = dfhitter.drop(columns = ['playerid', 'mlbamid'])
columns = ["PA", "HR", "SB", 'BABIP+', 'K%+', 'BB%+', 'ISO+', 'wRC+', 'Barrels', "Barrel%"]
dfhitter = dfhitter.fillna(0)
dfhitter[columns] = dfhitter[columns].astype('float')

# Get the list of columns to zscore
numbers = dfhitter.select_dtypes(include='number').columns

# Zscore the columns
dfhitter[numbers] = dfhitter[numbers].apply(stats.zscore)

# Add a column for the total z-score
dfhitter['Total Z-Score'] = pd.Series(dtype=float)
dfhitter['Total Z-Score'] = dfhitter[numbers].sum(axis=1).round(2)
dfhitter = dfhitter.merge(temp_df[['Name', 'playerid']], on=["Name"], how="left")

dfpitcher = pd.read_csv('pitcher.csv')
temp_df2 = dfpitcher[['Name', 'playerid']]
dfpitcher = dfpitcher.drop(columns = ['playerid', 'mlbamid'])
dfpitcher = dfpitcher.fillna(0)

columns2 = ['Stuff+', 'Location+', 'Pitching+', 'Starting', 'Relieving']
dfpitcher[columns2] = dfpitcher[columns2].astype('float')

# Get the list of columns to zscore
numbers2 = dfpitcher.select_dtypes(include='number').columns

# Zscore the columns
dfpitcher[numbers2] = dfpitcher[numbers2].apply(stats.zscore)

# Add a column for the total z-score
dfpitcher['Total Z-Score'] = pd.Series(dtype=float)
dfpitcher['Total Z-Score'] = dfpitcher[numbers2].sum(axis=1).round(2)
dfpitcher = dfpitcher.merge(temp_df2[['Name', 'playerid']], on=["Name"], how="left")

today = date.today()
today = datetime.strptime(
    "2023-10-31", "%Y-%m-%d"
).date()  # pinning to last day of baseball season

def hitters_wk_preprocessing(filepath):
    '''Creates weekly hitter calcs'''
    df = pd.read_csv(filepath, index_col=["playerid"])

    df["Barrel%"] = df["Barrel%"] = df["Barrel%"].str.rstrip("%").astype("float")
    filter = df[(df["PA"] > 10)]

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["playerid"].isin(excluded["playerid"])]
    df = df.merge(dfhitter[["playerid", "Total Z-Score"]], on=["playerid"], how="left")

    filters = df[
        (df["wRC"] > 135)
        & (df["OPS"] > 0.8)
        & (df["K"] < 100)
        & (df["BB"] > 100)
        & (df["Off"] > 3)
        & (df["Barrel"] > 10)
    ].sort_values(by="Off", ascending=False)
    return filters


def hitters_pa_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["playerid"])

    df["Barrel%"] = df["Barrel%"] = df["Barrel%"].str.rstrip("%").astype("float")
    filter = df[(df["PA"] > 10)]

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(columns={"K%-": "K", "BB%-": "BB"}, inplace=True)
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["playerid"].isin(excluded["playerid"])]
    df = df.merge(dfhitter[["playerid", "Total Z-Score"]], on=["playerid"], how="left")

    filters = df[
        (df["wRC"] > 115)
        & (df["OPS"] > 0.8)
        & (df["K"] < 110)
        & (df["BB"] > 90)
        & (df["Off"] > 5)
        & (df["Barrel"] > 10)
        & (df["PA"] > 40)
    ].sort_values(by="Off", ascending=False)
    return filters


def sp_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["playerid"])

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(
        columns={"K/BB": "KToBB", "HR/9": "HRPer9", "xFIP-": "XFIPMinus"}, inplace=True
    )
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["playerid"].isin(excluded["playerid"])]
    df = df.merge(dfpitcher[["playerid", "Total Z-Score"]], on=["playerid"], how="left")

    df["Barrel"] = df["Barrel"] = df["Barrel"].str.rstrip("%").astype("float")
    df["CSW"] = df["CSW"] = df["CSW"].str.rstrip("%").astype("float")

    filters1 = df[
        (df["Barrel"] < 7)
        & (df["Starting"] > 5)
        & (df["GS"] > 1)
        & (df["Pitching"] > 99)
        & (df["Total Z-Score"] > 8)
    ].sort_values(by="Starting", ascending=False)
    return filters1

def rp_preprocessing(filepath):
    df = pd.read_csv(filepath, index_col=["playerid"])

    df.columns = df.columns.str.replace("[+,-,%,]", "", regex=True)
    df.rename(
        columns={"K/BB": "KToBB", "HR/9": "HRPer9", "xFIP-": "XFIPMinus"}, inplace=True
    )
    df.fillna(0)
    df.reset_index(inplace=True)
    df = df[~df["playerid"].isin(excluded["playerid"])]
    df = df.merge(dfpitcher[["playerid", "Total Z-Score"]], on=["playerid"], how="left")

    df["Barrel"] = df["Barrel"] = df["Barrel"].str.rstrip("%").astype("float")
    df["CSW"] = df["CSW"] = df["CSW"].str.rstrip("%").astype("float")

    filters2 = df[
        (df["Barrel"] < 7)
        & (df["Total Z-Score"] > 8)
        & (df["Relieving"] > 0)
        & (df["Pitching"] > 99)
    ].sort_values(by="Relieving", ascending=False)
    return filters2


# Preprocess and export the dataframes to Excel workbook sheets
hitdaywindow = [7, 14]
pawindow = [40]
pitchdaywindow = [14, 30]
ipwindow = [10, 30]

df_list = []

with open("weeklyadds.csv", "w+") as f:
    for w in hitdaywindow:
        f.write(f"Hitters Last {w} Days\n\n")
        df = hitters_wk_preprocessing(f"fgl_hitters_last_{w}.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")

    for w in pawindow:
        f.write(f"Hitters {w} PA\n\n")
        df = hitters_pa_preprocessing(f"fgl_hitters_{w}_pa.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")

    for w in ipwindow:
        f.write(f"SP {w} Innings\n\n")
        df = sp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")
        f.write(f"RP {w} Innings\n\n")
        df = rp_preprocessing(f"fgl_pitchers_{w}_ip.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")

    for w in pitchdaywindow:
        f.write(f"Pitchers Last {w} Days\n\n")
        df = sp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")
        f.write(f"RP Last {w} Days\n\n")
        df = rp_preprocessing(f"fgl_pitchers_last_{w}.csv")
        df = df.sort_values(
            by="Total Z-Score", ascending=False
        )  # Sort by Zscore column
        df_list.append(df)
        df.to_csv(f, index=False)
        f.write("\n")