from typing import Dict
from google.adk import Agent
from google.adk.tools import ToolContext
from horoscope_agent.config.models import BASE_MODEL
from horoscope_agent.tools.horoscope import AstrologyObjects, get_chart, get_d1, get_d10, get_d7, get_d9

def create_astrology_subject(
    tool_context: ToolContext,
    name: str,
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    birth_second: int,
    latitude: float,
    longitude: float,
    utc: str
    ) -> Dict:
    astrologyObjects = AstrologyObjects(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_second, latitude, longitude, utc)
    tool_context.state["horoscope"] = astrologyObjects.horoscope
    tool_context.state["chart"] = astrologyObjects.chart
    tool_context.state["dasha"] = astrologyObjects.dasha
    return {"message": "states `horoscope`, `chart`, `dasha` have been initialized in context"}


handle_user_input = Agent(
    name="HandleUserInput",
    model=BASE_MODEL,
    description="Collects and prepares the user's birth details for horoscope computation.",
    instruction="""
        Politely ask the user for their:
        - full name
        - date of birth (DD-MM-YYYY)
        - time of birth (24-hour format)
        - city of birth

        Once all are provided, resolve that city to latitude, longitude, and UTC offset
        (use your internal knowledge or geolocation database).

        Then create and store the required horoscope-related objects (VedicHoroscopeData, ChartGenerator, etc.)
        by calling the `create_astrology_subject` tool. 

        Do not perform any predictions or chart generation here — only gather and initialize data.
    """,
    tools=[
        create_astrology_subject
    ]
)


horoscope_agent = Agent(
    name="HoroscopeAgent",
    model=BASE_MODEL,
    description="An agent that provides personalised horoscope predictions and divisional charts.",
    instruction="""
        You are HoroscopeAgent, responsible for generating and explaining divisional charts like D1, D7, D9, and D10.

        Always start by greeting the user warmly.

        Then, before calling any chart-related tool (`get_chart`, `get_d1`, `get_d7`, `get_d9`, or `get_d10`):
        1. Check if user details and horoscope objects exist in the session state (e.g., under 'horoscope', 'chart', or 'dasha').
        2. If not present, invoke the `HandleUserInput` sub agent 
           to collect missing information and initialize those objects.
        3. Once data is available, call the appropriate chart tool based on user's request.

        Always tell the user what you're doing (for example: “Let me fetch your birth data first…” or “Now generating your D9 chart…”).
        Then summarize and explain the chart result clearly in simple terms.
    """,
    tools=[
        get_chart,
        get_d1,
        get_d7,
        get_d9,
        get_d10,
    ],
    sub_agents=[handle_user_input]
)

root_agent = horoscope_agent