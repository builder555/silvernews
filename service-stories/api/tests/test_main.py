from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture()
def client():
    client = TestClient(app)
    return client


class TestMain:
    def test_ping(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"ping": "pong!"}
