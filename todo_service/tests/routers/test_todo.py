import unittest
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from auth.auth import get_current_active_user
from main import app
from schemas.todo import TodoSchema


class MockUser:
    def __init__(self, id):
        self.id = id


class TestTodoRoute(unittest.TestCase):

    def setUp(self):
        test_user_id = uuid4()

        def ignore_auth():
            return MockUser(test_user_id)

        app.dependency_overrides[get_current_active_user] = ignore_auth
        self.client = TestClient(app)
        self.test_user_id = test_user_id

    @patch('db.todo_repository.TodoRepository.get_todos_for_user')
    def test_read_todo(self, mock_get_todos_for_user):
        """Test the GET /todo endpoint"""

        todo_id = uuid4()
        todos = [
            TodoSchema(id=todo_id, title="Todo 1", description="Description 1", user_id=self.test_user_id)
        ]
        mock_get_todos_for_user.return_value = todos
        expected_json = [{
            "id": str(todo_id),
            "title": "Todo 1",
            "description": "Description 1",
        }]

        response = self.client.get("/todo")

        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json(), expected_json)
        mock_get_todos_for_user.assert_called_once_with(self.test_user_id)


if __name__ == '__main__':
    unittest.main()
