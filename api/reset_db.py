from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

from sql_app.database import engine
from sql_app import schemas
from sql_app import models, crud

from main import get_db

db: Session = list(Depends(get_db).dependency())[0]
for tbl in reversed(models.Base.metadata.sorted_tables):
    engine.execute(tbl.delete())
models.Base.metadata.create_all(bind=engine)



user = schemas.User(id=1103)
team = schemas.Team(id=1290)

crud.create_user(db, user)
crud.create_team(db, team)
crud.add_user_to_team(db, team.id, user.id)
