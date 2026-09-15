import math

import polars as pl

INPUT_FILE = "futures.csv"
BETLOG_FILE = "futuresbetlog.csv"
ANALYTICS_FILE = "futuresanalytics.csv"
PENDING_FILE = "pendingfuturesbets.csv"
CASHOUTS_FILE = "futurescashouts.csv"

CURRENCY_COLUMNS = [
    "Amount",
    "PushAmount",
    "PotentialProfit",
    "PotentialPayout",
    "Expected Value",
    "ActualPayout",
]


def currency(column: str) -> pl.Expr:
    """Format a numeric column as currency while preserving nulls as blanks."""
    return pl.col(column).map_elements(
        lambda value: f"${value:,.2f}" if value is not None else "",
        return_dtype=pl.String,
    )


def profit_by(column: str) -> pl.DataFrame:
    return (
        df.group_by(column)
        .agg(pl.col("ActualPayout").sum().round(2).alias("Profit"))
        .sort(column)
    )


def risk_by(column: str) -> pl.DataFrame:
    return (
        df.group_by(column)
        .agg(pl.col("Amount").sum().round(2).alias("MoneyRisked"))
        .sort(column)
    )


def write_analytics(sections: list[tuple[str, pl.DataFrame]]) -> None:
    with open(ANALYTICS_FILE, "w", encoding="utf-8", newline="") as output:
        for title, frame in sections:
            output.write(f"{title}\n")
            frame.write_csv(output)
            output.write("\n")


# Stripping code fields handles old rows containing values such as "W\t".
df = pl.read_csv(
    INPUT_FILE,
    schema_overrides={
        "Amount": pl.Float64,
        "Odds": pl.Float64,
        "PushAmount": pl.Float64,
    },
    try_parse_dates=True,
).with_columns(
    pl.col("Date").cast(pl.Date),
    pl.col("FreeBet").str.strip_chars(),
    pl.col("Result").str.strip_chars(),
    pl.col("Amount", "Odds").fill_null(0.0),
)

df = df.with_columns(pl.col("Odds").abs().alias("CleanedOdds"))
df = df.with_columns(
    pl.when(pl.col("Odds") > 0)
    .then(pl.col("CleanedOdds") / 100 * pl.col("Amount"))
    .otherwise(100 / pl.col("CleanedOdds") * pl.col("Amount"))
    .round(2)
    .alias("PotentialProfit"),
    pl.when(pl.col("Odds") > 0)
    .then(100 / (100 + pl.col("CleanedOdds")))
    .otherwise(pl.col("CleanedOdds") / (100 + pl.col("CleanedOdds")))
    .round(2)
    .alias("Probability"),
)
df = df.with_columns(
    pl.when(pl.col("FreeBet") == "Y")
    .then(pl.col("PotentialProfit"))
    .otherwise(pl.col("Amount") + pl.col("PotentialProfit"))
    .round(2)
    .alias("PotentialPayout"),
    (
        (pl.col("Probability") * pl.col("Amount")).ceil()
        - ((1 - pl.col("Probability")) * pl.col("Amount"))
    )
    .round(2)
    .alias("Expected Value"),
    (pl.col("Probability") * 100).round(2).alias("ImpliedProbability"),
).drop("Probability")

# Futures use P for pending and C for cashout. bet.csv uses different codes.
df = df.with_columns(
    pl.when((pl.col("Result") == "L") & (pl.col("FreeBet") == "N"))
    .then(-pl.col("Amount"))
    .when((pl.col("Result") == "L") & (pl.col("FreeBet") == "Y"))
    .then(0.0)
    .when((pl.col("Result") == "W") & (pl.col("FreeBet") == "Y"))
    .then(pl.col("PotentialProfit"))
    .when((pl.col("Result") == "W") & (pl.col("FreeBet") == "N"))
    .then(pl.col("PotentialPayout"))
    .when(pl.col("Result") == "C")
    .then(pl.col("PushAmount"))
    .when(pl.col("Result") == "P")
    .then(0.0)
    .otherwise(None)
    .cast(pl.Float64)
    .round(2)
    .alias("ActualPayout")
)

df.with_columns(currency(column) for column in CURRENCY_COLUMNS).write_csv(BETLOG_FILE)

roi_by_sport = (
    df.group_by("Sport")
    .agg(
        pl.col("ActualPayout").sum().round(2).alias("Profit"),
        pl.col("Amount").sum().round(2).alias("MoneyRisked"),
    )
    .with_columns(
        (pl.col("Profit") / pl.col("MoneyRisked") * 100).round(2).alias("ROI")
    )
    .sort("Sport")
)
profit_by_month = (
    df.group_by(pl.col("Date").dt.strftime("%Y-%m").alias("Date"))
    .agg(pl.col("ActualPayout").sum().round(2).alias("Profit"))
    .sort("Date")
)

total_won = df["ActualPayout"].sum()
total_risked = df["Amount"].sum()
total_roi = round(total_won / total_risked * 100, 2) if total_risked else None
total = pl.DataFrame(
    {
        "TotalWon": [total_won],
        "TotalRisked": [total_risked],
        "TotalROI": [total_roi],
    }
)

wins = df.filter(pl.col("Result") == "W").height
losses = df.filter(pl.col("Result") == "L").height
graded_bets = wins + losses
win_stats = pl.DataFrame(
    {
        "TotalBetsWon": [wins],
        "TotalBetsLost": [losses],
        "gamblerzscore": [
            round((wins - losses) / math.sqrt(graded_bets), 2) if graded_bets else None
        ],
        "winning_pct": [round(wins / graded_bets * 100, 2) if graded_bets else None],
    }
)

sections = [
    ("ROI By Sport", roi_by_sport),
    ("Profit by Sport", profit_by("Sport")),
    ("Risk by Sport", risk_by("Sport")),
    ("Profit by Month", profit_by_month),
    ("Profit by Sportsbook", profit_by("Sportsbook")),
    ("Risk by Sportsbook", risk_by("Sportsbook")),
    ("Profit by System", profit_by("System")),
    ("Total ROI", total),
    ("Total Win Percentage", win_stats),
    ("Profit by Free Bet vs. Money Bet", profit_by("FreeBet")),
    ("Risk by Free Bet vs. Money Bet", risk_by("FreeBet")),
]
money_columns = {"Profit", "MoneyRisked", "TotalWon", "TotalRisked"}
formatted_sections = [
    (
        title,
        frame.with_columns(
            currency(column) for column in frame.columns if column in money_columns
        ),
    )
    for title, frame in sections
]
write_analytics(formatted_sections)

df.filter(pl.col("Result") == "P").drop(
    "Result", "PushAmount", "CleanedOdds", "ActualPayout"
).write_csv(PENDING_FILE)

cashouts = (
    df.filter(pl.col("Result") == "C")
    .select("Pick", "Sport", "ActualPayout", "Amount")
    .with_columns(
        (pl.col("ActualPayout") / pl.col("Amount") * 100).round(2).alias("ROI")
    )
    .with_columns(currency("ActualPayout"), currency("Amount"))
)
cashouts.write_csv(CASHOUTS_FILE)
