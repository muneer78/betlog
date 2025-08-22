# Function to convert American odds to decimal odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    elif american_odds < 0:
        decimal_odds = 1 + (100 / abs(american_odds))
    else:
        return None  # Return None for American odds of 0
    return decimal_odds


# Input American odds for the current leg (Leg1 odds)
american_odds = float(input("Enter American odds: "))
boost = float(input("Enter boosted odds: "))

# Convert American odds to decimal odds
odds_decimal = american_to_decimal(american_odds)
boost_decimal = american_to_decimal(boost)

# Calculate boosted odds profit to original odds profit ratio
boost_percent = (boost_decimal / odds_decimal) - 1

print(f"The boosted odds increased your payout by {boost_percent * 100:.2f}%")
