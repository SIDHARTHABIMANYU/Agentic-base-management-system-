"""
Doctor model & availability data
Acts like an in-memory doctor database
"""

from typing import Dict, List


class Doctor:
    def __init__(
        self,
        id: int,
        name: str,
        specialization: str,
        available_slots: List[str]
    ):
        self.id = id
        self.name = name.lower()
        self.specialization = specialization.lower()
        self.available_slots = available_slots

    def is_available(self, time: str) -> bool:
        return time in self.available_slots

    def book_slot(self, time: str) -> bool:
        if time in self.available_slots:
            self.available_slots.remove(time)
            return True
        return False


# --------------------------------
# In-memory doctor registry
# --------------------------------

doctors: Dict[str, Doctor] = {

    # Cardiology
    "rajesh": Doctor(
        id=1,
        name="Rajesh",
        specialization="cardiologist",
        available_slots=["10:00", "11:00", "17:00"]
    ),

    "arun": Doctor(
        id=2,
        name="Arun",
        specialization="cardiologist",
        available_slots=["09:00", "14:00", "16:00"]
    ),

    # Dermatology
    "anita": Doctor(
        id=3,
        name="Anita",
        specialization="dermatologist",
        available_slots=["12:00", "15:00"]
    ),

    "meera": Doctor(
        id=4,
        name="Meera",
        specialization="dermatologist",
        available_slots=["10:30", "13:00", "16:30"]
    ),

    # Neurology
    "vikram": Doctor(
        id=5,
        name="Vikram",
        specialization="neurologist",
        available_slots=["09:30", "11:30", "15:30"]
    ),

    # Orthopedic
    "karthik": Doctor(
        id=6,
        name="Karthik",
        specialization="orthopedic",
        available_slots=["10:00", "12:00", "18:00"]
    ),

    "ravi": Doctor(
        id=7,
        name="Ravi",
        specialization="dentist",
        available_slots=["10:00", "11:00"]
    )
}


# --------------------------------
# Helper functions
# --------------------------------

def get_doctor_by_name(name: str) -> Doctor | None:
    """
    Find doctor by name
    """
    if not name:
        return None

    clean_name = name.lower().replace("dr.", "").replace("dr ", "").strip()

    return doctors.get(clean_name)


def get_doctors_by_specialization(specialization: str) -> List[Doctor]:
    """
    Find doctors by specialization
    """
    spec = specialization.lower().strip()

    return [
        doc for doc in doctors.values()
        if doc.specialization == spec
    ]


def list_doctors() -> List[Dict]:
    """
    Return doctor list for UI / API
    """
    return [
        {
            "id": doc.id,
            "name": doc.name.title(),
            "specialization": doc.specialization.title(),
            "available_slots": doc.available_slots
        }
        for doc in doctors.values()
    ]
