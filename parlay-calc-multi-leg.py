def american_to_decimal(odds):
    if odds > 0:
        return 1 + odds / 100
    return 1 + 100 / abs(odds)


def decimal_to_american(odds):
    if odds >= 2:
        return round((odds - 1) * 100)
    return round(-100 / (odds - 1))


decimal_odds = 1.0

while True:
    odds = float(input("Enter leg odds (0 to finish): "))

    if odds == 0:
        break

    decimal_odds *= american_to_decimal(odds)

    current_odds = decimal_to_american(decimal_odds)
    print(f"Current parlay: {current_odds:+d}")

    if decimal_odds < 2:
        needed_decimal = 2 / decimal_odds
        needed_odds = decimal_to_american(needed_decimal)
        print(f"Next leg needed for +100: {needed_odds:+d}")
    else:
        print("Parlay has reached +100 or better.")


bet = float(input("\nBet amount: $"))

american_odds = decimal_to_american(decimal_odds)
profit = bet * (decimal_odds - 1)
payout = bet * decimal_odds

print(f"\nFinal parlay odds: {american_odds:+d}")
print(f"Bet: ${bet:.2f}")
print(f"Profit: ${profit:.2f}")
print(f"Payout: ${payout:.2f}")
