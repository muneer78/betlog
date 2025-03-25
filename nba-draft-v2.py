import numpy as np
from collections import Counter

n_teams = 12
n_trials = int(1e7)

probs = [ 2**i for i in range(0,n_teams) ]
probs = [ prob_i / sum(probs) for prob_i in probs ]

lottery_results = np.zeros([n_trials, n_teams],dtype=np.int8) # to store the positions at each lottery
for i in range(n_trials):
    lottery_results[i,:] = np.random.choice(n_teams, n_teams, replace=False, p=probs)

for i in range(n_teams):
    positions = Counter(lottery_results[:,i])
    print("Team {}".format(i), dict(sorted(positions.items())))