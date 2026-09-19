def american_to_decimal(odds):
    return 1 + (odds / 100 if odds > 0 else 100 / abs(odds))


def main():
    stake = float(input("Free bet amount: $"))
    back = american_to_decimal(float(input("Back odds: ")))
    lay = american_to_decimal(float(input("Lay odds: ")))

    back_profit = stake * (back - 1)
    lay_stake = back_profit / lay
    liability = lay_stake * (lay - 1)
    profit = lay_stake
    conversion = profit / stake * 100

    print(f"Lay stake: ${lay_stake:.2f}")
    print(f"Lay liability: ${liability:.2f}")
    print(f"Guaranteed profit: ${profit:.2f}")
    print(f"Conversion: {conversion:.2f}%")


if __name__ == "__main__":
    main()
