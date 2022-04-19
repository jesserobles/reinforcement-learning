
"""

"""
import json
from typing import Optional

from fastapi import Security, Depends, FastAPI, HTTPException, Form
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session


from models import NORTH, SOUTH, EAST, WEST, GridMDP
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

with open("worlds.json", "r") as file:
    payload = json.load(file)

WORLDS = {int(ix): GridMDP(pl['cells'], terminals=[tuple(t) for t in pl['terminals']]) for ix, pl in payload.items()}

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MOVES = {
    "N": NORTH,
    "S": SOUTH,
    "E": EAST,
    "W": WEST
}

APIKEY = "1d34ba2a713f3751282e"
USERID = 1103
API_KEY = "1d34ba2a713f3751282e"
API_KEY_NAME = "x-api-key"
COOKIE_DOMAIN = "localtest.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)



async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

run_history = {}
# def read_root(api_key: APIKey = Depends(get_api_key)):

# Get Location
@app.get("/aip2pgaming/api/rl/gw.php")
def gw_get(type:str, teamId:int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=teamId)
    if type == "location":
        return {"code":"OK","world":db_team.current_world,"state": db_team.current_location}
    return {"code": "FAIL", "type": type}

# Enter world and Make a move requests
@app.post("/aip2pgaming/api/rl/gw.php")
def gw_post(type:str = Form(...), worldId:int = Form(...), teamId:int = Form(...), move:str = Form(None), db: Session = Depends(get_db)):
    if not (0 <= worldId <= 10):
        raise HTTPException(status_code=400, detail="Invalid world!")
    db_team = crud.get_team(db, team_id=teamId)
    if move and not move in ("N", "S", "E", "W"):
        raise HTTPException(status_code=400, detail="Invalid move!")

    # Enter a world:
    if type == "enter":
        # Enter a world, the location will be "0:0"
        # {"code":"OK","worldId":0,"runId":6177,"state":"0:0"}
        # First check if team already in a world, throw error if so
        if not db_team.current_world is None: # This should be None to be able to enter
            return {'code': 'FAIL', 'message': f'Cannot enter the world.  You are currently in world: {db_team.current_world}'}
        # Otherwise, create run, update world and current position
        run = crud.create_run(db, teamId=teamId, gworldId=worldId)
        db_team.current_world = worldId
        db_team.current_location = "0:0"
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return {"code":"OK","worldId":worldId,"runId":run.runId,"state":"0:0"}
    # Here is where the movement happens
    # TODO: Figure out how the scoreIncrement is calculated.
    if type == "move":
        if db_team.current_world is None: # user not in world
            return {'code': 'FAIL', 'message': "Team not in any world. Enter a world before making a move."}
        if db_team.current_world != worldId:
            return {'code': 'FAIL', 'message': f'Cannot move in this world.  You are currently in world: {db_team.current_world }'}
        # Otherwise, issue the move by adding a move and updating the team profile
        move_tuple = MOVES[move]
        move_payload = crud.make_move(db, teamId, worldId, move, move_tuple, WORLDS[worldId])
        if move_payload is None:
            return {"code": "FAIL", "message": "recieved None from make_move"}
        db_move = move_payload['move']
        db_run = move_payload['run']
        x, y = db_move.current_location.split(':')
        location = {"x": int(x), "y": int(y)}
        if db_run.complete:
            location = None
        payload = {
            "code": "OK",
            "worldId": worldId,
            "runId": db_run.runId,
            "reward": db_move.reward,
            "scoreIncrement": None,
            "newState":location
        }

        return payload
    return {"code": "FAIL", "message": f"Unknown operation type: {type}"}


@app.get("/aip2pgaming/api/rl/score.php")
def score():
    return {"code": "OK", "page": "score"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Enter a world, the location will be "0:0"
# {"code":"OK","worldId":0,"runId":6177,"state":"0:0"}


# Users and teams
@app.post("/users/")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)

@app.post("/teams/")
def create_team(team: schemas.Team, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team.id)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(db=db, team=team)


@app.get("/teams/{team_id}")
def get_team(team_id:int, db: Session = Depends(get_db)):
    team = crud.get_team(db, team_id=team_id)
    return team


@app.post("/teams/user/")
def add_user_to_team(team_id: int, user_id:int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=400, detail="Team doesn't exist")
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    return crud.add_user_to_team(db=db, team_id=team_id, user_id=user_id)