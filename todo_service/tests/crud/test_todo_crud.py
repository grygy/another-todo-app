import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID

from crud.todo_crud import TodoCRUD
from db.db_models.todo import TodoInDb
from db.todo_repository import TodoRepository


class MockTodoRepository(TodoRepository):
    def __init__(self):
        self.data = {}

    def get_all(self) -> list[TodoInDb]:
        return list(self.data.values())

    def get_by_id(self, id: UUID) -> TodoInDb:
        return self.data.get(id)

    def create(self, todo: TodoInDb) -> TodoInDb:
        self.data[todo.id] = todo
        return todo

    def update(self, todo: TodoInDb) -> TodoInDb:
        self.data[todo.id] = todo
        return todo

    def delete(self, id: UUID) -> None:
        if id in self.data:
            del self.data[id]


class TestTodoCRUD(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockTodoRepository()
        self.todo_crud = TodoCRUD(self.mock_repository)

    def test_get_all(self):
        # Arrange
        todo1 = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        todo2 = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174002"), title="Task 2", description="Description 2")
        self.mock_repository.data = {todo1.id: todo1, todo2.id: todo2}

        # Act
        result = self.todo_crud.get_all()

        # Assert
        self.assertEqual(result, [todo1, todo2])

    def test_get(self):
        # Arrange
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        # Act
        result = self.todo_crud.get(todo.id)

        # Assert
        self.assertEqual(result, todo)

    @patch("crud.base_crud.uuid")
    def test_create(self, mock_uuid):
        # Arrange
        todo_create = MagicMock()
        mock_uuid.uuid4.return_value = UUID("123e4567-e89b-12d3-a456-426614174001")

        # Act
        result = self.todo_crud.create(todo_create)

        # Assert
        self.assertEqual(result.id, UUID("123e4567-e89b-12d3-a456-426614174001"))
        self.assertEqual(result, todo_create)

    def test_update(self):
        # Arrange
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        # Act
        result = self.todo_crud.update(todo)

        # Assert
        self.assertEqual(result, todo)

    def test_delete(self):
        # Arrange
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        # Act
        self.todo_crud.delete(todo.id)

        # Assert
        self.assertNotIn(todo.id, self.mock_repository.data)


if __name__ == "__main__":
    unittest.main()
