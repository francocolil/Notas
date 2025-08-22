from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated

app = FastAPI()

database_name = "database.db"
url_database = f"sqlite:///{database_name}"
engine = create_engine(url_database, echo=True)

def create_database():
    return SQLModel.metadata.create_all(engine)

def session_database():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def database_create():
    create_database()

SessionDep = Annotated[Session, Depends(session_database)]