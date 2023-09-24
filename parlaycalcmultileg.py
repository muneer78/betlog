# Function to convert positive American odds to decimal odds
def american_to_decimal_positive(american_odds) :
    decimal_odds = (american_odds / 100) + 1
    return decimal_odds


# Function to convert negative American odds to decimal odds
def american_to_decimal_negative(american_odds) :
    decimal_odds = (100 / abs ( american_odds )) + 1
    return decimal_odds


# Function to convert decimal odds to American odds
def decimal_to_american(decimal_odds) :
    if decimal_odds > 2.0 :
        american_odds = (decimal_odds - 1) * 100
    else :
        american_odds = -100 / (decimal_odds - 1)
    return int ( american_odds )


# Function to calculate odds needed to reach a target parlay of +100
def calculate_parlay_odds(target_parlay_odds , current_parlay_odds) :
    needed_odds = (target_parlay_odds / current_parlay_odds) * -100
    return needed_odds


# Initialize variables
legs = [ ]  # List to store American odds for each leg
total_decimal_odds = 1  # Initialize total decimal odds to 1

# Input American odds for each leg of the parlay
while True :
    american_odds = float ( input ( "Enter American odds for the next leg (or 0 to calculate): " ) )

    if american_odds == 0 :
        break

    legs.append ( american_odds )

    if american_odds > 0 :
        decimal_odds = american_to_decimal_positive ( american_odds )
    else :
        decimal_odds = american_to_decimal_negative ( american_odds )

    total_decimal_odds *= decimal_odds  # Update total decimal odds based on each leg

# Calculate and display the total American odds
total_american_odds = decimal_to_american ( total_decimal_odds )

# Check if the total American odds are already above +100
if total_american_odds > 100 :
    print ( "This parlay is already above +100" )
else :
    # Calculate and display the required American odds to reach a parlay of +100
    required_odds = calculate_parlay_odds ( 100 , total_decimal_odds )
    print ( f"American odds needed to reach a parlay of +100: {int ( required_odds ):+d}" )

# Display the total American odds for the parlay
print ( f"Total American Odds for the Parlay: {int ( total_american_odds ):+d}" )