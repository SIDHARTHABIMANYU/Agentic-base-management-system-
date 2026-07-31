import re
from app.api.core.model.memory.conversation import (
    get_state,
    init_booking_state,
    update_state,
    is_booking_complete,
    clear_state
)

from app.api.core.model.utils.availability import list_available_slots
from app.api.core.model.utils.cancel import cancel_appointment
from app.api.core.model.DB.curd import create_appointment
from app.api.core.model.DB.session import SessionLocal
from app.api.core.model.doctor import list_doctors
from app.api.core.llm import chat_llm


def handle_intent(llm_data, chat_id):

    intent = llm_data.get("intent")
    doctor = llm_data.get("doctor")
    date = llm_data.get("date")
    time = llm_data.get("time")
    text = llm_data.get("text")

    state = get_state(chat_id)

    if text:
        lower_text = text.lower()

        # -----------------------------
        # MANUAL TIME DETECTION (fix LLM miss)
        # -----------------------------
        time_pattern = r"\b([01]?\d|2[0-3]):[0-5]\d\b"
        match = re.search(time_pattern, lower_text)
        if match:
            time = match.group(0)

        # -----------------------------
        # ANY DOCTOR DETECTION
        # -----------------------------
        if "any doctor" in lower_text:
            init_booking_state(chat_id)
            update_state(chat_id, "doctor", "any")
            intent = "book_appointment"

        # -----------------------------
        # GREETING
        # -----------------------------
        greetings = ["hello", "hi", "hey"]

        if lower_text in greetings:

            doctors = list_doctors()
            doc_names = ", ".join([d["name"] for d in doctors])

            return f"""
Hello! I'm the Appointment Booking AI Agent.
How can I help you today?

Available doctors:
{doc_names}

You can say:
• Book appointment
• Check doctor availability
• Cancel appointment
"""

        # -----------------------------
        # USER WANTS DIFFERENT DOCTOR
        # -----------------------------
        if "another doctor" in lower_text or "different doctor" in lower_text:

            doctors = list_doctors()
            doc_names = ", ".join([d["name"] for d in doctors])

            return f"""
Sure, you can choose another doctor.

Available doctors:
{doc_names}

Which doctor would you like to see?
"""

        # -----------------------------
        # SYMPTOM DETECTION
        # -----------------------------
        symptoms = [
            "pain",
            "fever",
            "headache",
            "tooth",
            "teeth",
            "cough",
            "cold",
            "stomach"
        ]

        if any(symptom in lower_text for symptom in symptoms):

            response = chat_llm(text)
            doctors = list_doctors()

            suggested_doctor = None

            # Example rule for dentist
            if "tooth" in lower_text or "teeth" in lower_text:

                for d in doctors:
                    if "dentist" in d["name"].lower():
                        suggested_doctor = d["name"]
                        break

            if suggested_doctor:

                init_booking_state(chat_id)
                update_state(chat_id, "doctor", suggested_doctor)

                slots = list_available_slots(suggested_doctor, "today")
                slot_text = ", ".join(slots) if slots else "No slots today"

                return f"""
{response}

I'm sorry to hear that. You may need to see a dentist.

Suggested doctor: Dr {suggested_doctor}

Available slots today:
{slot_text}

Would you like to book an appointment with Dr {suggested_doctor}?
You can also choose another doctor.
"""

            doctors = list_doctors()
            doc_names = ", ".join([d["name"] for d in doctors])

            return f"""
{response}

It might be a good idea to consult a doctor.

Available doctors:
{doc_names}

Would you like me to help you book an appointment?
"""

    # --------------------------------
    # FORCE BOOKING FLOW IF STATE EXISTS
    # --------------------------------
    if state:
        if doctor:
            update_state(chat_id, "doctor", doctor)

        if date:
            update_state(chat_id, "date", date)

        if time:
            update_state(chat_id, "time", time)

        intent = "book_appointment"

    # -----------------------------
    # GENERAL CHAT
    # -----------------------------
    if intent == "general_chat":

        response = chat_llm(text)
        doctors = list_doctors()

        doc_names = ", ".join([d["name"] for d in doctors])

        return f"""
{response}

If you're not feeling well,
I can help you book a doctor appointment.

Available doctors:
{doc_names}

You can say:
• Book appointment
• Check availability
• Cancel appointment
"""

    # -----------------------------
    # BOOK APPOINTMENT
    # -----------------------------
    if intent == "book_appointment":

        if not state:
            init_booking_state(chat_id)
            state = get_state(chat_id)

        if doctor:
            update_state(chat_id, "doctor", doctor)

        if date:
            update_state(chat_id, "date", date)

        if time:
            update_state(chat_id, "time", time)

        state = get_state(chat_id)

        # --------------------------------
        # HANDLE "ANY DOCTOR"
        # --------------------------------
        if state["doctor"] == "any":

            doctors = list_doctors()

            # ask date if not provided
            if not state["date"]:
                return "Sure! When would you like to visit?"

            available_options = []

            for d in doctors:
                slots = list_available_slots(d["name"], state["date"])
                if slots:
                    available_options.append(
                        f"Dr {d['name']} \u2192 {', '.join(slots)}"
                    )

            if not available_options:
                return "No doctors available on that date."

            return f"""
Here are available doctors and slots:

{chr(10).join(available_options)}

Please choose a doctor and time.
"""

        # ask doctor
        if not state["doctor"]:

            doctors = list_doctors()
            doc_names = ", ".join([d["name"] for d in doctors])

            return f"""
Which doctor would you like to see?

Available doctors:
{doc_names}
"""

        # ask date
        if not state["date"]:
            return f"When would you like to see Dr {state['doctor']}?"

        # show slots
        if not state["time"]:

            slots = list_available_slots(state["doctor"], state["date"])

            if not slots:
                return f"No slots available for Dr {state['doctor']} on {state['date']}"

            return f"""
Available slots for Dr {state['doctor']} on {state['date']}:
{', '.join(slots)}

Please choose a time.
"""

        # final booking
        if is_booking_complete(chat_id):

            booking_slot = f"{state['date']}{state['time']}"

            db = SessionLocal()

            create_appointment(
                db=db,
                user_id=chat_id,
                doctor_name=state["doctor"],
                booking_slot=booking_slot
            )

            db.close()

            message = f"""
Appointment booked successfully!

Doctor: Dr {state['doctor']}
Date: {state['date']}
Time: {state['time']}
"""

            clear_state(chat_id)

            return message

    # -----------------------------
    # CANCEL APPOINTMENT
    # -----------------------------
    elif intent == "cancel_appointment":

        if not doctor:
            return "Which doctor's appointment do you want to cancel?"

        if not date:
            return f"Which date is your appointment with Dr {doctor}?"

        if not time:
            return f"What time is the appointment with Dr {doctor}?"

        booking_slot = f"{date}{time}"

        cancelled = cancel_appointment(chat_id, doctor, booking_slot)

        if cancelled:
            return f"Appointment with Dr {doctor} on {date} at {time} has been cancelled."

        return "I couldn't find that appointment."

    # -----------------------------
    # CHECK AVAILABILITY
    # -----------------------------
    elif intent == "check_availability":

        if not doctor:

            doctors = list_doctors()
            doc_names = ", ".join([d["name"] for d in doctors])

            return f"""
Which doctor would you like to check?

Available doctors:
{doc_names}
"""

        if not date:
            return f"For which date do you want Dr {doctor}'s availability?"

        slots = list_available_slots(doctor, date)

        if not slots:
            return f"Dr {doctor} has no available slots on {date}."

        return f"Available slots for Dr {doctor} on {date}: {', '.join(slots)}"

    return chat_llm(text)