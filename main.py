from fastapi import FastAPI
from src.routers import users

app = FastAPI()

# Routers
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

