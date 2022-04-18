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
    user.teams.append(team)
    db.add(user)
    db.commit()
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

