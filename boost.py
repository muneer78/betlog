def calculate_boosted_payout(american_odds, wager, boost_percent):
  """Calculates the boosted payout on a bet with American odds.

  Args:
      american_odds: The American odds as an integer.
      wager: The amount wagered on the bet.
      boost_percent: The percentage boost as an integer (e.g., 50 for a 50% boost).

  Returns:
      A tuple containing the initial payout and the boosted payout (both as floats).
  """

  decimal_odds = 100 / (-american_odds + 100)
  initial_payout = decimal_odds * wager

  boosted_odds = decimal_odds * (1 + boost_percent / 100)
  boosted_payout = boosted_odds * wager

  return initial_payout, boosted_payout

# Example usage:
american_odds = -215
wager = 25
boost_percent = 33  # 10% boost

initial_payout, boosted_payout = calculate_boosted_payout(american_odds, wager, boost_percent)

print(f"Initial Payout: ${initial_payout:.2f}")
print(f"Boosted Payout: ${boosted_payout:.2f}")
