from google.adk import Agent

from app.agents.config.models import BASE_MODEL

horoscope_agent = Agent(
    name="Horoscope Agent",
    model=BASE_MODEL,
    description="An agent that provides personalised horoscope predictions",
)
