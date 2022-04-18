import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table('association', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('team_id', ForeignKey('teams.id'))
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    teams = relationship("Team",
                    secondary=association_table)

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    current_world = Column(Integer, default=None)
    current_location = Column(String, default=None)
    users = relationship("User",
                    secondary=association_table)
    runs = relationship("Run")
    

class Run(Base):
    """
    {"runId":"6177","teamId":"1290","gworldId":"0","createTs":"2022-04-17 13:12:55","score":"-887.2051825840535","moves":"24"}
    """
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    gworldId = Column(Integer, index=True)
    createTs = Column(DateTime, default=datetime.datetime.utcnow)
    teamId = Column(Integer, ForeignKey('teams.id'))
    moves = relationship("Move")

class Move(Base):
    __tablename__ = "moves"
    id = Column(Integer, primary_key=True, index=True)
    runId = Column(Integer, ForeignKey('runs.id'))
