from fastapi import APIRouter
from models import VoiceTranslation
from database import voice_translations_col
from datetime import datetime

router = APIRouter()


# 🔹 SAVE voice translation
@router.post("/translate")
def save_voice_translation(data: VoiceTranslation):
    doc = data.dict()
    doc["timestamp"] = datetime.utcnow()
    voice_translations_col.insert_one(doc)
    return {"message": "Voice translation saved"}


# 🔹 GET voice history — ab SABKA data
@router.get("/history/{email}")
def get_voice_history(email: str):
    items = []
    cursor = voice_translations_col.find({}).sort("timestamp", -1).limit(100)

    for doc in cursor:
        items.append({
            "text": doc.get("text", ""),
            "source_lang": doc.get("source_lang", ""),
            "target_lang": doc.get("target_lang", ""),
            "translated_text": doc.get("translated_text", ""),
            "timestamp": doc.get("timestamp").isoformat()
            if doc.get("timestamp") else None,
        })

    return {"history": items}