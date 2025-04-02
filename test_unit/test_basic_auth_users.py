from src.routers.basic_auth_users import router
#from src.routers.users import router
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
import requests
import pytest
from src.routers.basic_auth_users import search_user, current_user 
from os import environ

client = TestClient(router)
# client = TestClient(app)

def test_search_user():
    response = search_user("user1")
    assert response.username == "user1"

def test_login():
    body = { "username":"user1", "password":"123456" }
    response = client.post("/login", data=body)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "user1",
        "token_type": "bearer"
    }

def test_not_login():
    with pytest.raises(HTTPException) as exc_info:
            body = { "username":"not user", "password":"999999" }
            response = client.post("/login", data=body)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El usuario no es correcto."


def test_login_user_me():
    body = { "username":"user1", "password":"123456" }
    response_login = client.post("/login", data=body)
    assert response_login.status_code == 200
    assert response_login.json() == {
        "access_token": "user1",
        "token_type": "bearer"
    }

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer user1'
    }
    response = client.get("/users/me", headers=header)

    assert response.status_code == 200
    assert response.json()['username'] == "user1"

def test_login_user_me_disabled():
    body = { "username":"user2", "password":"654321" }
    response_login = client.post("/login", data=body)
    assert response_login.status_code == 200
    assert response_login.json() == {
        "access_token": "user2",
        "token_type": "bearer"
    }



    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer user2'
    }

    with pytest.raises(HTTPException) as exc_info:
            response = client.get("/users/me", headers=header)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Usuario inactivo."

