from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TodoBaseSchema(BaseModel):
    title: str
    description: str


class TodoSchema(TodoBaseSchema):
    id: UUID
    finished: datetime = None


class TodoCreateSchema(TodoBaseSchema):
    pass
