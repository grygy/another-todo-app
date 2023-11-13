from uuid import UUID

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.user import UserInDB

fake_users_db = {
    "johndoe": {
        "id": UUID("bd65600d-8669-4903-8a14-af88203add38"),
        "username": "johndoe",
        "hashed_password": "$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni",  # password=secret
    },
    "alice": {
        "id": UUID("8f965c8d-9dcc-4b8a-9b8c-3f6f8f92a662"),
        "username": "alice",
        "hashed_password": "$2b$12$fP1oXPuR9gb0keuNkVGSXuaCDJojiQ8.ma5Xa452R8efJhVOgcS6C",  # password=secret2
    },
}


def hash_password(password: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def check_password(plain_password: str, saved_hashed_password: str):
    return bcrypt.checkpw(plain_password.encode("utf-8"), saved_hashed_password.encode("utf-8"))


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token=Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
        current_user=Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
