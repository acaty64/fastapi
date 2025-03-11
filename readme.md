ACTIVAR ENTORNO venv

$ source .venv/bin/activate
=> (.env)


EJECUTA fastApi
(.env) fastapi dev main.py
=> crea archivo main.py
=> Responde a http://127.0.0.1:8000
=> Responde a http://127.0.0.1:8000/docs

LEVANTA EL SERVIDOR
(.env) uvicorn main:app --reload


ELIMINA LA CONEXION DEL PUERTO 8000
sudo lsof -t -i tcp:8000 | xargs kill -9


TDD
https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
https://medium.com/@adocquin/mastering-unit-tests-in-python-with-pytest-a-comprehensive-guide-896c8c894304

├── main_project_folder
│   ├── src
│   │   └── __init__.py
│   ├── tests
│   │   └── __init__.py
│   └── main.py




Agregar httpx
(.env) pip install httpx
Crear archivos TDD test_xxxx.py

EJECUTA TDD
(.env) pytest


ROUTERS
* Agregar carpeta routers
    * Incluir los modulos adicionales (no main)
    * incluir archivo __init__.py
* En los archivos de los modulos adicionales modificar 
    X from fastapi import FastAPI
    o from fastapi import APIRouter

    X app = FastAPI()
    o router = APIRouter()

    X @app
    o @router
* En main agregar
    from src.routers import modulos_adicional
    app.include_router(modulos_adicional.router)
* En test modificar
    X from src.modulo_adicional import app
    o from src.routers.modulo_adicional import router

    X client = TestClient(app)
    o client = TestClient(router)
* En test para probar errors modificar
    o import pytest
    o import httpx

    