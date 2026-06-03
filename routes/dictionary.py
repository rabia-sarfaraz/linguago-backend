from fastapi import APIRouter
from models import DictionaryEntry
from database import dictionary_cache_col
from datetime import datetime

router = APIRouter()


# 🔹 SAVE dictionary word
@router.post("/save")
def save_dictionary_word(data: DictionaryEntry):
    doc = data.dict()
    doc["timestamp"] = datetime.utcnow()
    dictionary_cache_col.insert_one(doc)
    return {"message": "Dictionary word saved"}


# 🔹 GET dictionary history — ab SABKA data
@router.get("/history/{email}")
def get_dictionary_history(email: str):
    items = []
    cursor = dictionary_cache_col.find({}).sort("timestamp", -1).limit(100)

    for doc in cursor:
        items.append({
            "word": doc.get("word", ""),
            "definition": doc.get("definition", ""),
            "timestamp": doc.get("timestamp").isoformat()
            if doc.get("timestamp") else None,
        })

    return {"history": items}