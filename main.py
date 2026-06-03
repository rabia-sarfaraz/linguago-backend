from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import translation, voice_translation, dictionary, chat, user, favorites

app = FastAPI(title="Language Translator Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(translation.router, prefix="/translation", tags=["Translation"])
app.include_router(voice_translation.router, prefix="/voice", tags=["Voice Translation"])
app.include_router(dictionary.router, prefix="/dictionary", tags=["Dictionary"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(user.router, prefix="/user", tags=["User"])           # 🆕
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])  # 🆕


@app.get("/")
def root():
    return {"message": "Backend running successfully 🚀"}