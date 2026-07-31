"""
Safe medical Q&A module

⚠️ This module:
- Does NOT diagnose
- Does NOT prescribe medication
- Does NOT replace a doctor
- ONLY gives general, educational information
"""

from app.api.core.llm import ask_llm


SAFETY_SYSTEM_PROMPT = """
You are a medical information assistant.

Rules:
- DO NOT diagnose diseases
- DO NOT prescribe medicines
- DO NOT give treatment plans
- DO NOT say "you have X disease"
- Always include a safety disclaimer
- Provide only general health information
- Encourage consulting a qualified doctor

If the user asks for diagnosis or treatment,
politely refuse and suggest seeing a doctor.
"""


def answer_medical_question(user_text: str) -> str:
    """
    Answer medical questions safely using LLM
    """

    try:
        llm_response = ask_llm(
            user_text=user_text,
            system_override=SAFETY_SYSTEM_PROMPT
        )

        # If LLM returned structured data by mistake, fallback
        if isinstance(llm_response, dict):
            return (
                "I'm here to provide general medical information only. "
                "For diagnosis or treatment, please consult a qualified doctor."
            )

        return (
            f"{llm_response}\n\n"
            "⚠️ This information is for educational purposes only "
            "and is not a medical diagnosis. Please consult a doctor."
        )

    except Exception:
        return (
            "I'm not able to answer that safely right now. "
            "Please consult a healthcare professional."
        )


