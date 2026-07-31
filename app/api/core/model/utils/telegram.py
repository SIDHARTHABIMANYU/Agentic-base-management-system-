print("🤖 BOT TOKEN")

import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    r = requests.post(url, json=payload, timeout=10)

    print("📤 Telegram status:", r.status_code)
    print("📤 Telegram response:", r.text)


