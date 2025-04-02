from fastapi import FastAPI
from src.routers import users, basic_auth_users

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(basic_auth_users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

