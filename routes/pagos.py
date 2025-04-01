from fastapi import APIRouter

pagos = APIRouter()

@pagos.get("/pagos")
def pago():
    return "Cuota pagada!!"