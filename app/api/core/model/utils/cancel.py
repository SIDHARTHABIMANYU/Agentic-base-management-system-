from app.api.core.model.DB.session import SessionLocal
from app.api.core.model.DB.curd import cancel_appointment as cancel_db


def cancel_appointment(user_id, doctor_name, booking_slot) -> bool:
    db = SessionLocal()
    result = cancel_db(db, user_id, doctor_name,booking_slot)
    db.close()
    return result
