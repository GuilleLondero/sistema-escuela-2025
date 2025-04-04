#Importaciones:

import sys
sys.tracebacklimit = 1

from fastapi import FastAPI
from routes.usuarios import usuario
from routes.pagos import pagos


#Creación de la aplicación FastAPI:

api_escu = FastAPI()
api_escu.include_router(usuario)
api_escu.include_router(pagos)


"""
#Definición de rutas (endpoints):
@app.get("/")
def helloword():
    return "hello world"

@app.get("/user")
def mostrarInfoUsua():
    return "“Hola Juancito! Has iniciado sesión con éxito!"

@app.get("/users/{user_id}")
def user():
    return "soy un usuario!!"

#Inicio del servidor Uvicorn:
run(app, host="192.168.0.191", port=8000) 
"""
