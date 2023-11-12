import unittest
from uuid import uuid4

from sqlalchemy import create_engine

from db.connection import Database
from db.todo_repository import TodoRepository
from models.todo import TodoInDb


class TestTodoRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')

        self.database = Database.get_instance(self.engine)
        self.database.create_all()

        self.todo_repository = TodoRepository(self.database)

    def tearDown(self):
        self.database.drop_all()

    def test_create_todo(self):
        todo = TodoInDb(id=uuid4(), title="Test Todo", description="Test description")

        created_todo = self.todo_repository.create(todo)

        self.assertIsNotNone(created_todo.id)
        self.assertEqual(created_todo.title, todo.title)
        self.assertEqual(created_todo.description, todo.description)

    def test_get_all_todos(self):
        todo1 = TodoInDb(id=uuid4(), title="Test Todo 1", description="Test description 1")
        todo2 = TodoInDb(id=uuid4(), title="Test Todo 2", description="Test description 2")
        self.todo_repository.create(todo1)
        self.todo_repository.create(todo2)

        todos = self.todo_repository.get_all()

        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].title, todo1.title)
        self.assertEqual(todos[0].description, todo1.description)
        self.assertEqual(todos[1].title, todo2.title)
        self.assertEqual(todos[1].description, todo2.description)

    def test_get_todo_by_id(self):
        todo = TodoInDb(id=uuid4(), title="Test Todo", description="Test description")
        self.todo_repository.create(todo)

        retrieved_todo = self.todo_repository.get_by_id(todo.id)

        self.assertEqual(retrieved_todo.title, todo.title)
        self.assertEqual(retrieved_todo.description, todo.description)

    def test_update_todo_by_id(self):
        todo = TodoInDb(id=uuid4(), title="Test Todo", description="Test description")
        self.todo_repository.create(todo)

        todo.title = "Updated title"
        todo.description = "Updated description"
        updated_todo = self.todo_repository.update(todo)

        self.assertEqual(updated_todo.title, todo.title)
        self.assertEqual(updated_todo.description, todo.description)

    def test_delete_todo_by_id(self):
        todo = TodoInDb(id=uuid4(), title="Test Todo", description="Test description")
        self.todo_repository.create(todo)

        self.todo_repository.delete(todo.id)

        should_be_none = self.todo_repository.get_by_id(todo.id)

        self.assertIsNone(should_be_none)


if __name__ == '__main__':
    unittest.main()
