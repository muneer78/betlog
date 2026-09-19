def profit_multiplier(odds):
    return odds / 100 if odds > 0 else 100 / abs(odds)


def american_odds(multiplier):
    return multiplier * 100 if multiplier >= 1 else -100 / multiplier


odds = float(input("Enter American odds: "))
boost = float(input("Enter profit boost %: "))
bet = input("Enter bet amount (optional): ")

profit = profit_multiplier(odds) * (1 + boost / 100)

print(f"Boosted odds: {american_odds(profit):+.0f}")

if bet:
    bet = float(bet)
    print(f"Profit: ${bet * profit:.2f}")
    print(f"Payout: ${bet * (1 + profit):.2f}")
