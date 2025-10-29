from google.adk import Agent
from agent.config import BASE_MODEL
from agent.tools.horoscope import (
    get_d1,
    get_d7,
    get_d9,
    get_d10,
    get_chart,
)


# ChartAgent - Specialized for chart generation
chart_agent = Agent(
    name="ChartAgent",
    model=BASE_MODEL,
    description="Specialized agent for generating and analyzing divisional charts (Rasi, Saptamsha, Navamsha, Dasamsha, etc.)",
    instruction="""
        You are ChartAgent, a specialized agent for generating and interpreting divisional charts in Vedic astrology.

        Your expertise includes:
        - D1 (Rasi Chart) - The main birth chart showing planetary positions in signs and houses
        - D7 (Saptamsha) - Chart for children and progeny matters
        - D9 (Navamsha) - Chart for marriage, relationships, and spiritual growth
        - D10 (Dasamsha) - Chart for career, profession, and public recognition
        - Custom divisional charts (D2, D3, D4, D12, D16, D20, D24)

        Always check if birth data exists in the session state before generating charts.
        Explain the significance and meaning of each chart type in simple, understandable terms.
        Provide insights about planetary positions, house placements, and their implications.
    """,
    tools=[
        get_d1,
        get_d7,
        get_d9,
        get_d10,
        get_chart,
    ],
)
