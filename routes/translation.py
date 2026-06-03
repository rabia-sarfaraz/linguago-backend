from fastapi import APIRouter
from models import Translation
from database import translations_col
from datetime import datetime

router = APIRouter()


# 🔹 SAVE translation (user_email phir bhi save hota hai record ke liye)
@router.post("/translate")
def save_translation(data: Translation):
    doc = data.dict()
    doc["timestamp"] = datetime.utcnow()
    translations_col.insert_one(doc)
    return {"message": "Text translation saved"}


# 🔹 GET history — ab SABKA data (email filter hata diya)
@router.get("/history/{email}")
def get_history(email: str):
    items = []
    # find({}) = sabka data, kisi ek user ka nahi
    cursor = translations_col.find({}).sort("timestamp", -1).limit(100)

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