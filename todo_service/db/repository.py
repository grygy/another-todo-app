import uuid
from typing import TypeVar, Protocol, Generic
from uuid import UUID

TWithId = TypeVar('TWithId', bound='HasId')


class HasId(Protocol):
    id: uuid.UUID


class IRepository(Generic[TWithId]):
    """Base interface for repository"""

    def get_all(self) -> list[TWithId]:
        """Get all items"""
        pass

    def get_by_id(self, id: UUID) -> TWithId:
        """Get a item by id"""
        pass

    def create(self, todo: TWithId) -> TWithId:
        """Create a item"""
        pass

    def update(self, todo: TWithId) -> TWithId:
        """Update a item"""
        pass

    def delete(self, id: UUID) -> None:
        """Delete a item"""
        pass
