from app.api.core.model.DB.session import SessionLocal
from app.api.core.model.DB.curd import is_slot_booked, get_booked_slots
from app.api.core.model.doctor import get_doctor_by_name
from app.api.core.model.utils.validation import is_valid_time


def check_availability(doctor_name, date, time):
    if not is_valid_time(time):
        return False

    doctor = get_doctor_by_name(doctor_name)
    if not doctor:
        return False

    if time not in doctor.available_slots:
        return False

    db = SessionLocal()
    booked = is_slot_booked(db, doctor.name, f"{date}_{time}")
    db.close()

    return not booked


def list_available_slots(doctor_name, date):
    doctor = get_doctor_by_name(doctor_name)
    if not doctor:
        return []

    db = SessionLocal()
    booked_times = {t for t in get_booked_slots(db, doctor.name, str(date) )}
    db.close()
    print(doctor.available_slots)
    print([t for t in doctor.available_slots if t not in booked_times] , booked_times)
    return [t for t in doctor.available_slots if t not in booked_times]
