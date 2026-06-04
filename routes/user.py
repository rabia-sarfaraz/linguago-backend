from fastapi import APIRouter, HTTPException
from models import UserSignup, UserLogin, UserProfileUpdate
from database import (
    users_col,
    translations_col,
    voice_translations_col,
    dictionary_cache_col,
    favorites_col,
)
from utils.auth import hash_password, verify_password
from datetime import datetime
from pydantic import BaseModel, EmailStr


router = APIRouter()


# 🆕 Naya model — Firebase signup ke liye (no password)
class FirebaseUserSignup(BaseModel):
    name: str
    email: EmailStr


# 🔹 SIGNUP (purana — abhi bhi rahega, koi farq nahi padta)
@router.post("/signup")
def signup(data: UserSignup):
    existing = users_col.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "phone": "",
        "language": "English",
        "country": "Pakistan",
        "created_at": datetime.utcnow(),
    }
    users_col.insert_one(user_doc)

    return {"message": "Account created successfully", "email": data.email}


# 🆕 FIREBASE SIGNUP — naya endpoint (Firebase users ke liye)
@router.post("/firebase-signup")
def firebase_signup(data: FirebaseUserSignup):
    existing = users_col.find_one({"email": data.email})
    if existing:
        # User pehle se hai to bhi success bhejo (no error)
        return {
            "message": "User already exists",
            "email": data.email,
        }

    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": "FIREBASE_AUTH",  # placeholder, Firebase handles real password
        "phone": "",
        "language": "English",
        "country": "Pakistan",
        "created_at": datetime.utcnow(),
        "auth_provider": "firebase",
    }
    users_col.insert_one(user_doc)

    return {
        "message": "Firebase profile created successfully",
        "email": data.email,
    }


# 🔹 LOGIN (purana — abhi bhi rahega)
@router.post("/login")
def login(data: UserLogin):
    user = users_col.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "message": "Login successful",
        "user": {
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "phone": user.get("phone", ""),
            "language": user.get("language", "English"),
            "country": user.get("country", "Pakistan"),
        },
    }


# 🔹 GET PROFILE
@router.get("/profile/{email}")
def get_profile(email: str):
    user = users_col.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "language": user.get("language", "English"),
        "country": user.get("country", "Pakistan"),
    }


# 🔹 UPDATE PROFILE
@router.put("/profile/{email}")
def update_profile(email: str, data: UserProfileUpdate):
    user = users_col.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_fields = {}
    if data.name is not None:
        update_fields["name"] = data.name
    if data.phone is not None:
        update_fields["phone"] = data.phone
    if data.language is not None:
        update_fields["language"] = data.language
    if data.country is not None:
        update_fields["country"] = data.country

    if update_fields:
        users_col.update_one({"email": email}, {"$set": update_fields})

    return {"message": "Profile updated successfully"}


# 🔹 STATS — sabka total (shared)
@router.get("/stats/{email}")
def get_stats(email: str):
    translations_count = translations_col.count_documents({})
    voice_count = voice_translations_col.count_documents({})
    dictionary_count = dictionary_cache_col.count_documents({})
    favorites_count = favorites_col.count_documents({})

    total_translations = translations_count + voice_count

    langs = set()
    for doc in translations_col.find({}, {"target_lang": 1}):
        if doc.get("target_lang"):
            langs.add(doc["target_lang"])
    for doc in voice_translations_col.find({}, {"target_lang": 1}):
        if doc.get("target_lang"):
            langs.add(doc["target_lang"])

    return {
        "translations": total_translations,
        "languages": len(langs),
        "saved": favorites_count,
        "dictionary_searches": dictionary_count,
    }