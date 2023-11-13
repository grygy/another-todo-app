from typing import List

from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from db.connection import Database, engine
from db.todo_repository import TodoRepository
from schemas.todo import TodoSchema

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[TodoSchema])
def get_todos(
        current_user=Depends(get_current_active_user)
):
    """Get all todos for current user"""
    todo_repository = TodoRepository(Database.get_instance(engine=engine))
    return todo_repository.get_todos_for_user(current_user.id)
