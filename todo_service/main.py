from fastapi import FastAPI

from db.connection import Database, engine
from routers import todo
from routers.user import user_router

app = FastAPI()

app.include_router(todo.router)
app.include_router(user_router)

# Database
database = Database.get_instance(engine)
database.create_all()

# Create sample data
database.create_sample_data()
