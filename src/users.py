from fastapi import FastAPI
from pydantic import BaseModel

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
    users = filter(lambda user: user.id == id, users_list)
    return list(users)[0]

@app.get("/usersjson")
async def usersjson():
    return [{"id" : 1, "name" : "usuario", "age": 25,"deactivate": False},
        { "id" : 2, "name" : "usuario_2", "age": 38, "deactivate": False},
        { "id" : 3, "name" : "usuario_3", "age": 29, "deactivate": True }]



# @app.post("/login")
# async def login(user: str, password: str):
#     if search_user(user).password != password:

#     response = "acreditado"
#     return {"user": user, "response": response}

# def search_user(user: str):
#     users = filter(lambda user: user.user == user, users_list)
#     user = users_list[0]
#     return user