from datetime import datetime
from kerykeion import AstrologicalSubject, Report


# --- ADK Agent Tool Interface ---
class AstrologyAgentTools:
    """
    Tools class designed for Google ADK agents.
    Methods here can be invoked remotely by an agent.
    Uses Kerykeion's AstrologicalSubject and Report classes.
    """

    @staticmethod
    def generate_subject(
        name: str, birth_date: datetime, city: str, lat: float, lng: float
    ) -> AstrologicalSubject:
        """
        Creates a Kerykeion AstrologicalSubject object from user input.

        Args:
            name (str): Name of the person.
            birth_date (datetime): Birth date and time with timezone info. eg: datetime(2003, 8, 19, 11, 55, tzinfo=ZoneInfo("Asia/Kolkata"))
            city (str): Birth city.
            lat (float): Latitude of the city.
            lng (float): Longitude of the city.

        Returns:
            dict: Serialized AstrologicalSubject attributes suitable for ADK consumption.
        """
        subject = AstrologicalSubject(
            name=name,
            year=birth_date.year,
            month=birth_date.month,
            day=birth_date.day,
            hour=birth_date.hour,
            minute=birth_date.minute,
            city=city,
            nation="IN",
            lat=lat,
            lng=lng,
            tz_str=birth_date.tzinfo.key,
            online=False,
            houses_system_identifier="W",  # Whole sign
            zodiac_type="Sidereal",
            sidereal_mode="LAHIRI",
        )
        # Serialize subject for ADK
        return subject

    @staticmethod
    def generate_report(subject: AstrologicalSubject) -> dict:
        """
        Generates a Kerykeion report object for a given subject.

        Args:
            subject (AstrologicalSubject): The subject for whom the report is generated.

        Returns:
            dict: Serialized report data suitable for ADK consumption.
        """
        report = Report(subject)
        return report.to_dict() if hasattr(report, "to_dict") else report.__dict__

    @staticmethod
    def print_subject_report(subject: AstrologicalSubject) -> dict:
        """
        Generates and prints a report for a subject.
        Returns the report as a dictionary for ADK agents.

        Args:
            subject (AstrologicalSubject): The subject for whom the report is generated.

        Returns:
            dict: Serialized report data.
        """
        report = Report(subject)
        report.print_report()
        return report.to_dict() if hasattr(report, "to_dict") else report.__dict__
