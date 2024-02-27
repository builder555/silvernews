import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app, get_db
from api.db_interactor import DB


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


@pytest.fixture()
def mock_db():
    mockdb = DB(path=":memory:")
    mockdb._create_table("""CREATE TABLE IF NOT EXISTS `stories`(
                          `id` integer PRIMARY KEY,
                          `title` text NOT NULL,
                          `content` text,
                          `url` text,
                          `poster` text NOT NULL
                          )""")
    mockdb._insert_data("INSERT INTO `stories` (`title`, `content`, `url`, `poster`) VALUES (?, ?, ?, ?)", 
                    ("Post 1", "This is the content of the first post", "", "user1"))
    mockdb._insert_data("INSERT INTO `stories` (`title`, `content`, `url`, `poster`) VALUES (?, ?, ?, ?)", 
                    ("Post 2", "This is the content of the second post", "", "user2"))
    app.dependency_overrides[get_db] = lambda: mockdb
    return mockdb


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
                "poster": "user1",
                "id": 1,
            },
            {
                "title": "Post 2",
                "url": "",
                "content": "This is the content of the second post",
                "poster": "user2",
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
                "poster": "user3",
            },
        )
        assert response.status_code == 200
        assert [dict(r) for r in mock_db.get_stories()] == [
            {
                "title": "Post 1",
                "url": "",
                "content": "This is the content of the first post",
                "poster": "user1",
                "id": 1,
            },
            {
                "title": "Post 2",
                "url": "",
                "content": "This is the content of the second post",
                "poster": "user2",
                "id": 2,
            },
            {
                "title": "Post 3",
                "url": "",
                "content": "This is the content of the third post",
                "poster": "user3",
                "id": 3,
            },
        ]