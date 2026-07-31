from fastapi import APIRouter, Request
from app.api.core.llm import extract_intent
from app.api.core.model.utils.helpers import handle_intent
from app.api.core.model.utils.telegram import send_telegram_message

router = APIRouter()

last_update_id = None

@router.post("/webhook")
async def webhook(request: Request):
    global last_update_id
    body = await request.json()
    update_id = body["update_id"]

    if last_update_id is not None and update_id <= last_update_id:
        print("⚠️ DUPLICATE UPDATE IGNORED:", update_id)
        return {"ok": True}

    last_update_id = update_id

    chat_id = body["message"]["chat"]["id"]
    user_message = body["message"]["text"]
    print("📥 RAW BODY:", body)
    print("🧠 TEXT SENT TO GEMINI:", user_message)
    
    llm_data = extract_intent(user_message)
    print("🧠 RAW GEMINI RESPONSE:", llm_data)

    reply = handle_intent(llm_data, chat_id)
    print("📤 FINAL REPLY:", reply)

    send_telegram_message(chat_id, reply)

    return {"ok": True}
   
