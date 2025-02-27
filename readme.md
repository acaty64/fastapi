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
Crear archivos TDD test_xxxx.py

EJECUTA TDD
(.env) pytest
