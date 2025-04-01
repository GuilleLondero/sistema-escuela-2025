from fastapi import APIRouter

usuario = APIRouter()

@usuario.get("/users")
def helloUser():
    return "Hellooo Usuario!!"