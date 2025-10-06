from google.adk import Agent
from config import BASE_MODEL
from horoscope_agent.tools.horoscope import AstrologyAgentTools

astrology_agent_tools = AstrologyAgentTools()

horoscope_agent = Agent(
    name="HoroscopeAgent",
    model=BASE_MODEL,
    description="An agent that provides personalised horoscope predictions and divisional charts.",
    instruction="""Greet the user first.
        Ask for their name, date of birth, time of birth, and city of birth.
        Use your internal knowledge to determine that city's latitude, longitude, and UTC offset.
        Then decide which divisional chart (D1, D7, D9, D10, etc.) to generate based on the user's intent.
        If intent is not given use D1 chart to provide basic prediction about his health, wealth, career, family, partner and longetivity.
        """,
    tools=[
        astrology_agent_tools.get_chart,
        astrology_agent_tools.get_d1,
        astrology_agent_tools.get_d7,
        astrology_agent_tools.get_d9,
        astrology_agent_tools.get_d10,
    ],
)

root_agent = horoscope_agent