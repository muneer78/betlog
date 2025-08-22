# Function to convert American odds to decimal odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    elif american_odds < 0:
        decimal_odds = 1 - (100 / american_odds)
    else:
        return None  # Return None for American odds of 0
    return decimal_odds


# Function to convert decimal odds to American odds
def decimal_to_american(decimal_odds):
    if decimal_odds > 2:
        american_odds = (decimal_odds - 1) * 100
    elif decimal_odds < 2:
        american_odds = -100 / (decimal_odds - 1)
    else:
        return 0  # Return 0 for even odds (decimal odds of 2)
    return int(american_odds)


# Input American odds for the current leg (Leg1 odds)
leg1_odds = float(input("Enter American odds for the first leg: "))

decimal_odds_leg1 = american_to_decimal(leg1_odds)
if decimal_odds_leg1 is not None:
    print(f"Decimal odds for the first leg: {decimal_odds_leg1:.2f}")
    required_odds = 2 / decimal_odds_leg1

    if leg1_odds > 0:
        required_american_odds = decimal_to_american(required_odds)
    elif leg1_odds < 0:
        required_american_odds = decimal_to_american(required_odds)
    else:
        required_american_odds = 0

    print(f"Odds needed to reach a parlay of +100: {required_odds:.2f}")
    print(
        f"American odds needed to reach a parlay of +100: {required_american_odds:+d}"
    )
else:
    print("American odds of 0 cannot be converted to decimal odds.")
