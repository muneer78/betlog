def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)


def expected_value(odds, probability):
    profit = odds / 100 if odds > 0 else 100 / -odds
    return probability * profit - (1 - probability)


def calculate_edge(odds, probability):
    return probability - american_to_probability(odds)


def main():
    odds = 10000
    probability = 0.15

    implied_probability = american_to_probability(odds)
    edge = calculate_edge(odds, probability)
    ev = expected_value(odds, probability)

    print(f"Implied probability: {implied_probability:.2%}")
    print(f"Your probability: {probability:.2%}")
    print(f"Edge: {edge:.2%}")
    print(f"EV: {ev:.2f} units")


if __name__ == "__main__":
    main()
