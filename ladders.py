import numpy as np
import pandas as pd

# Read the CSV file and parse the 'Date' column as datetime
df = pd.read_csv("recladders.csv")

# Format the 'Date' column as '%m/%d/%Y'
df["Date"] = pd.to_datetime(arg=df["Date"], format="%Y-%m-%d")

df["PotentialProfit"] = (df["Odds"] / 100) * df["Amount"]
df["PotentialProfit"] = df["PotentialProfit"].round(2)

df["PotentialProfit"] = df["PotentialProfit"].apply(pd.to_numeric, errors="coerce")

df["PotentialPayout"] = df["PotentialProfit"] + df["Amount"].apply(
    pd.to_numeric, errors="coerce"
)
df["PotentialPayout"] = df["PotentialPayout"].round(2)

df["ImpliedProbability"] = 100 / (100 + df["Odds"]).round(2)

df["ExpectedValue"] = np.ceil(df["ImpliedProbability"] * df["Amount"]) - (
    (1 - df["ImpliedProbability"]) * df["Amount"]
)
df["ExpectedValue"] = df["ExpectedValue"].apply(pd.to_numeric, errors="coerce")
df["ExpectedValue"] = df["ExpectedValue"].round(2)

df["ImpliedProbability"] = (df["ImpliedProbability"] * 100).apply(
    pd.to_numeric, errors="coerce"
)
df["ImpliedProbability"] = (df["ImpliedProbability"]).round(2)

df["ActualPayout"] = np.nan
df["ActualPayout"] = df["ActualPayout"].apply(pd.to_numeric, errors="coerce")
df["ActualPayout"] = df["ActualPayout"].astype("float")

for i, row in df.iterrows():
    if row["Result"] == "L":
        df.at[i, "ActualPayout"] = row["Amount"] * -1
    elif row["Result"] == "W":
        df.at[i, "ActualPayout"] = row["PotentialProfit"]
    elif row["Result"] == "P":
        df.at[i, "ActualPayout"] = 0

df_copy = df.copy()

currency_columns = [
    "Amount",
    "PotentialProfit",
    "PotentialPayout",
    "ExpectedValue",
    "ActualPayout",
]
for col in currency_columns:
    df_copy[col] = df_copy[col].apply(
        lambda x: "${:,.2f}".format(x) if pd.notnull(x) else ""
    )

df_copy.to_csv("futuresbetlog.csv", index=False)

df2 = (
    df.groupby(df["Date"].dt.strftime("%Y-%m"))["ActualPayout"]
    .sum()
    .reset_index()
    .sort_values(by=["Date"])
)
df3 = df[["bet_group", "Amount", "ActualPayout"]]
df3 = df3.groupby("bet_group").sum().reset_index()
df3["ROI"] = df3["ActualPayout"] / df3["Amount"]
df3["ROI"] = (df3["ROI"] * 100).round(2)
df3 = df3.reindex(columns=["bet_group", "ActualPayout", "Amount", "ROI"]).round(2)

# Sum column values for A, B and C
sum_a = df["ActualPayout"].sum()
sum_b = df["Amount"].sum()

# Write only the sums to new data frame
df4 = pd.DataFrame({"TotalWon": sum_a, "TotalRisked": sum_b}, index=[0])
columns = ["TotalWon", "TotalRisked"]
df4[columns] = df4[columns].round(2)

# Divide sum of A by sum of B
df4["TotalROI"] = (df4["TotalWon"] / df4["TotalRisked"] * 100).round(2)

substr1 = "W"
wins = df.Result.str.count(substr1).sum()

substr2 = "L"
losses = df.Result.str.count(substr2).sum()

squareroot = np.sqrt((wins + losses))

df5 = pd.DataFrame({"TotalBetsWon": wins, "TotalBetsLost": losses}, index=[0])

gamblerz = (wins - losses) / squareroot
df5["gamblerzscore"] = gamblerz.round(2)
winning_pct = (wins / (wins + losses)) * 80
df5["winning_pct"] = winning_pct.round(2)

list_of_dfs = [df2, df3, df4, df5]
for df in list_of_dfs:
    df.rename(columns={"Amount": "MoneyRisked", "ActualPayout": "Profit"}, inplace=True)
    try:
        df["Profit"] = df["Profit"].astype(float).map("${:,.2f}".format)
        df["MoneyRisked"] = df["MoneyRisked"].astype(float).map("${:,.2f}".format)
        df["TotalWon"] = df["TotalWon"].astype(float).map("${:,.2f}".format)
        df["TotalRisked"] = df["TotalRisked"].astype(float).map("${:,.2f}".format)
    except KeyError:
        pass

titles = ["Profit by Month", "ROI by Team", "Total ROI", "Total Win Percentage"]

with open("laddersanalytics.csv", "w+") as f:
    for i, dfs in enumerate(list_of_dfs):
        f.write(titles[i] + "\n")  # Write the title
        dfs.to_csv(f, index=False)
        f.write("\n")
