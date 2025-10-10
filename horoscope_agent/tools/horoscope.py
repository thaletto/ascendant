from typing import Dict
from google.adk.tools import ToolContext
from vedicastro.VedicAstro import VedicHoroscopeData
from app.utils.chart import ChartGenerator
from app.utils.dasha import DashaFinder


class AstrologyObjects:
    def __init__(
        self,
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
    ):
        self.horoscope = VedicHoroscopeData(
            year=birth_year,
            month=birth_month,
            day=birth_day,
            hour=birth_hour,
            minute=birth_minute,
            second=birth_second,
            latitude=latitude,
            longitude=longitude,
            utc=utc,
            ayanamsa="Lahiri",
            house_system="Whole Sign",
        )
        self.chart = ChartGenerator(self.horoscope)
        self.dasha = DashaFinder(self.horoscope)


def _reconstruct_astrology_objects(birth_data: Dict):
    """Helper function to reconstruct astrology objects from birth data."""
    horoscope = VedicHoroscopeData(
        year=birth_data["birth_year"],
        month=birth_data["birth_month"],
        day=birth_data["birth_day"],
        hour=birth_data["birth_hour"],
        minute=birth_data["birth_minute"],
        second=birth_data["birth_second"],
        latitude=birth_data["latitude"],
        longitude=birth_data["longitude"],
        utc=birth_data["utc"],
        ayanamsa=birth_data["ayanamsa"],
        house_system=birth_data["house_system"],
    )
    chart = ChartGenerator(horoscope)
    dasha = DashaFinder(horoscope)
    return horoscope, chart, dasha


def get_chart(tool_context: ToolContext, division: str) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    _, chart, _ = _reconstruct_astrology_objects(birth_data)
    return {f"{division}_chart": chart.get_chart(division_name=division)}


def get_d1(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    _, chart, _ = _reconstruct_astrology_objects(birth_data)
    return {"D1_chart": chart.get_d1()}


def get_d7(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    _, chart, _ = _reconstruct_astrology_objects(birth_data)
    return {"D7_chart": chart.get_d7()}


def get_d9(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    _, chart, _ = _reconstruct_astrology_objects(birth_data)
    return {"D9_chart": chart.get_d9()}


def get_d10(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    _, chart, _ = _reconstruct_astrology_objects(birth_data)
    return {"D10_chart": chart.get_d10()}
