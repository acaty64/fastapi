# from src.users import app
from src.routers.users import router
from fastapi.testclient import TestClient
from fastapi import HTTPException
import json
import requests
import pytest
from src.routers.users import search_user 

client = TestClient(router)

def test_search_user():
    response = search_user(1)
    print('prn test_search_user: ', response)
    assert response.status_code == 200

def test_usersjson():
    response = client.get("/usersjson")
    assert response.status_code == 201
    assert type(response.json()) == list
    #print('len response: ', len(response.json()))
    assert len(response.json()) > 0

def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) > 0

def test_user_by_id():
    resp = client.get("/users/")
    print('test_user_by_id', resp.json())
    response = client.get("/user/1")
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert len(response.json()) > 0


def test_user_error_by_id():
    response = client.get("/user/100")
    jsonResponse = response.json() 
    assert jsonResponse['status_code'] == 404
    assert jsonResponse['detail'] == 'No se ha encontrado el usuario.'

def test_add_user():
    get_response = client.get("/users")
    len_old = len(get_response.json())

    body = { "id":4, "name":"usuario_4", "age":20, "deactivate": False }
    response = client.post("/user", json=body)
    assert response.status_code == 201
    assert response.json() == body

    get_response = client.get("/users")
    len_new = len(get_response.json())
    assert len_old + 1 == len_new

def test_add_user_error():
    body = { "id":4, "name":"usuario_4", "age":20, "deactivate": False }
    with pytest.raises(HTTPException) as err:
        client.post("/user", json=body)
    assert err.value.status_code == 404
    assert err.value.detail == "El usuario ya existe."

def test_updated_user():
    id = 1
    body = { "id":id, "name":"usuario modificado", "age":10, "deactivate": True }
    response = client.put('/user', json=body)
    assert response.status_code == 200
    get_response = client.get("/user/" + str(id))
    assert response.json() == get_response.json()

def test_updated_user_error():
    id = 100
    body = { "id":id, "name":"usuario modificado", "age":10, "deactivate": True }
    with pytest.raises(HTTPException) as err:
        client.put('/user', json=body)
    assert err.value.status_code == 404
    assert err.value.detail == "No se ha encontrado el usuario a modificar."

def test_delete_user():
    get_response = client.get("/users")
    len_old = len(get_response.json())

    id = 2
    response = client.delete("/user/" + str(id))

    assert response.status_code == 200
    assert response.json()['detail'] == 'Registro eliminado: ' + str(id)

    get_response = client.get("/users")
    len_new = len(get_response.json())
    assert len_old - 1 == len_new

    response = client.get("/user/" + str(id))
    assert response.json()['status'] == 404
    assert response.json()['detail'] == 'No se ha encontrado el usuario.'
