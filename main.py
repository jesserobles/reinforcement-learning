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
    return episodeRewards

if __name__ == "__main__":
    #Use the API to pull the Gridworld first
    """Enter a world API call"""
    """grab the starting state from the return of the API call"""
    """Pass in the world and starting state into the play function"""
    