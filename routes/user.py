from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.modelo import session, User, UserDetail, PivoteUserCareer, InputUser, InputLogin, InputUserAddCareer
from sqlalchemy.orm import joinedload

# Creamos router para agrupar las rutas relacionadas con usuarios:
user = APIRouter()

@user.get("/")
### Ruta de prueba para verificar si el módulo de usuarios está funcionando bien
def helloUser():
    return "Hello Usuario !!!!!"

@user.get("/users/all")
### Devuelve todos los usuarios registrados junto con sus detalles personales.
### Hacemos uso de 'joinedload' para evitar múltiples consultas a la DB
def getAllUsers():
    try:
        # Ejecutamos una consulta a la DB de todos los usuarios y sus detalles en una sola consulta
        usersConDetail = session.query(User).options(joinedload(User.userdetail)).all()
        
        # Lista de salida para almacenar los datos formateados
        usuarios_con_detalle = []

        for user in usersConDetail:
            user_con_detalle = {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "first_name": user.userdetail.first_name,
                "last_name": user.userdetail.last_name,
                "dni": user.userdetail.dni,
                "type": user.userdetail.type,
                "email": user.userdetail.email,
            }
            usuarios_con_detalle.append(user_con_detalle)
        return JSONResponse(status_code=200, content=usuarios_con_detalle)
    except Exception as ex:
        print("Error ---->> ", ex)
        return {"message": "Error al obtener los usuarios"}
    
@user.get("/users/{us}/{pw}")
### Verificamos si existe el usuario y si la contraseña coincide. Ver de eliminar pasa los datos por URL!!
def loginUser(us:str, pw:str):
    usu = session.query(User).filter(User.username==us).first()
    if usu is None:
        return "Usuario no encontrado!"
    if usu.password==pw: 
        return "Usuario logueado con éxito!"
    else:
        return "Contraseña incorrecta!"

@user.post("/users/add")
### Creamos un nuevo usuario junto con su detalle personal.
def create_user(us: InputUser):
    try:
        newUser = User(us.username, us.password)
        newUserDetail = UserDetail(us.firstname, us.lastname, us.dni, us.type, us.email)
        newUser.userdetail = newUserDetail
        session.add(newUser)
        session.commit()
        return "Usuario creado con éxito!"
    except Exception as ex:
        session.rollback()
        print("Error ---->> ", ex)
    finally:
        session.close()
       
@user.post("/users/login")
### Verificamos si el usuario existe y la contraseña coincide. Recibe datos por body JSON.
def login_user(us: InputLogin):
    try:
        user = session.query(User).filter(User.username == us.username).first()
        if user and user.password == us.password:
            return {"message": "Login exitoso", "user_id": user.id}
        else:
            return {"message": "Invalid username or password"}
    except Exception as ex:
        print("Error ---->> ", ex)
    finally:
        session.close()
   
@user.post("/user/addcareer")
### Inscribe un usuario (alumno) a una carrera.
### Creamos una entrada en la tabla pivote entre User y Career.
def addCareer(ins: InputUserAddCareer):
    try: 
        newInsc = PivoteUserCareer(ins.id_user, ins.id_career)
        session.add(newInsc)
        session.commit()
        res = f"{newInsc.user.userdetail.first_name} {newInsc.user.userdetail.last_name} fue inscripto correctamente a {newInsc.career.name}"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al inscribir al alumno:", ex)
        import traceback
        traceback.print_exc()    
    finally:
        session.close()

@user.get("/user/career/{_username}")
### Devuelve una lista de carreras en las que está inscripto un usuario específico.
### Buscamos al usuario por username y recorre sus relaciones de inscripción.
def get_career_user(_username: str):
    try:
        userEncontrado = session.query(User).filter(User.username == _username ).first()
        arraySalida = []
        if(userEncontrado):
            inscrip_user = userEncontrado.pivoteusercareer
            for inscripcion in inscrip_user:
                career_detail = {
                    "usuario": f"{inscripcion.user.userdetail.first_name} {inscripcion.user.userdetail.last_name}",
                    "carrera": inscripcion.career.name,
                }
                arraySalida.append(career_detail)
            return arraySalida
        else:
            return "Usuario no encontrado!"
    except Exception as ex:
        session.rollback()
        print("Error al traer usuario y/o pagos")
    finally:
        session.close()