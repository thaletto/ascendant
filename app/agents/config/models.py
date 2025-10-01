from google.adk.models.lite_llm import LiteLlm

from app.config import BASE_MODEL

BASE_MODEL = LiteLlm(model=BASE_MODEL)