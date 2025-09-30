import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATBASE_URL", "sqlite+aiosqlite:///./horoscope_ai.db")