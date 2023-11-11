from uuid import UUID

from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str


class Todo(TodoBase):
    id: UUID


class TodoCreate(TodoBase):
    pass
