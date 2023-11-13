from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.auth import get_current_active_user, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_IN_MINUTES

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@user_router.post("/login")
def login(form_data=Depends(OAuth2PasswordRequestForm)):
    user = authenticate_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/users/me")
def read_users_me(
        current_user=Depends(get_current_active_user)
):
    return current_user
