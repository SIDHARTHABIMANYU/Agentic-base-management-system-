print("LLM MODULE LOADED")

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --------------------------------------------------
# 1️⃣ INTENT EXTRACTION (STRUCTURED)
# --------------------------------------------------

def extract_intent(user_text: str) -> dict:
    system_prompt = """
You are an appointment booking AI.

Extract intent and details.
Return ONLY valid JSON. Do not add explanations.

Allowed intents:
- book_appointment
- cancel_appointment
- check_availability
- general_chat

JSON format:
{
  "intent": "",
  "doctor": "",
  "date": "",
  "time": ""
}
"""

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        print("🧠 RAW GEMINI RESPONSE:", content)

        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON found")

        data = json.loads(content[start:end])

        # 🔥 IMPORTANT: preserve raw text
        data["text"] = user_text

        return data

    except Exception as e:
        print("❌ Gemini Intent Error:", e)
        return {
            "intent": "error",
            "doctor": "",
            "date": "",
            "time": "",
            "text": user_text
        }


# --------------------------------------------------
# 2️⃣ GENERAL CHAT (PLAIN TEXT)
# --------------------------------------------------

def chat_llm(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, friendly AI appointment booking assistant."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Gemini Chat Error:", e)
        return "Sorry, I'm having trouble responding right now."


# print(extract_intent("I want to cancel Dr Rajesh appointment on 2026-01-15 at 11:00"))