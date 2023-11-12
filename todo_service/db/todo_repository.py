from uuid import UUID

from sqlalchemy import select

from db.connection import Database
from db.db_models.todo import TodoInDb


class TodoRepository:
    """Repository for todo"""

    def __init__(self, database: Database):
        self.database = database

    def get_all(self):
        """Get all todos"""
        with self.database as session:
            statement = (
                select(TodoInDb)
            )
            result = session.execute(statement)
            return result.scalars().all()

    def get_by_id(self, todo_id: UUID):
        """Get a todo by id"""
        with self.database as session:
            statement = (
                select(TodoInDb).where(TodoInDb.id == todo_id)
            )
            result = session.execute(statement)
            return result.scalars().first()

    def create(self, todo: TodoInDb):
        """Create a todo"""
        with self.database as session:
            session.add(todo)
            session.commit()
            return session.execute(select(TodoInDb).where(TodoInDb.id == todo.id)).scalars().first()

    def update(self, todo: TodoInDb):
        """Update a todo"""
        with self.database as session:
            statement = (
                select(TodoInDb).where(TodoInDb.id == todo.id)
            )
            result = session.execute(statement)
            todo_in_db = result.scalars().first()
            todo_in_db.title = todo.title
            todo_in_db.description = todo.description
            session.commit()
            return session.execute(select(TodoInDb).where(TodoInDb.id == todo.id)).scalars().first()

    def delete(self, todo_id: UUID):
        """Delete a todo"""
        with self.database as session:
            statement = (
                select(TodoInDb).where(TodoInDb.id == todo_id)
            )
            result = session.execute(statement)
            todo_in_db = result.scalars().first()
            session.delete(todo_in_db)
            session.commit()