#Importaciones:

import sys # Importamos el módulo sys, que permite interactuar con el sistema y configurar el entorno de Python
sys.tracebacklimit = 1 # Limitamos la cantidad de líneas que se muestran en el traceback para ver errores

from fastapi import FastAPI #importamos FastAPI
from routes.usuarios import usuario
from routes.userdetail import userDetail
from fastapi.middleware.cors import CORSMiddleware

#Creación de la aplicación FastAPI:

api_escu = FastAPI()
api_escu.include_router(usuario)
api_escu.include_router(userDetail)


#Creación del Middleware:
api_escu.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["GET", "POST", "PUT", "DELETE"],
   allow_headers=["*"],
)



"""
Importás FastAPI
Creás una app
Definís una o más rutas usando decoradores como @app.get() o @app.post()
Respondes algo (texto, datos, etc.)

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
