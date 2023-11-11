from fastapi.encoders import jsonable_encoder

from main import client
from routers.todo import fake_todos_db


def test_read_todo():
    """Test the GET /todo endpoint"""
    response = client.get("/todo")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(fake_todos_db)
