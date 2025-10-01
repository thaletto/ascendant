from google.adk import Agent

from horoscope_agent.config.models import BASE_MODEL
from horoscope_agent.tools.horoscope import AstrologyAgentTools

astrology_agent_tools = AstrologyAgentTools()

horoscope_agent = Agent(
    name="HoroscopeAgent",
    model=BASE_MODEL,
    description="An agent that provides personalised horoscope predictions",
    instruction="""Greet the user first, If the user asks about astrology prediction ask for the user's name, birth date, and birth place, then use the tools to generate the subject and print the horoscope report.""",
    tools=[
        astrology_agent_tools.generate_report,
    ],
)

root_agent = horoscope_agent
