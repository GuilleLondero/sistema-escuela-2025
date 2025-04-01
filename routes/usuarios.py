from fastapi import APIRouter
from models.modelo import session, Usuario

usuario = APIRouter()

@usuario.get("/users")
def helloUser():
    return "Hellooo Usuario!!"

@usuario.get("/users/all")
def getAllusuario():
    try:
        return session.query(Usuario).all()

    except Exception as ex:
        print("Error :", ex)
        