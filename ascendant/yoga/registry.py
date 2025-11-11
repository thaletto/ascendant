from . import register_yoga, Yoga
from ascendant import BENEFIC_PLANETS


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
    Any planets (except Su) in the 2nd house from Mo
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
def anapha_yoga(yoga: Yoga):
    """
    Any planets in the 12th house from Moon
    """
    planets = yoga.planets_in_relative_house("Moon", -1)
    present = len(planets) > 0
    return {"name": "Anapha Yoga", "present": present, "details": f"Planets: {planets}"}


@register_yoga("Dhurdhua Yoga")
def dhurdhua_yoga(yoga: Yoga):
    """
    Any planets on either side of the Mo
    """
    planets = yoga.planets_in_relative_house(
        "Moon", -1
    ) + yoga.planets_in_relative_house("Moon", 2)
    present = len(planets) > 0
    return {
        "name": "Dhurdhura Yoga",
        "present": present,
        "details": f"Planets: {planets}",
    }


@register_yoga("Kemadurga Yoga")
def kemadurga_yoga(yoga: Yoga):
    """
    No planets on both side of the Mo
    """
    planets = yoga.planets_in_relative_house(
        "Moon", -1
    ) + yoga.planets_in_relative_house("Moon", 2)
    present = len(planets) == 0
    return {
        "name": "Kemadurga Yoga",
        "present": present,
        "details": f"Planets: {planets}",
    }


@register_yoga("Chandra Mangala Yoga")
def chandra_mangala_yoga(yoga: Yoga):
    """
    Ma cojoins Mo
    """
    mars_house = yoga.get_house_of_planet("Mars")
    moon_house = yoga.get_house_of_planet("Moon")
    present = mars_house == moon_house
    return {
        "name": "Chandra Managala Yoga",
        "present": present,
        "details": f"Mars in {mars_house}, Moon in {moon_house}",
    }


@register_yoga("Chandra Adhi Yoga")
def chandra_adhi_yoga(yoga: Yoga):
    """
    Benefics in sixth, seventh and eight houses from the Mo
    """
    planets = (
        yoga.planets_in_relative_house("Moon", 6)
        + yoga.planets_in_relative_house("Moon", 7)
        + yoga.planets_in_relative_house("Moon", 8)
    )
    present = all(planet in planets for planet in BENEFIC_PLANETS)
    details = (
        f"Benefic planets influencing the Moon are: {', '.join(BENEFIC_PLANETS)}."
        if present
        else "No benefic planets in 6th, 7th, or 8th houses from the Moon."
    )
    return {
        "name": "Chandra Adhi Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Lagna Adhi Yoga")
def lagna_adhi_yoga(yoga: Yoga):
    """
    Benefics in sixth, seventh and eight houses from the Asc
    """
    planets = (
        yoga.planets_in_relative_house("Lagna", 6)
        + yoga.planets_in_relative_house("Lagna", 7)
        + yoga.planets_in_relative_house("Lagna", 8)
    )
    present = all(planet in planets for planet in BENEFIC_PLANETS)
    details = (
        f"Benefic planets influencing the Lagna are: {', '.join(BENEFIC_PLANETS)}."
        if present
        else "No benefic planets in 6th, 7th, or 8th houses from the Lagna."
    )
    return {
        "name": "Lagna Adhi Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Chatussagara Yoga")
def chatussagara_yoga(yoga: Yoga):
    """
    All kendras (1st, 4th, 7th, 10th houses) are occupied by planets.
    """

    house_1 = yoga.planets_in_relative_house("Lagna", 1)
    house_4 = yoga.planets_in_relative_house("Lagna", 4)
    house_7 = yoga.planets_in_relative_house("Lagna", 7)
    house_10 = yoga.planets_in_relative_house("Lagna", 10)

    present = all([house_1, house_4, house_7, house_10])

    details = (
        f"Planets found — 1st: {', '.join(house_1) or 'None'}, "
        f"4th: {', '.join(house_4) or 'None'}, "
        f"7th: {', '.join(house_7) or 'None'}, "
        f"10th: {', '.join(house_10) or 'None'}."
    )

    return {
        "name": "Chatussagara Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Vasumathi Yoga")
