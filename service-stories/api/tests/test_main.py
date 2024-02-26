import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app, get_db


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


@pytest.fixture()
def mock_db():
    mockdb = MagicMock()
    mockdb.get_stories.return_value = [
        {
            "title": "Post 1",
            "url": "",
            "content": "This is the content of the first post",
            "id": 1,
        },
        {
            "title": "Post 2",
            "url": "",
            "content": "This is the content of the second post",
            "id": 2,
        },
    ]
    mockdb.add_story = MagicMock()
    original_get_db = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = lambda: mockdb
    yield mockdb
    app.dependency_overrides[get_db] = original_get_db


class TestMain:
    def test_ping(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}

    def test_get_stories(self, client, mock_db):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [
            {
                "title": "Post 1",
                "url": "",
                "content": "This is the content of the first post",
                "id": 1,
            },
            {
                "title": "Post 2",
                "url": "",
                "content": "This is the content of the second post",
                "id": 2,
            },
        ]

    def test_add_new_story(self, client, mock_db):
        response = client.post(
            "/",
            json={
                "title": "Post 3",
                "url": "",
                "content": "This is the content of the third post",
            },
        )
        assert response.status_code == 200
        mock_db.add_story.assert_called_once_with(
            {
                "title": "Post 3",
                "url": "",
                "content": "This is the content of the third post",
            }
        )
