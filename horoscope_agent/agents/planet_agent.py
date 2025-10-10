from google.adk import Agent
from horoscope_agent.config.models import BASE_MODEL
from horoscope_agent.tools.horoscope import (
    get_all_planetary_aspects,
    get_planetary_aspects_by_planets,
    get_planetary_aspects_by_type,
    get_planet_positions,
    get_planet_strength,
)


# PlanetAgent - Specialized for planetary positions and relationships
planet_agent = Agent(
    name="PlanetAgent",
    model=BASE_MODEL,
    description="Specialized agent for planetary positions, aspects, and relationships analysis",
    instruction="""
        You are PlanetAgent, a specialized agent for analyzing planetary positions, aspects, and relationships in Vedic astrology.

        Your expertise includes:
        - Planetary positions in signs and houses
        - Planetary aspects (conjunction, opposition, trine, square, sextile)
        - Planet strengths and conditions
        - Retrograde planet analysis
        - Planetary relationships and their effects
        - Individual planet analysis and interpretation

        Always check if birth data exists in the session state before analyzing planets.
        Explain the significance of planetary positions and their effects on personality and life events.
        Provide insights about planetary strengths, weaknesses, and remedies.
        Interpret planetary aspects and their influence on various life areas.
    """,
    tools=[
        get_all_planetary_aspects,
        get_planetary_aspects_by_planets,
        get_planetary_aspects_by_type,
        get_planet_positions,
        get_planet_strength,
    ],
)
