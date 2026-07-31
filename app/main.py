from fastapi import FastAPI
from app.api.webhook import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Appointment Booking AI Agent running"}
