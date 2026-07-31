"""
Notification utilities
(Currently console-based, can be replaced with
Telegram / Email / SMS later)
"""


def notify_user(user_id: str, message: str):
    print(f"📩 USER NOTIFICATION [{user_id}]: {message}")


def notify_doctor(doctor_name: str, message: str):
    print(f"🩺 DOCTOR NOTIFICATION [Dr. {doctor_name.title()}]: {message}")
