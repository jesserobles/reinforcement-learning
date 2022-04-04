import numpy as np
"""
Gridworld class contains and structures our grid/environment our agent will be
in with attributes such as what the starting location is, any blockades, the
goal location, and our available actions the agent may take.
Pass in our height and width to build grid if we 
"""
class GridWorld:
    def __init__(self,current_location):
        self.height = 40
        self.width = 40
        #initialize the grid as 0s
        self.grid = np.zeros((self.height, self.width)) - 1
        #set a random start location for the agent
        self.current_location = current_location
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
        if action == 'North':
            
        