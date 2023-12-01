# Function to convert positive American odds to decimal odds
def american_to_decimal_positive(american_odds):
    decimal_odds = (american_odds / 100) + 1
    return decimal_odds


# Function to convert negative American odds to decimal odds
def american_to_decimal_negative(american_odds):
    decimal_odds = (100 / abs(american_odds)) + 1
    return decimal_odds


# Function to convert decimal odds to American odds
def decimal_to_american(decimal_odds):
    if decimal_odds > 2.0:
        american_odds = (decimal_odds - 1) * 100
    else:
        american_odds = -100 / (decimal_odds - 1)
    return int(american_odds)


# Function to calculate odds needed to reach a target parlay of 2
# (equivalent to +100 in American odds)
def calculate_parlay_odds(target_parlay_odds, current_parlay_odds):
    needed_odds = target_parlay_odds / current_parlay_odds
    return needed_odds


# Initialize variables
legs = []  # List to store American odds for each leg
total_decimal_odds = 1.0  # Initialize total decimal odds to 1.0

# Input American odds for each leg of the parlay
while True:
    american_odds = float(
        input("Enter American odds for the next leg (or 0 to calculate): "))

    if american_odds == 0:
        break

    legs.append(american_odds)

    if american_odds > 0:
        decimal_odds = american_to_decimal_positive(american_odds)
    else:
        decimal_odds = american_to_decimal_negative(american_odds)

    total_decimal_odds *= decimal_odds  # Update total decimal odds based on each leg

# Calculate and display the total decimal odds
print(f"Total Decimal Odds for the Parlay: {total_decimal_odds:.2f}")

# Check if the total decimal odds are already above 2.0 (equivalent to
# +100 in American odds)
if total_decimal_odds >= 2.0:
    print("This parlay is already above +100 in American odds")
else:
    # Calculate the odds needed for the next leg to make the parlay reach 2.0
    # in decimal odds
    required_odds = calculate_parlay_odds(2.0, total_decimal_odds)

    # Convert the required decimal odds to American odds for the output
    required_odds_american = decimal_to_american(required_odds)

    print(
        f"To achieve a parlay odds of +100 with the current legs and a new leg, the next leg needs to have American odds of {required_odds_american:+d}")

# Display the total American odds for the parlay
total_american_odds = decimal_to_american(total_decimal_odds)
print(f"Total American Odds for the Parlay: {total_american_odds:+d}")
