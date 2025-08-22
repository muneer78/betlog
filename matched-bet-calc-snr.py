def american_to_decimal(odds):
    if odds > 0:
        return (odds / 100) + 1
    else:
        return (100 / abs(odds)) + 1


def calculate_matched_bet(stake, back_odds, lay_odds):
    back_odds_decimal = american_to_decimal(back_odds)
    lay_odds_decimal = american_to_decimal(lay_odds)

    # Calculate the potential profit from the back bet (stake not returned for free bet)
    back_profit = stake * (back_odds_decimal - 1)

    # Calculate the lay stake required to match the potential profit
    lay_stake = back_profit / lay_odds_decimal  # Adjusted formula for free bets

    return lay_stake


def main():
    stake = float(input("Enter the amount of your free bet: "))
    back_odds = float(input("Enter the back bet odds (American odds): "))
    lay_odds = float(input("Enter the lay bet odds (American odds): "))

    lay_stake = calculate_matched_bet(stake, back_odds, lay_odds)

    print(f"The amount to be placed for the lay bet is: ${lay_stake:.2f}")


if __name__ == "__main__":
    main()
