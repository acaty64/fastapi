from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

#4:17:10
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entidad user
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "user1": {
        "username": "user1",
        "fullname": "primer usuario",
        "email": "primero@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "user2": {
        "username": "user2",
        "fullname": "segundo usuario",
        "email": "segundo@gmail.com",
        "disable": True,
        "password": "654321"
    },
    "user3": {
        "username": "user3",
        "fullname": "tercer usuario",
        "email": "tercero@gmail.com",
        "disable": False,
        "password": "123654321"
    },
}

@app.get('/')
async def root():
    return {"message": "Hello World from basic_auth_users.py"}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas.", 
            header={"WWW-Authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario inactivo.")
    return user

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto.")
    
    user = search_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="El password no es correcto.")
    
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }

@app.get("/users/me", status_code=status.HTTP_200_OK)
async def me(user: User = Depends(current_user)):
    return user

# async def me(user: User):
#     return user

