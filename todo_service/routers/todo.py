import os
from typing import List
from uuid import uuid4, UUID

import aiohttp
from dotenv import load_dotenv
from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from db.connection import Database, engine
from db.todo_repository import TodoRepository
from models.todo import TodoInDb
from schemas.todo import TodoSchema, TodoCreateSchema

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

load_dotenv()

notification_url = os.getenv("NOTIFICATION_URL")


@router.get("/", response_model=List[TodoSchema])
def get_todos(
        current_user=Depends(get_current_active_user)
):
    """Get all todos for current user"""
    todo_repository = TodoRepository(Database.get_instance(engine=engine))
    response = map(
        lambda todo: TodoSchema(id=todo.id, title=todo.title, description=todo.description, finished=todo.finished),
        todo_repository.get_todos_for_user(current_user.id))
    return list(response)


@router.post("/", response_model=TodoSchema)
def create_todo(
        todo: TodoCreateSchema,
        current_user=Depends(get_current_active_user)
):
    """Create a new todo"""
    todo_for_db = TodoInDb(**todo.dict(), user_id=current_user.id, id=uuid4)
    todo_repository = TodoRepository(Database.get_instance(engine=engine))
    created_todo = todo_repository.create(todo_for_db)
    return TodoSchema(id=created_todo.id, title=created_todo.title, description=created_todo.description)


@router.put("/done/{todo_id}", response_model=TodoSchema)
async def mark_as_done(
        todo_id: str,
        current_user=Depends(get_current_active_user)
):
    """Mark a todo as done"""
    todo_repository = TodoRepository(Database.get_instance(engine=engine))
    todo = todo_repository.mark_as_finished(UUID(todo_id), current_user.id)
    print("TODO", todo)
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{notification_url}/notification/",
                                json={"message": f"Todo DONE: {todo.title}"}
                                ) as response:
            if response.status != 200:
                raise Exception("Failed to send notification to Discord")
            return TodoSchema(id=todo.id, title=todo.title, description=todo.description,
                              finished=todo.finished)
