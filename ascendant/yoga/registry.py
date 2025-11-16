from ascendant.types import PlanetsType
from ascendant.yoga import register_yoga, Yoga
from ascendant.const import BENEFIC_PLANETS


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
    planets = [p for p in planets if p["name"] != "Sun"]
    present = len(planets) > 0
    return {
        "name": "Sunapha Yoga",
        "present": present,
        "details": f"Planets: {planets}",
    }


@register_yoga("Anapha Yoga")
def anapha_yoga(yoga: Yoga):
    """
    Any planets in the 12th house from Mo
    """
    planets = yoga.planets_in_relative_house("Moon", -1)
    present = len(planets) > 0
    return {"name": "Anapha Yoga", "present": present, "details": f"Planets: {planets}"}


@register_yoga("Dhurdhua Yoga")
def dhurdhua_yoga(yoga: Yoga):
    """
    Any planets on either side of the Mo
    """
    p12 = yoga.planets_in_relative_house("Moon", -1)
    p2 = yoga.planets_in_relative_house("Moon", 2)
    if len(p12) > 0 or len(p2) > 0:
        present = True
    else:
        present = False
    planets = [p["name"] for p in p12] + [p["name"] for p in p2]
    return {
        "name": "Dhurdhua Yoga",
        "present": present,
        "details": f"Planets: {planets}",
    }


@register_yoga("Kemadurga Yoga")
def kemadurga_yoga(yoga: Yoga):
    """
    No planets on both side of the Mo
    """
    p12 = yoga.planets_in_relative_house("Moon", -1)
    p2 = yoga.planets_in_relative_house("Moon", 2)
    if len(p12) == 0 and len(p2) == 0:
        present = True
    else:
        present = False
    planets = [p["name"] for p in p12] + [p["name"] for p in p2]
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
        "name": "Chandra Mangala Yoga",
        "present": present,
        "details": f"Mars in {mars_house}, Moon in {moon_house}",
    }


@register_yoga("Chandra Adhi Yoga")
def chandra_adhi_yoga(yoga: Yoga):
    """
    Benefics in sixth, seventh and eight houses from the Moon.
    """
    planets: PlanetsType = (
        yoga.planets_in_relative_house("Moon", 6)
        + yoga.planets_in_relative_house("Moon", 7)
        + yoga.planets_in_relative_house("Moon", 8)
    )

    present = all(p["name"] in BENEFIC_PLANETS for p in planets)

    if present:
        benefics = ", ".join(p["name"] for p in planets)
        details = f"Benefic planets placed in the 6th, 7th and 8th houses from the Moon: {benefics}."
    else:
        non_benefics = ", ".join(
            p["name"] for p in planets if p["name"] not in BENEFIC_PLANETS
        )
        details = (
            f"Non-benefic planets found in the 6th, 7th or 8th houses from the Moon: {non_benefics}."
            if non_benefics
            else "No benefic influence on the Moon from the 6th, 7th or 8th houses."
        )

    return {
        "name": "Chandra Adhi Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Lagna Adhi Yoga")
def lagna_adhi_yoga(yoga: Yoga):
    """
    Benefics in the 6th, 7th and 8th houses from the Ascendant.
    """
    planets = (
        yoga.planets_in_relative_house("Lagna", 6)
        + yoga.planets_in_relative_house("Lagna", 7)
        + yoga.planets_in_relative_house("Lagna", 8)
    )

    present = all(p["name"] in BENEFIC_PLANETS for p in planets)

    if present:
        benefics = ", ".join(p["name"] for p in planets)
        details = f"Benefic planets placed in the 6th, 7th and 8th houses from the Lagna: {benefics}."
    else:
        non_benefics = ", ".join(
            p["name"] for p in planets if p["name"] not in BENEFIC_PLANETS
        )
        details = (
            f"Non-benefic planets found in the 6th, 7th or 8th houses from the Lagna: {non_benefics}."
            if non_benefics
            else "No benefic influence on the Lagna from the 6th, 7th or 8th houses."
        )

    return {
        "name": "Lagna Adhi Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Chatussagara Yoga")
