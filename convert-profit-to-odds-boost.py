# Function to convert American odds to decimal odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    elif american_odds < 0:
        decimal_odds = 1 + (100 / abs(american_odds))
    else:
        return None  # Return None for American odds of 0
    return decimal_odds


def decimal_to_american(decimal_odds):
    if decimal_odds > 2:
        american_odds = (decimal_odds - 1) * 100
    elif decimal_odds < 2:
        american_odds = -100 / (decimal_odds - 1)
    else:
        return 0  # Return 0 for even odds (decimal odds of 2)
    return int(american_odds)


# Input American odds for the current leg (Leg1 odds)
american_odds = float(input("Enter American odds: "))
boost = float(input("Enter profit boost: "))

# Convert American odds to decimal odds
odds_decimal = american_to_decimal(american_odds)

# Calculate boosted odds profit to original odds profit ratio
minus_stake = odds_decimal - 1
boosted = (minus_stake * (1 + (boost / 100))) + 1
american_odds_after_boost = decimal_to_american(boosted)

print(f"The odds after the boost are {american_odds_after_boost}")
