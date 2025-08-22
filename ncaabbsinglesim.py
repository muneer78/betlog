import csv
import random
import math
from rich import print

# write round of 64 bracket to list
next_round_teams = []
with open("bracket2024.csv", mode="r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        next_round_teams.append(line)

# write everything to results text file
with open("results.txt", "w") as f:
    while 1:
        # define list of teams for this round and clean list for next round
        teams = next_round_teams
        next_round_teams = []

        # print which round we are in
        print(f"######### ROUND OF {len(teams)} #########\n", file=f)

        # loop through all the teams, 2 at a time (each pass of the loop those two teams play eachother)
        for i in range(0, len(teams), 2):
            # print the teams playing one another
            print(
                f"#{teams[i][1]} {teams[i][0]} plays #{teams[i + 1][1]} {teams[i + 1][0]}",
                file=f,
            )

            # get the difference in team seeding
            seed_weight = int(teams[i][1]) - int(teams[i + 1][1])

            # compute a 'correction' factor based on the difference in seeding
            correction = round(math.sqrt(abs(seed_weight) * 50), 4)
            if seed_weight < 0:
                correction = -1 * correction

            # compute a random number between 0 and 100
            r1 = random.randint(0, 100)

            # print out the seed weight and random number
            print(f"seed weight: {correction:.4f}", file=f)
            print(f"random integer (0-100): {r1}", file=f)

            # pick winner based on random number and 'correction' factor
            if r1 < (50 + correction):
                next_round_teams.append(teams[i + 1])
            else:
                next_round_teams.append(teams[i])

            # print results
            print(
                f"since {r1} {'>' if r1 > 50 + correction else '<'} {(50 + correction):.4f}"
                + f" #{next_round_teams[-1][1]} {next_round_teams[-1][0]} wins\n",
                file=f,
            )

        # add a few line break between rounds
        print("\n\n", file=f)

        # if the number of next round teams is 1, we know we just finished the last round
        if len(next_round_teams) == 1:
            break
