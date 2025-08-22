import math

import polars as pl

# Load data from CSV using Polars
df = pl.read_csv("futures.csv", try_parse_dates=True)

# Define the columns you want to convert to float and fill NaN with 0
cols_to_convert = ["Amount", "Odds", "PushAmount"]

# Convert specified columns to float and fill NaN with 0
for col in cols_to_convert:
    df = df.with_columns(
        pl.when(df[col].is_not_null())
        .then(df[col].cast(float))
        .otherwise(pl.col(col))
        .alias(col)
    )

# Create 'CleanedOdds' column
df = df.with_columns(df["Odds"].abs().alias("CleanedOdds"))

# Calculate 'PotentialProfit' column
df = df.with_columns(
    pl.when(df["Odds"] > 0)
    .then((df["CleanedOdds"] / 100) * df["Amount"])
    .otherwise((100 / df["CleanedOdds"]) * df["Amount"])
    .round(2)
    .alias("PotentialProfit")
)

# Convert 'PotentialProfit' and 'CleanedOdds' columns to numeric, handling
# coercion
cols2 = ["PotentialProfit", "CleanedOdds"]

# Convert specified columns to float
for col in cols2:
    df = df.with_columns(
        pl.when(df[col].is_not_null()).then(df[col].cast(float)).otherwise(0).alias(col)
    )

# Calculate the "PotentialPayout" column based on 'FreeBet' column
df = df.with_columns(
    pl.when(df["FreeBet"] == "N")
    .then(df["Amount"] + df["PotentialProfit"])
    .otherwise(df["PotentialProfit"])
    .round(2)
    .alias("PotentialPayout")
)

# Calculate 'ImpliedProbability' column
df = df.with_columns(
    pl.when(df["Odds"] > 0)
    .then((100 / (100 + df["CleanedOdds"])))
    .otherwise((df["CleanedOdds"]) / (100 + df["CleanedOdds"]))
    .round(2)
    .alias("ImpliedProbability")
)

# Calculate 'Expected Value' column
df = df.with_columns(
    (
        (df["ImpliedProbability"] * df["Amount"]).ceil()
        - ((1 - df["ImpliedProbability"]) * df["Amount"])
    )
    .cast(float)
    .round(2)
    .alias("Expected Value")
)

# Convert 'ImpliedProbability' column to percentage
df = df.with_columns((df["ImpliedProbability"] * 100).alias("ImpliedProbability"))

# df = df.with_columns(pl.col('ActualPayout').fill_nan(0))

# Update 'ActualPayout' based on conditions
df = df.with_columns(
    pl.when((df["Result"] == "L") & (df["FreeBet"] == "N"))
    .then(df["Amount"] * -1)
    .when((df["Result"] == "L") & (df["FreeBet"] == "Y"))
    .then(0)
    .when((df["Result"] == "W") & (df["FreeBet"] == "Y"))
    .then(df["PotentialProfit"])
    .when((df["Result"] == "W") & (df["FreeBet"] == "N"))
    .then(df["PotentialPayout"])
    .when(df["Result"] == "Pe")
    .then(0)
    .when(df["Result"] == "P")
    .then(df["PushAmount"])
    .otherwise(df["PotentialPayout"])
    .round(2)
    .alias("ActualPayout")
)

# Create a copy of the DataFrame for formatting
df_copy = df.clone()

# Format currency columns
currency_columns = [
    "Amount",
    "PushAmount",
    "PotentialProfit",
    "PotentialPayout",
    "Expected Value",
    "ActualPayout",
]
for col in currency_columns:
    df_copy = df_copy.with_columns(
        df_copy[col].map_elements(
            lambda x: "${:,.2f}".format(x) if x is not None else ""
        )
    )

# Save the formatted DataFrame to a CSV file
df_copy.write_csv("futuresbetlog.csv")

# Group and calculate 'ROI' by 'Sport'
df2 = df[["Sport", "Amount", "ActualPayout"]]
df2 = df2.group_by("Sport").agg(
    pl.sum("ActualPayout").alias("ActualPayout"),
    pl.sum("Amount").alias("Amount"),
    ((pl.sum("ActualPayout") / pl.sum("Amount")) * 100).round(2).alias("ROI"),
)

# Extract year and month from the 'Date' column
df3 = df.with_columns(
    df["Date"].map_elements(lambda x: x.year).alias("Year"),
    df["Date"].map_elements(lambda x: x.month).alias("Month"),
)

# Group and calculate 'TotalPayout' by year and month
df3 = df3.group_by(["Year", "Month"]).agg(
    pl.sum("ActualPayout").round(2).alias("TotalPayout")
)

# Sort the DataFrame by 'Year' and 'Month'
df3 = df3.sort(["Year", "Month"])

# Group and calculate 'ROI' by 'Sportsbook'
df4 = df[["Sportsbook", "Amount", "ActualPayout"]]
df4 = df4.group_by("Sportsbook").agg(
    pl.sum("ActualPayout").alias("ActualPayout"),
    pl.sum("Amount").alias("Amount"),
    ((pl.sum("ActualPayout") / pl.sum("Amount")) * 100).round(2).alias("ROI"),
)

