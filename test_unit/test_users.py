from src.users import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_usersjson():
    response = client.get("/usersjson")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) > 0

def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) > 0

def test_user_by_id():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert len(response.json()) > 0

# def test_login():
#     user = "usuario"
#     password = "secret"
#     response = client.post("/login")
#     assert response == 200