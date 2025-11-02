from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import Base, engine
from . import models
from .routes import books
import os

app = FastAPI(title="Books API", version="1.0.0", redirect_slashes=True)

Base.metadata.create_all(bind=engine)

# CORS setup (update later to your Render URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "*",# for now allow all origins — you can restrict later
        "https://pdf-books-1.onrender.com/",  # ✅ replace with your frontend Render URL
        "http://localhost:5173",               # ✅ for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "dist"

os.makedirs(STATIC_DIR / "pages", exist_ok=True)

# Serve static files (for book pages)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routers
app.include_router(books.router)

# Serve built React frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/")
def root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Backend is running 🚀"}
    