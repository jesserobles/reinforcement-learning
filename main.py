"""
Add Play function
input: environment, agent, number of trials, and
the max amount of steps it go through until it ends the process or until the game has reached a
terminal state
outputs: reward per episode
Possibly extract the play function out and just place into our main call 
this way we have more control over when to make the next action or get the score
"""
import time

def play(environment, agent, trials, maxSteps):
    episodeRewards = []
    
    for trial in range(trials):
        totalReward = 0
        step = 0
        terminate = False
        while step < maxSteps and terminate != True:
            previousState = environment.current_location
            action = agent.actionSelection
            #set timer for 15 seconds before next step to API
            time.sleep(15)
            reward = environment.make_step(action)
            #call API pass action taken to make step
            """Place Make a move api call here"""
            newCurrentState = environment.current_location
            agent.learn(previousState, reward, newCurrentState, action)
            totalReward += reward
            step+=1
            if environment.check_state == 'TERMINAL':
                environment.__init__()
                terminate = True
        episodeRewards.append(totalReward)
        time.sleep(600)
    return episodeRewards

if __name__ == "__main__":
    #Use the API to pull the Gridworld first
    """Enter a world API call"""
    """grab the starting state from the return of the API call"""
    """Pass in the world and starting state into the play function"""
    from collections import Counter
    from q_learning_agent import run_trial
    count = 100
    rewards = []
    win_loss = {1: "WINS", -1: "LOSSES"}
    for trial in range(count):
        print(f"Running trial {trial + 1} of {count}")
        rewards.append(win_loss[run_trial(100, Ne=2)])
    c = Counter(rewards)
    if "LOSSES" not in c:
        c["LOSSES"] = 0
    if "WINS" not in c:
        c['WINS'] = 0
    print(c)
"""
#For the real API, run like this:
from q_learning_agent import run_trial
world_id = 0
base_url = 'https://www.notexponential.com/'
trial = run_trial(world_id, gamma=0.9, Ne=5, Rplus=2, x_range=(0,39), y_range=(0,39), base_url=base_url, slp=1.5)
"""