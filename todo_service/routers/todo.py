import uuid
from typing import List

from fastapi import APIRouter

from schemas.todo import Todo

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

fake_todos_db = [{"id": uuid.UUID("bd65600d-8669-4903-8a14-af88203add38"), "title": "Foo", "description": "Fighters"}]


@router.get("/", response_model=List[Todo])
def get_todos():
    """Get all todos"""
    return fake_todos_db
