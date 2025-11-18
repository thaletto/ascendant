from typing import Dict, List
from ascendant.const import BENEFIC_PLANETS
from ascendant.types import PLANETS, RASHIS, YogaType
from ascendant.yoga.base import Yoga, register_yoga


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
    result["strength"] = (strength1 + strength2 + strength3 + strength4) / 4

    status = "formed" if result["present"] else "not formed"
    result["details"] = f"""Pushkala Yoga {status}
        \nCondition 1: {condition1} Strength 1: {strength1}
        \nCondition 2: {condition2} Strength 2: {strength2}
        \nCondition 3: {condition3} Strength 3: {strength3}
        \nCondition 4: {condition4} Strength 1: {strength4}
        \nTotal Strength: {result["strength"]}
        """

    return result
