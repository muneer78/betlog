def american_to_implied_prob(american_odds):
    if american_odds > 0:
        implied_prob = 100 / (american_odds + 100)
    else:
        implied_prob = -american_odds / (-american_odds + 100)
    return implied_prob


def calculate_no_vig_odds(american_odds, user_confidence):
    implied_prob = american_to_implied_prob(american_odds)
    no_vig_prob = 1 / (implied_prob - (1 - implied_prob))
    no_vig_odds = 1 / no_vig_prob

    # Calculate the edge
    edge = user_confidence - implied_prob

    return no_vig_odds, edge


def implied_prob_to_american(implied_prob):
    if implied_prob > 0.5:
        american_odds = -100 / (implied_prob / (1 - implied_prob))
    else:
        american_odds = (1 - implied_prob) / implied_prob * 100
    return int(american_odds) if american_odds.is_integer(
    ) else round(american_odds)


def calculate_no_vig_to_american(no_vig_odds):
    implied_prob = 1 / no_vig_odds
    american_odds = implied_prob_to_american(implied_prob)
    return american_odds


# Example usage:
given_american_odds = (
    10000  # Replace with the American odds you want to remove the vig from
)
# Replace with the user's confidence in winning (as a decimal)
user_confidence = 0.15

no_vig_odds, edge = calculate_no_vig_odds(given_american_odds, user_confidence)
american_odds = calculate_no_vig_to_american(no_vig_odds)

print(f"Edge: {edge:.2%}")
