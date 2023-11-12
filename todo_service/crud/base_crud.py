import uuid
from typing import TypeVar, Generic, List, Protocol

from db.repository import IRepository

TWithId = TypeVar('TWithId', bound='HasId')
TWithoutId = TypeVar('TWithoutId')


class HasId(Protocol):
    id: uuid.UUID


class BaseCRUD(Generic[TWithId, TWithoutId]):
    """Base CRUD class with default methods to Create, Read, Update, Delete

    Extendable by concrete class requirements
    """

    def __init__(self, repository: IRepository):
        self.repository = repository

    def get(self, todo_id: uuid.UUID) -> TWithId:
        """Get a single item from the database"""
        item = self.repository.get_by_id(todo_id)
        return item

    def get_all(self) -> List[TWithId]:
        """Get all items from the database"""
        return self.repository.get_all()

    def create(self, item: TWithoutId) -> TWithId:
        """Create an item in the database

        Adds an id to the item and add it to the database
        """
        item.id = uuid.uuid4()
        return self.repository.create(item)

    def update(self, item: TWithId) -> TWithId:
        """Update an item in the database"""
        return self.repository.update(item)

    def delete(self, todo_id: uuid.UUID) -> None:
        """Delete an item from the database"""
        return self.repository.delete(todo_id)
