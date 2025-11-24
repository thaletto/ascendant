from typing import Dict, List
from ascendant.const import BENEFIC_PLANETS, RASHI_LORD_MAP
from ascendant.types import HOUSES, PLANETS, RASHI_LORDS, RASHIS, YogaType
from ascendant.yoga.base import Yoga, register_yoga, register_yogas


@register_yoga("GajaKesari")
def GajaKesari(yoga: Yoga) -> YogaType:
    """
    Ju in kendra from Mo
    """
    result: YogaType = {
        "id": "",
        "name": "GajaKesari",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    moon_house = yoga.get_house_of_planet("Moon")
    jupiter_house = yoga.get_house_of_planet("Jupiter")
    if not moon_house or not jupiter_house:
        result["present"] = False
        result["details"] = "Moon or Jupiter not found"
        result["strength"] = 0

    present = yoga.planet_in_kendra_from(moon_house, "Jupiter")
    result["present"] = present
    result["details"] = f"Jupiter in house {jupiter_house} and Moon is in {moon_house}"

    kendra_strength = {0: 1.0, 4: 0.75, 10: 0.75, 7: 0.9}
    distance = (jupiter_house - moon_house) % 12 + 1
    result["strength"] = kendra_strength.get(distance, 0)

    return result


@register_yoga("Sunapha")
def Sunapha(yoga: Yoga) -> YogaType:
    """
    Any planets (except Su) in the 2nd house from Mo
    """
    result: YogaType = {
        "id": "",
        "name": "Sunapha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    planets = yoga.planets_in_relative_house("Moon", 2)
    planets = [p for p in planets if p["name"] != "Sun"]
    if not planets:
        result["details"] = "No planets in 2nd house from Moon"
        return result

    WEIGHTS: Dict[PLANETS, float] = {
        "Jupiter": 1.0,
        "Venus": 0.9,
        "Mercury": 0.8,
        "Moon": 0.7,
    }
    DEFAULT_WEIGHT = 0.5

    strengths = []
    names = []
    for p in planets:
        name = p["name"]
        strength = WEIGHTS.get(name, DEFAULT_WEIGHT)
        strengths.append(strength)
        names.append(f"{name}({strength})")

    result["present"] = len(planets) > 0
    result["strength"] = sum(strengths) / len(strengths)
    result["details"] = "Planets (excluding Sun) in 2nd house from Moon: " + ", ".join(
        names
    )

    return result


@register_yoga("Anapha")
def Anapha(yoga: Yoga) -> YogaType:
    """
    Any planets in the 12th house from Mo
    """
    result: YogaType = {
        "id": "",
        "name": "Anapha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    planets = yoga.planets_in_relative_house("Moon", 12)
    if not planets:
        result["details"] = "No planets in 12th house from Moon"
        return result

    WEIGHTS: Dict[PLANETS, float] = {
        "Jupiter": 1.0,
        "Venus": 0.9,
        "Mercury": 0.8,
        "Moon": 0.7,
    }
    DEFAULT_WEIGHT = 0.5

    strengths = []
    names = []
    for p in planets:
        name = p["name"]
        strength = WEIGHTS.get(name, DEFAULT_WEIGHT)
        strengths.append(strength)
        names.append(f"{name}({strength})")

    result["present"] = len(planets) > 0
    result["strength"] = sum(strengths) / len(strengths)
    result["details"] = "Planets in 12th house from Moon: " + ", ".join(names)

    return result


@register_yoga("Dhurdhua")
def Dhurdhua(yoga: Yoga) -> YogaType:
    """
    Any planets on either side of the Mo
    """
    result: YogaType = {
        "id": "",
        "name": "Dhurdhua",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    sunapha_result = Sunapha(yoga)
    anapha_result = Anapha(yoga)

    result["present"] = sunapha_result["present"] and anapha_result["present"]
    result["strength"] = (sunapha_result["strength"] + anapha_result["strength"]) / 2
    result["details"] = (
        f"Anapha Yoga Details: {anapha_result['details']} \n Sunapha Yoga Details: {sunapha_result['details']}"
    )
    return result


@register_yoga("KemaDurga")
def KemaDurga(yoga: Yoga) -> YogaType:
    """
    No planets on both side of the Mo
    """
    result: YogaType = {
        "id": "",
        "name": "KemaDurga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    sunapha_result = Sunapha(yoga)
    anapha_result = Anapha(yoga)

    result["present"] = not sunapha_result["present"] and not anapha_result["present"]
    result["strength"] = (sunapha_result["strength"] + anapha_result["strength"]) / 2
    result["details"] = (
        f"Anapha Yoga Details: {anapha_result['details']} \n Sunapha Yoga Details: {sunapha_result['details']}"
    )
    return result


@register_yoga("ChandraMangala")
def ChandraMangala(yoga: Yoga) -> YogaType:
    """
    Ma cojoins Mo
    """
    result: YogaType = {
        "id": "",
        "name": "ChandraMangala",
        "present": False,
        "strength": 1,
        "details": "",
        "type": "Negative",
    }
    mars_house = yoga.get_house_of_planet("Mars")
    moon_house = yoga.get_house_of_planet("Moon")

    result["present"] = mars_house == moon_house
    result["details"] = f"Mars in {mars_house}, Moon in {moon_house}"

    return result


@register_yoga("ChandraAdhiYoga")
def ChandraAdhiYoga(yoga: Yoga) -> YogaType:
    """
    All Benefics (Ju, Ve, Me) in 6th, 7th & 8th houses from Moon
    """
    result: YogaType = {
        "id": "",
        "name": "ChandraAdhiYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    HOUSE_STRENGTH = {6: 0.75, 7: 1.0, 8: 0.75}

    # Collect planets in 6, 7, 8
    planets_6 = yoga.planets_in_relative_house("Moon", 6)
    planets_7 = yoga.planets_in_relative_house("Moon", 7)
    planets_8 = yoga.planets_in_relative_house("Moon", 8)

    planets = planets_6 + planets_7 + planets_8
    planets_names = [p["name"] for p in planets]

    # Check presence
    result["present"] = all(benefic in planets_names for benefic in BENEFIC_PLANETS)

    # Calculate strength
    strength_sum = 0.0
    for p in planets:
        if p["name"] in BENEFIC_PLANETS:
            relative_pos = yoga.relative_house("Moon", p["name"])
            strength_sum += HOUSE_STRENGTH.get(relative_pos, 0)

    # Normalize
    result["strength"] = strength_sum / len(BENEFIC_PLANETS)

    result["details"] = (
        f"{', '.join(planets_names)} in 6th, 7th and 8th houses from the Mo"
    )

    return result


@register_yoga("LagnaAdhiYoga")
def LagnaAdhiYoga(yoga: Yoga) -> YogaType:
    """
    All Benefics (Ju, Ve, Me) in 6th, 7th & 8th houses from Moon
    """
    result: YogaType = {
        "id": "",
        "name": "LagnaAdhiYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    HOUSE_STRENGTH = {6: 0.75, 7: 1.0, 8: 0.75}

    # Collect planets in 6, 7, 8
    planets_6 = yoga.planets_in_relative_house("Lagna", 6)
    planets_7 = yoga.planets_in_relative_house("Lagna", 7)
    planets_8 = yoga.planets_in_relative_house("Lagna", 8)

    planets = planets_6 + planets_7 + planets_8
    planets_names = [p["name"] for p in planets]

    # Check presence
    result["present"] = all(benefic in planets_names for benefic in BENEFIC_PLANETS)

    # Calculate strength
    strength_sum = 0.0
    for p in planets:
        if p["name"] in BENEFIC_PLANETS:
            relative_pos = yoga.relative_house("Lagna", p["name"])
            strength_sum += HOUSE_STRENGTH.get(relative_pos, 0)

    # Normalize
    result["strength"] = strength_sum / len(BENEFIC_PLANETS)

    result["details"] = (
        f"{', '.join(planets_names)} in 6th, 7th and 8th houses from the Mo"
    )

    return result


@register_yoga("Chatussagara")
def Chatussagara(yoga: Yoga) -> YogaType:
    """
    All kendras (1st, 4th, 7th, 10th houses) must be occupied by planets.
    """
    result: YogaType = {
        "id": "",
        "name": "Chatussagara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    house_1 = yoga.planets_in_relative_house("Lagna", 1)
    house_4 = yoga.planets_in_relative_house("Lagna", 4)
    house_7 = yoga.planets_in_relative_house("Lagna", 7)
    house_10 = yoga.planets_in_relative_house("Lagna", 10)

    houses = [house_1, house_4, house_7, house_10]

    occupied_flags = [len(h) > 0 for h in houses]
    result["present"] = all(occupied_flags)

    # Details text
    result["details"] = (
        f"Planet counts — 1st house: {len(house_1)}, "
        f"4th house: {len(house_4)}, "
        f"7th house: {len(house_7)}, "
        f"10th house: {len(house_10)}."
    )

    # Strength logic
    if result["present"]:
        occupied_kendras = sum(1 for h in houses if len(h) > 0)
        total_planets = sum(len(h) for h in houses)

        kendra_strength = occupied_kendras / 4
        density_strength = min(total_planets / 12, 1)

        result["strength"] = round(0.7 * kendra_strength + 0.3 * density_strength, 2)
    else:
        result["strength"] = 0.0

    return result


@register_yoga("Vasumathi")
def Vasumathi(yoga: Yoga) -> YogaType:
    """
    Benefic planets occupy the upachaya houses (3, 6, 10, or 11)
    either from the Ascendant or from the Moon.
    """
    result: YogaType = {
        "id": "",
        "name": "Vasumathi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    UPACHAYA_STRENGTH = {3: 0.6, 6: 0.75, 10: 0.9, 11: 1.0}

    # Check from Moon
    moon_positions = [
        (3, yoga.planets_in_relative_house("Moon", 3)),
        (6, yoga.planets_in_relative_house("Moon", 6)),
        (10, yoga.planets_in_relative_house("Moon", 10)),
        (11, yoga.planets_in_relative_house("Moon", 11)),
    ]

    # Check from Lagna
    lagna_positions = [
        (3, yoga.planets_in_relative_house("Lagna", 3)),
        (6, yoga.planets_in_relative_house("Lagna", 6)),
        (10, yoga.planets_in_relative_house("Lagna", 10)),
        (11, yoga.planets_in_relative_house("Lagna", 11)),
    ]

    # Collect benefics from Moon
    benefics_moon = []
    moon_strength = 0.0
    for house, plist in moon_positions:
        for p in plist:
            if p["name"] in BENEFIC_PLANETS:
                benefics_moon.append(p["name"])
                moon_strength += UPACHAYA_STRENGTH[house] * 1.0

    # Collect benefics from Lagna
    benefics_lagna = []
    lagna_strength = 0.0
    for house, plist in lagna_positions:
        for p in plist:
            if p["name"] in BENEFIC_PLANETS:
                benefics_lagna.append(p["name"])
                lagna_strength += UPACHAYA_STRENGTH[house] * 0.8

    # Yoga is present if benefics occupy upachaya houses from EITHER Moon OR Lagna
    present_from_moon = bool(benefics_moon)
    present_from_lagna = bool(benefics_lagna)
    present = present_from_moon or present_from_lagna

    # Use the stronger condition (Moon takes precedence if both are present)
    if present_from_moon:
        result["strength"] = round(min(moon_strength / 3.0, 1.0), 2)
        result["details"] = (
            f"From Moon: {', '.join(benefics_moon)} in upachaya houses (3, 6, 10, 11)."
        )
    elif present_from_lagna:
        result["strength"] = round(min(lagna_strength / 3.0, 1.0), 2)
        result["details"] = (
            f"From Ascendant: {', '.join(benefics_lagna)} in upachaya houses (3, 6, 10, 11)."
        )
    else:
        result["strength"] = 0.0
        result["details"] = (
            "No benefic planets occupy upachaya houses from either Moon or Ascendant."
        )

    result["present"] = present

    return result


@register_yoga("Rajalakshana")
def Rajalakshana(yoga: Yoga) -> YogaType:
    """
    Ju, Ve, Me, and Mo should be in the Ascendant or any Kendra (1, 4, 7, 10).
    """
    result: YogaType = {
        "id": "",
        "name": "Rajalakshana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    kendras = [1, 4, 7, 10]

    planets_in_kendras = []
    for house in kendras:
        planets_in_kendras.extend(yoga.planets_in_relative_house("Lagna", house))

    kendra_names = [p["name"] for p in planets_in_kendras]

    benefics_in_kendra = [p for p in BENEFIC_PLANETS if p in kendra_names]

    result["present"] = all(rp in kendra_names for rp in BENEFIC_PLANETS)

    if planets_in_kendras:
        result["details"] = f"Planets in Kendras: {', '.join(kendra_names)}."
    else:
        result["details"] = "No planets found in kendras."

    if result["present"]:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.7, 4: 0.6}
        total_strength = 0
        lagna_house = yoga.get_house_of_planet("Lagna")
        if lagna_house:
            for p_name in benefics_in_kendra:
                p_house = yoga.get_house_of_planet(p_name)
                if p_house:
                    kendra_pos = (p_house - lagna_house + 12) % 12 + 1
                    total_strength += kendra_strength_map.get(kendra_pos, 0.5)

            result["strength"] = (
                total_strength / len(BENEFIC_PLANETS) if BENEFIC_PLANETS else 0
            )

    return result


@register_yoga("Sakata")
def Sakata(yoga: Yoga) -> YogaType:
    """
    Mo is in 6th, 8th, or 12th house from Ju.
    """
    result: YogaType = {
        "id": "",
        "name": "Sakata",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    relative_house = yoga.relative_house("Jupiter", "Moon")
    result["present"] = relative_house in [6, 8, 12]

    if relative_house:
        result["details"] = f"Moon is {relative_house} houses away from Jupiter."
        strength_map = {12: 1.0, 8: 0.8, 6: 0.6}
        result["strength"] = strength_map.get(relative_house, 0.0)
    else:
        result["details"] = (
            "Unable to determine relative house between Moon and Jupiter."
        )
        result["strength"] = 0.0

    return result


@register_yoga("Amala")
def Amala(yoga: Yoga) -> YogaType:
    """
    10th house from Mo or Asc occupied by any benefic planet.
    """
    result: YogaType = {
        "id": "",
        "name": "Amala",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    from_moon = yoga.planets_in_relative_house("Moon", 10)
    from_lagna = yoga.planets_in_relative_house("Lagna", 10)

    benefics_moon = [p for p in from_moon if p["name"] in BENEFIC_PLANETS]
    benefics_lagna = [p for p in from_lagna if p["name"] in BENEFIC_PLANETS]

    result["present"] = bool(benefics_moon or benefics_lagna)

    details_list = []
    strength = 0
    planet_strength = {"Jupiter": 1.0, "Venus": 0.9, "Mercury": 0.8, "Moon": 0.7}

    if benefics_moon:
        details_list.append(
            f"From Moon: {', '.join([p['name'] for p in benefics_moon])} in 10th."
        )
        for p in benefics_moon:
            strength += planet_strength.get(p["name"], 0.5)

    if benefics_lagna:
        details_list.append(
            f"From Ascendant: {', '.join([p['name'] for p in benefics_lagna])} in 10th."
        )
        for p in benefics_lagna:
            strength += planet_strength.get(p["name"], 0.5) * 0.8

    if result["present"]:
        result["details"] = " ".join(details_list)
        total_benefics = len(benefics_moon) + len(benefics_lagna)
        result["strength"] = strength / total_benefics if total_benefics > 0 else 0.0
    else:
        result["details"] = (
            "No benefic planets occupy the 10th house from Moon or Ascendant."
        )
        result["strength"] = 0.0

    return result


@register_yoga("Parvata")
def Parvata(yoga: Yoga) -> YogaType:
    """
    6th and 8th houses should be either unoccupied or occupied only by benefic planets.
    """
    result: YogaType = {
        "id": "",
        "name": "Parvata",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    house_6_planets = yoga.planets_in_relative_house("Lagna", 6)
    house_8_planets = yoga.planets_in_relative_house("Lagna", 8)

    house_6_names = [p["name"] for p in house_6_planets]
    house_8_names = [p["name"] for p in house_8_planets]

    house_6_ok = not house_6_planets or all(p in BENEFIC_PLANETS for p in house_6_names)
    house_8_ok = not house_8_planets or all(p in BENEFIC_PLANETS for p in house_8_names)

    result["present"] = house_6_ok and house_8_ok

    result["details"] = (
        f"6th house: {', '.join(house_6_names) or 'Empty'}; "
        f"8th house: {', '.join(house_8_names) or 'Empty'}."
    )

    if result["present"]:
        strength = 2.0
        if house_6_planets:
            strength -= 0.2 * len(house_6_planets)
        if house_8_planets:
            strength -= 0.2 * len(house_8_planets)
        result["strength"] = strength / 2.0
    else:
        result["strength"] = 0.0

    return result


@register_yoga("Kahala")
def Kahala(yoga: Yoga) -> YogaType:
    """
    Lords of fourth and ninth houses in kendras from each other.
    """
    result: YogaType = {
        "id": "",
        "name": "Kahala",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    lord_of_4 = yoga.get_lord_of_house(4)
    lord_of_9 = yoga.get_lord_of_house(9)

    if not lord_of_4 or not lord_of_9:
        result["details"] = "Could not determine lords of 4th and 9th houses."
        return result

    house_of_lord_of_4 = yoga.get_house_of_planet(lord_of_4)
    house_of_lord_of_9 = yoga.get_house_of_planet(lord_of_9)

    if not house_of_lord_of_4 or not house_of_lord_of_9:
        result["details"] = "Could not find house for lord of 4th or 9th."
        return result

    result["present"] = yoga.planet_in_kendra_from(house_of_lord_of_4, lord_of_9)

    result["details"] = (
        f"Lord of 4th house ({lord_of_4}) in house {house_of_lord_of_4} & Lord of 9th house ({lord_of_9}) in house {house_of_lord_of_9}."
    )

    if result["present"]:
        relative_pos = (house_of_lord_of_9 - house_of_lord_of_4 + 12) % 12 + 1
        kendra_map = {1: 1.0, 4: 0.75, 7: 0.9, 10: 0.75}
        result["strength"] = kendra_map.get(relative_pos, 0)

    return result


@register_yoga("VesiYoga")
def VesiYoga(yoga: Yoga) -> YogaType:
    """
    Planets other than Mo occupy 2nd house from Su.
    """
    result: YogaType = {
        "id": "",
        "name": "VesiYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    planets = yoga.planets_in_relative_house("Sun", 2)
    planets = [p for p in planets if p["name"] != "Moon"]

    result["present"] = len(planets) > 0
    result["details"] = (
        f"Planets in 2nd house from Sun are {[p['name'] for p in planets]}"
    )

    if result["present"]:
        strength = 0
        planet_strength = {"Jupiter": 1.0, "Venus": 0.9, "Mercury": 0.8}
        for p in planets:
            if p["name"] in BENEFIC_PLANETS:
                strength += planet_strength.get(p["name"], 0.5)
            else:
                strength -= 0.5
        result["strength"] = max(0, strength / len(planets))

    return result


@register_yoga("VasiYoga")
def VasiYoga(yoga: Yoga) -> YogaType:
    """
    Planets other than Mo occupy 12th house from Su.
    """
    result: YogaType = {
        "id": "",
        "name": "VasiYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    planets = yoga.planets_in_relative_house("Sun", 12)
    planets = [p for p in planets if p["name"] != "Moon"]

    result["present"] = len(planets) > 0
    result["details"] = (
        f"Planets in 12th house from Sun are {[p['name'] for p in planets]}"
    )

    if result["present"]:
        strength = 0
        planet_strength = {"Jupiter": 1.0, "Venus": 0.9, "Mercury": 0.8}
        for p in planets:
            if p["name"] in BENEFIC_PLANETS:
                strength += planet_strength.get(p["name"], 0.5)
            else:
                strength -= 0.5
        result["strength"] = max(0, strength / len(planets))

    return result


@register_yoga("ObhayachariYoga")
def ObhayachariYoga(yoga: Yoga) -> YogaType:
    """
    Planets other than Mo are on either side of the Su.
    """
    result: YogaType = {
        "id": "",
        "name": "ObhayachariYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    vesi = VesiYoga(yoga)
    vasi = VasiYoga(yoga)

    result["present"] = vesi["present"] and vasi["present"]
    result["details"] = f"Vesi Yoga: {vesi['details']}. Vasi Yoga: {vasi['details']}"

    if result["present"]:
        result["strength"] = (vesi["strength"] + vasi["strength"]) / 2

    return result


@register_yoga("Hamsa")
def Hamsa(yoga: Yoga) -> YogaType:
    """
    Ju must be in Sg, Pi or Cn and must be place in a Kendra from Asc.
    """
    result: YogaType = {
        "id": "",
        "name": "Hamsa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    ju_house = yoga.get_house_of_planet("Jupiter")
    if not ju_house:
        result["details"] = "Jupiter not found."
        return result

    ju_rashi = yoga.get_rashi_of_house(ju_house)

    own_signs: List[RASHIS] = ["Sagittarius", "Pisces"]
    exaltation_sign: RASHIS = "Cancer"

    in_own_or_exalted_sign = ju_rashi in own_signs or ju_rashi == exaltation_sign

    lagna_house = yoga.get_house_of_planet("Lagna")
    in_kendra = False
    if lagna_house:
        in_kendra = yoga.planet_in_kendra_from(lagna_house, "Jupiter")

    result["present"] = in_own_or_exalted_sign and in_kendra

    result["details"] = f"Jupiter is in {ju_rashi} (house {ju_house})."

    if result["present"] and lagna_house:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.9, 4: 0.7}
        kendra_pos = (ju_house - lagna_house + 12) % 12 + 1
        strength = kendra_strength_map.get(kendra_pos, 0.5)
        if ju_rashi == exaltation_sign:
            strength *= 1.2
        result["strength"] = min(1.0, strength)

    return result


@register_yoga("Malavya")
def Malavya(yoga: Yoga) -> YogaType:
    """
    Ve must be in Ta, Li or Pi and must be place in a Kendra from Asc
    """
    result: YogaType = {
        "id": "",
        "name": "Malavya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    ve_house = yoga.get_house_of_planet("Venus")
    if not ve_house:
        result["details"] = "Venus not found."
        return result

    ve_rashi = yoga.get_rashi_of_house(ve_house)

    own_signs: List[RASHIS] = ["Taurus", "Libra"]
    exaltation_sign: RASHIS = "Pisces"

    in_own_or_exalted_sign = ve_rashi in own_signs or ve_rashi == exaltation_sign

    lagna_house = yoga.get_house_of_planet("Lagna")
    in_kendra = False
    if lagna_house:
        in_kendra = yoga.planet_in_kendra_from(lagna_house, "Venus")

    result["present"] = in_own_or_exalted_sign and in_kendra

    result["details"] = f"Venus is in {ve_rashi} (house {ve_house})."

    if result["present"] and lagna_house:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.9, 4: 0.7}
        kendra_pos = (ve_house - lagna_house + 12) % 12 + 1
        strength = kendra_strength_map.get(kendra_pos, 0.5)
        if ve_rashi == exaltation_sign:
            strength *= 1.2
        result["strength"] = min(1.0, strength)

    return result


@register_yoga("Sasa")
def Sasa(yoga: Yoga) -> YogaType:
    """
    Sa must be in Li, Cp or Aq and must be place in a Kendra from Asc
    """
    result: YogaType = {
        "id": "",
        "name": "Sasa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    sa_house = yoga.get_house_of_planet("Saturn")
    if not sa_house:
        result["details"] = "Saturn not found."
        return result

    sa_rashi = yoga.get_rashi_of_house(sa_house)

    own_signs: List[RASHIS] = ["Capricorn", "Aquarius"]
    exaltation_sign: RASHIS = "Libra"

    in_own_or_exalted_sign = sa_rashi in own_signs or sa_rashi == exaltation_sign

    lagna_house = yoga.get_house_of_planet("Lagna")
    in_kendra = False
    if lagna_house:
        in_kendra = yoga.planet_in_kendra_from(lagna_house, "Saturn")

    result["present"] = in_own_or_exalted_sign and in_kendra

    result["details"] = f"Saturn is in {sa_rashi} (house {sa_house})."

    if result["present"] and lagna_house:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.9, 4: 0.7}
        kendra_pos = (sa_house - lagna_house + 12) % 12 + 1
        strength = kendra_strength_map.get(kendra_pos, 0.5)
        if sa_rashi == exaltation_sign:
            strength *= 1.2
        result["strength"] = min(1.0, strength)

    return result


@register_yoga("Ruchaka")
def Ruchaka(yoga: Yoga) -> YogaType:
    """
    Ma must be in Ar, Sc or Cp and must be place in a Kendra from Asc
    """
    result: YogaType = {
        "id": "",
        "name": "Ruchaka",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    ma_house = yoga.get_house_of_planet("Mars")
    if not ma_house:
        result["details"] = "Mars not found."
        return result

    ma_rashi = yoga.get_rashi_of_house(ma_house)

    own_signs: List[RASHIS] = ["Aries", "Scorpio"]
    exaltation_sign: RASHIS = "Capricorn"

    in_own_or_exalted_sign = ma_rashi in own_signs or ma_rashi == exaltation_sign

    lagna_house = yoga.get_house_of_planet("Lagna")
    in_kendra = False
    if lagna_house:
        in_kendra = yoga.planet_in_kendra_from(lagna_house, "Mars")

    result["present"] = in_own_or_exalted_sign and in_kendra

    result["details"] = f"Mars is in {ma_rashi} (house {ma_house})."

    if result["present"] and lagna_house:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.9, 4: 0.7}
        kendra_pos = (ma_house - lagna_house + 12) % 12 + 1
        strength = kendra_strength_map.get(kendra_pos, 0.5)
        if ma_rashi == exaltation_sign:
            strength *= 1.2
        result["strength"] = min(1.0, strength)

    return result


@register_yoga("Bhadra")
def Bhadra(yoga: Yoga) -> YogaType:
    """
    Ma must be in Ge or Vi and must be place in a Kendra from Asc
    """
    result: YogaType = {
        "id": "",
        "name": "Bhadra",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    me_house = yoga.get_house_of_planet("Mercury")
    if not me_house:
        result["details"] = "Mercury not found."
        return result

    me_rashi = yoga.get_rashi_of_house(me_house)

    own_signs: List[RASHIS] = ["Gemini", "Virgo"]
    exaltation_sign: RASHIS = "Virgo"

    in_own_or_exalted_sign = me_house in own_signs or me_rashi == exaltation_sign

    lagna_house = yoga.get_house_of_planet("Lagna")
    in_kendra = False
    if lagna_house:
        in_kendra = yoga.planet_in_kendra_from(lagna_house, "Mercury")

    result["present"] = in_own_or_exalted_sign and in_kendra

    result["details"] = f"Mars is in {me_rashi} (house {me_house})."

    if result["present"] and lagna_house:
        kendra_strength_map = {1: 1.0, 10: 0.8, 7: 0.9, 4: 0.7}
        kendra_pos = (me_house - lagna_house + 12) % 12 + 1
        strength = kendra_strength_map.get(kendra_pos, 0.5)
        if me_rashi == exaltation_sign:
            strength *= 1.2
        result["strength"] = min(1.0, strength)

    return result


@register_yoga("BuddhaAditya")
def BuddhaAditya(yoga: Yoga) -> YogaType:
    """
    Me combines with the Su
    """
    result: YogaType = {
        "id": "",
        "name": "BuddhaAditya",
        "present": False,
        "strength": 1.0,
        "details": "",
        "type": "Positive",
    }
    me_house = yoga.get_house_of_planet("Mercury")
    su_house = yoga.get_house_of_planet("Sun")
    result["present"] = me_house == su_house
    result["details"] = f"Mercury is in house {me_house} and Sun is in house {su_house}"

    return result


@register_yoga("Pushkala")
def Pushkala(yoga: Yoga) -> YogaType:
    """
    Pushkala Yoga:
    1. Lord of Moon's sign is associated with Lagna lord (aspect/conjunction)
    2. Moon's lord is in a Kendra OR in an intimate friend's sign
    3. Moon's lord aspects Lagna directly
    4. Lagna is occupied by a powerful planet
    """
    result: YogaType = {
        "id": "",
        "name": "Pushkala",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get required houses and lords
    moon_house = yoga.get_house_of_planet("Moon")
    lagna_house = yoga.get_house_of_planet("Lagna")

    if not moon_house or not lagna_house:
        result["details"] = "Moon or Lagna not found"
        return result

    moon_lord = yoga.get_lord_of_house(moon_house)
    lagna_lord = yoga.get_lord_of_house(lagna_house)
    moon_lord_house = yoga.get_house_of_planet(moon_lord)
    lagna_lord_house = yoga.get_house_of_planet(lagna_lord)

    if not all([moon_lord, lagna_lord, moon_lord_house, lagna_lord_house]):
        result["details"] = "Could not determine all required lords and houses"
        return result

    # Get moon lord aspects
    chart = yoga.__chart__
    try:
        moon_lord_aspects = chart.graha_drishti(n=1, planet=moon_lord)[0]
        aspect_houses = moon_lord_aspects.get("aspect_houses", [])
    except (KeyError, IndexError, TypeError):
        result["details"] = "Could not determine moon lord aspects"
        return result

    # Condition 1: Association (aspect or conjunction)
    is_conjunction = lagna_lord_house == moon_lord_house
    is_aspect = any(lagna_lord_house in house_dict for house_dict in aspect_houses)
    condition1 = is_conjunction or is_aspect
    strength1 = 1.0 if is_conjunction else 0.8 if is_aspect else 0.0

    # Condition 2: Kendra or Friend Sign
    in_kendra = yoga.planet_in_kendra_from(lagna_house, moon_lord)
    moon_lord_planet = next(
        (p for p in yoga.chart[moon_lord_house]["planets"] if p["name"] == moon_lord),
        None,
    )
    in_friend_sign = bool(moon_lord_planet and "Friend" in moon_lord_planet["inSign"])
    condition2 = in_kendra or in_friend_sign
    strength2 = 1.0 if in_kendra else 0.8 if in_friend_sign else 0.0

    # Condition 3: Aspect to Lagna
    condition3 = any(lagna_house in house_dict for house_dict in aspect_houses)
    strength3 = 1.0 if condition3 else 0.0

    # Condition 4: Lagna has a powerful planet
    lagna_planets = yoga.planets_in_relative_house("Lagna", 1)
    condition4 = False
    strength4 = 0.0
    for planet in lagna_planets:
        is_powerful, planet_strength = yoga.isPlanetPowerful(planet)
        if is_powerful:
            condition4 = True
            strength4 = max(strength4, planet_strength)

    # Final evaluation
    result["present"] = condition1 and condition2 and condition3 and condition4
    result["strength"] = (
        (strength1 + strength2 + strength3 + strength4) / 4 if result["present"] else 0
    )

    status = "formed" if result["present"] else "not formed"
    result["details"] = f"""Pushkala Yoga {status}
        \nMoon Lord & Lagna Lord Associated: {condition1}, Strength: {strength1}
        \nMoon Lord in Kendra or Friend's sign: {condition2}, Strength: {strength2}
        \nMoon Lord aspects Lagna: {condition3}, Strength: {strength3}
        \nLagna is occupied by powerful planet: {condition4}, Strength: {strength4}
        \nTotal Strength: {result["strength"]}
        """

    return result


@register_yoga("Lakshmi")
def Lakshmi(yoga: Yoga) -> YogaType:
    """
    Lagna Lord is Powerful and the Lord of the 9th occupies its own or exaltation sign identical with a Kendra or Trikona
    """
    result: YogaType = {
        "id": "",
        "name": "Lakshmi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    lagna_lord = yoga.get_lord_of_planet("Lagna")
    Lagna_Lord_Planet = yoga.get_planet_by_name(lagna_lord)
    isPowerful, strength1 = yoga.isPlanetPowerful(Lagna_Lord_Planet)

    if not isPowerful:
        result["present"] = False
        result["details"] = "Lord of Lagna not Powerful"
        return result

    condition2 = False
    lord_of_9 = yoga.get_lord_of_house(9)
    lord_of_9_planet = yoga.get_planet_by_name(lord_of_9)
    for inSign in lord_of_9_planet["inSign"]:
        if inSign == "Own":
            condition2, strength2 = True, 0.8
        elif inSign == "Exalted":
            condition2, strength2 = True, 1

    if not condition2:
        result["present"] = False
        result["details"] = "Lord of 9th house not in Own or Exalted Sign"
        return result

    condition3 = False
    in_Kendra = yoga.planet_in_kendra_from(lord_of_9, 1)
    in_Trikona = yoga.planet_in_trikona_from(lord_of_9, 1)
    if in_Kendra or in_Trikona:
        condition3, strength3 = True, 1

    result["present"] = isPowerful and condition2 and condition3
    result["strength"] = (strength1 + strength2 + strength3) / 3
    result["details"] = "Lakshmi Yoga Formed"

    return result


@register_yoga("Gauri")
def Gauri(yoga: Yoga) -> YogaType:
    """
    The Lord of the Navamsa, occupied by the Lord of the tenth, joins the tenth house in exaltation and combines with the Lord of Lagna.
    """
    result: YogaType = {
        "id": "",
        "name": "Gauri",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    L10 = yoga.get_lord_of_house(10)
    D9 = yoga.__chart__.get_varga_chakra_chart(9)

    for house, data in D9.items():
        for planet in data["planets"]:
            if planet["name"] == L10:
                sign = planet["sign"]["name"]
                NavamsaSignLord: RASHI_LORDS = RASHI_LORD_MAP.get(sign)

    NSL_house = yoga.get_house_of_planet(NavamsaSignLord)
    if NSL_house != 10:
        result["details"] = (
            f"10th Lord's ({L10}) Navamsa Lord ({NavamsaSignLord}) is not in 10th house of D1"
        )
        return result

    NSL_planet = yoga.get_planet_by_name(NavamsaSignLord)

    condition2 = False
    for inSign in NSL_planet["inSign"]:
        if inSign == "Exalted":
            condition2 = True

    if not condition2:
        result["details"] = f"{NSL_planet['name']} not in 10th house"
        return result

    LL = yoga.get_lord_of_planet("Lagna")
    LLH = yoga.get_house_of_planet(LL)

    if LLH != 10:
        result["details"] = (
            f"Lagna Lord: {LL} must be with {NSL_planet['name']} in 10th house"
        )

    result["present"] = True
    result["strength"] = 1
    result["details"] = "Gauri Yoga Formed"

    return result


@register_yoga("Bharathi")
def Bharathi(yoga: Yoga) -> YogaType:
    """
    The Lord of the Navamsa, occupied by the Lords of the second,
    fifth and eleventh, is exalted and combined with the ninth Lord.
    """
    result: YogaType = {
        "id": "",
        "name": "Bharathi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Lords of 2, 5, 11
    L2 = yoga.get_lord_of_house(2)
    L5 = yoga.get_lord_of_house(5)
    L11 = yoga.get_lord_of_house(11)

    key_lords = [L2, L5, L11]

    D9 = yoga.__chart__.get_varga_chakra_chart(9)
    navamsa_sign_lords = []

    # --- STEP 1: Find Navamsa Sign Lords occupied by 2L, 5L, 11L ---
    for house, data in D9.items():
        for planet in data["planets"]:
            if planet["name"] in key_lords:
                sign = planet["sign"]["name"]
                nsl = RASHI_LORD_MAP.get(sign)
                if nsl:
                    navamsa_sign_lords.append(nsl)

    if not navamsa_sign_lords:
        result["details"] = "No Navamsa-sign lord found for L2/L5/L11"
        return result

    # --- STEP 2: Check each Navamsa-sign-lord ---
    L9 = yoga.get_lord_of_house(9)
    L9_house = yoga.get_house_of_planet(L9)

    for NSL in navamsa_sign_lords:
        NSL_house = yoga.get_house_of_planet(NSL)
        NSL_planet = yoga.get_planet_by_name(NSL)

        # CONDITION A → NSL must be exalted
        exalted = any(flag == "Exalted" for flag in NSL_planet["inSign"])
        if not exalted:
            continue

        # CONDITION B → NSL must join L9
        if NSL_house != L9_house:
            continue

        # If any NSL satisfies both → Yoga formed
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"Bharathi Yoga formed: Navamsa-sign-lord {NSL} is exalted "
            f"and conjunct 9th lord {L9} in house {L9_house}."
        )
        return result

    # If none matched
    result["details"] = "No Navamsa-sign-lord is exalted and conjunct the 9th lord"
    return result


@register_yoga("Chapa")
def Chapa(yoga: Yoga) -> YogaType:
    """
    Lagna Lord is exalted and the fourth and tenth Lord have interchanged houses
    """
    result: YogaType = {
        "id": "",
        "name": "Chapa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get Lagna Lord
    lagna_house = yoga.get_house_of_planet("Lagna")
    if not lagna_house:
        result["details"] = "Lagna not found"
        return result

    lagna_lord = yoga.get_lord_of_house(lagna_house)
    if not lagna_lord:
        result["details"] = "Could not determine Lagna Lord"
        return result

    # Check if Lagna Lord is exalted
    lagna_lord_planet = yoga.get_planet_by_name(lagna_lord)
    if not lagna_lord_planet:
        result["details"] = f"Could not find planet {lagna_lord}"
        return result

    is_exalted = any(flag == "Exalted" for flag in lagna_lord_planet["inSign"])
    if not is_exalted:
        result["details"] = f"Lagna Lord {lagna_lord} is not exalted"
        return result

    # Get 4th and 10th house lords
    lord_of_4 = yoga.get_lord_of_house(4)
    lord_of_10 = yoga.get_lord_of_house(10)

    if not lord_of_4 or not lord_of_10:
        result["details"] = "Could not determine lords of 4th and 10th houses"
        return result

    # Get houses where these lords are located
    house_of_lord_4 = yoga.get_house_of_planet(lord_of_4)
    house_of_lord_10 = yoga.get_house_of_planet(lord_of_10)

    if not house_of_lord_4 or not house_of_lord_10:
        result["details"] = "Could not find houses for lords of 4th and 10th"
        return result

    # Check if they have interchanged houses (lord of 4th in 10th, lord of 10th in 4th)
    houses_interchanged = (house_of_lord_4 == 10) and (house_of_lord_10 == 4)

    result["present"] = is_exalted and houses_interchanged

    if result["present"]:
        result["strength"] = 1.0
        result["details"] = (
            f"Chapa Yoga formed: Lagna Lord {lagna_lord} is exalted. "
            f"Lord of 4th ({lord_of_4}) in 10th house, Lord of 10th ({lord_of_10}) in 4th house."
        )
    else:
        result["details"] = (
            f"Lagna Lord {lagna_lord} exalted: {is_exalted}. "
            f"4th lord ({lord_of_4}) in house {house_of_lord_4}, "
            f"10th lord ({lord_of_10}) in house {house_of_lord_10}. "
            f"Houses interchanged: {houses_interchanged}"
        )

    return result


@register_yoga("Sreenatha")
def Sreenatha(yoga: Yoga) -> YogaType:
    """
    The exalted Lord of the seventh occupies the tenth house and the Lord of the tenth is with the Lord of the ninth.
    """
    result: YogaType = {
        "id": "",
        "name": "Sreenatha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get 7th, 9th, and 10th house lords
    lord_of_7 = yoga.get_lord_of_house(7)
    lord_of_9 = yoga.get_lord_of_house(9)
    lord_of_10 = yoga.get_lord_of_house(10)

    if not lord_of_7 or not lord_of_9 or not lord_of_10:
        result["details"] = "Could not determine lords of 7th, 9th, or 10th houses"
        return result

    # Check if Lord of 7th is exalted
    lord_of_7_planet = yoga.get_planet_by_name(lord_of_7)
    if not lord_of_7_planet:
        result["details"] = f"Could not find planet {lord_of_7}"
        return result

    is_exalted = any(flag == "Exalted" for flag in lord_of_7_planet["inSign"])
    if not is_exalted:
        result["details"] = f"Lord of 7th house {lord_of_7} is not exalted"
        return result

    # Check if Lord of 7th occupies 10th house
    house_of_lord_7 = yoga.get_house_of_planet(lord_of_7)
    if not house_of_lord_7:
        result["details"] = f"Could not find house for {lord_of_7}"
        return result

    in_10th_house = house_of_lord_7 == 10
    if not in_10th_house:
        result["details"] = (
            f"Lord of 7th {lord_of_7} is exalted but in house {house_of_lord_7}, not 10th"
        )
        return result

    # Check if Lord of 10th is with Lord of 9th (conjunction)
    house_of_lord_10 = yoga.get_house_of_planet(lord_of_10)
    house_of_lord_9 = yoga.get_house_of_planet(lord_of_9)

    if not house_of_lord_10 or not house_of_lord_9:
        result["details"] = "Could not find houses for lords of 9th and 10th"
        return result

    lords_conjunct = house_of_lord_10 == house_of_lord_9

    result["present"] = is_exalted and in_10th_house and lords_conjunct

    if result["present"]:
        result["strength"] = 1.0
        result["details"] = (
            f"Sreenatha Yoga formed: Exalted Lord of 7th ({lord_of_7}) in 10th house. "
            f"Lord of 10th ({lord_of_10}) and Lord of 9th ({lord_of_9}) conjunct in house {house_of_lord_10}."
        )
    else:
        result["details"] = (
            f"Lord of 7th {lord_of_7} exalted: {is_exalted}, in 10th: {in_10th_house}. "
            f"10th lord ({lord_of_10}) in {house_of_lord_10}, 9th lord ({lord_of_9}) in {house_of_lord_9}. "
            f"Conjunct: {lords_conjunct}"
        )

    return result


@register_yogas(
    "Lagna Malika",
    "Dhana Malika",
    "Vikrama Malika",
    "Sukha Malika",
    "Putra Malika",
    "Satru Malika",
    "Kalatra Malika",
    "Randhra Malika",
    "Bhagya Malika",
    "Karma Malika",
    "Labha Malika",
    "Vraya Malika",
)
def Malika(yoga: Yoga) -> Dict[str, YogaType]:
    """All seven planets occupy seven houses continuously reckoned from starting house"""
    results: Dict[str, YogaType] = {}

    def is_consecutive(arr):
        arr = sorted(arr)
        return all(arr[i] + 1 == arr[i + 1] for i in range(len(arr) - 1))

    MALIKA_YOGAS = {
        1: ("Lagna Malika", "Positive"),
        2: ("Dhana Malika", "Positive"),
        3: ("Vikrama Malika", "Neutral"),
        4: ("Sukha Malika", "Positive"),
        5: ("Putra Malika", "Positive"),
        6: ("Satru Malika", "Negative"),
        7: ("Kalatra Malika", "Positive"),
        8: ("Randhra Malika", "Negative"),
        9: ("Bhagya Malika", "Positive"),
        10: ("Karma Malika", "Positive"),
        11: ("Labha Malika", "Positive"),
        12: ("Vraya Malika", "Positive"),
    }

    houses: HOUSES = []
    for planet in yoga.__chart__.get_planets():
        if planet["name"] in ["Rahu", "Ketu"]:
            continue

        h = yoga.get_house_of_planet(planet["name"])
        houses.append(h)
    houses.sort()

    for i in range(1, 13):
        yoga_name, type = MALIKA_YOGAS[i]
        present = False
        strength = 0.0
        if houses[0] == i or houses[-1] == i:
            if is_consecutive(houses):
                present = True
                strength = 1.0

        results[yoga_name] = {
            "id": "",
            "name": yoga_name,
            "present": present,
            "strength": strength,
            "details": f"{yoga_name}: {present}",
            "type": type,
        }

    return results


@register_yoga("Sankha")
def Sankha(yoga: Yoga) -> YogaType:
    """
    Lord of 5th and 6th house in mutual kendras and lord of lagna is powerful
    """
    result: YogaType = {
        "id": "",
        "name": "Sankha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get lords of 5th and 6th houses
    lord_of_5 = yoga.get_lord_of_house(5)
    lord_of_6 = yoga.get_lord_of_house(6)

    if not lord_of_5 or not lord_of_6:
        result["details"] = "Could not determine lords of 5th and 6th houses."
        return result

    # Get houses where these lords are located
    house_of_lord_5 = yoga.get_house_of_planet(lord_of_5)
    house_of_lord_6 = yoga.get_house_of_planet(lord_of_6)

    if not house_of_lord_5 or not house_of_lord_6:
        result["details"] = "Could not find houses for lords of 5th and 6th."
        return result

    # Check if they are in mutual kendras
    lord_5_in_kendra_from_lord_6 = yoga.planet_in_kendra_from(
        house_of_lord_6, lord_of_5
    )
    lord_6_in_kendra_from_lord_5 = yoga.planet_in_kendra_from(
        house_of_lord_5, lord_of_6
    )

    mutual_kendras = lord_5_in_kendra_from_lord_6 and lord_6_in_kendra_from_lord_5

    if not mutual_kendras:
        result["details"] = (
            f"Lords of 5th ({lord_of_5}) and 6th ({lord_of_6}) not in mutual kendras."
        )
        return result

    # Check if lord of lagna is powerful
    lagna_lord = yoga.get_lord_of_house(1)
    if not lagna_lord:
        result["details"] = "Could not determine lord of lagna."
        return result

    lagna_lord_planet = yoga.get_planet_by_name(lagna_lord)
    if not lagna_lord_planet:
        result["details"] = f"Could not find planet {lagna_lord}."
        return result

    is_powerful, lagna_lord_strength = yoga.isPlanetPowerful(lagna_lord_planet)

    if not is_powerful:
        result["details"] = f"Lord of lagna ({lagna_lord}) is not powerful."
        return result

    # Calculate strength based on mutual kendra positions
    relative_pos_5_from_6 = (house_of_lord_5 - house_of_lord_6 + 12) % 12 + 1
    relative_pos_6_from_5 = (house_of_lord_6 - house_of_lord_5 + 12) % 12 + 1

    kendra_strength_map = {1: 1.0, 4: 0.75, 7: 0.9, 10: 0.75}
    strength_5 = kendra_strength_map.get(relative_pos_5_from_6, 0.5)
    strength_6 = kendra_strength_map.get(relative_pos_6_from_5, 0.5)
    mutual_kendra_strength = (strength_5 + strength_6) / 2

    # Final strength is average of mutual kendra strength and lagna lord strength
    result["present"] = True
    result["strength"] = (mutual_kendra_strength + lagna_lord_strength) / 2
    result["details"] = (
        f"Lord of 5th ({lord_of_5}) in house {house_of_lord_5} and "
        f"Lord of 6th ({lord_of_6}) in house {house_of_lord_6} are in mutual kendras. "
        f"Lord of lagna ({lagna_lord}) is powerful."
    )

    return result


@register_yoga("Bheri")
def Bheri(yoga: Yoga) -> YogaType:
    """
    Venus and Jupiter in mutual Kendras and the lord of 9th is powerfully disposed.
    """
    result: YogaType = {
        "id": "",
        "name": "Bheri",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get houses where Venus and Jupiter are located
    house_of_venus = yoga.get_house_of_planet("Venus")
    house_of_jupiter = yoga.get_house_of_planet("Jupiter")

    if not house_of_venus or not house_of_jupiter:
        result["details"] = "Could not find houses for Venus and Jupiter."
        return result

    # Check if they are in mutual kendras
    venus_in_kendra_from_jupiter = yoga.planet_in_kendra_from(house_of_jupiter, "Venus")
    jupiter_in_kendra_from_venus = yoga.planet_in_kendra_from(house_of_venus, "Jupiter")

    mutual_kendras = venus_in_kendra_from_jupiter and jupiter_in_kendra_from_venus

    if not mutual_kendras:
        result["details"] = (
            f"Venus in house {house_of_venus} and Jupiter in house {house_of_jupiter} "
            f"are not in mutual kendras."
        )
        return result

    # Check if lord of 9th is powerful
    lord_of_9 = yoga.get_lord_of_house(9)
    if not lord_of_9:
        result["details"] = "Could not determine lord of 9th house."
        return result

    lord_of_9_planet = yoga.get_planet_by_name(lord_of_9)
    if not lord_of_9_planet:
        result["details"] = f"Could not find planet {lord_of_9}."
        return result

    is_powerful, lord_of_9_strength = yoga.isPlanetPowerful(lord_of_9_planet)

    if not is_powerful:
        result["details"] = f"Lord of 9th house ({lord_of_9}) is not powerful."
        return result

    # Calculate strength based on mutual kendra positions
    relative_pos_venus_from_jupiter = (house_of_venus - house_of_jupiter + 12) % 12 + 1
    relative_pos_jupiter_from_venus = (house_of_jupiter - house_of_venus + 12) % 12 + 1

    kendra_strength_map = {1: 1.0, 4: 0.75, 7: 0.9, 10: 0.75}
    strength_venus = kendra_strength_map.get(relative_pos_venus_from_jupiter, 0.5)
    strength_jupiter = kendra_strength_map.get(relative_pos_jupiter_from_venus, 0.5)
    mutual_kendra_strength = (strength_venus + strength_jupiter) / 2

    # Final strength is average of mutual kendra strength and lord of 9th strength
    result["present"] = True
    result["strength"] = (mutual_kendra_strength + lord_of_9_strength) / 2
    result["details"] = (
        f"Venus in house {house_of_venus} and Jupiter in house {house_of_jupiter} "
        f"are in mutual kendras. Lord of 9th house ({lord_of_9}) is powerful."
    )

    return result


@register_yoga("Gaja")
def Gaja(yoga: Yoga) -> YogaType:
    """
    Lord of the 9th from the 11th occupies the 11th in conjuction with the Moon and aspected by the lord of the 11th
    """
    result: YogaType = {
        "id": "",
        "name": "Gaja",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Calculate 9th house from 11th: (11 + 9 - 1) % 12 = 7
    lord_of_7 = yoga.get_lord_of_house(7)
    if not lord_of_7:
        result["details"] = "Could not determine lord of 7th house."
        return result

    # Get lord of 11th house
    lord_of_11 = yoga.get_lord_of_house(11)
    if not lord_of_11:
        result["details"] = "Could not determine lord of 11th house."
        return result

    # Check if lord of 7th is in house 11
    house_of_lord_7 = yoga.get_house_of_planet(lord_of_7)
    if not house_of_lord_7:
        result["details"] = f"Could not find house for lord of 7th ({lord_of_7})."
        return result

    if house_of_lord_7 != 11:
        result["details"] = (
            f"Lord of 7th ({lord_of_7}) is in house {house_of_lord_7}, not in 11th house."
        )
        return result

    # Check if Moon is in house 11 (conjunction with lord of 7th)
    moon_house = yoga.get_house_of_planet("Moon")
    if not moon_house:
        result["details"] = "Could not find Moon."
        return result

    if moon_house != 11:
        result["details"] = (
            f"Moon is in house {moon_house}, not in 11th house with lord of 7th."
        )
        return result

    # Check if lord of 11th aspects house 11
    chart = yoga.__chart__
    try:
        lord_of_11_aspects = chart.graha_drishti(n=1, planet=lord_of_11)[0]
        aspect_houses = lord_of_11_aspects.get("aspect_houses", [])
    except (KeyError, IndexError, TypeError):
        result["details"] = (
            f"Could not determine aspects of lord of 11th ({lord_of_11})."
        )
        return result

    is_aspect = any(11 in house_dict for house_dict in aspect_houses)
    if not is_aspect:
        result["details"] = f"Lord of 11th ({lord_of_11}) does not aspect house 11."
        return result

    # All conditions met - calculate strength
    # Strength based on conjunction (1.0) and aspect (0.8)
    conjunction_strength = 1.0  # Lord of 7th and Moon in same house
    aspect_strength = 0.8  # Lord of 11th aspects house 11

    # Check if lord of 7th is powerful for additional strength
    lord_of_7_planet = yoga.get_planet_by_name(lord_of_7)
    lord_of_7_power_strength = 0.5  # default
    if lord_of_7_planet:
        is_powerful, power_strength = yoga.isPlanetPowerful(lord_of_7_planet)
        if is_powerful:
            lord_of_7_power_strength = power_strength

    result["present"] = True
    result["strength"] = (
        conjunction_strength + aspect_strength + lord_of_7_power_strength
    ) / 3
    result["details"] = (
        f"Lord of 7th ({lord_of_7}) in house 11 in conjunction with Moon. "
        f"Lord of 11th ({lord_of_11}) aspects house 11."
    )

    return result


@register_yoga("Kalanidhi")
def Kalanidhi(yoga: Yoga) -> YogaType:
    """
    Jupiter is placed in the 2nd or 5th house, The sign in that house is owned by Me (Ge/Vi) or Ve (Ta/Li) and Jupiter is joined or associated with Mercury and Venus
    """
    result: YogaType = {
        "id": "",
        "name": "Kalanidhi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Check if Jupiter is in 2nd or 5th house
    jupiter_house = yoga.get_house_of_planet("Jupiter")
    if not jupiter_house:
        result["details"] = "Could not find Jupiter."
        return result

    if jupiter_house not in [2, 5]:
        result["details"] = (
            f"Jupiter is in house {jupiter_house}, not in 2nd or 5th house."
        )
        return result

    # Get the sign of Jupiter's house and check if it's Taurus, Libra, Gemini, or Virgo
    jupiter_house_sign = yoga.get_rashi_of_house(jupiter_house)
    if not jupiter_house_sign:
        result["details"] = f"Could not determine sign of house {jupiter_house}."
        return result

    # Check if the sign is Taurus, Libra, Gemini, or Virgo
    if jupiter_house_sign not in ["Taurus", "Libra", "Gemini", "Virgo"]:
        result["details"] = (
            f"Sign in house {jupiter_house} is {jupiter_house_sign}, "
            f"not Taurus, Libra, Gemini, or Virgo."
        )
        return result

    # Check if Jupiter is associated with Mercury (conjunction or aspect)
    mercury_house = yoga.get_house_of_planet("Mercury")
    if not mercury_house:
        result["details"] = "Could not find Mercury."
        return result

    # Check conjunction (same house)
    jupiter_mercury_conjunction = jupiter_house == mercury_house

    # Check aspect
    chart = yoga.__chart__
    jupiter_mercury_aspect = False
    try:
        mercury_aspects = chart.graha_drishti(n=1, planet="Mercury")[0]
        aspect_houses = mercury_aspects.get("aspect_houses", [])
        jupiter_mercury_aspect = any(
            jupiter_house in house_dict for house_dict in aspect_houses
        )
    except (KeyError, IndexError, TypeError):
        pass

    jupiter_mercury_associated = jupiter_mercury_conjunction or jupiter_mercury_aspect

    if not jupiter_mercury_associated:
        result["details"] = (
            f"Jupiter in house {jupiter_house} is not associated with Mercury "
            f"(Mercury in house {mercury_house})."
        )
        return result

    # Check if Jupiter is associated with Venus (conjunction or aspect)
    venus_house = yoga.get_house_of_planet("Venus")
    if not venus_house:
        result["details"] = "Could not find Venus."
        return result

    # Check conjunction (same house)
    jupiter_venus_conjunction = jupiter_house == venus_house

    # Check aspect
    jupiter_venus_aspect = False
    try:
        venus_aspects = chart.graha_drishti(n=1, planet="Venus")[0]
        aspect_houses = venus_aspects.get("aspect_houses", [])
        jupiter_venus_aspect = any(
            jupiter_house in house_dict for house_dict in aspect_houses
        )
    except (KeyError, IndexError, TypeError):
        pass

    jupiter_venus_associated = jupiter_venus_conjunction or jupiter_venus_aspect

    if not jupiter_venus_associated:
        result["details"] = (
            f"Jupiter in house {jupiter_house} is not associated with Venus "
            f"(Venus in house {venus_house})."
        )
        return result

    # All conditions met - calculate strength
    # Strength based on house position, sign ownership, and associations
    house_strength = 1.0 if jupiter_house == 5 else 0.9  # 5th house is stronger
    sign_ownership_strength = 1.0  # Already verified

    # Association strengths
    mercury_strength = 1.0 if jupiter_mercury_conjunction else 0.8
    venus_strength = 1.0 if jupiter_venus_conjunction else 0.8

    result["present"] = True
    result["strength"] = (
        house_strength + sign_ownership_strength + mercury_strength + venus_strength
    ) / 4
    result["details"] = (
        f"Jupiter in house {jupiter_house} ({jupiter_house_sign}). "
        f"Associated with Mercury (house {mercury_house}, "
        f"{'conjunction' if jupiter_mercury_conjunction else 'aspect'}) and "
        f"Venus (house {venus_house}, "
        f"{'conjunction' if jupiter_venus_conjunction else 'aspect'})."
    )

    return result


@register_yoga("Amsavatara")
def Amsavatara(yoga: Yoga) -> YogaType:
    """
    Venus and Jupiter in Kendras, the Lagna falls in a movable sign and Saturn must be exalted in a Kendra.
    """
    result: YogaType = {
        "id": "",
        "name": "Amsavatara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Get Lagna house and sign
    lagna_house = yoga.get_house_of_planet("Lagna")
    if not lagna_house:
        result["details"] = "Could not find Lagna."
        return result

    lagna_sign = yoga.get_rashi_of_house(lagna_house)
    if not lagna_sign:
        result["details"] = f"Could not determine sign of Lagna house {lagna_house}."
        return result

    # Check if Lagna is in a movable sign (Aries, Cancer, Libra, Capricorn)
    movable_signs = ["Aries", "Cancer", "Libra", "Capricorn"]
    if lagna_sign not in movable_signs:
        result["details"] = (
            f"Lagna is in {lagna_sign} (house {lagna_house}), not in a movable sign."
        )
        return result

    # Check if Venus is in a Kendra (from Lagna, house 1)
    venus_in_kendra = yoga.planet_in_kendra_from(lagna_house, "Venus")
    if not venus_in_kendra:
        venus_house = yoga.get_house_of_planet("Venus")
        result["details"] = (
            f"Venus is not in a Kendra from Lagna "
            f"(Venus in house {venus_house}, Lagna in house {lagna_house})."
        )
        return result

    # Check if Jupiter is in a Kendra (from Lagna, house 1)
    jupiter_in_kendra = yoga.planet_in_kendra_from(lagna_house, "Jupiter")
    if not jupiter_in_kendra:
        jupiter_house = yoga.get_house_of_planet("Jupiter")
        result["details"] = (
            f"Jupiter is not in a Kendra from Lagna "
            f"(Jupiter in house {jupiter_house}, Lagna in house {lagna_house})."
        )
        return result

    # Check if Saturn is exalted
    saturn_planet = yoga.get_planet_by_name("Saturn")
    if not saturn_planet:
        result["details"] = "Could not find Saturn."
        return result

    is_exalted = any(flag == "Exalted" for flag in saturn_planet["inSign"])
    if not is_exalted:
        result["details"] = "Saturn is not exalted."
        return result

    # Check if Saturn is in a Kendra (from Lagna, house 1)
    saturn_in_kendra = yoga.planet_in_kendra_from(lagna_house, "Saturn")
    if not saturn_in_kendra:
        saturn_house = yoga.get_house_of_planet("Saturn")
        result["details"] = (
            f"Saturn is exalted but not in a Kendra from Lagna "
            f"(Saturn in house {saturn_house}, Lagna in house {lagna_house})."
        )
        return result

    # All conditions met - calculate strength
    venus_house = yoga.get_house_of_planet("Venus")
    jupiter_house = yoga.get_house_of_planet("Jupiter")
    saturn_house = yoga.get_house_of_planet("Saturn")

    # Kendra strength map (1st=1.0, 4th=0.75, 7th=0.9, 10th=0.75)
    kendra_strength_map = {1: 1.0, 4: 0.75, 7: 0.9, 10: 0.75}

    # Calculate relative positions from Lagna
    def relative_house_from_lagna(planet_house: int) -> int:
        return (planet_house - lagna_house) % 12 + 1

    venus_relative = relative_house_from_lagna(venus_house)
    jupiter_relative = relative_house_from_lagna(jupiter_house)
    saturn_relative = relative_house_from_lagna(saturn_house)

    venus_strength = kendra_strength_map.get(venus_relative, 0.5)
    jupiter_strength = kendra_strength_map.get(jupiter_relative, 0.5)
    saturn_strength = kendra_strength_map.get(saturn_relative, 0.5)

    # Exaltation strength for Saturn
    saturn_exaltation_strength = 1.0

    # Movable sign strength
    movable_sign_strength = 1.0

    result["present"] = True
    result["strength"] = (
        venus_strength
        + jupiter_strength
        + saturn_strength
        + saturn_exaltation_strength
        + movable_sign_strength
    ) / 5
    result["details"] = (
        f"Venus in house {venus_house} (Kendra from Lagna), "
        f"Jupiter in house {jupiter_house} (Kendra from Lagna), "
        f"Lagna in {lagna_sign} (movable sign), "
        f"Saturn in house {saturn_house} (exalted, Kendra from Lagna)."
    )

    return result


@register_yoga("HariHaraBrahma")
def HariHaraBrahma(yoga: Yoga) -> YogaType:
    """
    Benefics are in the 8th or 12th house from the 2nd lord; or the Jupiter, the Moon and Mercury are in the 4th, 9th and 8th from the 7th lord, or the Sun, Venus and Mars are in the 4th, 10th and 11th from the lord of Lagna.
    """
    result: YogaType = {
        "id": "",
        "name": "Amsavatara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    cond1_present = False
    cond2_present = False
    cond3_present = False

    lord_of_2 = yoga.get_lord_of_house(2)
    if not lord_of_2:
        cond1_details = "Could not determine lord of 2nd house."
    else:
        planets_8th_from_L2 = yoga.planets_in_relative_house(lord_of_2, 8)
        planets_12th_from_L2 = yoga.planets_in_relative_house(lord_of_2, 12)

        benefics_in_8th = [
            p["name"] for p in planets_8th_from_L2 if p["name"] in BENEFIC_PLANETS
        ]
        benefics_in_12th = [
            p["name"] for p in planets_12th_from_L2 if p["name"] in BENEFIC_PLANETS
        ]

        if benefics_in_8th or benefics_in_12th:
            cond1_present = True
            cond1_details = f"Benefics in 8th ({', '.join(benefics_in_8th) or 'None'}) or 12th ({', '.join(benefics_in_12th) or 'None'}) from 2nd lord {lord_of_2}."

            total_benefics_found = len(benefics_in_8th) + len(benefics_in_12th)
            if total_benefics_found > 0:
                strength_sum = 0.0
                for p_name in benefics_in_8th + benefics_in_12th:
                    planet_obj = yoga.get_planet_by_name(p_name)
                    if planet_obj:
                        is_powerful, power_strength = yoga.isPlanetPowerful(planet_obj)
                        strength_sum += power_strength if is_powerful else 0.5
                cond1_strength = strength_sum / total_benefics_found
        else:
            cond1_details = f"No benefics in 8th or 12th from 2nd lord {lord_of_2}."

    # Condition 2: Jupiter, the Moon, and Mercury are in the 4th, 9th, and 8th from the 7th lord, respectively.
    cond2_present = False
    cond2_strength = 0.0
    cond2_details = ""

    lord_of_7 = yoga.get_lord_of_house(7)
    if not lord_of_7:
        cond2_details = "Could not determine lord of 7th house."
    else:
        ju_in_4th = yoga.relative_house(lord_of_7, "Jupiter") == 4
        mo_in_9th = yoga.relative_house(lord_of_7, "Moon") == 9
        me_in_8th = yoga.relative_house(lord_of_7, "Mercury") == 8

        if ju_in_4th and mo_in_9th and me_in_8th:
            cond2_present = True
            cond2_details = f"Jupiter in 4th, Moon in 9th, and Mercury in 8th from 7th lord {lord_of_7}."

            strength_sum = 0.0
            planets_to_check = ["Jupiter", "Moon", "Mercury"]

            for p_name in planets_to_check:
                planet_obj = yoga.get_planet_by_name(p_name)
                if planet_obj:
                    is_powerful, power_strength = yoga.isPlanetPowerful(planet_obj)
                    strength_sum += power_strength if is_powerful else 0.7
            cond2_strength = strength_sum / len(planets_to_check)
        else:
            cond2_details = f"Jupiter in 4th from {lord_of_7}: {ju_in_4th}, Moon in 9th from {lord_of_7}: {mo_in_9th}, Mercury in 8th from {lord_of_7}: {me_in_8th}."

    # Condition 3: The Sun, Venus, and Mars are in the 4th, 10th, and 11th from the lord of Lagna, respectively.
    cond3_present = False
    cond3_strength = 0.0
    cond3_details = ""

    lagna_lord = yoga.get_lord_of_house(1)
    if not lagna_lord:
        cond3_details = "Could not determine lord of Lagna."
    else:
        su_in_4th = yoga.relative_house(lagna_lord, "Sun") == 4
        ve_in_10th = yoga.relative_house(lagna_lord, "Venus") == 10
        ma_in_11th = yoga.relative_house(lagna_lord, "Mars") == 11

        if su_in_4th and ve_in_10th and ma_in_11th:
            cond3_present = True
            cond3_details = f"Sun in 4th, Venus in 10th, and Mars in 11th from Lagna lord {lagna_lord}."

            strength_sum = 0.0
            planets_to_check = ["Sun", "Venus", "Mars"]

            for p_name in planets_to_check:
                planet_obj = yoga.get_planet_by_name(p_name)
                if planet_obj:
                    is_powerful, power_strength = yoga.isPlanetPowerful(planet_obj)
                    strength_sum += power_strength if is_powerful else 0.7
            cond3_strength = strength_sum / len(planets_to_check)
        else:
            cond3_details = f"Sun in 4th from {lagna_lord}: {su_in_4th}, Venus in 10th from {lagna_lord}: {ve_in_10th}, Mars in 11th from {lagna_lord}: {ma_in_11th}."

    details_list = []
    total_strength = 0.0
    num_conditions_met = 0

    if cond1_present:
        result["present"] = True
        total_strength += cond1_strength
        num_conditions_met += 1
        details_list.append(f"Condition 1 met: {cond1_details}")
    else:
        details_list.append(f"Condition 1 not met: {cond1_details}")

    if cond2_present:
        result["present"] = True
        total_strength += cond2_strength
        num_conditions_met += 1
        details_list.append(f"Condition 2 met: {cond2_details}")
    else:
        details_list.append(f"Condition 2 not met: {cond2_details}")

    if cond3_present:
        result["present"] = True
        total_strength += cond3_strength
        num_conditions_met += 1
        details_list.append(f"Condition 3 met: {cond3_details}")
    else:
        details_list.append(f"Condition 3 not met: {cond3_details}")

    if result["present"]:
        result["strength"] = round(total_strength / num_conditions_met, 2)
        result["details"] = "HariHaraBrahma Yoga formed. " + " ".join(details_list)
    else:
        result["details"] = "HariHaraBrahma Yoga not formed. " + " ".join(details_list)

    return result


@register_yoga("Mridanga")
def Mridanga(yoga: Yoga) -> YogaType:
    """
    Lagna Lord must be powerful,
    9th lord must be powerful,
    9th house must get benefic influence
    """
    result: YogaType = {
        "id": "",
        "name": "Mridanga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    LL_name = yoga.get_lord_of_planet("Lagna")
    LL = yoga.get_planet_by_name(LL_name)
    LL_isPowerful = yoga.isPlanetPowerful(LL)

    if not LL_isPowerful:
        result["details"] = f"Lagna Lord, {LL_name} is not powerful"
        return result

    L9_name = yoga.get_lord_of_house(9)
    L9 = yoga.get_planet_by_name(L9_name)
    L9_isPowerful = yoga.isPlanetPowerful(L9)

    if not L9_isPowerful:
        result["details"] = f"Lord of 9th house, {L9_name} is not powerful"
        return result

    H9_is_benefic = yoga.is_house_benefic_aspected(9)
    if not H9_is_benefic:
        result["details"] = "9th House does have benefic planets influcence"
        return result

    result["present"] = True
    result["strength"] = 1
    result["details"] = (
        f"Lagna Lord {LL_name}, Lord of 9 {L9_name} are powerful and House 9 has benefic influence"
    )
    return result


@register_yoga("Parijatha")
def Parijatha(yoga: Yoga) -> YogaType:
    """
    Lagna Lord must be powerful, must be in Kendra/Trikona.
    Navamsa Lord of Lagna Lord must be powerful
    """
    result: YogaType = {
        "id": "",
        "name": "Parijatha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    LL_name = yoga.get_lord_of_planet("Lagna")
    LL = yoga.get_planet_by_name(LL_name)
    LL_isPowerful = yoga.isPlanetPowerful(LL)

    if not LL_isPowerful:
        result["details"] = f"Lagna Lord, {LL_name} is not powerful"
        return result

    LL_house = yoga.get_house_of_planet(LL_name)
    if LL_house not in [1, 4, 7, 10, 5, 9]:
        result["details"] = f"Lagna lord is placed in {LL_house} not in Kendra/Trikona"
        return result

    D9 = yoga.__chart__.get_varga_chakra_chart(9)

    for house, data in D9.items():
        for planet in data["planets"]:
            if planet["name"] == LL_name:
                NL_LL_name = RASHI_LORD_MAP[planet["sign"]]

    NL_LL = yoga.get_planet_by_name(NL_LL_name)
    if yoga.isPlanetPowerful(NL_LL):
        result["present"] = True
        result["strength"] = 1
        result["details"] = (
            f"LL {LL_name} is powerful and in Kendra/Trikona. Navamsa Lord of LL is also powerful in D1"
        )
    
    result["details"] = "Navamsa Lord of Lagna Lord is not powerful in D1"
    return result


@register_yoga("Kusuma")
def Kusuma(yoga: Yoga) -> YogaType:
    """
    Ju in Asc, Mo in 7th and Su in 2nd house
    """
    result: YogaType = {
        "id": "",
        "name": "Kusuma",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    Ju_house = yoga.get_house_of_planet("Jupiter")
    if Ju_house != 1:
        result["details"] = "Jupiter is not in Asc"
        return result
    
    Mo_house = yoga.get_house_of_planet("Moon")
    if Mo_house != 7:
        result["details"] = "Moon is not in 7th house"
        return result
    
    Su_house = yoga.get_house_of_planet("Sun")
    if Su_house != 2:
        result["details"] = "Sun is not in 2nd house"
        return result
    
    result["present"] = True
    result["strength"] = 1
    result["details"] = "Jupiter, Moon and Sun are in 1st, 7th and 2nd houses respectively"
    return result
