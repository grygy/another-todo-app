from sqlalchemy import Engine
from sqlalchemy.orm import Session

from db.db_models.base import Base
from db.db_models.todo import TodoInDb


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

    def drop_all(self):
        Base.metadata.drop_all(self.engine)
        TodoInDb.metadata.drop_all(self.engine)

    def __enter__(self):
        self.session = Session(self.engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
