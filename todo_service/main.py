import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine

from db.connection import Database
from routers import todo
from routers.user import user_router

# load .env variables
load_dotenv()

app = FastAPI()

app.include_router(todo.router)
app.include_router(user_router)

# Database
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)
database = Database.get_instance(engine)
database.create_all()
