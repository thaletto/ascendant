"""
Main FastAPI application for Ascendant - AI Astrology Intelligence System.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import users, prediction
from app.db.client import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting Ascendant - AI Astrology Intelligence System...")
    await init_db()
    print("✅ Database initialized successfully")
    print("🔮 Ascendant astrology agents ready")
    yield
    # Shutdown
    print("🛑 Shutting down Ascendant...")


# Create FastAPI application
app = FastAPI(
    title="Ascendant - AI Astrology Intelligence System",
    description="A modular, multi-astrology intelligence system for advanced astrological analysis, chart synthesis, and contextual reasoning",
    version="1.0.0",
    lifespan=lifespan,
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
app.include_router(prediction.router)


@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.

    Returns:
        Status message indicating the API is running
    """
    return {"status": "Ascendant - AI Astrology Intelligence System running 🔮"}


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
        "version": "1.0.0",
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
            "detail": str(exc)
            if os.getenv("DEBUG", "false").lower() == "true"
            else None,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True, log_level="info")
