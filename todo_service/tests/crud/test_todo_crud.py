import unittest
from unittest.mock import MagicMock
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
        todo1 = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        todo2 = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174002"), title="Task 2", description="Description 2")
        self.mock_repository.data = {todo1.id: todo1, todo2.id: todo2}

        result = self.todo_crud.get_all()

        self.assertEqual(result, [todo1, todo2])

    def test_get(self):
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        result = self.todo_crud.get(todo.id)

        self.assertEqual(result, todo)

    def test_create(self):
        todo_create = MagicMock()

        result = self.todo_crud.create(todo_create)

        self.assertEqual(result, todo_create)

    def test_update(self):
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        result = self.todo_crud.update(todo)

        self.assertEqual(result, todo)

    def test_delete(self):
        todo = TodoInDb(id=UUID("123e4567-e89b-12d3-a456-426614174001"), title="Task 1", description="Description 1")
        self.mock_repository.data = {todo.id: todo}

        self.todo_crud.delete(todo.id)

        self.assertNotIn(todo.id, self.mock_repository.data)


if __name__ == "__main__":
    unittest.main()
