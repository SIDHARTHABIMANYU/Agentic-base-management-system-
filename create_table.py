from app.api.core.model.DB.session import engine
from app.api.core.model.DB.base import Base

# 🔥 IMPORTANT: import ALL models here
from app.api.core.model.appointment import Appointment
from app.api.core.model.user import User
# add doctor DB model later if you create one

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done ✅")
