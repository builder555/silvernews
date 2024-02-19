import pytest
from fastapi.testclient import TestClient
from api.main import app, get_db


@pytest.fixture()
def client():
    client = TestClient(app)
    return client

def mock_get_db():
    class MockDB:
        def get_stories(self):
            return [
                {"title": "Post 1", "url": "", "content": "This is the content of the first post"},
                {"title": "Post 2", "url": "", "content": "This is the content of the second post"},
            ]
    return MockDB()

app.dependency_overrides[get_db] = mock_get_db

class TestMain:
    def test_ping(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}

    def test_get_stories(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [
            {"title": "Post 1", "url": "", "content": "This is the content of the first post"},
            {"title": "Post 2", "url": "", "content": "This is the content of the second post"},
        ]
