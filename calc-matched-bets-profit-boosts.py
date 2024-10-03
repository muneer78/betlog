def american_to_decimal(odds):
    if odds < 0:
        return round((100 / abs(odds)) + 1, 2)
    else:
        return round((odds / 100) + 1, 2)
def calculate_arbitrage_profit(odds_a, odds_b, stake):
    # Convert American odds to decimal
    odds_a_decimal = american_to_decimal(odds_a)
    odds_b_decimal = american_to_decimal(odds_b)

    # Calculate arbitrage percentages
    arbitrage_percent_a = (1 / odds_a_decimal) * 100
    arbitrage_percent_b = (1 / odds_b_decimal) * 100
    total_arbitrage_percent = arbitrage_percent_a + arbitrage_percent_b

    if total_arbitrage_percent > 100:
        print("This is not an arbitrage opportunity.")
        return 0, 0, 0, 0, 0

    # Calculate stake for outcome B
    stake_b = stake * (odds_a_decimal / odds_b_decimal)

    # Calculate profit for outcome B
    profit_b = (stake_b * odds_b_decimal) - stake

    # Calculate profit for outcome A
    profit_a = (stake * odds_a_decimal) - stake_b

    # Calculate potential losses if each bet loses
    loss_1 = (-1 * stake)
    loss_2 = (-1 * stake_b)

    # Adjust profit for each outcome if each bet loses
    outcome_1 = profit_a + loss_1
    outcome_2 = profit_b + loss_2

    # Calculate payouts if each bet wins
    payout_outcome_1 = stake + outcome_1
    payout_outcome_2 = stake_b + outcome_2

    return outcome_1, outcome_2, stake_b, loss_1, loss_2, payout_outcome_1, payout_outcome_2

# Example usage
odds_a_american = -117
odds_b_american = 150
stake = 10  # Example stake

outcome_1, outcome_2, stake_b, loss_1, loss_2, payout_outcome_1, payout_outcome_2 = calculate_arbitrage_profit(odds_a_american, odds_b_american, stake)
print("Stake for outcome B: ${:.2f}".format(stake_b))
print("Profit for Outcome 1: ${:.2f}".format(outcome_1))
print("Profit for Outcome 2: ${:.2f}".format(outcome_2))
print("Payout if Outcome 1 wins: ${:.2f}".format(payout_outcome_1))
print("Payout if Outcome 2 wins: ${:.2f}".format(payout_outcome_2))