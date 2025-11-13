from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.routers import articles, news
from backend.database import engine, Base, DB_AVAILABLE

# Import models to register them with Base
from backend import models

# Create database tables (only if database is available)
if DB_AVAILABLE and engine:
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified automatically")
    except Exception as e:
        print(f"⚠️  Warning: Could not create database tables: {e}")
else:
    print("⚠️  Database not available - tables will not be created")

app = FastAPI(
    title="AI News Agency API",
    description="AI-powered news agency with semantic search capabilities",
    version="1.0.0"
)

# CORS configuration - MUST be before routes
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(articles.router, prefix="/api", tags=["articles"])
app.include_router(news.router, prefix="/api", tags=["news"])

@app.get("/")
async def root():
    return {"message": "AI News Agency API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

