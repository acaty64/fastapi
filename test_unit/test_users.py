from src.users import app
from fastapi.testclient import TestClient
import json
import requests

client = TestClient(app)

def test_usersjson():
    response = client.get("/usersjson")
    assert response.status_code == 200
    assert type(response.json()) == list
    print('len response: ', len(response.json()))
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


def test_user_error_by_id():
    response = client.get("/user/100")
    assert response.status_code == 200
    # assert type(response.json()) == dict
    jsonResponse = response.json() 
    assert jsonResponse['status'] == 'error'

def test_add_user():
    get_response = client.get("/users")
    len_old = len(get_response.json())

    body = { "id":4, "name":"usuario_4", "age":20, "deactivate": False }
    response = client.post("/user", json=body)
    print(response.json()['message'])
    assert response.json()['message'] == 'Usuario agregado.'
    assert response.status_code == 200

    get_response = client.get("/users")
    len_new = len(get_response.json())
    assert len_old + 1 == len_new

    response = client.post("/user", json=body)
    print(response.json()['message'])
    assert response.json()['message'] == 'El usuario ya existe.'
