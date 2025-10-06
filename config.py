import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DATABASE_URL = os.getenv("DATBASE_URL", "sqlite+aiosqlite:///./horoscope_ai.db")
BASE_MODEL_ID = os.getenv("BASE_MODEL_ID")