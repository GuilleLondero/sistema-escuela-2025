from fastapi import APIRouter
from models.modelo import Career, InputCareer, session
from fastapi.responses import JSONResponse

# Creamos router para agrupar las rutas relacionadas con carreras:
career = APIRouter()

@career.get("/career/all")
#  Obtenemos la lista de todas las carreras registradas en la base de datos.
def get_careers():
    return session.query(Career).all()




# @career.put("/careers/{id}") 
# def update_career(id: int, input: InputCareer):
#     carrera = session.query(Career).filter(Career.id == id).first()
#     if carrera:
#         carrera.name = input.name
#         carrera.active = input.active  # permite reactivar/desactivar
#         session.commit()
#         return {"success": True}
#     return {"success": False, "message": "Carrera no encontrada"}


from fastapi.responses import JSONResponse

@career.put("/careers/{id}")
def update_career(id: int, input: InputCareer):
    try:
        carrera = session.query(Career).filter(Career.id == id).first()
        if carrera:
            carrera.name = input.name
            carrera.active = input.active
            session.commit()
            return {"success": True}
        return {"success": False, "message": "Carrera no encontrada"}
    except Exception as e:
        session.rollback()
        print("Error al actualizar carrera:", e)  # 👈 esto es clave
        return JSONResponse(status_code=500, content={"message": "Error interno"})



@career.delete("/careers/{id}")
def delete_career(id: int):
    carrera = session.query(Career).filter(Career.id == id).first()
    if carrera:
        carrera.active = False
        session.commit()
        return {"success": True}
    return {"success": False, "message": "Carrera no encontrada"}



@career.post("/career/add")
#  Agregamos una nueva carrera al sistema, recibiendo los datos por body (JSON).
def add_career(carrera_ingresada: InputCareer):
    try:
        newCareer = Career(carrera_ingresada.name)
        session.add(newCareer)
        session.commit()
        res = f"carrera {carrera_ingresada.name} guardada correctamente!"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al agregar career --> ", ex) 
    finally:
        session.close()


        
# Devuelve una lista de carreras activas
@career.get("/careers/active")
def get_active_careers():
    try:
        carreras = session.query(Career).filter(Career.active == True).all()
        result = [{"id": c.id, "name": c.name} for c in carreras]
        return result
    except Exception as e:
        session.rollback()
        print("Error:", e)
        return JSONResponse(status_code=500, content={"message": "Error interno"})