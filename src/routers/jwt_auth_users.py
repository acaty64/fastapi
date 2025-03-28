from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 ### minuto
SECRET_KEY = "secretsecret" ## o un Hexadecimal aleatorio

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$PBxdDNWXxPmTYEd13fyrZOAbXF.RoqJO12LeykIDSvyCZlRATBKr6"
    },
    "user2": {
        "username": "user2",
        "fullname": "segundo usuario",
        "email": "segundo@gmail.com",
        "disable": True,
        "password": "$2a$12$22NGc6DNvh0NULc7MqoDCOF.sz1IXf38ZZAmJp5GAw1KJ/p8IIPjO"
    },
    "user3": {
        "username": "user3",
        "fullname": "tercer usuario",
        "email": "tercero@gmail.com",
        "disable": False,
        "password": "$2a$12$uVg2siK3CGxoJHsW.MTl9e/RmxBfU2wWu4xelb/3il/GGButDQvl."
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Credenciales de autenticación inválidas.", 
                    headers={"WWW-Authenticate": "Bearer"}) 
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return search_user(username)

async def current_user(user:User = Depends(auth_user)):
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
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="El password no es correcto.")
    
    access_token = {
            "sub": user.username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        }

    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm = ALGORITHM),
        "token_type": "bearer"
    }


@app.get("/users/me", status_code=status.HTTP_200_OK)
async def me(user: User = Depends(current_user)):
    return user