def american_to_decimal(odds):
    if odds > 0:
        return (odds / 100) + 1
    else:
        return (100 / abs(odds)) + 1


def calculate_lay_stake_with_stake_returned(stake, back_odds, lay_odds):
    back_odds_decimal = american_to_decimal(back_odds)
    lay_odds_decimal = american_to_decimal(lay_odds)

    # Calculate the total return (profit + stake returned) from the back bet
    back_total_return = stake * back_odds_decimal

    # Calculate the lay stake required to match the total return
    lay_stake = (
        back_total_return / lay_odds_decimal
    )  # Adjusted formula when stake is returned

    return lay_stake


def main():
    stake = float(input("Enter the amount of your bet: "))
    back_odds = float(input("Enter the back bet odds (American odds): "))
    lay_odds = float(input("Enter the lay bet odds (American odds): "))

    lay_stake = calculate_lay_stake_with_stake_returned(stake, back_odds, lay_odds)

    print(f"The amount to be placed for the lay bet is: ${lay_stake:.2f}")


if __name__ == "__main__":
    main()
