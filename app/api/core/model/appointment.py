from sqlalchemy import Column, String
from app.api.core.model.DB.base import Base

from datetime import datetime
from typing import List
from app.api.core.model.doctor import Doctor

class Appointment(Base):
    __tablename__ = "appointment_details"   # 👈 EXACT table name

    user_id = Column(String, primary_key=True)
    doctor_name = Column(String, nullable=False)
    booking_slot = Column(String, nullable=False)
    status = Column(String, default="BOOKED")







