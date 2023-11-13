from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth.auth import fake_users_db, get_current_active_user, check_password
from models.user import UserInDB

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_router.post("/token")
def login(form_data=Depends(OAuth2PasswordRequestForm)):
    print(form_data)
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    if not check_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@user_router.get("/users/me")
def read_users_me(
        current_user=Depends(get_current_active_user)
):
    return current_user
