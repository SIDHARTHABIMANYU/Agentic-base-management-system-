from typing import Dict, Optional

_conversation_store: Dict[int, Dict] = {}

def get_state(chat_id: int) -> Optional[Dict]:
    return _conversation_store.get(chat_id)

def set_state(chat_id: int, state: Dict):
    _conversation_store[chat_id] = state

def clear_state(chat_id: int):
    if chat_id in _conversation_store:
        del _conversation_store[chat_id]

def init_booking_state(chat_id: int):
    _conversation_store[chat_id] = {
        "intent": "book_appointment",
        "doctor": None,
        "date": None,
        "time": None
    }

def update_state(chat_id: int, key: str, value: str):
    if chat_id not in _conversation_store:
        return
    _conversation_store[chat_id][key] = value

def is_booking_complete(chat_id: int) -> bool:
    state = _conversation_store.get(chat_id)
    if not state:
        return False
    return all([
        state.get("doctor"),
        state.get("date"),
        state.get("time")
    ])
