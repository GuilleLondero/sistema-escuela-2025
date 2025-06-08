from fastapi import APIRouter
from models.modelo import session, Usuario, InputUsuario

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
        
@usuario.get("/users/{identificador}")
def obtenerUser(identificador:int) :
    return session.query(Usuario).filter(Usuario.id==identificador).first()      

@usuario.get("/usuario/{us}/{pw}")
def loginUser(us:str, pw:str):
    usu = session.query(Usuario).filter(Usuario.username==us).first()
    if usu.password==pw:
        return "Usuario logueado con exito"
    else:
        return "Usuario o contraseñaincorrecta"
    

@usuario.post("/users/new")   #/add
def create_user(us: InputUsuario) :
    try:
        usu = Usuario(us.username, us.password)
        session.add(usu)
        session.commit()
        return "Usuario creado con éxito"
    except Exception as ex:
        print("Error --->", ex)


