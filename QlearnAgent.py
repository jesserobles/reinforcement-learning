"""
Our Q agent be the agent exporing the gridworld that will track the current
Q table values, the rewards received after an action, actions the agent currently
can take, and the location the agent currently is in. We will have the learning function
set within our Q Agent as it traverses through the grid world
"""
import numpy as np

class QAgent:
    def __init__(self, alpha, gamma, location_state, actions, rewards, state_to_location):
        self.alpha = alpha
        self.gamma = gamma
        self.location_state = location_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location
        #initializing the Q learning table
        loc_state_length = len(location_state)
        self.Q = np.zeros((loc_state_length,loc_state_length), dtype = None, order = 'C')
        
    def training(self, start_location, end_location, iterations)
        