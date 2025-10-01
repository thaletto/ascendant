from google.adk.models.lite_llm import LiteLlm

from config import BASE_MODEL, OPENROUTER_API_KEY

BASE_MODEL = LiteLlm(
    model=BASE_MODEL,
    api_key=OPENROUTER_API_KEY
)