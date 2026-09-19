import polars as pl
from scipy.stats import poisson

SCHEDULE_FILE = "roster-resource-download.xlsx"
PITCHERS_FILE = "fangraphs-leaderboards.csv"
TEAMS_FILE = "fangraphs-leaderboards (1).csv"


def implied_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)


def fair_odds(probability):
    if probability >= 0.5:
        return round(-100 * probability / (1 - probability))
    return round(100 * (1 - probability) / probability)


def prop_probability(average, line, side):
    cutoff = int(line)

    if side == "OVER":
        return poisson.sf(cutoff, average)

    return poisson.cdf(cutoff, average)


def load_pitchers():
    return (
        pl.read_csv(PITCHERS_FILE)
        .with_columns(
            (pl.col("SO") / pl.col("GS")).alias("K/GS"),
            (pl.col("BB") / pl.col("GS")).alias("BB/GS"),
            (pl.col("IP") / pl.col("GS")).alias("IP/G"),
        )
        .filter(
            (pl.col("GS") > 1)
            & pl.col("IP/G").is_between(5, 7)
            & (pl.col("K/GS") <= 9)
            & (pl.col("BB/GS") <= 6)
        )
    )


def load_teams():
    teams = pl.read_csv(TEAMS_FILE).select("Team", "K%", "BB%")

    k_rank = (
        teams.sort("K%", descending=True)
        .with_row_index("KRank", offset=1)
        .select("Team", "KRank")
    )

    bb_rank = (
        teams.sort("BB%").with_row_index("BBRank", offset=1).select("Team", "BBRank")
    )

    return k_rank.join(bb_rank, on="Team")


def load_schedule(day):
    pitcher_col = 1 if day == "today" else 2

    df = pl.read_excel(SCHEDULE_FILE).select(pl.all().gather([0, pitcher_col]))

    team_col, pitcher_col = df.columns

    return (
        df.rename({pitcher_col: "Name"})
        .with_columns(
            pl.col("Name")
            .str.split("\n")
            .list.slice(1)
            .list.join("\n")
            .str.replace_all(r"\s*\([RL]\)", "")
            .str.strip_chars(),
            pl.col(team_col)
            .str.split("\n")
            .list.first()
            .str.replace("@ ", "")
            .alias("Team"),
        )
        .select("Name", "Team")
    )


def find_candidates(day):
    pitchers = load_pitchers()
    schedule = load_schedule(day).join(
        load_teams(),
        on="Team",
        how="left",
    )

    k_overs = (
        schedule.join(
            pitchers.sort("K%+", descending=True).head(25).select("Name", "K/GS"),
            on="Name",
        )
        .filter(pl.col("KRank") <= 10)
        .select(
            "Name",
            pl.lit("K").alias("Prop"),
            pl.lit("OVER").alias("Side"),
            pl.col("K/GS").alias("Average"),
        )
    )

    bb_unders = (
        schedule.join(
            pitchers.sort("BB%+").head(25).select("Name", "BB/GS"),
            on="Name",
        )
        .filter(pl.col("BBRank") <= 10)
        .select(
            "Name",
            pl.lit("BB").alias("Prop"),
            pl.lit("UNDER").alias("Side"),
            pl.col("BB/GS").alias("Average"),
        )
    )

    return pl.concat([k_overs, bb_unders])


def evaluate_bet(name, prop, side, average, line, odds):
    probability = prop_probability(average, line, side)
    implied = implied_probability(odds)
    edge = probability - implied

    return {
        "Name": name,
        "Prop": prop,
        "Side": side,
        "Average": round(average, 2),
        "Line": line,
        "Probability": round(probability, 4),
        "Fair Odds": fair_odds(probability),
        "Book Odds": odds,
        "Edge": round(edge, 4),
        "Bet": edge > 0,
    }
