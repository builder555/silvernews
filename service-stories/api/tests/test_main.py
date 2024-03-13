import pytest
from fastapi.testclient import TestClient
from api.main import app, get_db
from api.db_interactor import DB


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True)
def mock_db():
    mockdb = DB(path=":memory:")
    mockdb._create_table(
        """CREATE TABLE IF NOT EXISTS `stories`(
                            `id` integer PRIMARY KEY,
                            `title` text NOT NULL,
                            `content` text,
                            `url` text,
                            `poster` text NOT NULL
                          )"""
    )
    mockdb._create_table(
        """CREATE TABLE IF NOT EXISTS `comments`(
                            `id` integer PRIMARY KEY,
                            `story` integer NOT NULL,
                            `content` text,
                            `parent` integer,
                            `poster` text NOT NULL
                          )"""
    )
    mockdb._insert_data(
        "INSERT INTO `stories` (`title`, `content`, `url`, `poster`) VALUES (?, ?, ?, ?)",
        ("Post 1", "This is the content of the first post", "", "user1"),
    )
    mockdb._insert_data(
        "INSERT INTO `stories` (`title`, `content`, `url`, `poster`) VALUES (?, ?, ?, ?)",
        ("Post 2", "This is the content of the second post", "", "user2"),
    )
    app.dependency_overrides[get_db] = lambda: mockdb
    return mockdb


class TestMain:
    def test_ping(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}

    def test_get_stories(self, client):
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
        response = client.get("/")
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
            {
                "title": "Post 3",
                "url": "",
                "content": "This is the content of the third post",
                "poster": "user3",
                "id": 3,
            },
        ]

    def test_require_url_or_content_to_add_story(self, client):
        payload = {"title": "Post 3", "poster": "user3"}
        response = client.post("/", json=payload)
        assert response.status_code == 418
        response = client.post("/", json={**payload, "url": "https://www.google.com"})
        assert response.status_code == 200
        response = client.post("/", json={**payload, "content": "test content"})
        assert response.status_code == 200

    def test_get_one_story(self, client):
        response = client.get("/1")
        assert response.status_code == 200
        assert response.json() == {
            "title": "Post 1",
            "url": "",
            "content": "This is the content of the first post",
            "poster": "user1",
            "id": 1,
        }

    def test_getting_non_existent_story_returns_404(self, client):
        response = client.get("/100")
        assert response.status_code == 404
        assert response.json() == {"detail": "Story not found"}

    def test_add_comment_to_story(self, client):
        response = client.post(
            "/1/comments", json={"content": "This is a comment", "poster": "user1"}
        )
        assert response.status_code == 200

    def test_cannot_add_comment_to_non_existent_story(self, client):
        response = client.post(
            "/100/comments", json={"content": "This is a comment", "poster": "user1"}
        )
        assert response.status_code == 404

    def test_add_nested_comment(self, client):
        response = client.post(
            "/1/comments", json={"content": "This is a comment", "poster": "user1"}
        )
        response = client.post(
            "/1/comments/1", json={"content": "This is a comment", "poster": "user1"}
        )
        assert response.status_code == 200

    def test_cannot_add_nested_comment_to_non_existent_comment(self, client):
        response = client.post(
            "/1/comments/100", json={"content": "This is a comment", "poster": "user1"}
        )
        assert response.status_code == 404

    def test_get_comments(self, client):
        client.post("/1/comments", json={"content": "This is a comment", "poster": "user1"})
        client.post(
            "/1/comments/1", json={"content": "This is a nested comment", "poster": "user2"}
        )
        response = client.get("/1/comments")
        assert response.json() == [
            {
                "content": "This is a comment",
                "poster": "user1",
                "id": 1,
                "parent": None,
                "story": 1,
            },
            {
                "id": 2,
                "content": "This is a nested comment",
                "poster": "user2",
                "parent": 1,
                "story": 1,
            },
        ]
