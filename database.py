from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database()

# Existing collections
translations_col = db["translations"]
voice_translations_col = db["voice_translations"]
dictionary_cache_col = db["dictionary_cache"]
chat_history_col = db["chat_history"]

# 🆕 New collections
users_col = db["users"]          # user accounts
favorites_col = db["favorites"]  # saved/favorite items

# 🆕 Create unique index on email (taake duplicate accounts na banein)
try:
    users_col.create_index("email", unique=True)
except Exception as e:
    print(f"Index creation note: {e}")