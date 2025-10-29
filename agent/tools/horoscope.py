from typing import Dict, List
from google.adk.tools import ToolContext
from vedicastro.VedicAstro import VedicHoroscopeData
from ascendant.chart import Chart
from ascendant.dasha import DashaFinder
from app.utils.planets import PlanetaryAspects


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
        self.chart = Chart(self.horoscope)
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
    chart = Chart(horoscope)
    dasha = DashaFinder(horoscope)
    return horoscope, chart, dasha


def _cleanup_astrology_objects(horoscope, chart, dasha):
    """Helper function to clean up astrology objects and free memory."""
    try:
        # Clear references to help garbage collection
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        if hasattr(chart, "chart"):
            chart.chart = None
        if hasattr(chart, "planets"):
            chart.planets = None
        if hasattr(dasha, "chart"):
            dasha.chart = None
        # Force garbage collection of these objects
        del horoscope, chart, dasha
    except Exception:
        # Ignore cleanup errors to avoid affecting the main functionality
        pass


def get_chart(tool_context: ToolContext, division: str) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {f"{division}_chart": chart.get_chart(division_name=division)}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_d1(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"D1_chart": chart.get_d1()}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_d7(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"D7_chart": chart.get_d7()}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_d9(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"D9_chart": chart.get_d9()}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_d10(tool_context: ToolContext) -> Dict:
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"D10_chart": chart.get_d10()}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


# Dasha Tools
def get_vimshottari_dasha(tool_context: ToolContext) -> Dict:
    """Get complete Vimshottari Dasha timeline."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"vimshottari_dasha": dasha.get_vimshottari_dasha()}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_current_dasha(tool_context: ToolContext) -> Dict:
    """Get current Mahadasha and Bhukti."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"current_dasha": dasha.get_bhuthi_by_index(-1)}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_next_dasha(tool_context: ToolContext) -> Dict:
    """Get next Mahadasha and Bhukti."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        result = {"next_dasha": dasha.get_bhuthi_by_index(1)}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


def get_dasha_by_period(
    tool_context: ToolContext, start_date: str, end_date: str
) -> Dict:
    """Get Dasha periods for a specific time range."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

    horoscope, chart, dasha = _reconstruct_astrology_objects(birth_data)
    try:
        # This would need to be implemented in DashaFinder
        # For now, return a placeholder
        result = {"dasha_period": f"Dasha periods from {start_date} to {end_date}"}
        return result
    finally:
        _cleanup_astrology_objects(horoscope, chart, dasha)


# Planet Tools
def get_all_planetary_aspects(tool_context: ToolContext) -> Dict:
    """Get all planetary aspects in the chart."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

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
    aspects = PlanetaryAspects(horoscope)
    try:
        result = {"planetary_aspects": aspects.get_aspects_table()}
        return result
    finally:
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        if hasattr(aspects, "_aspects"):
            aspects._aspects = None
        del horoscope, aspects


def get_planetary_aspects_by_planets(
    tool_context: ToolContext, planets: List[str]
) -> Dict:
    """Get aspects for specific planets."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

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
    aspects = PlanetaryAspects(horoscope)
    try:
        result = {"filtered_aspects": aspects.filter_by_planets(planets)}
        return result
    finally:
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        if hasattr(aspects, "_aspects"):
            aspects._aspects = None
        del horoscope, aspects


def get_planetary_aspects_by_type(
    tool_context: ToolContext, aspect_types: List[str]
) -> Dict:
    """Get aspects of specific types (conjunction, opposition, trine, etc.)."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

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
    aspects = PlanetaryAspects(horoscope)
    try:
        result = {"aspects_by_type": aspects.filter_by_aspect_type(aspect_types)}
        return result
    finally:
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        if hasattr(aspects, "_aspects"):
            aspects._aspects = None
        del horoscope, aspects


def get_planet_positions(tool_context: ToolContext) -> Dict:
    """Get current positions of all planets."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

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
    try:
        chart = horoscope.generate_chart()
        positions = []
        for planet in chart.objects:
            positions.append(
                {
                    "planet": planet.id,
                    "longitude": planet.lon,
                    "sign": chart.getSign(planet.lon),
                    "house": chart.getHouse(planet.lon),
                    "is_retrograde": planet.isRetrograde(),
                }
            )
        result = {"planet_positions": positions}
        return result
    finally:
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        del horoscope


def get_planet_strength(tool_context: ToolContext, planet_name: str) -> Dict:
    """Get the strength and condition of a specific planet."""
    birth_data = tool_context.state.get("birth_data")
    if not birth_data:
        return {"message": "birth data is not in context, call handle_user_input first"}

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
    try:
        chart = horoscope.generate_chart()
        # Find the planet
        planet_obj = None
        for planet in chart.objects:
            if planet.id.lower() == planet_name.lower():
                planet_obj = planet
                break

        if not planet_obj:
            return {"error": f"Planet {planet_name} not found in chart"}

        # Get planet details
        planet_data = {
            "planet": planet_obj.id,
            "longitude": planet_obj.lon,
            "sign": chart.getSign(planet_obj.lon),
            "house": chart.getHouse(planet_obj.lon),
            "is_retrograde": planet_obj.isRetrograde(),
            "strength": "Normal",  # This would need more sophisticated calculation
        }

        result = {"planet_analysis": planet_data}
        return result
    finally:
        if hasattr(horoscope, "chart"):
            horoscope.chart = None
        del horoscope
