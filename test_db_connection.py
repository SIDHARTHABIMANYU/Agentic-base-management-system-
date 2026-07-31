print("🚀 Starting DB connectivity test...")

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 🔧 CHANGE ONLY IF NEEDED
DB_USER = "postgres"
DB_PASSWORD = "6603"   # <-- put your postgres password
DB_HOST = "localhost"
DB_PORT = "5433"                     # <-- you said 5433
DB_NAME = "appointment_db"

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("🔗 DATABASE URL constructed")

try:
    engine = create_engine(DATABASE_URL)
    print("✅ Engine created")

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    print("✅ Session opened")

    # 🔍 Simple select (connection test)
    result = db.execute(text("SELECT 1"))
    print("✅ SELECT 1 executed:", result.scalar())

    # 🧾 Insert sample record
    insert_query = text("""
        INSERT INTO appointment_details
        (user_id, user_name, doctor_name, booking_slot, status)
        VALUES (:user_id, :user_name, :doctor_name, :booking_slot, :status)
    """)

    db.execute(
        insert_query,
        {
            "user_id": 999,
            "user_name": "Test User",
            "doctor_name": "Dr Test",
            "booking_slot": "2026-01-15 11:00",
            "status": "BOOKED"
        }
    )

    db.commit()
    print("🎉 INSERT SUCCESSFUL — record added!")

except Exception as e:
    print("❌ ERROR OCCURRED")
    print(e)

finally:
    try:
        db.close()
        print("🔒 DB session closed")
    except:
        pass
