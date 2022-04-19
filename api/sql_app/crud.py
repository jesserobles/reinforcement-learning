import random
from typing import Tuple

from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(id=user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_team(db: Session, team: schemas.Team):
    db_team = models.Team(id=team.id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db: Session, team_id):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def add_user_to_team(db: Session, team_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    team.users.append(user)
    db.add(team)
    db.add(user)
    db.commit()
    db.refresh(team)
    db.refresh(user)
    return {"user": user, "team": team}

def get_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).offset(skip).limit(limit).all()


def create_run(db: Session, teamId: int, gworldId: int):
    db_run = models.Run(gworldId=gworldId, teamId=teamId)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def enter_world(db: Session, teamId: int, gworldId: int):
    # Should we do something with the run/runid?
    db_team = get_team(db, teamId)
    if not db_team:
        raise HTTPException(status_code=400, detail="Team doesn't exist!")
    # Create a run, set the team.current_world = worldId, and team.current_position = "0:0".
    run = create_run(db, teamId, gworldId)
    db_team.current_world = gworldId
    db_team.current_position = "0:0"
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

def make_move(db: Session, teamId: int, gworldId: int, direction:str, move_tuple: Tuple[int, int], mdp):
    # Get team
    db_team = get_team(db, teamId)
    current_position = tuple([int(i) for i in db_team.current_location.split(':')])
    next_position = take_single_action(mdp, current_position, move_tuple)
    reward = mdp.R(next_position)
    # Get run
    db_run = db.query(models.Run)\
        .filter(
            models.Run.gworldId == gworldId,
            models.Run.teamId == teamId,
            models.Run.complete == False)\
        .order_by(models.Run.createTs.desc()).first()
    if not db_run:
        return
    db_run.moves += 1
    db_run.score += reward
    
    prv = ':'.join(str(i) for i in current_position)
    crnt = ':'.join(str(i) for i in next_position)
    db_team.current_location = crnt
    if next_position in mdp.terminals: # This should end the game
        db_run.complete = True
        db_team.current_location = None
        db_team.current_world = None
    db.add(db_team)
    db_move = models.Move(runId=db_run.runId, direction=direction, previous_location=prv, current_location=crnt, reward=reward)
    db.add(db_run)
    db.add(db_move)
    db.commit()
    db.refresh(db_run)
    db.refresh(db_move)
    db.refresh(db_team)
    return {"move": db_move, "run": db_run}

def take_single_action(mdp, s, a):
    """
    Select outcome of taking action a
    in state s. Weighted Sampling.
    """
    # x = random.uniform(0, 1)
    # cumulative_probability = 0.0
    # for probability_state in mdp.T(s, a):
    #     probability, state = probability_state
    #     cumulative_probability += probability
    #     if x < cumulative_probability:
    #         break
    transitions = mdp.T(s, a)
    weights = [i[0] for i in transitions]
    states = [i[-1] for i in transitions]
    state = random.choices(states, weights=weights)[0]
    return state
