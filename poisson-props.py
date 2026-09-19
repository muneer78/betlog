"""

file format:
name,average,line,over_odds,under_odds
Player A rebounds,2.7,3.5,280,-350
Player B assists,5.8,5.5,110,-140
Player C threes,3.2,2.5,-125,100

uv run python poisson-props.py props.csv

"""

import csv
import sys

from scipy.stats import poisson


def implied_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)


def fair_odds(probability):
    if probability >= 0.5:
        return round(-100 * probability / (1 - probability))
    return round(100 * (1 - probability) / probability)


def analyze(row):
    average = float(row["average"])
    line = float(row["line"])
    over_odds = int(row["over_odds"])
    under_odds = int(row["under_odds"])

    cutoff = int(line)

    over_probability = poisson.sf(cutoff, average)
    under_probability = poisson.cdf(cutoff, average)

    over_edge = over_probability - implied_probability(over_odds)
    under_edge = under_probability - implied_probability(under_odds)

    if over_edge > under_edge and over_edge > 0:
        bet = "OVER"
    elif under_edge > 0:
        bet = "UNDER"
    else:
        bet = "NO BET"

    return {
        **row,
        "over_fair_odds": fair_odds(over_probability),
        "under_fair_odds": fair_odds(under_probability),
        "bet": bet,
    }


with open(sys.argv[1], newline="") as f:
    bets = list(csv.DictReader(f))

for bet in map(analyze, bets):
    print(
        f"{bet['name']}: "
        f"Over {bet['over_fair_odds']:+} | "
        f"Under {bet['under_fair_odds']:+} | "
        f"{bet['bet']}"
    )
