from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Entidad user
class User(BaseModel):
    id: int
    name: str
    age: int
    deactivate: bool

# Lista de datos (base de datos ficticio)
users_list = [ User(id = 1, name = "usuario", age= 25, deactivate = False), 
            User(id = 2, name = "usuario_2", age = 38, deactivate = False), 
            User(id= 3, name = "usuario_3", age = 29, deactivate = True) ]


@app.get("/users")
async def users():
    return users_list

@app.get("/user/{id}")
async def user(id: int):
    return search_user( id )

@app.get("/usersjson")
async def usersjson():
    return [{"id" : 1, "name" : "usuario", "age": 25,"deactivate": False},
        { "id" : 2, "name" : "usuario_2", "age": 38, "deactivate": False},
        { "id" : 3, "name" : "usuario_3", "age": 29, "deactivate": True }]

@app.post("/user/")
async def user(user:User):
    if type(search_user(user.id)) == User:
        return {'status': 'error', 'message': 'El usuario ya existe.'}
    else:
        users_list.append(user)
        return {'status': 'Ok', 'message': 'Usuario agregado.'}


def search_user( id: int ):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {'status': 'error', 'message': 'No se ha encontrado el usuario'}
