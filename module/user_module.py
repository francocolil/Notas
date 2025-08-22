from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True, index=True)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: str
    password:str