from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.modelo import session, User, UserDetail, PivoteUserCareer, InputUser, InputLogin, InputUserAddCareer
from sqlalchemy.orm import joinedload
from auth.security import Security


# Creamos router para agrupar las rutas relacionadas con usuarios:
user = APIRouter()

@user.get("/")
### Ruta de prueba para verificar si el módulo de usuarios está funcionando bien
def helloUser():
    return "Hello Usuario !!!!!"

@user.get("/users/all")
### Devuelve todos los usuarios registrados junto con sus detalles personales.
### Hacemos uso de 'joinedload' para evitar múltiples consultas a la DB
def getAllUsers(req: Request):
    try:
        has_access = Security.verify_token(req.headers)
        if "iat" in has_access:
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
        else:
            return JSONResponse(
           status_code=401,
           content=has_access,
       )
    except Exception as ex:
        print("Error ---->> ", ex)
        return {"message": "Error al obtener los usuarios"}
    

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
def login_post(userIn: InputLogin):
   try:
        # Buscamos al usuario por username:
        user = session.query(User).filter(User.username == userIn.username).first()
        
        # Verificamos que el usuario exista y que coincida la contraseña:
        if user and user.password == userIn.password:
            tkn = Security.generate_token(user) # Generamos token con los datos del usuario
            if not tkn:
                return JSONResponse(
                    status_code=500,
                    content={"message": "Error en la generación del token"}
                )
            # Preparamos respuesta c/datos user
            res = {
                "status": "success",
                "token": tkn,
                "user": {
                    "username": user.username,
                    "first_name": user.userdetail.first_name,
                    "last_name": user.userdetail.last_name,
                    "email": user.userdetail.email,
                    "type": user.userdetail.type
                },
                "message": "Usuario logueado con éxito"
            }
            print(res)
            return JSONResponse(status_code=200, content=res)
        else:
            return JSONResponse(
            status_code=401,
            content={"message": "Usuario o contraseña inválida"}
        )
   except Exception as ex:
       print("Error ---->>", ex)
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


## Devuelve una lista de todos los alumnos inscriptos a alguna carrera.
@user.get("/users/alumnos")
def get_all_students():
    try:
        alumnos = session.query(User).all()
        salida = []
        for u in alumnos:
            if u.userdetail.type.lower() == "alumno":
                carrera = (
                    u.pivoteusercareer[0].career.name
                    if u.pivoteusercareer else "Sin carrera"
                )
                salida.append({
                    "id": u.id,
                    "username": u.username,
                    "nombre": u.userdetail.first_name,
                    "apellido": u.userdetail.last_name,
                    "email": u.userdetail.email,
                    "carrera": carrera
                })
        return salida
    except Exception as e:
        session.rollback()
        print("Error al traer alumnos:", e)
        return JSONResponse(status_code=500, content={"message": "Error interno"})
    

#permite cambias contraseña de cada usuario
@user.post("/users/change-password")
def change_password(request: Request, data: dict):
    try:
        headers = request.headers
        payload = Security.verify_token(headers)

        if "iat" not in payload:
            return JSONResponse(status_code=401, content={"message": "Token inválido"})

        username = payload["username"]
        new_password = data.get("new_password")

        if not new_password:
            return JSONResponse(status_code=400, content={"message": "Nueva contraseña requerida"})

        user = session.query(User).filter(User.username == username).first()

        if user:
            user.password = new_password
            session.commit()
            return {"success": True, "message": "Contraseña actualizada correctamente"}
        else:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

    except Exception as e:
        session.rollback()
        print("Error al cambiar contraseña:", e)
        return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})
    

    from fastapi import APIRouter
from models.modelo import Career, session
from fastapi.responses import JSONResponse

career = APIRouter()
