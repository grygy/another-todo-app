from datetime import datetime, timedelta
from typing import Any, Dict
from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from models.user import UserInDB

fake_users_db = {
    UUID("bd65600d-8669-4903-8a14-af88203add38"): {
        "id": UUID("bd65600d-8669-4903-8a14-af88203add38"),
        "username": "johndoe",
        "hashed_password": "$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni",  # password=secret
    },
    UUID("8f965c8d-9dcc-4b8a-9b8c-3f6f8f92a662"): {
        "id": UUID("8f965c8d-9dcc-4b8a-9b8c-3f6f8f92a662"),
        "username": "alice",
        "hashed_password": "$2b$12$fP1oXPuR9gb0keuNkVGSXuaCDJojiQ8.ma5Xa452R8efJhVOgcS6C",  # password=secret2
    },
}

# TODO put this in a .env file
SECRET_KEY = "1cbf94982753ebbcfceed6cba5588d9f8e76fe5164563399b506d181e2e58ad1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID | None = None


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def get_user(db: Dict[UUID, Any], id: UUID):
    if id in db:
        user_dict = db[id]
        return UserInDB(**user_dict)


def get_user_by_username(db: Dict[UUID, Any], username: str):
    for user_id in db:
        user = get_user(db, user_id)
        if user.username == username:
            return user


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
    user_in_db = get_user_by_username(fake_users_db, username)
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
    user = get_user(fake_users_db, id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user=Depends(get_current_user)
):
    return current_user