def vasumathi_yoga(yoga: Yoga):
    """
    Benefic planets occupy the upachaya houses (3, 6, 10, or 11)
    either from the Ascendant or from the Moon.
    """

    # From Moon
    moon_upachayas = (
        yoga.planets_in_relative_house("Moon", 3)
        + yoga.planets_in_relative_house("Moon", 6)
        + yoga.planets_in_relative_house("Moon", 10)
        + yoga.planets_in_relative_house("Moon", 11)
    )

    # From Ascendant
    lagna_upachayas = (
        yoga.planets_in_relative_house("Lagna", 3)
        + yoga.planets_in_relative_house("Lagna", 6)
        + yoga.planets_in_relative_house("Lagna", 10)
        + yoga.planets_in_relative_house("Lagna", 11)
    )

    # Benefic planets in either reference
    benefics_moon = [p for p in BENEFIC_PLANETS if p in moon_upachayas]
    benefics_lagna = [p for p in BENEFIC_PLANETS if p in lagna_upachayas]

    present = bool(benefics_moon or benefics_lagna)

    if present:
        details = []
        if benefics_moon:
            details.append(f"From Moon: {', '.join(benefics_moon)} in upachayas.")
        if benefics_lagna:
            details.append(f"From Ascendant: {', '.join(benefics_lagna)} in upachayas.")
        details = " ".join(details)
    else:
        details = (
            "No benefic planets occupy upachaya houses from either Moon or Ascendant."
        )

    return {
        "name": "Vasumathi Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Rajalakshana Yoga")
def rajalakshana_yoga(yoga: Yoga):
    """
    Jupiter, Venus, Mercury, and Moon should be in Ascendant or in any Kendra (1, 4, 7, 10).
    """

    required_planets = ["Jupiter", "Venus", "Mercury", "Moon"]
    kendras = [1, 4, 7, 10]

    # Collect all planets in kendras
    planets_in_kendras = []
    for house in kendras:
        planets_in_kendras += yoga.planets_in_relative_house("Lagna", house)

    present = all(p in planets_in_kendras for p in required_planets)

    details = (
        f"Planets in Kendras: {', '.join(planets_in_kendras)}."
        if planets_in_kendras
        else "No planets found in kendras."
    )

    return {
        "name": "Rajalakshana Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Sakata Yoga")
def sakata_yoga(yoga: Yoga):
    """
    Mo is in 6th, 8th, or 12th house from Ju.
    """

    relative_house = yoga.relative_house("Jupiter", "Moon")
    present = relative_house in [6, 8, 12]

    details = (
        f"Moon is {relative_house} houses away from Jupiter."
        if relative_house
        else "Unable to determine relative house between Moon and Jupiter."
    )

    return {
        "name": "Sakata Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Amala Yoga")
def amala_yoga(yoga: Yoga):
    """
    10th house from Mo or Asc occupied by any benefic planet.
    """

    from_moon = yoga.planets_in_relative_house("Moon", 10)
    from_lagna = yoga.planets_in_relative_house("Lagna", 10)

    benefics_moon = [p for p in BENEFIC_PLANETS if p in from_moon]
    benefics_lagna = [p for p in BENEFIC_PLANETS if p in from_lagna]

    present = bool(benefics_moon or benefics_lagna)

    if present:
        details = []
        if benefics_moon:
            details.append(f"From Moon: {', '.join(benefics_moon)} in 10th.")
        if benefics_lagna:
            details.append(f"From Ascendant: {', '.join(benefics_lagna)} in 10th.")
        details = " ".join(details)
    else:
        details = "No benefic planets occupy the 10th house from Moon or Ascendant."

    return {
        "name": "Amala Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Parvata Yoga")
def parvata_yoga(yoga: Yoga):
    """
    6th and 8th houses should be either unoccupied or occupied only by benefic planets.
    """

    house_6 = yoga.planets_in_relative_house("Lagna", 6)
    house_8 = yoga.planets_in_relative_house("Lagna", 8)

    def is_benefic_or_empty(planets):
        return not planets or all(p in BENEFIC_PLANETS for p in planets)

    house_6_ok = is_benefic_or_empty(house_6)
    house_8_ok = is_benefic_or_empty(house_8)

    present = house_6_ok and house_8_ok

    details = (
        f"6th house: {', '.join(house_6) or 'Empty'}; "
        f"8th house: {', '.join(house_8) or 'Empty'}."
    )

    return {
        "name": "Parvata Yoga",
        "present": present,
        "details": details,
    }