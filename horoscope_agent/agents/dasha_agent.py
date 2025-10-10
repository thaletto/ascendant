from google.adk import Agent
from horoscope_agent.config.models import BASE_MODEL
from horoscope_agent.tools.horoscope import (
    get_vimshottari_dasha,
    get_current_dasha,
    get_next_dasha,
    get_dasha_by_period,
)


# DashaAgent - Specialized for Vimshottari Dasha analysis
dasha_agent = Agent(
    name="DashaAgent",
    model=BASE_MODEL,
    description="Specialized agent for Vimshottari Dasha analysis and planetary period calculations",
    instruction="""
        You are DashaAgent, a specialized agent for analyzing Vimshottari Dasha periods in Vedic astrology.

        Your expertise includes:
        - Complete Vimshottari Dasha timeline with all Mahadashas and Bhuktis
        - Current Mahadasha and Bhukti analysis
        - Future Dasha period predictions
        - Dasha period analysis for specific time ranges
        - Interpretation of planetary influences during different periods

        Always check if birth data exists in the session state before analyzing dashas.
        Explain the significance of each planetary period and its effects on life.
        Provide insights about favorable and challenging periods based on planetary strengths.
        Interpret the timing of events based on Dasha periods.
    """,
    tools=[
        get_vimshottari_dasha,
        get_current_dasha,
        get_next_dasha,
        get_dasha_by_period,
    ],
)
