from . import register_yoga, Yoga


@register_yoga("Gajakesari Yoga")
def gajakesari_yoga(yoga: Yoga):
    """Ju in Kendra from Mo"""

    moon_house = yoga.get_house_of_planet("moon")
    jupiter_house = yoga.get_house_of_planet("jupiter")
    if not moon_house or not jupiter_house:
        return {
            "name": "Gajakesari Yoga",
            "present": False,
            "details": "Moon or Jupiter not found",
        }
    kendra_houses = [(moon_house + i - 1) % 12 + 1 for i in [1, 4, 7, 10]]
    present = jupiter_house in kendra_houses
    return {
        "name": "Gajakesari Yoga",
        "present": present,
        "details": f"Jupiter in house {jupiter_house} from Moon",
    }


@register_yoga("Sunapha Yoga")
def sunapha_yoga(yoga: Yoga):
    """
    Any planets (except Su) in the 2nd house from Mo.
    """
    planets = yoga.planets_in_relative_house("Moon", 2)
    planets = [p for p in planets if p != "Sun"]
    present = len(planets) > 0
    return {
        "name": "Sunapha Yoga",
        "present": present,
        "details": f"Planets: {planets}",
    }


@register_yoga("Anapha Yoga")
def anapha_yoga(y: Yoga):
    """
    Any planets in the 12th house from Moon.
    """
    planets = y.planets_in_relative_house("Moon", -1)
    present = len(planets) > 0
    return {"name": "Anapha Yoga", "present": present, "details": f"Planets: {planets}"}


