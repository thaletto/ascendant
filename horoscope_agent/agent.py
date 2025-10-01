from google.adk import Agent

from horoscope_agent.config.models import BASE_MODEL

horoscope_agent = Agent(
    name="Horoscope Agent",
    model=BASE_MODEL,
    description="An agent that provides personalised horoscope predictions",
)

root_agent = horoscope_agent