import pytest
from src.routers.jwt_auth_users import router
from fastapi.testclient import TestClient
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.routers.jwt_auth_users import search_user, current_user, search_user_db 
from os import environ
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

client = TestClient(router)

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 ### minuto
SECRET_KEY = "secretsecret" ## o un Hexadecimal aleatorio

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

def test_search_user():
    response = search_user("user1")
    assert response.username == "user1"

def test_login():
    body = { "username":"user1", "password":"123456" }
    response = client.post("/login", data=body)
    assert response.status_code == 200

    user = search_user(body['username'])

    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    assert response.json() == {
                                "access_token": token,
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

    user = search_user(body['username'])
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)

    assert response_login.json() == {'access_token':token, 'token_type': 'bearer'}

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    response = client.get("/users/me", headers=header)
    assert response.status_code == 200
    assert response.json()['username'] == "user1"

def test_login_user_me_disabled():
    body = { "username":"user2", "password":"654321" }
    response_login = client.post("/login", data=body)
    assert response_login.status_code == 200

    user = search_user(body['username'])
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)

    assert response_login.json() == {'access_token':token, 'token_type': 'bearer'}

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    with pytest.raises(HTTPException) as exc_info:
            response = client.get("/users/me", headers=header)
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Usuario inactivo."
