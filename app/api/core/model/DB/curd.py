from sqlalchemy.orm import Session
from app.api.core.model.appointment import Appointment
from app.api.core.model.appointment import Appointment
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_USER = "postgres"
DB_PASSWORD = "6603"   # <-- put your postgres password
DB_HOST = "localhost"
DB_PORT = "5433"                     # <-- you said 5433
DB_NAME = "appointment_db"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
def create_appointment(
    db,
    user_id: str,
    doctor_name: str,
    booking_slot: str
):
    

    engine = create_engine(DATABASE_URL)
    print("✅ Engine created")

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    print("✅ Session opened")

    # 🔍 Simple select (connection test)
    result = db.execute(text("SELECT 1"))
    print("✅ SELECT 1 executed:", result.scalar())
    #result = db.execute("SELECT COUNT(*) FROM appointment_details")
    #count = result.scalar()  # returns the integer count

    # 2️⃣ Generate serial_no
    #serial_no = count + 1
    # 🧾 Insert sample record
    insert_query = text("""
        INSERT INTO appointment_details
        (serial_no, user_id, user_name, doctor_name, booking_slot, status)
        VALUES (:serial_no, :user_id, :user_name, :doctor_name, :booking_slot, :status)
    """)
    count = db.execute(
        text("SELECT COUNT(*) FROM appointment_details")
    ).scalar()
    db.execute(
        insert_query,
        {
            "user_id": user_id,
            "user_name": "Test User",
            "doctor_name": doctor_name,
            "booking_slot": booking_slot.replace(" ", ""),
            "status": "BOOKED",
            "serial_no" : count + 1
        }
    )

    db.commit()


from sqlalchemy import text
from sqlalchemy.orm import Session

def is_slot_booked(db: Session, doctor_name, booking_slot) -> bool:
    print(doctor_name, booking_slot, "@@@@@@@")
    query = text("""
        SELECT 1
        FROM appointment_details
        WHERE doctor_name = :doctor_name
          AND booking_slot = :booking_slot
          AND status = 'BOOKED'
        LIMIT 1
    """)

    result = db.execute(
        query,
        {
            "doctor_name": doctor_name,
            "booking_slot": booking_slot,
        }
    ).first()

    return result is not None


def cancel_appointment(db: Session, user_id, doctor_name,booking_slot ) -> bool:
    print("LLAmaA", user_id , booking_slot)
    insert_query = text("""
        UPDATE appointment_details
        SET status = 'CANCELLED'
        WHERE user_id = :user_id
        AND booking_slot = :booking_slot;
    """)

    db.execute(
        insert_query,
        {
            "user_id": user_id,
            "user_name": "Test User",
            "doctor_name": doctor_name,
            "booking_slot": booking_slot,
        }
    )

    db.commit()

    return True


from sqlalchemy import text
from sqlalchemy.orm import Session

def get_booked_slots(db: Session, doctor_name: str, date: str):
    print(doctor_name, "@@@@" , date)
    date = "%" + date + "%"
    print(date)
    query = text("""
        SELECT booking_slot
        FROM appointment_details
        WHERE doctor_name = :doctor_name
          AND booking_slot like :date
          AND status = 'BOOKED'
        ORDER BY booking_slot
    """)


    result = db.execute(
        query,
        {
            "doctor_name": doctor_name,
            "date": date
        }
    ).fetchall()

    # return list of datetime slots
    print(result)
    print([row[0][10::] for row in result])
    return [row[0][10::] for row in result]

