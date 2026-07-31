"""
User model for mapping Telegram chat_id to user info

For now this is in-memory.
Later it can be moved to Postgres without changing logic.
"""

from datetime import datetime
from typing import Dict, Optional


class User:
    def __init__(self, chat_id: int, name: str = ""):
        self.chat_id = chat_id
        self.name = name
        self.created_at = datetime.utcnow()


# In-memory user registry (acts like DB for now)
_users: Dict[int, User] = {}


def get_or_create_user(chat_id: int, name: str = "") -> User:
    """
    Fetch existing user or create new one
    """
    if chat_id not in _users:
        _users[chat_id] = User(chat_id=chat_id, name=name)
    return _users[chat_id]


def get_user(chat_id: int) -> Optional[User]:
    """
    Get user by chat_id
    """
    return _users.get(chat_id)


