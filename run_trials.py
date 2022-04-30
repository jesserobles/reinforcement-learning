from collections import Counter
from time import time
from q_learning_agent import run_single_trial, orientations, QLearningAgent


world_id = 9

base_url = 'https://www.notexponential.com/'
agent = QLearningAgent(orientations, gamma=0.9, Ne=2, Rplus=10, x_range=(0,39), y_range=(0,39), base_url=base_url)

trials = []
num_trials = 1
start = time()
for t in range(num_trials):
    print(f"Running trial {t + 1} of {num_trials}")
    try:
        trial = run_single_trial(agent, world_id, slp=1.5)
    # trial = run_trial(world_id, gamma=0.9, Ne=2, Rplus=2, x_range=(0,39), y_range=(0,39), base_url=base_url, slp=1.5)
        trials.append(trial)
    except:
        print("API ERROR")
        agent.save_q_values(world_id)
        break
end = time()
print(f"Ran {t + 1} trials in: {end - start}")
c = Counter(trials)
print(c)