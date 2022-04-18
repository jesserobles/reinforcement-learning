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
from collections import defaultdict

import numpy as np

from api.models import sequential_decision_environment
class QAgent:
    def __init__(self, environment, alpha=0.1, gamma=1, epsilon = 0.05):
        if not(0< gamma <= 1):
            raise ValueError("Gamma must be 0 < gamma <= 1")
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        #the environment input would be the Grid world
        self.environment = environment
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
class QLearningAgent:
    """
    [Figure 21.8]
    An exploratory Q-learning agent. It avoids having to learn the transition
    model because the Q-value of a state can be related directly to those of
    its neighbors.
    import sys
    from mdp import sequential_decision_environment
    north = (0, 1)
    south = (0,-1)
    west = (-1, 0)
    east = (1, 0)
    policy = {(0, 2): east, (1, 2): east, (2, 2): east, (3, 2): None, (0, 1): north, (2, 1): north,
              (3, 1): None, (0, 0): north, (1, 0): west, (2, 0): west, (3, 0): west,}
    q_agent = QLearningAgent(sequential_decision_environment, Ne=5, Rplus=2, alpha=lambda n: 60./(59+n))
    for i in range(200):
        run_single_trial(q_agent,sequential_decision_environment)
    q_agent.Q[((0, 1), (0, 1))] >= -0.5
    True
    q_agent.Q[((1, 0), (0, -1))] <= 0.5
    True
    """

    def __init__(self, mdp, Ne, Rplus, alpha=None):

        self.gamma = mdp.gamma
        self.terminals = mdp.terminals
        self.all_act = mdp.actlist
        self.Ne = Ne  # iteration limit in exploration function
        self.Rplus = Rplus  # large value to assign before iteration limit
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.s = None
        self.a = None
        self.r = None

        if alpha:
            self.alpha = alpha
        else:
            self.alpha = lambda n: 1. / (1 + n)  # udacity video

    def f(self, u, n):
        """Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        Same as ADP agent in book."""
        if n < self.Ne:
            return self.Rplus
        else:
            return u

    def actions_in_state(self, state):
        """Return actions possible in given state.
        Useful for max and argmax."""
        if state in self.terminals:
            return [None]
        else:
            return self.all_act

    def __call__(self, percept):
        s1, r1 = self.update_state(percept)
        Q, Nsa, s, a, r = self.Q, self.Nsa, self.s, self.a, self.r
        alpha, gamma, terminals = self.alpha, self.gamma, self.terminals,
        actions_in_state = self.actions_in_state

        if s in terminals:
            Q[s, None] = r1
        if s is not None:
            Nsa[s, a] += 1
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * max(Q[s1, a1]
                                                           for a1 in actions_in_state(s1)) - Q[s, a])
        if s in terminals:
            self.s = self.a = self.r = None
        else:
            self.s, self.r = s1, r1
            self.a = max(actions_in_state(s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
        return self.a

    def update_state(self, percept):
        """To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward)."""
        return percept
import random
def run_single_trial(agent_program, mdp):
    """Execute trial for given agent_program
    and mdp. mdp should be an instance of subclass
    of mdp.MDP """
    def take_single_action(mdp, s, a):
        """
        Select outcome of taking action a
        in state s. Weighted Sampling.
        """
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for probability_state in mdp.T(s, a):
            probability, state = probability_state
            cumulative_probability += probability
            if x < cumulative_probability:
                break
        return state
    current_state = mdp.init
    while True:
        current_reward = mdp.R(current_state)
        percept = (current_state, current_reward)
        next_action = agent_program(percept)
        if next_action is None:
            break
        current_state = take_single_action(mdp, current_state, next_action)