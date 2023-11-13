from uuid import UUID

from pydantic import BaseModel


class LoginUser(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: UUID
    username: str
