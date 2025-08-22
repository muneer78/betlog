from rich import print


def implied_probability(odds):
    """Convert odds to implied probability"""
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)


odds = float(input("Enter odds: "))

implied_prob = implied_probability(odds) * 100

print(f"The implied probability is {implied_prob:.2f}%")