def chatussagara_yoga(yoga: Yoga):
    """
    All kendras (1st, 4th, 7th, 10th houses) must be occupied by planets.
    """

    house_1 = yoga.planets_in_relative_house("Lagna", 1)
    house_4 = yoga.planets_in_relative_house("Lagna", 4)
    house_7 = yoga.planets_in_relative_house("Lagna", 7)
    house_10 = yoga.planets_in_relative_house("Lagna", 10)

    # Each house must have at least one planet
    present = all(len(h) > 0 for h in [house_1, house_4, house_7, house_10])

    # Show only counts
    details = (
        f"Planet counts — 1st: {len(house_1)}, "
        f"4th: {len(house_4)}, "
        f"7th: {len(house_7)}, "
        f"10th: {len(house_10)}."
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

    moon_names = [p["name"] for p in moon_upachayas]
    lagna_names = [p["name"] for p in lagna_upachayas]

    benefics_moon = [name for name in moon_names if name in BENEFIC_PLANETS]
    benefics_lagna = [name for name in lagna_names if name in BENEFIC_PLANETS]

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
    Ju, Ve, Me, and Mo should be in the Ascendant or any Kendra (1, 4, 7, 10).
    """
    kendras = [1, 4, 7, 10]

    planets_in_kendras = []
    for house in kendras:
        planets_in_kendras += yoga.planets_in_relative_house("Lagna", house)

    kendra_names = [p["name"] for p in planets_in_kendras]

    present = all(rp in kendra_names for rp in BENEFIC_PLANETS)

    if planets_in_kendras:
        details = f"Planets in Kendras: {', '.join(kendra_names)}."
    else:
        details = "No planets found in kendras."

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

    benefics_moon = [p for p in from_moon if p["name"] in BENEFIC_PLANETS]
    benefics_lagna = [p for p in from_lagna if p["name"] in BENEFIC_PLANETS]

    present = bool(benefics_moon or benefics_lagna)

    if present:
        details = []
        if benefics_moon:
            details.append(f"From Moon: {', '.join([p['name'] for p in benefics_moon])} in 10th.")
        if benefics_lagna:
            details.append(f"From Ascendant: {', '.join([p['name'] for p in benefics_lagna])} in 10th.")
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
        f"6th house: {', '.join([p['name'] for p in house_6]) or 'Empty'}; "
        f"8th house: {', '.join([p['name'] for p in house_8]) or 'Empty'}."
    )

    return {
        "name": "Parvata Yoga",
        "present": present,
        "details": details,
    }


@register_yoga("Kahala Yoga")
def kahala_yoga(yoga: Yoga):
    """
    Lords of fourth and ninth houses in kendras from each other.
    """
    lord_of_4 = yoga.get_lord_of_house(4)
    lord_of_9 = yoga.get_lord_of_house(9)

    house_of_lord_of_4 = yoga.get_house_of_planet(lord_of_4)
    house_of_lord_of_9 = yoga.get_house_of_planet(lord_of_9)

    present = yoga.planet_in_kendra_from(house_of_lord_of_4, house_of_lord_of_9)
    return {
        "name": "Kahala Yoga",
        "present": present,
        "details": f"Lord of 4th house {lord_of_4} in {house_of_lord_of_4} house & Lord of 9th house {lord_of_9} in {house_of_lord_of_9} house.",
    }


@register_yoga("Vesi Yoga")
def vesi_yoga(yoga: Yoga):
    """
    Planets other than Mo occupy 2nd house from Su.
    """
    planets = yoga.planets_in_relative_house("Sun", 2)

    present = any(p["name"] != "Moon" for p in planets)
    return {
        "name": "Vesi Yoga",
        "present": present,
        "details": f"Planets in 2nd house from Sun are {[p['name'] for p in planets]}",
    }


@register_yoga("Vasi Yoga")
def vasi_yoga(yoga: Yoga):
    """
    Planets other than Mo occupy 12th house from Su.
    """
    planets = yoga.planets_in_relative_house("Sun", 12)

    present = any(p["name"] != "Moon" for p in planets)
    return {
        "name": "Vasi Yoga",
        "present": present,
        "details": f"Planets in 12th house from Sun are {[p['name'] for p in planets]}",
    }


@register_yoga("Obhayachari Yoga")
def obhayachari_yoga(yoga: Yoga):
    """
    Planets other than Mo are on either side of the Su.
    """
    planets = yoga.planets_in_relative_house("Sun", 2) + yoga.planets_in_relative_house(
        "Sun", 12
    )

    present = any(p["name"] != "Moon" for p in planets)
    return {
        "name": "Obhayachari Yoga",
        "present": present,
        "details": f"Planets in 2nd and 12th houses from Sun are {[p['name'] for p in planets]}",
    }


@register_yoga("Hamsa Yoga")
def hamsa_yoga(yoga: Yoga):
    """
    Ju must be in Sg, Pi or Cn and must be place in a Kendra from Asc.
    """
    Cn_house = yoga.get_house_of_rashi("Cancer")
    Sg_house = yoga.get_house_of_rashi("Sagittarius")
    Pi_house = yoga.get_house_of_rashi("Pisces")
    Ju_house = yoga.get_house_of_planet("Jupiter")
    present = (
        yoga.planet_in_kendra_from(Cn_house, "Jupiter")
        or yoga.planet_in_kendra_from(Sg_house, "Jupiter")
        or yoga.planet_in_kendra_from(Pi_house, "Jupiter")
    )
    return {
        "name": "Hamsa Yoga",
        "present": present,
        "details": f"Ju house is {Ju_house}, Cn house is {Cn_house}, Sg house is {Sg_house} and Pi house is {Pi_house}",
    }


@register_yoga("Malavya Yoga")
def malavya_yoga(yoga: Yoga):
    """
    Ve occupies a kendra of his own house or exalation sign.
    """
    Ta_house = yoga.get_house_of_rashi("Taurus")
    Li_house = yoga.get_house_of_rashi("Libra")
    Pi_house = yoga.get_house_of_rashi("Pisces")
    Ve_house = yoga.get_house_of_planet("Venus")
    present = (
        yoga.planet_in_kendra_from(Ta_house, "Venus")
        or yoga.planet_in_kendra_from(Li_house, "Venus")
        or yoga.planet_in_kendra_from(Pi_house, "Venus")
    )
    return {
        "name": "Malavya Yoga",
        "present": present,
        "details": f"Ve house is {Ve_house}, Ta house is {Ta_house}, Li house is {Li_house} and Li house is {Li_house}",
    }


@register_yoga("Sasa Yoga")
def sasa_yoga(yoga: Yoga):
    """
    Sa occupies a kendra of his own house or exalation sign.
    """
    Li_house = yoga.get_house_of_rashi("Libra")
    Cp_house = yoga.get_house_of_rashi("Capricorn")
    Aq_house = yoga.get_house_of_rashi("Aquarius")
    Sa_house = yoga.get_house_of_planet("Saturn")
    present = (
        yoga.planet_in_kendra_from(Li_house, "Saturn")
        or yoga.planet_in_kendra_from(Cp_house, "Saturn")
        or yoga.planet_in_kendra_from(Aq_house, "Saturn")
    )
    return {
        "name": "Sasa Yoga",
        "present": present,
        "details": f"Sa house is {Sa_house}, Li house is {Li_house}, Cp house is {Cp_house} and Aq house is {Aq_house}",
    }
