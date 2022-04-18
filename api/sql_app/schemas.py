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
    # id: int
    gworldId: int
    team: Team

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True