# Group and calculate 'TotalPayout' by 'System'
df5 = df.group_by("System").agg(pl.sum("ActualPayout").round(2).alias("TotalPayout"))

# Group and calculate 'ROI' by 'FreeBet'
df6 = df[["FreeBet", "Amount", "ActualPayout"]]
df6 = df6.group_by("FreeBet").agg(
    pl.sum("ActualPayout").alias("ActualPayout"),
    pl.sum("Amount").alias("Amount"),
    ((pl.sum("ActualPayout") / pl.sum("Amount")) * 100).round(2).alias("ROI"),
)

# Calculate total sums and ROI
total_won = df["ActualPayout"].sum()
total_risked = df["Amount"].sum()
total_roi = (total_won / total_risked) * 100

# Create DataFrame for total statistics
df7 = pl.DataFrame(
    {"TotalWon": [total_won], "TotalRisked": [total_risked], "TotalROI": [total_roi]}
)

# Filter the DataFrame to select rows where 'Result' is equal to 'W'
filtered_df1 = df.filter(pl.col("Result") == "W")

# Count the number of rows in the filtered DataFrame and alias the result as 'Wins'
# wins = filtered_df1.agg(pl.count().alias('Wins'))
wins = len(filtered_df1)

# Filter the DataFrame to select rows where 'Result' is equal to 'W'
filtered_df2 = df.filter(pl.col("Result") == "L")

# Count the number of rows in the filtered DataFrame and alias the result as 'Wins'
# losses = filtered_df2.agg(pl.count().alias('Losses'))
losses = len(filtered_df2)

# Calculate win count, loss count, Gambler's Z-Score, and winning percentage
# wins = df.group_by('Result').filter(pl.col('Result') == 'W').agg(pl.count().alias('Wins'))
# losses = wins = df.group_by('Result').filter(pl.col('Result') == 'L').agg(pl.count().alias('Losses'))
# squareroot = pl.sqrt(wins + losses)
squareroot = math.sqrt(wins + losses)
gamblerz = (wins - losses) / squareroot
winning_pct = (wins / (wins + losses)) * 100

df8 = pl.DataFrame(
    {
        "TotalBetsWon": [wins],
        "TotalBetsLost": [losses],
        "GamblerzScore": [gamblerz],
        "WinningPercentage": [winning_pct],
    }
)

# Create a list of DataFrames and corresponding titles
list_of_dfs = [df2, df3, df4, df5, df6, df7, df8]
titles = [
    "ROI By Sport",
    "Profit by Month",
    "ROI by Sportsbook",
    "Profit by System",
    "Free Bet ROI",
    "Total Win Percentage",
    "Total ROI",
]

# Define the CSV file path
csv_file_path = "futuresanalytics.csv"

# Open the CSV file for writing
with open(csv_file_path, "w+") as f:
    for i, current_df in enumerate(list_of_dfs):
        # Write the title as a comment in the CSV file
        f.write(f"# {titles[i]}\n")

        # Create a temporary DataFrame with only the title as a single row
        title_df = pl.DataFrame([titles[i]])

        # Write the title DataFrame to the CSV file using polars.write_csv
        title_df.write_csv(
            f, has_header=False, separator=",", line_terminator="\n", quote='"'
        )

        # Write an empty line to separate sections
        f.write("\n")

        # Write the current DataFrame to the CSV file using polars.write_csv
        current_df.write_csv(
            f, has_header=True, separator=",", line_terminator="\n", quote='"'
        )

# Filter rows with 'Result' equal to 'Pe' and 'P'
filter1 = df.filter((df["Result"] == "Pe") | (df["Result"] == "P"))

# Drop columns
columns_to_drop = ["Result", "PushAmount"]
filter1 = filter1.drop(columns_to_drop)

# Save the filtered DataFrame to a CSV file
filter1.write_csv(
    "pendingfuturesbets.csv",
    has_header=True,
    separator=",",
    line_terminator="\n",
    quote='"',
)

# Filter rows with 'Result' equal to 'P' and update 'ActualPayout'
filter2 = df.filter(df["Result"] == "P")
filter2 = filter2.with_columns(
    pl.when(filter2["Result"] == "P")
    .then(filter2["PushAmount"])
    .otherwise(filter2["ActualPayout"])
    .cast(float)
    .round(2)
    .alias("ActualPayout")
)

# Select and format columns
cols3 = ["Amount", "ActualPayout"]
filter2 = filter2.select(cols3).with_columns(
    pl.col("Amount").cast(float).map_elements(lambda x: "${:,.2f}".format(x)),
    pl.col("ActualPayout").cast(float).map_elements(lambda x: "${:,.2f}".format(x)),
)

# Save the filtered and formatted DataFrame to a CSV file
filter2.write_csv(
    "futurescashouts.csv",
    has_header=True,
    separator=",",
    line_terminator="\n",
    quote='"',
)
