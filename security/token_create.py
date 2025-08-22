from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from pydantic import BaseModel
import database
import security
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme_token = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    email: str | None = None


def create_token_user(data:dict, expire_delta_token: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta_token:
        expire = datetime.now(timezone.utc) + expire_delta_token
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY,ALGORITHM)
    return encode_jwt


async def decode_token_user(token:Annotated[str, Depends(oauth2_scheme_token)], session:database.SessionDep):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales Invalidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        play_load = jwt.decode(token, SECRET_KEY, ALGORITHM)
        email = play_load.get("sub")
        if email is None:
            raise credentials_error
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_error
    user = security.user_email_in_database(user_email=token_data.email, session=session)
    if user is None:
        raise credentials_error
    return user