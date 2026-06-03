from fastapi import APIRouter
from models import ChatMessage
from database import chat_history_col
from config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
from datetime import datetime
import httpx

router = APIRouter()


# 🔹 GENERATE chat reply via Groq
@router.post("/generate")
def generate_chat(data: ChatMessage):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful translator. Reply naturally in the requested language.",
                },
                {
                    "role": "user",
                    "content": f"Translate this to {data.target_lang}: {data.prompt}",
                },
            ],
            "temperature": 0.3,
        }

        response = httpx.post(
            GROQ_API_URL, headers=headers, json=payload, timeout=30.0
        )

        if response.status_code != 200:
            return {"text": f"⚠️ Groq error: {response.status_code}"}

        result = response.json()
        text = result["choices"][0]["message"]["content"].strip()

        # Save in MongoDB
        chat_history_col.insert_one({
            "prompt": data.prompt,
            "reply": text,
            "target_lang": data.target_lang,
            "user_email": data.user_email,
            "timestamp": datetime.utcnow(),
        })

        return {"text": text}

    except Exception as e:
        return {"text": f"⚠️ Error: {e}"}