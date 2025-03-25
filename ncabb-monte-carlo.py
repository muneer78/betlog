import csv
import random
import math
from collections import Counter

year = '2025'

# Function to simulate a single round
def simulate_round(teams):
    next_round_teams = []
    winners_per_round = []
    for i in range(0, len(teams), 2):
        seed_weight = int(teams[i][1]) - int(teams[i + 1][1])
        correction = round(math.sqrt(abs(seed_weight) * 50), 4)
        if seed_weight < 0:
            correction = -1 * correction
        r1 = random.randint(0, 100)
        if r1 < (50 + correction):
            next_round_teams.append(teams[i + 1])
            winners_per_round.append(teams[i + 1][0])
        else:
            next_round_teams.append(teams[i])
            winners_per_round.append(teams[i][0])
    return next_round_teams, winners_per_round

# write round of 64 bracket to list
next_round_teams = []
with open(fr'/Users/muneer78/Documents/Projects/fantasy-sports/bracket{year}.csv', mode='r') as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        next_round_teams.append(line)

# Store winners for each game in each round
round_winners = {round_num: [] for round_num in range(1, 7)}

# Run simulations
for simulation in range(5):
    teams = next_round_teams[:]
    for round_num in range(1, 7):
        if len(teams) == 1:
            break
        teams, winners_per_round = simulate_round(teams)
        round_winners[round_num].extend(winners_per_round)

# Find the most common winners for each game in each round
most_common_winners_per_round = {}
for round_num, winners in round_winners.items():
    most_common_winners_per_round[round_num] = Counter(winners).most_common()

# Write the most common winners for each game in each round to final output
with open(fr"/Users/muneer78/Downloads/{year}_montecarlo_results.txt", "w") as f:
    for round_num, winners in most_common_winners_per_round.items():
        print(f"Round of {2**(6-round_num)}:", file=f)
        for i, (winner, count) in enumerate(winners):
            print(f"Team {i+1}: {winner} ({count} times)", file=f)
        print("\n", file=f)

print(f"Simulation complete. Results written to {year}_montecarlo_results.txt")