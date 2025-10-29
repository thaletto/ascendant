from typing import Dict
from google.adk import Agent
from google.adk.tools import ToolContext
from agent.config import BASE_MODEL
from agent.agents import chart_agent
from agent.agents import dasha_agent
from agent.agents import planet_agent


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
    utc: str,
) -> Dict:
    """Create and store birth data for astrology analysis."""
    # Store only the essential birth data that can be serialized
    birth_data = {
        "name": name,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "birth_day": birth_day,
        "birth_hour": birth_hour,
        "birth_minute": birth_minute,
        "birth_second": birth_second,
        "latitude": latitude,
        "longitude": longitude,
        "utc": utc,
        "ayanamsa": "Lahiri",
        "house_system": "Whole Sign",
    }

    tool_context.state["birth_data"] = birth_data
    return {
        "message": "Birth data has been stored and is ready for astrology analysis",
        "birth_data": birth_data,
    }


# Root Agent - General Reasoning & Context Manager
root_agent = Agent(
    name="AscendantRootAgent",
    model=BASE_MODEL,
    description="Root agent for the Ascendant astrology intelligence system - coordinates specialized agents for comprehensive astrological analysis",
    instruction="""
        You are the Ascendant Root Agent, the main coordinator of a modular astrology intelligence system.

        Your role is to:
        1. **Context Management**: Ensure birth data is available before delegating to specialists
        2. **Agent Coordination**: Route requests to the appropriate specialized agents
        3. **Synthesis**: Combine insights from multiple agents for comprehensive analysis
        4. **User Experience**: Provide clear, coherent responses that integrate multiple perspectives

        **Available Specialized Agents:**
        - **ChartAgent**: Handles divisional charts (D1, D7, D9, D10, etc.)
        - **DashaAgent**: Manages Vimshottari Dasha analysis and planetary periods
        - **PlanetAgent**: Analyzes planetary positions, aspects, and relationships

        **Workflow:**
        1. Always start by greeting the user warmly
        2. Check if birth data exists in session state
        3. If not, invoke create_astrology_subject to collect birth details
        4. Once data is available, route requests to appropriate specialized agents
        5. Synthesize results from multiple agents when needed
        6. Provide comprehensive, easy-to-understand explanations

        **Specialization Areas:**
        - **Chart Requests**: Delegate to ChartAgent for D1, D7, D9, D10 charts
        - **Dasha Analysis**: Delegate to DashaAgent for planetary periods
        - **Planet Analysis**: Delegate to PlanetAgent for positions and aspects
        - **Comprehensive Analysis**: Coordinate multiple agents for holistic insights

        Always explain what you're doing and provide clear, actionable insights.
        Integrate information from multiple agents to give complete astrological perspectives.
    """,
    tools=[create_astrology_subject],
    sub_agents=[
        chart_agent,
        dasha_agent,
        planet_agent,
    ],
)
