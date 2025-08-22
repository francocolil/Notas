from sqlmodel import select
from database.connection import SessionDep
from passlib.context import CryptContext
import module

context_hash = CryptContext(schemes=["bcrypt"])

def password_hash(password:str):
    return context_hash.hash(password)

def verify_password(password_plain:str, password_hashed:str):
    return context_hash.verify(password_plain, password_hashed)

def user_email_in_database(user_email:str, session:SessionDep):
    user_database = session.exec(select(module.User).where(module.User.email == user_email)).first()
    return user_database

def login_acces_user(user_email:str, user_password:str, session:SessionDep):
    user_database = session.exec(select(module.User).where(module.User.email == user_email)).first()
    if not user_database:
        return False
    if not verify_password(user_password, user_database.password):
        return False
    return user_database


