from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import Base, engine
from . import models
from .routes import books
import os

# --- Initialize app ---
app = FastAPI(title="Books API", version="1.0.0")

# --- Create database tables ---
Base.metadata.create_all(bind=engine)

# --- CORS setup (important for Render + React) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with your frontend Render URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define paths ---
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "dist"

# Ensure folders exist
os.makedirs(STATIC_DIR / "pages", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Mount static files ---
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# --- Include routers ---
app.include_router(books.router)

# --- Serve built React frontend (Render + local) ---
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# --- Root endpoint ---
@app.get("/")
def root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Backend is running 🚀"}
