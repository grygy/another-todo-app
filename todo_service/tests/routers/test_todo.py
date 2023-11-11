import unittest

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from main import app
from routers.todo import fake_todos_db


class TestTodoRoute(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_read_todo(self):
        """Test the GET /todo endpoint"""
        response = self.client.get("/todo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), jsonable_encoder(fake_todos_db))


if __name__ == '__main__':
    unittest.main()
