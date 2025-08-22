from fastapi import FastAPI, Form, HTTPException, status, Depends
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import select
import module
import security
import database
import module


app = FastAPI()

database.database_create()

EXPIRE_TOKEN_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/register_user", response_model=module.UserPublic)
def register_user(user_register: Annotated[module.UserCreate, Form()], session:database.SessionDep):
    hashed_password = security.password_hash(user_register.password)
    user = module.User(email=user_register.email, password=hashed_password)
    session.add(user)
    session.commit()
    return user


@app.post("/token")
async def login_user_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session:database.SessionDep) -> Token:
    user = security.login_acces_user(user_email=form_data.username, user_password=form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o Password son incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
            )
    acces_token_expires = timedelta(minutes=EXPIRE_TOKEN_MINUTES)
    acces_token = security.create_token_user(data={"sub": user.email}, expire_delta_token=acces_token_expires)
    return Token(access_token=acces_token, token_type="bearer")

@app.post("/register_note", response_model=module.NotePublic)
def register_note(current_user: Annotated[module.User, Depends(security.decode_token_user)], note_module:Annotated[module.NoteCreate, Form()], session: database.SessionDep):
    user = session.exec(select(module.User).where(module.User.id == current_user.id)).first()
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Debe inicar sesion"
        )
    create_note = module.Note(name_note = note_module.name_note, description = note_module.description, id_user = user.id)
    session.add(create_note)
    session.commit()
    return create_note


@app.get("/view_notes_user")
def view_notes_user(current_user:Annotated[module.User, Depends(security.decode_token_user)], session:database.SessionDep):
    notes_user = session.exec(select(module.Note).where(module.Note.id_user == current_user.id)).all()
    if not notes_user:
        return "Usted no tiene ninguna nota registrada"
    return notes_user
