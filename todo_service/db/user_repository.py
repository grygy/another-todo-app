import uuid
from uuid import UUID

from sqlalchemy import select

from db.connection import Database
from db.repository import IRepository
from models.user import UserInDb


class UserRepository(IRepository[UserInDb]):
    """Repository for user"""

    def __init__(self, database: Database):
        self.database = database

    def get_all(self) -> list[UserInDb]:
        """Get all users"""
        with self.database as session:
            statement = (
                select(UserInDb)
            )
            result = session.execute(statement)
            return result.scalars().all()

    def get_by_id(self, id: UUID) -> UserInDb:
        """Get a user by id"""
        with self.database as session:
            statement = (
                select(UserInDb).where(UserInDb.id == id)
            )
            result = session.execute(statement)
            return result.scalars().first()

    def get_by_username(self, username: str) -> UserInDb:
        """Get a user by username"""
        with self.database as session:
            statement = (
                select(UserInDb).where(UserInDb.username == username)
            )
            result = session.execute(statement)
            return result.scalars().first()

    def create(self, user: UserInDb) -> UserInDb:
        """Create a user with new id"""
        with self.database as session:
            user.id = uuid.uuid4()
            session.add(user)
            session.commit()
            return session.execute(select(UserInDb).where(UserInDb.id == user.id)).scalars().first()

    def update(self, user: UserInDb) -> UserInDb:
        """Update a user"""
        with self.database as session:
            statement = (
                select(UserInDb).where(UserInDb.id == user.id)
            )
            result = session.execute(statement)
            user_in_db = result.scalars().first()
            user_in_db.username = user.username
            user_in_db.hashed_password = user.hashed_password
            session.commit()
            return session.execute(select(UserInDb).where(UserInDb.id == user.id)).scalars().first()

    def delete(self, id: UUID) -> None:
        """Delete a user"""
        with self.database as session:
            statement = (
                select(UserInDb).where(UserInDb.id == id)
            )
            result = session.execute(statement)
            user_in_db = result.scalars().first()
            session.delete(user_in_db)
            session.commit()
