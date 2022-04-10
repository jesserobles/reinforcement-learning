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
    def __init__(self, environment, alpha=0.1, gamma=1, epsilon = 0.05):
        if not(0< gamma <= 1):
            raise ValueError("Gamma must be 0 < gamma <= 1")
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        #the environment input would be the Grid world
        self.environment
        self.qTable = dict()
        #Initializing the q table to have zero values for possible moves
        for x in range(environment.height):
            for y in range(environment.width):
                self.qTable[(x,y)]={'NORTH':0,'EAST':0,'SOUTH':0,'WEST':0,'NORTHEAST':0,'NORTHWEST':0,'SOUTHEAST':0,'SOUTHWEST':0}
    
    """
    Returns the best action based on the Q value table. If there are more than one optimal choice
    we choose a random choice.
    """
    def actionSelection(self, availActions):
        if np.random.uniform(0,1) < self.epsilon:
            action = availActions(np.random.randint(0, len(availActions)))
        else:
            currentStateQValues = self.qTable[self.environment.current_state]
            maxQval = max(currentStateQValues)
            #select a random choice from our Q table where the value is equal to the max Qvalue
            action = np.random.choice([k for k, v in currentStateQValues.items() if v == maxQval])
        return action
    
    """
    function learn grabs the new state's Q values and the max of those values where we then
    set as the current value as this will be our new current state if the action is performed
    """
    def learn(self, oldState, reward, newState, action):
        newStateQvalue = self.qTable[newState]
        maxNewStateQvalue = max(newStateQvalue.values())
        currentQValue = self.qTable[oldState][action]
        self.qTable[oldState][action] = (1-self.alpha) * currentQValue + self.alpha * (reward + self.gamma * maxNewStateQvalue)
        
        
""" self.location_state = location_state
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
'"""