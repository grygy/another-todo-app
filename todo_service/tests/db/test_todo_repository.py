import unittest
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import create_engine

from db.connection import Database
from db.todo_repository import TodoRepository
from models.todo import TodoInDb
from models.user import UserInDb


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

    def test_get_todo_for_user(self):
        user1_id = uuid4()
        user2_id = uuid4()
        user1 = UserInDb(id=user1_id, username="johndoe",
                         hashed_password="$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni")
        user2 = UserInDb(id=user2_id, username="alice",
                         hashed_password="$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni")

        with self.database as session:
            session.add(user1)
            session.add(user2)
            session.commit()

        todo1 = TodoInDb(id=uuid4(), title="Test Todo 1", description="Test description 1", user_id=user1_id)
        todo2 = TodoInDb(id=uuid4(), title="Test Todo 2", description="Test description 2", user_id=user1_id)
        todo3 = TodoInDb(id=uuid4(), title="Test Todo 3", description="Test description 3", user_id=user2_id)
        self.todo_repository.create(todo1)
        self.todo_repository.create(todo2)
        self.todo_repository.create(todo3)

        todos = self.todo_repository.get_todos_for_user(user1_id)

        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].title, todo1.title)
        self.assertEqual(todos[0].description, todo1.description)
        self.assertEqual(todos[1].title, todo2.title)
        self.assertEqual(todos[1].description, todo2.description)

    def test_mark_as_finished(self):
        user1_id = uuid4()
        user1 = UserInDb(id=user1_id, username="johndoe",
                         hashed_password="$2b$12$ioi5mfXvg2UzzuxriShJY./e7ShlW.jk2wCbNqaCvykzLL7MOkCni")

        with self.database as session:
            session.add(user1)
            session.commit()

        todo_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
        todo = TodoInDb(id=todo_id, title="Test Todo", description="Test description", user_id=user1_id)
        created = self.todo_repository.create(todo)

        finished_todo = self.todo_repository.mark_as_finished(created.id, user1_id)

        self.assertIsNotNone(finished_todo.finished)
        self.assertIsInstance(finished_todo.finished, datetime)

        retrieved_todo = self.todo_repository.get_by_id(created.id)
        self.assertIsNotNone(retrieved_todo.finished)
        self.assertIsInstance(retrieved_todo.finished, datetime)


if __name__ == '__main__':
    unittest.main()
