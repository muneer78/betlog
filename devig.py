def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)


def probability_to_american(probability):
    if probability >= 0.5:
        return round(-100 * probability / (1 - probability))
    return round(100 * (1 - probability) / probability)


def devig(odds1, odds2):
    prob1 = american_to_probability(odds1)
    prob2 = american_to_probability(odds2)

    total = prob1 + prob2

    return prob1 / total, prob2 / total


def main():
    odds1 = -110
    odds2 = -110

    prob1, prob2 = devig(odds1, odds2)

    print(f"Side 1: {prob1:.2%} ({probability_to_american(prob1):+d})")
    print(f"Side 2: {prob2:.2%} ({probability_to_american(prob2):+d})")


if __name__ == "__main__":
    main()
