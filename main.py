"""
Main FastAPI application for Horoscope AI Backend.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db import init_db
from models import StatusResponse
from routes import users, predictions, chat

# Set up environment variables
os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key-here")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting Horoscope AI Backend...")
    await init_db()
    print("✅ Database initialized successfully")
    yield
    # Shutdown
    print("🛑 Shutting down Horoscope AI Backend...")

# Create FastAPI application
app = FastAPI(
    title="Horoscope AI Backend",
    description="A prototype backend for AI-powered horoscope predictions and chat",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(chat.router)

@app.get("/", response_model=StatusResponse)
async def root():
    """
    Root endpoint to check if the API is running.
    
    Returns:
        Status message indicating the API is running
    """
    return StatusResponse(status="Horoscope AI Backend running 🚀")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        Health status of the API
    """
    return {
        "status": "healthy",
        "message": "All systems operational",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
