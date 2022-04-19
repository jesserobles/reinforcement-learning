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
import json
import os
from pathlib import Path
from time import sleep

import numpy as np
import requests
from requests.exceptions import HTTPError

from api.models import sequential_decision_environment


orientations = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]
MOVES = {
    (1, 0): 'E', (0, 1): 'N', 
    (-1, 0): 'W', (0, -1): 'S'
}


class QLearningAgent:
    def __init__(self, all_act, gamma, Ne, Rplus, alpha=None, team_id=1290, base_url="http://localhost:8000/"):
        with open("api_key.json", "r") as file:
            self.HEADERS = json.load(file)
        self.gamma = gamma
        self.all_act = all_act
        self.Ne = Ne  # iteration limit in exploration function
        self.Rplus = Rplus  # large value to assign before iteration limit
        self.Q = defaultdict(float)
        self.Nsa = defaultdict(float)
        self.s = None
        self.a = None
        self.r = None
        self.team_id = team_id
        self.base_url = base_url

        if alpha:
            self.alpha = alpha
        else:
            # self.alpha = lambda n: 1. / (1 + n)
            self.alpha = lambda n: 60./(59+n)
    
    def validate_response(func):
        """
        A decorator to validate the responses for the methods in this class.
        It simply checks that code=OK.
        """
        def wraps(*args, **kwargs):
            response = func(*args, **kwargs)
            payload = response.json()
            if payload["code"] != "OK":
                raise HTTPError(f"Received unexpected code: {payload['code']}, message: {payload['message']}")
            return response
        return wraps

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
        return self.all_act
    
    def serialize_dict(self, payload:dict):
        serialized = {str(key): value for key, value in payload.items()}
        # for key, value in payload.items():
        #     state, action = key
        #     state = ','.join(str(s) for s in state)
        #     action = ','.join(str(a) for a in action)
        #     serialized[':'.join([state, action])] = value
        return serialized
    
    def deserialize_dict(self, payload:dict):
        deserialized = {eval(key): value for key, value in payload.items()}
        # for key, value in payload.items():
        #     k = tuple(tuple([int(i) for i in ch.split(',')]) for ch in key.split(':'))
        #     deserialized[k] = value
        return defaultdict(float, deserialized)

    @validate_response
    def move(self, action:str, world_id:int):
        resp = self._move(action, world_id)

        return resp
    
    @validate_response
    def _move(self, action:str, world_id:int):
        data = {'type': 'move', 'teamId': self.team_id, 'move': action, 'worldId': world_id}
        return requests.post(f'{self.base_url}aip2pgaming/api/rl/gw.php', data=data, headers=self.HEADERS)

    @validate_response
    def enter_world(self, world_id:int):
        data = {'type': 'enter', 'worldId': world_id, 'teamId': self.team_id}
        r = requests.post(f'{self.base_url}aip2pgaming/api/rl/gw.php', data=data, headers=self.HEADERS)

        return r

    def load_q_values(self, world_id, folder="data"):
        file_location = os.path.join(folder, f"{world_id}.json")
        if not os.path.exists(file_location): return
        with open(file_location, "r") as file:
            payload = json.load(file)
        self.Q = self.deserialize_dict(payload['q'])
        self.Nsa = self.deserialize_dict(payload['n'])
    
    def save_q_values(self, world_id, folder="data"):
        file_location = os.path.join(folder, f"{world_id}.json")
        q_payload = self.serialize_dict(self.Q)
        n_payload = self.serialize_dict(self.Nsa)
        payload = {"q": q_payload, "n": n_payload}
        with open(file_location, "w") as file:
            json.dump(payload, file)
        
    def __call__(self, percept):
        s1, r1 = self.update_state(percept)
        Q, Nsa, s, a, r = self.Q, self.Nsa, self.s, self.a, self.r
        alpha, gamma = self.alpha, self.gamma#, self.terminals,
        actions_in_state = self.actions_in_state
        if s is not None:
            Nsa[s, a] += 1
            Q[s, a] += alpha(Nsa[s, a]) * (r + gamma * max(Q[s1, a1]
                                                           for a1 in actions_in_state(s1)) - Q[s, a])
        self.s, self.r = s1, r1
        self.a = max(actions_in_state(s1), key=lambda a1: self.f(Q[s1, a1], Nsa[s1, a1]))
        return self.a

    def update_state(self, percept):
        """To be overridden in most cases. The default case
        assumes the percept to be of type (state, reward)."""
        return percept

def run_trial(world_id):
    agent = QLearningAgent(orientations, gamma=0.9, Ne=5, Rplus=2, alpha=lambda n: 60./(59+n))#, base_url='https://www.notexponential.com/')
    # Load any persisted Q-values
    agent.load_q_values(world_id)
    # Enter world
    r = agent.enter_world(0) #{"code":"OK","worldId":0,"runId":6177,"state":"0:0"}
    current_state = tuple([int(s) for s in r.json()['state'].split(':')])
    percept = (current_state, 0)
    next_action = agent(percept)
    direction = MOVES[next_action]
    while True:
        print(f"Current state: {current_state}, Moving: {direction}")
        r = agent.move(direction, world_id)
        current_state = r.json()['newState']
        current_reward = r.json()['reward']
        if current_state is None: # Game ended
            print("Breaking")
            break
        current_state = (int(current_state['x']), int(current_state['y']))
        percept = (current_state, current_reward)
        next_action = agent(percept)
        direction = MOVES[next_action]
        sleep(0.5)
    agent.save_q_values(world_id)
    
