# https://medium.com/@kasperjuunge/fastapi-an-example-of-test-driven-development-%EF%B8%8F-21109ea901ae

from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World"
    }

def test_root_404():
    response = client.get("/foo")
    assert response.status_code == 404

def test_url():
    response = client.get("/url")
    assert response.status_code == 200
    assert response.json() == {
        "url": "https://mouredev.com/python"
    }
