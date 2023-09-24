# Function to convert positive American odds to decimal odds
def american_to_decimal_positive(american_odds):
    decimal_odds = (american_odds / 100) + 1
    return decimal_odds

# Function to convert negative American odds to decimal odds
def american_to_decimal_negative(american_odds):
    decimal_odds = (100 / abs(american_odds)) + 1
    return decimal_odds

# Function to calculate odds needed to reach a parlay of +100
def calculate_parlay_odds(target_parlay_odds, current_parlay_odds):
    needed_odds = (target_parlay_odds / current_parlay_odds) * -100
    return needed_odds

# Input American odds for the current parlay
current_parlay_odds = float(input("Enter American odds for the current parlay: "))

if current_parlay_odds > 0:
    decimal_odds = american_to_decimal_positive(current_parlay_odds)
    print(f"Decimal odds: {decimal_odds:.2f}")
    target_parlay_odds = 100  # Set the target parlay odds to +100
    target_decimal_odds = 1 + (target_parlay_odds / 100)
    required_decimal_odds = target_decimal_odds / decimal_odds
    required_american_odds = (required_decimal_odds - 1) * 100
    print(f"Odds needed to reach a parlay of +100: {required_decimal_odds:.2f}")
    print(f"American odds needed to reach a parlay of +100: {int(required_american_odds):+d}")
elif current_parlay_odds < 0:
    decimal_odds = american_to_decimal_negative(current_parlay_odds)
    print(f"Decimal odds: {decimal_odds:.4f}")
    target_parlay_odds = 100  # Set the target parlay odds to +100
    target_decimal_odds = 1 + (target_parlay_odds / 100)
    required_decimal_odds = target_decimal_odds / decimal_odds
    required_american_odds = -100 / (required_decimal_odds - 1)
    print(f"Odds needed to reach a parlay of +100: {required_decimal_odds:.2f}")
    print(f"American odds needed to reach a parlay of +100: {int(required_american_odds):+d}")
else:
    print("American odds of 0 cannot be converted to decimal odds.")