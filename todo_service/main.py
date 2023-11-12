import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine

from crud.todo_crud import TodoCRUD
from db.connection import Database
from db.db_models.todo import TodoInDb
from db.todo_repository import TodoRepository
from routers import todo

# load .env variables
load_dotenv()

app = FastAPI()

app.include_router(todo.router)

# Database
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)
database = Database.get_instance(engine)
database.create_all()

todo_crud = TodoCRUD(TodoRepository(database))

todo_crud.create(TodoInDb(title="Test Todo", description="Test description"))
print(todo_crud.get_all())
