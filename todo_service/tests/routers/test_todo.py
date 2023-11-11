from main import client


def test_read_todo():
    """Test the GET /todo endpoint"""
    response = client.get("/todo")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": "Foo",
            "description": "Fighters",
            "id": "bd65600d-8669-4903-8a14-af88203add38"
        }
    ]
