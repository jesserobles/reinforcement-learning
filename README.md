# reinforcement-learning

## Running against the real API
You need to create an `api_key.json` file in this directory with the following format:
```json
{
    "x-api-key": "XXXX",
    "userId": "1103",
    "User-Agent": "AI-Students"
}
```

Then, you can run a single trial in python as follows:

```python
from q_learning_agent import run_trial
world_id = 0
base_url = 'https://www.notexponential.com/'
trial = run_trial(world_id, gamma=0.9, Ne=5, Rplus=2, x_range=(0,39), y_range=(0,39), base_url=base_url, slp=1.5)
```
Note that the `slp` parameter determines how long the agent waits before submitting a move to the API. You can also run multiple trials at a time to collect more data:

```python
from collections import Counter
from time import time
from q_learning_agent import run_trial
world_id = 0
base_url = 'https://www.notexponential.com/'
trials = []
num_trials = 100
start = time()
for t in range(num_trials):
    print(f"Running trial {t + 1} of {num_trials}")
    trial = run_trial(world_id, gamma=0.9, Ne=2, Rplus=2, x_range=(0,39), y_range=(0,39), base_url=base_url, slp=1.5)
    trials.append(trial)
end = time()
print(f"Elapsed: {end - start}")
c = Counter(trials)
print(c)
```

## Run mock api
Install the libraries in the requirements.txt file (you can use a virtual environment manager such as venv, pipenv, or conda).

To create a virtual environment, you can run the following
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This will create a folder named venv with the virtual environment files and install the dependencies.

From the api directory, run the following.
```bash
uvicorn main:app --reload
```

## Resetting the database
To reset the database (delete all runs/moves/users/teams, adds default user and team), run the `reset_db.py` file in the api folder. Note that you need to run it in the same python environment as the api.
```bash
python reset_db.py
```

Sample responses

Enter a world:
```json
{"code":"OK","worldId":0,"runId":6177,"state":"0:0"}
```

Get location:
```json
{"code":"OK","world":"0","state":"0:0"}
```

Make a move: (all north)
```json
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.1000000000000000055511151231257827021181583404541015625,"newState":{"x":"0","y":1}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0899999999999999966693309261245303787291049957275390625,"newState":{"x":"0","y":2}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.08000000000000000166533453693773481063544750213623046875,"newState":{"x":"0","y":3}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.070000000000000006661338147750939242541790008544921875,"newState":{"x":1,"y":"3"}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.070000000000000006661338147750939242541790008544921875,"newState":{"x":"1","y":4}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.059999999999999997779553950749686919152736663818359375,"newState":{"x":0,"y":"4"}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.05000000000000000277555756156289135105907917022705078125,"newState":{"x":0,"y":"4"}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.05000000000000000277555756156289135105907917022705078125,"newState":{"x":"0","y":5}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.040000000000000000832667268468867405317723751068115234375,"newState":{"x":"0","y":6}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.040000000000000000832667268468867405317723751068115234375,"newState":{"x":"0","y":7}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0299999999999999988897769753748434595763683319091796875,"newState":{"x":"0","y":8}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0299999999999999988897769753748434595763683319091796875,"newState":{"x":"0","y":9}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0299999999999999988897769753748434595763683319091796875,"newState":{"x":"0","y":10}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0299999999999999988897769753748434595763683319091796875,"newState":{"x":1,"y":"10"}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0200000000000000004163336342344337026588618755340576171875,"newState":{"x":"1","y":11}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0200000000000000004163336342344337026588618755340576171875,"newState":{"x":"1","y":12}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0200000000000000004163336342344337026588618755340576171875,"newState":{"x":"1","y":13}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0200000000000000004163336342344337026588618755340576171875,"newState":{"x":"1","y":14}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.0200000000000000004163336342344337026588618755340576171875,"newState":{"x":"1","y":15}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.01000000000000000020816681711721685132943093776702880859375,"newState":{"x":"1","y":16}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.01000000000000000020816681711721685132943093776702880859375,"newState":{"x":"1","y":17}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.01000000000000000020816681711721685132943093776702880859375,"newState":{"x":"1","y":18}}
{"code":"OK","worldId":0,"runId":"6177","reward":-0.1000000000000000055511151231257827021181583404541015625,"scoreIncrement":-0.01000000000000000020816681711721685132943093776702880859375,"newState":{"x":"1","y":19}}
{"code":"OK","worldId":0,"runId":"6177","reward":-10000,"scoreIncrement":-886.2899999999999636202119290828704833984375,"newState":null}
```
```json
{"code":"OK","worldId":0,"runId":"14","reward":10000,"scoreIncrement":51.54,"newState": null}
```

Get runs:
```json
{"runs":[{"runId":"6177","teamId":"1290","gworldId":"0","createTs":"2022-04-17 13:12:55","score":"-887.2051825840535","moves":"24"},{"runId":"6176","teamId":"1290","gworldId":"0","createTs":"2022-04-14 06:00:49","score":"-985.6724250933917","moves":"23"}],"code":"OK"}
```