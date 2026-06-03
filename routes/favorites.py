from fastapi import APIRouter
from models import FavoriteItem
from database import favorites_col
from datetime import datetime

router = APIRouter()


# 🔹 ADD favorite
@router.post("/add")
def add_favorite(data: FavoriteItem):
    doc = data.dict()
    doc["timestamp"] = datetime.utcnow()
    favorites_col.insert_one(doc)
    return {"message": "Added to favorites"}


# 🔹 GET favorites — ab SABKA data
@router.get("/{email}")
def get_favorites(email: str):
    items = []
    cursor = favorites_col.find({}).sort("timestamp", -1).limit(100)

    for doc in cursor:
        items.append({
            "id": str(doc.get("_id")),
            "item_type": doc.get("item_type", ""),
            "original_text": doc.get("original_text", ""),
            "result_text": doc.get("result_text", ""),
            "source_lang": doc.get("source_lang"),
            "target_lang": doc.get("target_lang"),
            "timestamp": doc.get("timestamp").isoformat()
            if doc.get("timestamp") else None,
        })

    return {"favorites": items}


# 🔹 DELETE favorite
@router.delete("/remove/{favorite_id}")
def remove_favorite(favorite_id: str):
    from bson import ObjectId
    try:
        favorites_col.delete_one({"_id": ObjectId(favorite_id)})
        return {"message": "Removed from favorites"}
    except Exception as e:
        return {"message": f"Error: {e}"}