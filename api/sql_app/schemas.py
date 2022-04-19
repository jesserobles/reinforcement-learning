import datetime
from typing import List

from pydantic import BaseModel

class UserBase(BaseModel):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TeamBase(BaseModel):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class User(UserBase):
    teams: List[TeamBase] = []
    class Config:
        orm_mode = True

class Team(TeamBase):
    users: List[UserBase] = []
    current_world: int = None
    current_location: str = None
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Run(BaseModel):
    runId: int = None
    gworldId: int
    team: Team
    createTs: datetime.datetime
    score: float
    moves: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True