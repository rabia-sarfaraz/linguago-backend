from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============ EXISTING MODELS (user_email added) ============
class Translation(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    translated_text: str
    user_email: Optional[str] = None  # 🆕 kis user ki translation
    timestamp: Optional[datetime] = None


class VoiceTranslation(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    translated_text: str
    voice_url: Optional[str] = None
    user_email: Optional[str] = None  # 🆕
    timestamp: Optional[datetime] = None


class DictionaryEntry(BaseModel):
    word: str
    definition: str
    examples: Optional[List[str]] = []
    pronunciation: Optional[str] = None
    user_email: Optional[str] = None  # 🆕
    timestamp: Optional[datetime] = None


class ChatMessage(BaseModel):
    prompt: str
    target_lang: str
    user_email: Optional[str] = None  # 🆕


# ============ 🆕 NEW USER MODELS ============
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None


# ============ 🆕 FAVORITES MODEL ============
class FavoriteItem(BaseModel):
    user_email: str
    item_type: str          # "translation" ya "dictionary"
    original_text: str
    result_text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    timestamp: Optional[datetime] = None