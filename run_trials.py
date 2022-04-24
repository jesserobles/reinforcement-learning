from collections import Counter
from time import time
from q_learning_agent import run_trial
world_id = 0
base_url = 'https://www.notexponential.com/'
trials = []
num_trials = 100
start = time()
for t in range(num_trials):
    print(f"Running trial {t + 1} of {num_trials}")
    trial = run_trial(world_id, gamma=0.9, Ne=2, Rplus=2, x_range=(0,39), y_range=(0,39), base_url=base_url, slp=1.5)
    trials.append(trial)
end = time()
print(f"Elapsed: {end - start}")
c = Counter(trials)
print(c)