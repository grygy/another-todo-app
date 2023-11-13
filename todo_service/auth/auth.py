from datetime import datetime, timedelta
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from db.connection import Database, engine
from db.user_repository import UserRepository

# TODO put this in a .env file
SECRET_KEY = "1cbf94982753ebbcfceed6cba5588d9f8e76fe5164563399b506d181e2e58ad1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")

user_repository = UserRepository(Database.get_instance(engine=engine))


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID | None = None


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, saved_hashed_password: str):
    return bcrypt.checkpw(plain_password.encode("utf-8"), saved_hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    user_in_db = user_repository.get_by_username(username)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user_in_db


async def get_current_user(token=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = user_repository.get_by_id(token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user=Depends(get_current_user)
):
    return current_user
