"""
Our Q agent be the agent exporing the gridworld that will track the current
Q table values, the rewards received after an action, actions the agent currently
can take, and the location the agent currently is in. We will have the learning function
set within our Q Agent as it traverses through the grid world
Possible changes:
    we may need to have a attribute of last location or funciton for 
    next moves in this class vs within the Gridworld
    class. (same for when we check the state if it is termianl)
    Dependent on what is given to us from the API
"""
import numpy as np

class QAgent:
    def __init__(self, location_state, actions, rewards, state_to_location, alpha=0.1, gamma=1, epsilon = 0.05):
        if not(0< gamma <= 1):
            raise ValueError("Gamma must be 0 < gamma <= 1")
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.location_state = location_state
        self.actions = actions
        self.rewards = rewards or {state: 0 for state in self.states}
        self.state_to_location = state_to_location
        #initializing the Q learning table
        loc_state_length = len(location_state)
        self.Q = np.zeros((loc_state_length,loc_state_length), dtype = None, order = 'C')
        
    def training(self, start_location, end_location, iterations):
        rewards_new = np.copy(self.rewards)
        ending_state = self.location_state[end_location]
        rewards_new[ending_state, ending_state] = 999
        
        for i in range(iterations):
            current_state = np.random.randint()