import os
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from models.base import Base
from models.todo import TodoInDb
from models.user import UserInDb

# load .env variables
load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)


class Database:
    """Singleton class to manage the database connection"""

    __instance = None

    @staticmethod
    def get_instance(engine: Engine):
        """Static access method"""
        if Database.__instance is None:
            Database(engine)
        return Database.__instance

    def __init__(self, engine: Engine):
        """Virtually private constructor"""
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            self.engine = engine
            self.session = None

    def create_all(self):
        Base.metadata.create_all(self.engine)
        TodoInDb.metadata.create_all(self.engine)
        UserInDb.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)
        TodoInDb.metadata.drop_all(self.engine)
        UserInDb.metadata.drop_all(self.engine)

    def create_sample_data(self):
        with self as session:
            if session.query(UserInDb).count() > 0:
                return
            user1 = UserInDb(id=uuid4(), username="johndoe",
                             hashed_password="$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni")
            session.add(user1)
            session.commit()

    def __enter__(self):
        self.session = Session(self.engine)
        return self.session
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
