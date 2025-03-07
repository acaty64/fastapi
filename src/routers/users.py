from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

router = APIRouter()

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


@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id: int):
    return search_user( id )

@router.get("/usersjson", status_code=status.HTTP_201_CREATED)
async def usersjson():
    return [{"id" : 1, "name" : "usuario", "age": 25,"deactivate": False},
        { "id" : 2, "name" : "usuario_2", "age": 38, "deactivate": False},
        { "id" : 3, "name" : "usuario_3", "age": 29, "deactivate": True }]

@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'El usuario ya existe.')

    users_list.append(user)
    return user

@router.put("/user/")
async def user(user:User):
    for index, saved_used in enumerate(users_list):
        if saved_used.id == user.id:
            users_list[index] = user
            return users_list[index]
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No se ha encontrado el usuario a modificar.')
    # return {'status': 'error', 'message': 'No se ha encontrado el usuario a modificar.'}


@router.delete("/user/{id}", status_code=status.HTTP_200_OK)
async def user(id:int):
    for index, saved_used in enumerate(users_list):
        if saved_used.id == id:
            item_deleted = users_list.pop(index)
            return {'detail': 'Registro eliminado: ' + str(item_deleted.id)}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No se ha encontrado el usuario a eliminar.')
    # return {'status': 'error', 'message': 'No se ha encontrado el usuario a eliminar.'}


def search_user( id: int ):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        #raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='No se ha encontrado el usuario.')
        return {'status': 404, 'detail': 'No se ha encontrado el usuario.'}
