import requests

user_id = 1103
team_id = 1290

r = requests.post('http://localhost:8000/users/', json={"id": user_id})

r = requests.post('http://localhost:8000/teams/', json={"id": team_id})

r = requests.post('http://localhost:8000/teams/user/', params={"user_id": user_id, "team_id": team_id})

# Enter a world
data = {'type': 'enter', 'worldId': 0, 'teamId': 1290}
r = requests.post('http://localhost:8000/aip2pgaming/api/rl/gw.php', data=data)

# Make a move
data = {'type': 'move', 'teamId': 1290, 'move': 'N', 'worldId': 0}
r = requests.post('http://localhost:8000/aip2pgaming/api/rl/gw.php', data=data)

data = {'type': 'move', 'teamId': 1290, 'move': 'E', 'worldId': 0}
r = requests.post('http://localhost:8000/aip2pgaming/api/rl/gw.php', data=data)


# Enter a world
data = {'type': 'enter', 'worldId': 1, 'teamId': 1290}
r = requests.post('http://localhost:8000/aip2pgaming/api/rl/gw.php', data=data)

# Make a move
data = {'type': 'move', 'teamId': 1290, 'move': 'N', 'worldId': 1}
r = requests.post('http://localhost:8000/aip2pgaming/api/rl/gw.php', data=data)