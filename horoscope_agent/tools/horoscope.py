from typing import Dict
from kerykeion import AstrologicalSubject, Report

# ------------------------------
# Horoscope Agent Tool
# ------------------------------
class AstrologyAgentTools:
    """
    AstrologyAgentTools provides tools for generating horoscope reports 
    in the Horoscope AI agent using primitive input types for ADK compatibility.

    This class is designed to work with Google ADK automatic function calling. 
    It avoids complex object inputs and only accepts strings, integers, and floats.

    Usage:
        tools = AstrologyAgentTools()
        report = tools.generate_report(
            name="Laxman",
            year=2003,
            month=8,
            day=19,
            hour=11,
            minute=55,
            tz_str="Asia/Kolkata",
            city="Chennai",
            lat=13.0827,
            lng=80.2707
        )
    """

    @staticmethod
    def generate_report(
        name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        tz_str: str,
        city: str,
        lat: float,
        lng: float
    ) -> Dict:
        """
        Generates a horoscope report for a person using Kerykeion.

        The function creates an AstrologicalSubject object from the provided
        primitive inputs, generates a horoscope Report, and serializes it as a dictionary
        suitable for use with Google ADK.

        Parameters:
            name (str): Name of the person.
            year (int): Birth year.
            month (int): Birth month (1-12).
            day (int): Birth day (1-31).
            hour (int): Birth hour in 24-hour format.
            minute (int): Birth minute.
            tz_str (str): Timezone string (e.g., "Asia/Kolkata").
            city (str): Birth city.
            lat (float): Latitude of the city.
            lng (float): Longitude of the city.

        Returns:
            Dict: Serialized horoscope report suitable for ADK consumption.
        """
        # create subject
        subject = AstrologicalSubject(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            city=city,
            nation="IN",
            lat=lat,
            lng=lng,
            tz_str=tz_str,
            online=False,
            houses_system_identifier="W",
            zodiac_type="Sidereal",
            sidereal_mode="LAHIRI",
        )

        # generate report
        report = Report(subject)

        # serialize as dict for ADK
        return report.to_dict()
