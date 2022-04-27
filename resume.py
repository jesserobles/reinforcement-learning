from collections import Counter
from time import time
import requests

from q_learning_agent import resume_game, QLearningAgent, orientations

world_id = 1

base_url = 'https://www.notexponential.com/'
agent = QLearningAgent(orientations, gamma=0.9, Ne=5, Rplus=10, x_range=(0,39), y_range=(0,39), base_url=base_url)

try:
    reward = resume_game(agent, world_id=world_id, slp=1.5)
except:
    agent.save_q_values(world_id)


# url = 'https://www.notexponential.com/aip2pgaming/api/rl/gw.php'
# url2 = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php'
# url3 = 'https://www.notexponential.com/aip2pgaming/api/rl/reset.php'

# HEADERS = {
#     'x-api-key': "1d34ba2a713f3751282e",
#     'userid': "1103",
#     'User-Agent': 'AI-Students' # Server throws security exception if this isn't set.
# }

# def north():
#     data = {'type': 'move', 'teamId': 1290, 'move': 'N', 'worldId': 0}
#     r = requests.post(url, data=data, headers=HEADERS)
#     print(r.json())

# def east():
#     data = {'type': 'move', 'teamId': 1290, 'move': 'E', 'worldId': 0}
#     r = requests.post(url, data=data, headers=HEADERS)
#     print(r.json())