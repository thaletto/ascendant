"""
Simple script to run the Horoscope AI Backend.
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        print("⚠️  Warning: OPENAI_API_KEY not set. Please set it in your environment or .env file")
        print("   You can get an API key from: https://platform.openai.com/api-keys")
        print("   The application will still start but horoscope generation will fail.")
        print()
    
    print("🚀 Starting Horoscope AI Backend...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔗 Interactive API explorer at: http://localhost:8000/redoc")
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
