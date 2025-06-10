from fastapi import APIRouter
from models.modelo import Career, InputCareer, session

# Creamos router para agrupar las rutas relacionadas con carreras:
career = APIRouter()

@career.get("/career/all")
#  Obtenemos la lista de todas las carreras registradas en la base de datos.
def get_careers():
    return session.query(Career).all()

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