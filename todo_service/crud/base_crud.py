import uuid
from typing import TypeVar, Generic, List, Protocol

TWithId = TypeVar('TWithId', bound='HasId')
TWithoutId = TypeVar('TWithoutId')


class HasId(Protocol):
    id: uuid.UUID


class BaseCRUD(Generic[TWithId, TWithoutId]):
    """Base CRUD class with default methods to Create, Read, Update, Delete

    Extendable by concrete class requirements
    """

    def __init__(self, db: List[TWithId]):
        self.db = db

    def get(self, todo_id: uuid.UUID) -> TWithId:
        """Get a single item from the database"""
        item = filter(lambda x: x.id == todo_id, self.db)
        return next(item, None)

    def get_all(self) -> List[TWithId]:
        """Get all items from the database"""
        return self.db

    def create(self, item: TWithoutId) -> TWithId:
        """Create an item in the database

        Adds an id to the item and add it to the database
        """
        item.id = uuid.uuid4()
        self.db.append(item)
        return item

    def update(self, item: TWithId) -> TWithId:
        """Update an item in the database"""
        old_item = self.get(item.id)
        if old_item is None:
            raise ValueError(f"Item with id {item.id} not found")
        index = self.db.index(old_item)
        self.db[index] = item
        return item

    def delete(self, todo_id: uuid.UUID) -> None:
        """Delete an item from the database"""
        item = self.get(todo_id)
        if item is None:
            raise ValueError(f"Item with id {todo_id} not found")
        self.db.remove(item)
