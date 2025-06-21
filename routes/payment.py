from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.modelo import Payment, InputPayment, User, session
from sqlalchemy.orm import joinedload

payment = APIRouter()


@payment.get("/payment/all/detailled")
def get_payments():
    paymentsDetailled = []
    allPayments = session.query(Payment).all()
    for pay in allPayments:
        result = {
            "id_pago": pay.id,
            "monto": pay.amount,
            "afecha de pago": pay.created_at,
            "mes_pagado": pay.affected_month,
            "alumno": f"{pay.user.userdetail.first_name} {pay.user.userdetail.last_name}",
            "carrera afectada": pay.career.name,
        }
        paymentsDetailled.append(result)
    return paymentsDetailled
    ##return session.query(Payment).options(joinedload(Payment.user)).userdetail


@payment.get("/payment/user/{_username}")
def payment_user(_username: str):
    try:
        user = session.query(User).filter(User.username == _username).first()
        if not user:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

        payments = (
            session.query(Payment)
            .filter(Payment.id_user == user.id, Payment.active == True)
            .order_by(Payment.created_at.desc())
            .all()
        )

        result = [
            {
                "id": pay.id,
                "amount": pay.amount,
                "fecha_pago": pay.created_at,
                "usuario": f"{user.userdetail.first_name} {user.userdetail.last_name}",
                "carrera": pay.career.name,
                "mes_afectado": pay.affected_month,
            }
            for pay in payments
        ]

        return result
    except Exception as ex:
        session.rollback()
        print("Error:", ex)
        return JSONResponse(status_code=500, content={"message": "Error interno"})



@payment.post("/payment/add")
def add_payment(pay: InputPayment):
    try:
        newPayment = Payment(pay.id_career, pay.id_user, pay.amount, pay.affected_month)
        session.add(newPayment)
        session.commit()
        res = f"Pago para el alumno {newPayment.user.userdetail.first_name} {newPayment.user.userdetail.last_name}, aguardado!"
        print(res)
        return res
    except Exception as ex:
        session.rollback()
        print("Error al guardar un pago --> ", ex)
    finally:
        session.close()


@payment.put("/payments/{id}")
def update_payment(id: int, input: InputPayment):
    try:
        pay = session.query(Payment).filter(Payment.id == id).first()
        if not pay:
            return JSONResponse(status_code=404, content={"message": "Pago no encontrado"})

        pay.id_user = input.id_user
        pay.id_career = input.id_career
        pay.amount = input.amount
        pay.affected_month = input.affected_month
        pay.active = input.active

        session.commit()
        return {"success": True}
    except Exception as e:
        session.rollback()
        print("Error al actualizar pago:", e)
        return JSONResponse(status_code=500, content={"message": "Error interno"})



@payment.delete("/payment/{id}")
def delete_payment(id: int):
    try:
        pay = session.query(Payment).filter(Payment.id == id).first()
        if not pay:
            return JSONResponse(status_code=404, content={"message": "Pago no encontrado"})

        pay.active = False
        session.commit()
        return {"success": True, "message": "Pago dado de baja lógicamente"}
    except Exception as ex:
        session.rollback()
        print("Error al eliminar pago:", ex)
        return JSONResponse(status_code=500, content={"message": "Error interno"})


@payment.get("/payments/active")
def get_active_payments():
    try:
        pagos = session.query(Payment).filter(Payment.active == True).all()
        result = [
            {
                "id": p.id,
                "monto": p.amount,
                "fecha": p.created_at,
                "mes_afectado": p.affected_month,
                "alumno": f"{p.user.userdetail.first_name} {p.user.userdetail.last_name}",
                "carrera": p.career.name
            }
            for p in pagos
        ]
        return result
    except Exception as e:
        session.rollback()
        print("Error al traer pagos activos:", e)
        return JSONResponse(status_code=500, content={"message": "Error interno"})
