import numpy as np
"""
Gridworld class contains and structures our grid/environment our agent will be
in with attributes such as what the starting location is, any blockades, the
goal location, and our available actions the agent may take.
Pass in our height and width to build grid out the grid also confused on how 
we determine our terminal state from the API
"""
class GridWorld:
    def __init__(self,current_location,terminal_states):
        self.height = 40
        self.width = 40
        #initialize the grid as 0s
        self.grid = np.zeros((self.height, self.width)) - 1
        #set a random start location for the agent
        self.current_location = current_location
        self.terminal_states = terminal_states
        self.actions = ['NORTH','EAST','SOUTH','WEST','NORTHEAST','NORTHWEST','SOUTHEAST','SOUTHWEST']
    
    def get_available_actions(self):
        return self.actions
    
    def agent_location(self):
        grid = np.zeros((self.height, self.width))
        grid[self.current.locaiton[0],self.current_location[1]] = 1
        return grid
    
    def get_reward(self, new_location):
        return self.grid[new_location[0],new_location[1]]
    
    def make_step(self, action):
        last_location = self.current_location
        if action == 'NORTH':
            if last_location[0] == 0:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]+1, self.current_location[1])
                reward = self.get_reward(self.current_location)
        elif action == 'NORTHEAST':
            if last_location[0] == 0 or last_location[1] == self.width-1:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]+1, self.current_location[1]+1)
                reward = self.get_reward(self.current_location)
        elif action == 'NORTHWEST':
            if last_location[0] == 0 or last_location[1] == 0:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]+1, self.current_location[1]-1)
                reward = self.get_reward(self.current_location)
        elif action == 'SOUTH':
            if last_location[0] == self.height-1:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]-1, self.current_location[1])
                reward = self.get_reward(self.current_location)
        elif action == 'SOUTHEAST':
            if last_location[0] == self.height-1 or last_location[1] == self.width-1:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]-1, self.current_location[1]+1)
                reward = self.get_reward(self.current_location)
        elif action == 'SOUTHWEST':
            if last_location[0] == self.height-1 or last_location[1] == 0:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]-1, self.current_location[1]-1)
                reward = self.get_reward(self.current_location)
        elif action == 'WEST':
            if last_location[1] == 0:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]+1, self.current_location[1])
                reward = self.get_reward(self.current_location)
        elif action == 'EAST':
            if last_location[0] == self.width-1:
                reward = self.get_reward(self.current_location)
            else:
                self.current_location = (self.current_location[0]+1, self.current_location[1])
                reward = self.get_reward(self.current_location)
        return reward
    
    #Checks if our current state is a terminal state based on a defined terminal state
    """
        unsure if this function is needed as unsure how this is determined and if it is not
        given how is it given from the API will the state we find just return terminal?
    """
    def check_state(self):
        if self.current_location in self.terminal:
            return 'TERMINAL'
        