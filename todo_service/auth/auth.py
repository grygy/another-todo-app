from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.user import UserInDB

fake_users_db = {
    "johndoe": {
        "id": UUID("bd65600d-8669-4903-8a14-af88203add38"),
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "id": UUID("8f965c8d-9dcc-4b8a-9b8c-3f6f8f92a662"),
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
    },
}


def hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


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
