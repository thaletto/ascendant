from typing import Dict
from ascendant.const import (
    BENEFIC_PLANETS,
    DEEP_EXALTATION_POINTS,
    MALEFIC_PLANETS,
    RASHI_LORD_MAP,
    CLASSICAL_PLANETS,
)
from ascendant.types import YogaType
from ascendant.yoga.base import Yoga, register_yoga, register_yogas


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
    result["details"] = (
        "Jupiter, Moon and Sun are in 1st, 7th and 2nd houses respectively"
    )
    return result


@register_yoga("Matsya")
def Matsya(yoga: Yoga) -> YogaType:
    """
    Lagna and the 9th are joined by malefics
    5th by both malefic and benefics
    4th and 8th are joined by malefics
    """
    result: YogaType = {
        "id": "",
        "name": "Matsya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Lagna (1st) and 9th joined by malefics
    planets_in_1 = yoga.planets_in_relative_house("Lagna", 1)
    planets_in_9 = yoga.planets_in_relative_house("Lagna", 9)
    malefics_in_1 = [p["name"] for p in planets_in_1 if p["name"] in MALEFIC_PLANETS]
    malefics_in_9 = [p["name"] for p in planets_in_9 if p["name"] in MALEFIC_PLANETS]
    if not (len(malefics_in_1) > 0 and len(malefics_in_9) > 0):
        result["details"] = (
            f"Malefics not found in both 1st ({', '.join(malefics_in_1) or 'None'}) and 9th ({', '.join(malefics_in_9) or 'None'}) houses."
        )
        return result

    # Condition 2: 5th by both malefic and benefics
    planets_in_5 = yoga.planets_in_relative_house("Lagna", 5)
    malefics_in_5 = [p["name"] for p in planets_in_5 if p["name"] in MALEFIC_PLANETS]
    benefics_in_5 = [p["name"] for p in planets_in_5 if p["name"] in BENEFIC_PLANETS]
    if not (len(malefics_in_5) > 0 and len(benefics_in_5) > 0):
        result["details"] = (
            f"Both malefics ({', '.join(malefics_in_5) or 'None'}) and benefics ({', '.join(benefics_in_5) or 'None'}) not found in 5th house."
        )
        return result

    # Condition 3: 4th and 8th joined by malefics
    planets_in_4 = yoga.planets_in_relative_house("Lagna", 4)
    planets_in_8 = yoga.planets_in_relative_house("Lagna", 8)
    malefics_in_4 = [p["name"] for p in planets_in_4 if p["name"] in MALEFIC_PLANETS]
    malefics_in_8 = [p["name"] for p in planets_in_8 if p["name"] in MALEFIC_PLANETS]
    if not (len(malefics_in_4) > 0 and len(malefics_in_8) > 0):
        result["details"] = (
            f"Malefics not found in both 4th ({', '.join(malefics_in_4) or 'None'}) and 8th ({', '.join(malefics_in_8) or 'None'}) houses."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Matsya Yoga are met."

    return result


@register_yoga("Kurma")
def Kurma(yoga: Yoga) -> YogaType:
    """
    Benefics occupy the 5th, 6th and 7th and join their exaltation, own or friendly Navamsas
    or
    Benefics occupy the 1st, 3rd, and 11th identical with their exaltation, own or friendly signs.
    """
    result: YogaType = {
        "id": "",
        "name": "Kurma",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition A: Benefics in 5, 6, 7 and dignified in D9
    benefics_in_5 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 5)
        if p["name"] in BENEFIC_PLANETS
    ]
    benefics_in_6 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 6)
        if p["name"] in BENEFIC_PLANETS
    ]
    benefics_in_7 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 7)
        if p["name"] in BENEFIC_PLANETS
    ]

    if len(benefics_in_5) > 0 and len(benefics_in_6) > 0 and len(benefics_in_7) > 0:
        all_benefics_A = benefics_in_5 + benefics_in_6 + benefics_in_7
        all_benefics_names_A = [p["name"] for p in all_benefics_A]

        dignified_benefics = 0
        d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
        dignity_details = []
        for benefic_name in all_benefics_names_A:
            for house_data in d9_chart.values():
                for planet in house_data["planets"]:
                    if planet["name"] == benefic_name:
                        sign = planet["sign"]["name"]
                        is_dignified = False
                        if benefic_name == "Mercury" and sign in ["Gemini", "Virgo"]:
                            is_dignified = True
                        elif benefic_name == "Jupiter" and sign in [
                            "Sagittarius",
                            "Pisces",
                            "Cancer",
                        ]:
                            is_dignified = True
                        elif benefic_name == "Venus" and sign in [
                            "Taurus",
                            "Libra",
                            "Pisces",
                        ]:
                            is_dignified = True

                        if is_dignified:
                            dignified_benefics += 1
                        dignity_details.append(
                            f"{benefic_name} in D9 sign {sign} (dignified: {is_dignified})"
                        )

        if dignified_benefics == len(all_benefics_names_A):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                "Benefics in 5th, 6th, 7th are all dignified in Navamsa.\n"
                + ", ".join(dignity_details)
            )
            return result

    # Condition B: Benefics in 1, 3, 11 and dignified in D1
    benefics_in_1 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 1)
        if p["name"] in BENEFIC_PLANETS
    ]
    benefics_in_3 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 3)
        if p["name"] in BENEFIC_PLANETS
    ]
    benefics_in_11 = [
        p
        for p in yoga.planets_in_relative_house("Lagna", 11)
        if p["name"] in BENEFIC_PLANETS
    ]

    if len(benefics_in_1) > 0 and len(benefics_in_3) > 0 and len(benefics_in_11) > 0:
        all_benefics_B = benefics_in_1 + benefics_in_3 + benefics_in_11

        dignified_count = 0
        dignity_details_B = []
        for p in all_benefics_B:
            is_dignified = "Exalted" in p["inSign"] or "Own" in p["inSign"]
            if is_dignified:
                dignified_count += 1
            dignity_details_B.append(
                f"{p['name']} in D1 sign (dignified: {is_dignified})"
            )

        if dignified_count == len(all_benefics_B):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                "Benefics in 1st, 3rd, 11th are all dignified in Rasi.\n"
                + ", ".join(dignity_details_B)
            )
            return result

    result["details"] = "Neither condition for Kurma Yoga was met."
    return result


@register_yoga("Devendra")
def Devendra(yoga: Yoga) -> YogaType:
    """
    Lagna is in fixed sign,
    the lords lagna and the 11th interchange their houses,
    and the lords of 2nd and 10th interchange their houses
    """
    result: YogaType = {
        "id": "",
        "name": "Devendra",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Lagna in a fixed sign
    lagna_house = yoga.get_house_of_planet("Lagna")
    lagna_rashi = yoga.get_rashi_of_house(lagna_house)
    fixed_signs = ["Taurus", "Leo", "Scorpio", "Aquarius"]
    if lagna_rashi not in fixed_signs:
        result["details"] = f"Lagna sign '{lagna_rashi}' is not a fixed sign."
        return result

    # Condition 2: Lords of 1st and 11th interchange houses
    lord_of_1 = yoga.get_lord_of_house(1)
    lord_of_11 = yoga.get_lord_of_house(11)
    if not lord_of_1 or not lord_of_11:
        result["details"] = "Could not determine lords of 1st or 11th house."
        return result
    house_of_lord_1 = yoga.get_house_of_planet(lord_of_1)
    house_of_lord_11 = yoga.get_house_of_planet(lord_of_11)
    if not (house_of_lord_1 == 11 and house_of_lord_11 == 1):
        result["details"] = (
            f"Lords of 1st ({lord_of_1} in {house_of_lord_1}) and 11th ({lord_of_11} in {house_of_lord_11}) do not interchange houses."
        )
        return result

    # Condition 3: Lords of 2nd and 10th interchange houses
    lord_of_2 = yoga.get_lord_of_house(2)
    lord_of_10 = yoga.get_lord_of_house(10)
    if not lord_of_2 or not lord_of_10:
        result["details"] = "Could not determine lords of 2nd or 10th house."
        return result
    house_of_lord_2 = yoga.get_house_of_planet(lord_of_2)
    house_of_lord_10 = yoga.get_house_of_planet(lord_of_10)
    if not (house_of_lord_2 == 10 and house_of_lord_10 == 2):
        result["details"] = (
            f"Lords of 2nd ({lord_of_2} in {house_of_lord_2}) and 10th ({lord_of_10} in {house_of_lord_10}) do not interchange houses."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Devendra Yoga are met."

    return result


@register_yoga("Makuta")
def Makuta(yoga: Yoga) -> YogaType:
    """
    Ju is in the 9th house from the 9th Lord
    A benefic is in the 9th from Ju
    Sa is in the 10th house
    """
    result: YogaType = {
        "id": "",
        "name": "Makuta",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    # Condition 1: Jupiter in 9th from 9th Lord
    lord_of_9 = yoga.get_lord_of_house(9)
    if not lord_of_9:
        result["details"] = "Could not determine lord of 9th."
        return result
    relative_pos_ju = yoga.relative_house(lord_of_9, "Jupiter")
    if relative_pos_ju != 9:
        result["details"] = (
            f"Jupiter is in {relative_pos_ju} from 9th lord ({lord_of_9}), not 9th."
        )
        return result

    # Condition 2: A benefic in 9th from Jupiter
    planets_9th_from_ju = yoga.planets_in_relative_house("Jupiter", 9)
    benefics_9th_from_ju = [
        p["name"] for p in planets_9th_from_ju if p["name"] in BENEFIC_PLANETS
    ]
    if not (len(benefics_9th_from_ju) > 0):
        result["details"] = "No benefics found in 9th house from Jupiter."
        return result

    # Condition 3: Saturn in 10th house
    house_of_saturn = yoga.get_house_of_planet("Saturn")
    if house_of_saturn != 10:
        result["details"] = f"Saturn is in house {house_of_saturn}, not 10th."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Makuta Yoga are met."

    return result


@register_yoga("Chandika")
def Chandika(yoga: Yoga) -> YogaType:
    """
    Lagna in fixed sign,
    Lagna aspected by Lord of 6th
    and Navamsa Lords of Lords of 6th and 9th must be cojoined with Su,
    """
    result: YogaType = {
        "id": "",
        "name": "Chandika",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Lagna in a fixed sign
    lagna_house = yoga.get_house_of_planet("Lagna")
    lagna_rashi = yoga.get_rashi_of_house(lagna_house)
    fixed_signs = ["Taurus", "Leo", "Scorpio", "Aquarius"]
    if lagna_rashi not in fixed_signs:
        result["details"] = f"Lagna sign '{lagna_rashi}' is not a fixed sign."
        return result

    # Condition 2: Lagna aspected by Lord of 6th
    lord_of_6 = yoga.get_lord_of_house(6)
    if not lord_of_6:
        result["details"] = "Could not determine lord of 6th."
        return result
    try:
        lord_of_6_aspects = yoga.__chart__.graha_drishti(n=1, planet=lord_of_6)[0]
        aspect_houses = lord_of_6_aspects.get("aspect_houses", [])
        if not any(lagna_house in house_dict for house_dict in aspect_houses):
            result["details"] = f"Lagna is not aspected by 6th lord ({lord_of_6})."
            return result
    except (KeyError, IndexError, TypeError):
        result["details"] = f"Could not get aspects for {lord_of_6}."
        return result

    # Condition 3: Navamsa Lords of L6 and L9 cojoined with Sun
    L6 = lord_of_6
    L9 = yoga.get_lord_of_house(9)
    if not L9:
        result["details"] = "Could not determine lord of 9th."
        return result

    D9 = yoga.__chart__.get_varga_chakra_chart(9)
    NSL6, NSL9 = None, None
    for _house, data in D9.items():
        for planet in data["planets"]:
            if planet["name"] == L6:
                NSL6 = RASHI_LORD_MAP.get(planet["sign"]["name"])
            if planet["name"] == L9:
                NSL9 = RASHI_LORD_MAP.get(planet["sign"]["name"])

    if not NSL6 or not NSL9:
        result["details"] = f"Could not find Navamsa lords for {L6} or {L9}."
        return result

    house_nsl6 = yoga.get_house_of_planet(NSL6)
    house_nsl9 = yoga.get_house_of_planet(NSL9)
    house_sun = yoga.get_house_of_planet("Sun")

    if not (house_nsl6 and house_nsl9 and house_sun):
        result["details"] = "Could not find houses for NSL6, NSL9, or Sun."
        return result

    if not (house_nsl6 == house_sun and house_nsl9 == house_sun):
        result["details"] = (
            f"Navamsa lords of L6({NSL6} in {house_nsl6}) and L9({NSL9} in {house_nsl9}) are not co-joined with Sun (in {house_sun})."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Chandika Yoga are met."

    return result


@register_yoga("Jaya")
def Jaya(yoga: Yoga) -> YogaType:
    """
    The lord of 6th is debliated and the lord of 10th is deep exaltation (+/- 5 degree from deep exaltation degree)
    """
    result: YogaType = {
        "id": "",
        "name": "Jaya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Lord of 6th is debilitated
    lord_of_6 = yoga.get_lord_of_house(6)
    if not lord_of_6:
        result["details"] = "Could not determine lord of 6th."
        return result
    p6 = yoga.get_planet_by_name(lord_of_6)
    if not p6 or "Debilitated" not in p6["inSign"]:
        result["details"] = f"Lord of 6th ({lord_of_6}) is not debilitated."
        return result

    # Condition 2: Lord of 10th is in deep exaltation
    lord_of_10 = yoga.get_lord_of_house(10)
    if not lord_of_10:
        result["details"] = "Could not determine lord of 10th."
        return result
    p10 = yoga.get_planet_by_name(lord_of_10)
    if not p10:
        result["details"] = f"Could not find planet object for {lord_of_10}. "
        return result

    p10_name = p10["name"]
    if p10_name not in DEEP_EXALTATION_POINTS:
        result["details"] = f"{p10_name} does not have a deep exaltation point."
        return result

    exaltation_info = DEEP_EXALTATION_POINTS[p10_name]
    p10_house = yoga.get_house_of_planet(p10_name)
    p10_sign = yoga.get_rashi_of_house(p10_house)

    if p10_sign != exaltation_info["sign"]:
        result["details"] = (
            f"{p10_name} is in {p10_sign}, not its exaltation sign {exaltation_info['sign']}. "
        )
        return result

    p10_degree = p10["longitude"] % 30
    exalt_degree = exaltation_info["degree"]
    if not (abs(p10_degree - exalt_degree) <= 5):
        result["details"] = (
            f"{p10_name} at {p10_degree:.2f} is not within 5 degrees of deep exaltation point ({exalt_degree})."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Jaya Yoga are met."
    return result


@register_yoga("Vidyut")
def Vidyut(yoga: Yoga) -> YogaType:
    """
    The 11th lord is in deep exaltation (+/- 5 degree from deep exaltation degree)
    and joins Venus in a Kendra from the lord of Lagna
    """
    result: YogaType = {
        "id": "",
        "name": "Vidyut",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: 11th lord in deep exaltation
    lord_of_11 = yoga.get_lord_of_house(11)
    if not lord_of_11:
        result["details"] = "Could not determine lord of 11th."
        return result
    p11 = yoga.get_planet_by_name(lord_of_11)
    if not p11:
        result["details"] = f"Could not find planet object for {lord_of_11}. "
        return result

    p11_name = p11["name"]
    if p11_name not in DEEP_EXALTATION_POINTS:
        result["details"] = f"{p11_name} does not have a deep exaltation point."
        return result

    exaltation_info = DEEP_EXALTATION_POINTS[p11_name]
    p11_house = yoga.get_house_of_planet(p11_name)
    p11_sign = yoga.get_rashi_of_house(p11_house)

    if p11_sign != exaltation_info["sign"]:
        result["details"] = (
            f"{p11_name} is in {p11_sign}, not its exaltation sign {exaltation_info['sign']}. "
        )
        return result

    p11_degree = p11["longitude"] % 30
    exalt_degree = exaltation_info["degree"]
    if not (abs(p11_degree - exalt_degree) <= 5):
        result["details"] = (
            f"{p11_name} at {p11_degree:.2f} is not within 5 degrees of deep exaltation point ({exalt_degree})."
        )
        return result

    # Condition 2: joins Venus in a Kendra from the lord of Lagna
    house_of_l11 = yoga.get_house_of_planet(lord_of_11)
    house_of_venus = yoga.get_house_of_planet("Venus")
    if house_of_l11 != house_of_venus:
        result["details"] = (
            f"11th lord ({lord_of_11}) and Venus are not in the same house."
        )
        return result

    lord_of_1 = yoga.get_lord_of_house(1)
    if not lord_of_1:
        result["details"] = "Could not determine lord of Lagna."
        return result

    base_house = yoga.get_house_of_planet(lord_of_1)
    if not base_house:
        result["details"] = f"Could not find house of Lagna lord ({lord_of_1})."
        return result

    target_house = house_of_l11
    kendra_offsets = [1, 4, 7, 10]
    kendra_houses = [
        ((base_house - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets
    ]
    if target_house not in kendra_houses:
        result["details"] = (
            f"House of 11th lord and Venus ({target_house}) is not in a Kendra from Lagna lord's house ({base_house})."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Vidyut Yoga are met."
    return result


@register_yoga("Gandharva")
def Gandharva(yoga: Yoga) -> YogaType:
    """
    The 10th Lord is in the Kama Trikona (3, 7, 11) and the Lord of Lagna and Jupiter are in association
    The Sun being exalted and the Moon occupies the 9th
    """
    result: YogaType = {
        "id": "",
        "name": "Gandharva",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: 10th Lord in Kama Trikona (3, 7, 11)
    lord_of_10 = yoga.get_lord_of_house(10)
    if not lord_of_10:
        result["details"] = "Could not determine lord of 10th."
        return result
    house_of_l10 = yoga.get_house_of_planet(lord_of_10)
    if house_of_l10 not in [3, 7, 11]:
        result["details"] = (
            f"10th lord ({lord_of_10}) is in house {house_of_l10}, not in a Kama Trikona (3, 7, 11)."
        )
        return result

    # Condition 2: Lord of Lagna and Jupiter are in association
    lord_of_1 = yoga.get_lord_of_house(1)
    if not lord_of_1:
        result["details"] = "Could not determine lord of Lagna."
        return result
    house_of_l1 = yoga.get_house_of_planet(lord_of_1)
    house_of_ju = yoga.get_house_of_planet("Jupiter")
    if house_of_l1 != house_of_ju:
        result["details"] = "Lagna lord and Jupiter are not in the same house."
        return result

    # Condition 3: Sun is exalted
    sun_planet = yoga.get_planet_by_name("Sun")
    if not sun_planet or "Exalted" not in sun_planet["inSign"]:
        result["details"] = "Sun is not exalted."
        return result

    # Condition 4: Moon occupies the 9th
    moon_house = yoga.get_house_of_planet("Moon")
    if moon_house != 9:
        result["details"] = f"Moon is in house {moon_house}, not the 9th."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Gandharva Yoga are met."
    return result


@register_yoga("Vishnu")
def Vishnu(yoga: Yoga) -> YogaType:
    """
    The lord of the Navamsa in which the 9th lord is placed
    and the 10th lord joins the 2nd house in conjunction with the 9th lord
    """
    result: YogaType = {
        "id": "",
        "name": "Vishnu",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l9 = yoga.get_lord_of_house(9)
    l10 = yoga.get_lord_of_house(10)
    if not l9 or not l10:
        result["details"] = "Could not determine lord of 9th or 10th."
        return result

    # Condition: l9, l10 and NL9L must be in the 2nd house
    house_of_l9 = yoga.get_house_of_planet(l9)
    house_of_l10 = yoga.get_house_of_planet(l10)

    if house_of_l9 != 2 or house_of_l10 != 2:
        result["details"] = (
            f"9th lord ({l9} in {house_of_l9}) and 10th lord ({l10} in {house_of_l10}) are not both in the 2nd house."
        )
        return result

    # Find Navamsa lord of L9's Navamsa sign (NL9L)
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    l9_d9_sign = None
    for _house, data in d9_chart.items():
        for planet in data["planets"]:
            if planet["name"] == l9:
                l9_d9_sign = planet["sign"]["name"]
                break
        if l9_d9_sign:
            break

    if not l9_d9_sign:
        result["details"] = f"Could not find {l9} in the Navamsa chart."
        return result

    NL9L = RASHI_LORD_MAP.get(l9_d9_sign)
    if not NL9L:
        result["details"] = (
            f"Could not determine the lord of Navamsa sign {l9_d9_sign}. "
        )
        return result

    house_of_nl9l = yoga.get_house_of_planet(NL9L)
    if house_of_nl9l != 2:
        result["details"] = (
            f"Navamsa lord of 9th lord ({NL9L}) is not in the 2nd house."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = (
        f"9th lord ({l9}), 10th lord ({l10}), and Navamsa lord of 9th lord ({NL9L}) are all in the 2nd house."
    )
    return result


@register_yoga("Brahma")
def Brahma(yoga: Yoga) -> YogaType:
    """
    Jupiter and Venus are in Kendras respectively from the lords of the 9th and 11th
    and Mercury is in Kendras from the lord of either Lagna or the 10th
    """
    result: YogaType = {
        "id": "",
        "name": "Brahma",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    kendra_offsets = [1, 4, 7, 10]

    # Condition 1: Jupiter in Kendra from 9th lord
    l9 = yoga.get_lord_of_house(9)
    if not l9:
        result["details"] = "Could not determine lord of 9th."
        return result
    h_l9 = yoga.get_house_of_planet(l9)
    h_ju = yoga.get_house_of_planet("Jupiter")
    if not h_l9 or not h_ju:
        result["details"] = "Could not locate 9th lord or Jupiter."
        return result
    kendra_from_l9 = [((h_l9 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]
    if h_ju not in kendra_from_l9:
        result["details"] = "Jupiter is not in a Kendra from the 9th lord."
        return result

    # Condition 2: Venus in Kendra from 11th lord
    l11 = yoga.get_lord_of_house(11)
    if not l11:
        result["details"] = "Could not determine lord of 11th."
        return result
    h_l11 = yoga.get_house_of_planet(l11)
    h_ve = yoga.get_house_of_planet("Venus")
    if not h_l11 or not h_ve:
        result["details"] = "Could not locate 11th lord or Venus."
        return result
    kendra_from_l11 = [((h_l11 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]
    if h_ve not in kendra_from_l11:
        result["details"] = "Venus is not in a Kendra from the 11th lord."
        return result

    # Condition 3: Mercury in Kendra from Lagna lord OR 10th lord
    l1 = yoga.get_lord_of_house(1)
    l10 = yoga.get_lord_of_house(10)
    if not l1 or not l10:
        result["details"] = "Could not determine lord of 1st or 10th."
        return result
    h_l1 = yoga.get_house_of_planet(l1)
    h_l10 = yoga.get_house_of_planet(l10)
    h_me = yoga.get_house_of_planet("Mercury")
    if not h_l1 or not h_l10 or not h_me:
        result["details"] = "Could not locate 1st lord, 10th lord or Mercury."
        return result

    kendra_from_l1 = [((h_l1 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]
    kendra_from_l10 = [((h_l10 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]

    me_kendra_l1 = h_me in kendra_from_l1
    me_kendra_l10 = h_me in kendra_from_l10

    if not (me_kendra_l1 or me_kendra_l10):
        result["details"] = (
            "Mercury is not in a Kendra from either the Lagna lord or the 10th lord."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0

    details_parts = []
    details_parts.append(f"Jupiter (h{h_ju}) in Kendra from 9th lord ({l9} in h{h_l9})")
    details_parts.append(
        f"Venus (h{h_ve}) in Kendra from 11th lord ({l11} in h{h_l11})"
    )

    mercury_kendra_details = []
    if me_kendra_l1:
        mercury_kendra_details.append(f"Lagna lord ({l1} in h{h_l1})")
    if me_kendra_l10:
        mercury_kendra_details.append(f"10th lord ({l10} in h{h_l10})")

    if mercury_kendra_details:
        details_parts.append(
            f"Mercury (h{h_me}) in Kendra from {' and '.join(mercury_kendra_details)}"
        )

    result["details"] = "; ".join(details_parts)
    return result


@register_yoga("Indra")
def Indra(yoga: Yoga) -> YogaType:
    """
    The lord of the 5th and 11th interchange their houses and the Moon is in the 5th
    """
    result: YogaType = {
        "id": "",
        "name": "Indra",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    # Condition 1: Lord of 5th and 11th interchange
    l5 = yoga.get_lord_of_house(5)
    l11 = yoga.get_lord_of_house(11)
    if not l5 or not l11:
        result["details"] = "Could not determine lord of 5th or 11th."
        return result

    h_l5 = yoga.get_house_of_planet(l5)
    h_l11 = yoga.get_house_of_planet(l11)

    if not (h_l5 == 11 and h_l11 == 5):
        result["details"] = "Lords of 5th and 11th do not interchange houses."
        return result

    # Condition 2: Moon is in the 5th
    h_mo = yoga.get_house_of_planet("Moon")
    if h_mo != 5:
        result["details"] = "Moon is not in the 5th house."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Indra Yoga are met."
    return result


@register_yoga("Ravi")
def Ravi(yoga: Yoga) -> YogaType:
    """
    The Sun joins the 10th and the lord of 10th must be in 3rd in conjunction with Saturn
    """
    result: YogaType = {
        "id": "",
        "name": "Ravi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Sun in 10th house
    h_su = yoga.get_house_of_planet("Sun")
    if h_su != 10:
        result["details"] = "Sun is not in the 10th house."
        return result

    # Condition 2: Lord of 10th in 3rd with Saturn
    l10 = yoga.get_lord_of_house(10)
    if not l10:
        result["details"] = "Could not determine lord of 10th."
        return result
    h_l10 = yoga.get_house_of_planet(l10)
    h_sa = yoga.get_house_of_planet("Saturn")

    if not (h_l10 == 3 and h_sa == 3):
        result["details"] = (
            "Lord of 10th is not in the 3rd house in conjunction with Saturn."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Ravi Yoga are met."
    return result


@register_yoga("Go")
def Go(yoga: Yoga) -> YogaType:
    """
    Jupiter in Moolatrikona with the lord of the 2nd house and the lord of Lagna is in exaltation
    """
    result: YogaType = {
        "id": "",
        "name": "Go",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1: Jupiter in Moolatrikona and with 2nd lord
    p_ju = yoga.get_planet_by_name("Jupiter")
    if not p_ju or "Moola Trikona" not in p_ju["inSign"]:
        result["details"] = "Jupiter is not in Moolatrikona."
        return result

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        result["details"] = "Could not determine lord of 2nd."
        return result

    h_ju = yoga.get_house_of_planet("Jupiter")
    h_l2 = yoga.get_house_of_planet(l2)
    if h_ju != h_l2:
        result["details"] = "Jupiter is not in conjunction with the 2nd lord."
        return result

    # Condition 2: Lord of Lagna is in exaltation
    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not determine lord of Lagna."
        return result

    p_l1 = yoga.get_planet_by_name(l1)
    if not p_l1 or "Exalted" not in p_l1["inSign"]:
        result["details"] = "Lord of Lagna is not exalted."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "All conditions for Go Yoga are met."
    return result


@register_yoga("Thrilochana")
def Thrilochana(yoga: Yoga) -> YogaType:
    """
    The Sun, Moon and Mars are in trines with each other
    """
    result: YogaType = {
        "id": "",
        "name": "Thrilochana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    h_su = yoga.get_house_of_planet("Sun")
    h_mo = yoga.get_house_of_planet("Moon")
    h_ma = yoga.get_house_of_planet("Mars")

    if not all([h_su, h_mo, h_ma]):
        details = []
        if not h_su:
            details.append("Sun")
        if not h_mo:
            details.append("Moon")
        if not h_ma:
            details.append("Mars")
        result["details"] = f"Could not locate: {', '.join(details)}."
        return result

    # A grand trine means planets are in signs of the same element,
    # which are 4 signs (120 degrees) apart.
    # e.g., houses 1, 5, 9 or 2, 6, 10 etc.
    houses = sorted([h_su, h_mo, h_ma])

    # The difference between sorted house numbers must be 4.
    if (houses[1] - houses[0] == 4) and (houses[2] - houses[1] == 4):
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"Sun, Moon, and Mars are in a grand trine at houses {h_su}, {h_mo}, and {h_ma}. "
        )
    else:
        result["details"] = (
            f"Sun (h{h_su}), Moon (h{h_mo}), and Mars (h{h_ma}) do not form a grand trine."
        )

    return result


@register_yoga("Kulavardhana")
def Kulavardhana(yoga: Yoga) -> YogaType:
    """
    All planets are in the 5th house from either Lagna, the Sun and the Moon
    Shadow planets are not considered
    """
    result: YogaType = {
        "id": "",
        "name": "Kulavardhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}
    if not all(planet_locations.values()):
        missing = [p for p, h in planet_locations.items() if h is None]
        result["details"] = (
            f"Could not locate all classical planets: {', '.join(missing)}."
        )
        return result

    # Check if all planets are in the same house
    occupied_houses = set(planet_locations.values())
    if len(occupied_houses) > 1:
        planets_by_house = {}
        for p, h in planet_locations.items():
            if h not in planets_by_house:
                planets_by_house[h] = []
            planets_by_house[h].append(p)
        details_list = []
        for h in sorted(planets_by_house.keys()):
            details_list.append(f"House {h}: {', '.join(planets_by_house[h])}")
        result["details"] = (
            f"Classical planets are not in a single house. Planet distribution: {'; '.join(details_list)}"
        )
        return result

    the_house = occupied_houses.pop()
    planets_in_the_house = list(planet_locations.keys())

    # Case 1: 5th house from Lagna
    if the_house == 5:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"All classical planets ({', '.join(planets_in_the_house)}) are in the 5th house from Lagna."
        )
        return result

    # Case 2: 5th house from Sun
    h_su = yoga.get_house_of_planet("Sun")
    if h_su:
        target_house_from_sun = ((h_su - 1 + 4) % 12) + 1
        if the_house == target_house_from_sun:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"All classical planets ({', '.join(planets_in_the_house)}) are in house {the_house}, which is the 5th from the Sun (in house {h_su})."
            )
            return result

    # Case 3: 5th house from Moon
    h_mo = yoga.get_house_of_planet("Moon")
    if h_mo:
        target_house_from_moon = ((h_mo - 1 + 4) % 12) + 1
        if the_house == target_house_from_moon:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"All classical planets ({', '.join(planets_in_the_house)}) are in house {the_house}, which is the 5th from the Moon (in house {h_mo})."
            )
            return result

    result["details"] = (
        f"All classical planets are in house {the_house}, but this is not the 5th from Lagna, Sun, or Moon. "
        f"5th from Lagna is 5. 5th from Sun (in house {h_su}) is {((h_su - 1 + 4) % 12) + 1}. 5th from Moon (in house {h_mo}) is {((h_mo - 1 + 4) % 12) + 1}."
    )
    return result


@register_yogas("Yupa", "Ishu", "Sakti", "Danda", "Nav", "Kuta", "Chhatra", "Chapa")
def AkritiYogas(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Yupa: Planets occupy four consecutive houses starting from the Lagna.
    Ishu: Planets occupy four consecutive houses starting from the Nadir (fourth house).
    Sakti: Planets occupy four consecutive houses starting from the 7th house.
    Danda: Planets occupy four consecutive houses starting from the 10th house.
    Nav: All seven planets in seven consecutive houses starting from the 1st.
    Kuta: All seven planets in seven consecutive houses starting from the 4th.
    Chhatra: All seven planets in seven consecutive houses starting from the 7th.
    Chapa: All seven planets in seven consecutive houses starting from the 10th.

    Shadow planets are not considered.
    """
    yoga_definitions = {
        "Yupa": {"house_count": 4, "start_house": 1, "type": "Positive"},
        "Ishu": {"house_count": 4, "start_house": 4, "type": "Positive"},
        "Sakti": {"house_count": 4, "start_house": 7, "type": "Negative"},
        "Danda": {"house_count": 4, "start_house": 10, "type": "Negative"},
        "Nav": {"house_count": 7, "start_house": 1, "type": "Neutral"},
        "Kuta": {"house_count": 7, "start_house": 4, "type": "Negative"},
        "Chhatra": {"house_count": 7, "start_house": 7, "type": "Positive"},
        "Chapa": {"house_count": 7, "start_house": 10, "type": "Positive"},
    }

    results: Dict[str, YogaType] = {
        name: {
            "id": "",
            "name": name,
            "present": False,
            "strength": 0.0,
            "details": f"Condition for {name} Yoga not met.",
            "type": definition["type"],
        }
        for name, definition in yoga_definitions.items()
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        for name in results:
            results[name]["details"] = "Could not locate all classical planets."
        return results

    for name, definition in yoga_definitions.items():
        required_house_count = definition["house_count"]
        start_house = definition["start_house"]

        required_houses_set = {
            ((start_house + i - 1) % 12) + 1 for i in range(required_house_count)
        }

        occupied_houses = set(planet_locations.values())

        condition_met = False
        if required_house_count == 4 and occupied_houses.issubset(required_houses_set):
            condition_met = True
        elif required_house_count == 7 and occupied_houses == required_houses_set:
            condition_met = True

        if condition_met:
            results[name]["present"] = True
            results[name]["strength"] = 1.0

            planets_by_house = {}
            for p, h in planet_locations.items():
                if h not in planets_by_house:
                    planets_by_house[h] = []
                planets_by_house[h].append(p)

            details_list = []
            for h in sorted(list(required_houses_set)):
                planets_str = ", ".join(planets_by_house.get(h, []))
                details_list.append(
                    f"House {h}: {planets_str if planets_str else 'Empty'}"
                )

            results[name]["details"] = (
                f"All {required_house_count} classical planets are in {required_house_count} consecutive houses starting from house {start_house}. Planets found: {'; '.join(details_list)}."
            )
        else:
            outside_planets = []
            for planet, house in planet_locations.items():
                if house not in required_houses_set:
                    outside_planets.append(f"{planet} in house {house}")

            results[name]["details"] = (
                f"For {name} Yoga, all {required_house_count} classical planets must be in houses {', '.join(map(str, sorted(list(required_houses_set))))}. Planets outside this range: {', '.join(outside_planets)}."
            )

    return results


@register_yoga("Ardha Chandra")
def ArdhaChandra(yoga: Yoga) -> YogaType:
    """
    All planets occupy seven consecutive houses not starting from 1, 4, 7, 10
    """
    result: YogaType = {
        "id": "",
        "name": "Ardha Chandra",
        "present": False,
        "strength": 0.0,
        "details": "ArdhaChandra Yoga not formed.",
        "type": "Positive",
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    if len(occupied_houses) != 7:
        result["details"] = (
            f"The 7 classical planets do not occupy exactly 7 unique houses. They occupy {len(occupied_houses)} houses: {sorted(list(occupied_houses))}"
        )
        return result

    for start_house in range(1, 13):
        # Exclude starts for Nav, Kuta, Chhatra, Chapa
        if start_house in [1, 4, 7, 10]:
            continue

        consecutive_houses = {(start_house + i - 1) % 12 + 1 for i in range(7)}
        if occupied_houses == consecutive_houses:
            result["present"] = True
            result["strength"] = 1.0

            planets_by_house = {}
            for p, h in planet_locations.items():
                if h not in planets_by_house:
                    planets_by_house[h] = []
                planets_by_house[h].append(p)

            details_list = []
            for h in sorted(list(consecutive_houses)):
                planets_str = ", ".join(planets_by_house.get(h, []))
                details_list.append(
                    f"House {h}: {planets_str if planets_str else 'Empty'}"
                )

            result["details"] = (
                f"ArdhaChandra Yoga is formed. All 7 classical planets are in 7 consecutive houses starting from house {start_house}. Planet positions: {'; '.join(details_list)}"
            )
            return result

    return result


@register_yoga("Chandra")
def Chandra(yoga: Yoga) -> YogaType:
    """
    All planets occupy the 1, 3, 5, 7, 9 and 11th houses.
    """
    result: YogaType = {
        "id": "",
        "name": "Chandra",
        "present": False,
        "strength": 0.0,
        "details": "Chandra Yoga not formed.",
        "type": "Positive",
    }

    required_houses = {1, 3, 5, 7, 9, 11}
    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    if occupied_houses == required_houses:
        result["present"] = True
        result["strength"] = 1.0

        planets_by_house = {}
        for p, h in planet_locations.items():
            if h not in planets_by_house:
                planets_by_house[h] = []
            planets_by_house[h].append(p)

        details_list = []
        for h in sorted(list(required_houses)):
            planets_str = ", ".join(planets_by_house.get(h, []))
            details_list.append(f"House {h}: {planets_str if planets_str else 'Empty'}")

        result["details"] = (
            f"Chandra Yoga is formed. All planets are in houses 1, 3, 5, 7, 9, 11. Planet positions: {'; '.join(details_list)}"
        )
    else:
        result["details"] = (
            f"Chandra Yoga not formed. All planets are not in houses 1, 3, 5, 7, 9, 11. Occupied houses: {sorted(list(occupied_houses))}"
        )

    return result


@register_yogas("Gada Kendra Stithi", "Sakata Kendra Stithi", "Vihaga Kendra Stithi")
def KendraStithiYogas(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Gada Kendra Stithi: All planets occupy adjacent kendra houses.
    Sakata Kendra Stithi: All planets occupy 1st and 7th kendra houses.
    Vihaga Kendra Stithi: All planets occupy 4th and 10th kendra houses.
    """
    results: Dict[str, YogaType] = {
        "Gada Kendra Stithi": {
            "id": "",
            "name": "Gada Kendra Stithi",
            "present": False,
            "strength": 0.0,
            "details": "Gada Yoga not formed.",
            "type": "Positive",
        },
        "Sakata Kendra Stithi": {
            "id": "",
            "name": "Sakata Kendra Stithi",
            "present": False,
            "strength": 0.0,
            "details": "Sakata Yoga not formed.",
            "type": "Negative",
        },
        "Vihaga Kendra Stithi": {
            "id": "",
            "name": "Vihaga Kendra Stithi",
            "present": False,
            "strength": 0.0,
            "details": "Vihaga Yoga not formed.",
            "type": "Negative",
        },
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        for name in results:
            results[name]["details"] = "Could not locate all classical planets."
        return results

    occupied_houses = set(planet_locations.values())
    occupied_houses_str = ", ".join(map(str, sorted(list(occupied_houses))))

    # Sakata
    if occupied_houses.issubset({1, 7}):
        results["Sakata Kendra Stithi"]["present"] = True
        results["Sakata Kendra Stithi"]["strength"] = 1.0
        results["Sakata Kendra Stithi"]["details"] = (
            f"Sakata Yoga formed. All planets are in houses 1 and 7. Occupied houses: {occupied_houses_str}"
        )
    else:
        results["Sakata Kendra Stithi"]["details"] = (
            f"Sakata Yoga not formed. All planets must be in houses 1 and 7. Occupied houses: {occupied_houses_str}"
        )

    # Vihaga
    if occupied_houses.issubset({4, 10}):
        results["Vihaga Kendra Stithi"]["present"] = True
        results["Vihaga Kendra Stithi"]["strength"] = 1.0
        results["Vihaga Kendra Stithi"]["details"] = (
            f"Vihaga Yoga formed. All planets are in houses 4 and 10. Occupied houses: {occupied_houses_str}"
        )
    else:
        results["Vihaga Kendra Stithi"]["details"] = (
            f"Vihaga Yoga not formed. All planets must be in houses 4 and 10. Occupied houses: {occupied_houses_str}"
        )

    # Gada
    gada_pairs = [{1, 4}, {4, 7}, {7, 10}, {10, 1}]
    gada_formed = False
    for pair in gada_pairs:
        if occupied_houses.issubset(pair):
            results["Gada Kendra Stithi"]["present"] = True
            results["Gada Kendra Stithi"]["strength"] = 1.0
            results["Gada Kendra Stithi"]["details"] = (
                f"Gada Yoga formed. All planets are in houses {pair}. Occupied houses: {occupied_houses_str}"
            )
            gada_formed = True
            break
    if not gada_formed:
        results["Gada Kendra Stithi"]["details"] = (
            f"Gada Yoga not formed. All planets must be in one of the adjacent kendra pairs (1,4), (4,7), (7,10), or (10,1). Occupied houses: {occupied_houses_str}"
        )

    return results


@register_yogas("Vajra", "Yava")
def VajraYavaYoga(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Vajra: Benefics occupy the Lagna and 7th house, while malefics occupy the 4th and 10th house.
    Yava: Malefics occupy the Lagna and 7th house, while benefics occupy the 4th and 10th house.
    """
    results = {
        "Vajra": {
            "id": "",
            "name": "Vajra",
            "present": False,
            "strength": 0.0,
            "details": "Vajra Yoga not formed.",
            "type": "Positive",
        },
        "Yava": {
            "id": "",
            "name": "Yava",
            "present": False,
            "strength": 0.0,
            "details": "Yava Yoga not formed.",
            "type": "Negative",
        },
    }

    planets_in_1 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 1)]
    planets_in_7 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 7)]
    planets_in_4 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 4)]
    planets_in_10 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 10)]

    # Conditions for Vajra Yoga
    benefics_in_1_or_7 = any(p in BENEFIC_PLANETS for p in planets_in_1) or any(
        p in BENEFIC_PLANETS for p in planets_in_7
    )
    no_malefics_in_1_7 = not any(
        p in MALEFIC_PLANETS for p in planets_in_1
    ) and not any(p in MALEFIC_PLANETS for p in planets_in_7)

    malefics_in_4_or_10 = any(p in MALEFIC_PLANETS for p in planets_in_4) or any(
        p in MALEFIC_PLANETS for p in planets_in_10
    )
    no_benefics_in_4_10 = not any(
        p in BENEFIC_PLANETS for p in planets_in_4
    ) and not any(p in BENEFIC_PLANETS for p in planets_in_10)

    vajra_cond1 = benefics_in_1_or_7 and no_malefics_in_1_7
    vajra_cond2 = malefics_in_4_or_10 and no_benefics_in_4_10

    if vajra_cond1 and vajra_cond2:
        results["Vajra"]["present"] = True
        results["Vajra"]["strength"] = 1.0
        results["Vajra"]["details"] = (
            "Vajra Yoga formed: Benefics in houses 1 and/or 7, and Malefics in houses 4 and/or 10."
        )
    else:
        details = []
        if not vajra_cond1:
            details.append(
                f"Benefics are not exclusively in houses 1 and 7. House 1 planets: {planets_in_1}, House 7 planets: {planets_in_7}"
            )
        if not vajra_cond2:
            details.append(
                f"Malefics are not exclusively in houses 4 and 10. House 4 planets: {planets_in_4}, House 10 planets: {planets_in_10}"
            )
        results["Vajra"]["details"] = "Vajra Yoga not formed. " + " ".join(details)

    # Conditions for Yava Yoga
    malefics_in_1_or_7 = any(p in MALEFIC_PLANETS for p in planets_in_1) or any(
        p in MALEFIC_PLANETS for p in planets_in_7
    )
    no_benefics_in_1_7 = not any(
        p in BENEFIC_PLANETS for p in planets_in_1
    ) and not any(p in BENEFIC_PLANETS for p in planets_in_7)

    benefics_in_4_or_10 = any(p in BENEFIC_PLANETS for p in planets_in_4) or any(
        p in BENEFIC_PLANETS for p in planets_in_10
    )
    no_malefics_in_4_10 = not any(
        p in MALEFIC_PLANETS for p in planets_in_4
    ) and not any(p in MALEFIC_PLANETS for p in planets_in_10)

    yava_cond1 = malefics_in_1_or_7 and no_benefics_in_1_7
    yava_cond2 = benefics_in_4_or_10 and no_malefics_in_4_10

    if yava_cond1 and yava_cond2:
        results["Yava"]["present"] = True
        results["Yava"]["strength"] = 1.0
        results["Yava"]["details"] = (
            "Yava Yoga formed: Malefics in houses 1 and/or 7, and Benefics in houses 4 and/or 10."
        )
    else:
        details = []
        if not yava_cond1:
            details.append(
                f"Malefics are not exclusively in houses 1 and 7. House 1 planets: {planets_in_1}, House 7 planets: {planets_in_7}"
            )
        if not yava_cond2:
            details.append(
                f"Benefics are not exclusively in houses 4 and 10. House 4 planets: {planets_in_4}, House 10 planets: {planets_in_10}"
            )
        results["Yava"]["details"] = "Yava Yoga not formed. " + " ".join(details)

    return results


@register_yoga("Sringhataka")
def Sringhataka(yoga: Yoga) -> YogaType:
    """
    All classical planets occupy the Lagna and its trines
    """
    result: YogaType = {
        "id": "",
        "name": "Sringhataka",
        "present": False,
        "strength": 0.0,
        "details": "Sringhataka Yoga not formed.",
        "type": "Positive",
    }

    required_houses = {1, 5, 9}
    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    if occupied_houses.issubset(required_houses):
        result["present"] = True
        result["strength"] = 1.0

        planets_by_house = {}
        for p, h in planet_locations.items():
            if h not in planets_by_house:
                planets_by_house[h] = []
            planets_by_house[h].append(p)

        details_list = []
        for h in sorted(list(required_houses)):
            planets_str = ", ".join(planets_by_house.get(h, []))
            details_list.append(f"House {h}: {planets_str if planets_str else 'Empty'}")

        result["details"] = (
            f"Sringhataka Yoga is formed. All planets are in houses 1, 5, 9. Planet positions: {'; '.join(details_list)}"
        )
    else:
        outside_planets = []
        for planet, house in planet_locations.items():
            if house not in required_houses:
                outside_planets.append(f"{planet} in house {house}")
        result["details"] = (
            f"Sringhataka Yoga not formed. All planets must be in houses 1, 5, and 9. Planets outside these houses: {', '.join(outside_planets)}"
        )

    return result


@register_yoga("Hala")
def Hala(yoga: Yoga) -> YogaType:
    """
    All classical planets are located in trine-house pattern but not Lagna's Trine
    """
    result: YogaType = {
        "id": "",
        "name": "Hala",
        "present": False,
        "strength": 0.0,
        "details": "Hala Yoga not formed.",
        "type": "Positive",
    }

    trine_patterns = [{2, 6, 10}, {3, 7, 11}, {4, 8, 12}]
    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    for pattern in trine_patterns:
        if occupied_houses.issubset(pattern):
            result["present"] = True
            result["strength"] = 1.0

            planets_by_house = {}
            for p, h in planet_locations.items():
                if h not in planets_by_house:
                    planets_by_house[h] = []
                planets_by_house[h].append(p)

            details_list = []
            for h in sorted(list(pattern)):
                planets_str = ", ".join(planets_by_house.get(h, []))
                details_list.append(
                    f"House {h}: {planets_str if planets_str else 'Empty'}"
                )

            result["details"] = (
                f"Hala Yoga is formed. All planets are in houses {pattern}. Planet positions: {'; '.join(details_list)}"
            )
            return result

    result["details"] = (
        f"Hala Yoga not formed. All planets are not in a trine pattern other than Lagna's trine. Occupied houses: {sorted(list(occupied_houses))}"
    )
    return result


@register_yoga("Kamala")
def Kamala(yoga: Yoga) -> YogaType:
    """
    All classical planets are situated in four kendras
    """
    result: YogaType = {
        "id": "",
        "name": "Kamala",
        "present": False,
        "strength": 0.0,
        "details": "Kamala Yoga not formed.",
        "type": "Positive",
    }

    required_houses = {1, 4, 7, 10}
    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    if occupied_houses.issubset(required_houses):
        result["present"] = True
        result["strength"] = 1.0

        planets_by_house = {}
        for p, h in planet_locations.items():
            if h not in planets_by_house:
                planets_by_house[h] = []
                planets_by_house[h].append(p)

        details_list = []
        for h in sorted(list(required_houses)):
            planets_str = ", ".join(planets_by_house.get(h, []))
            details_list.append(f"House {h}: {planets_str if planets_str else 'Empty'}")

        result["details"] = (
            f"Kamala Yoga is formed. All planets are in the four kendras. Planet positions: {'; '.join(details_list)}"
        )
    else:
        outside_planets = []
        for planet, house in planet_locations.items():
            if house not in required_houses:
                outside_planets.append(f"{planet} in house {house}")
        result["details"] = (
            f"Kamala Yoga not formed. All planets must be in the four kendras. Planets outside these houses: {', '.join(outside_planets)}"
        )

    return result


@register_yoga("Vapee")
def Vapee(yoga: Yoga) -> YogaType:
    """
    The planets are ranged in the four Panarapas (2, 5, 8, 11) or the four Apoklimas (3, 6, 9, 12).
    """
    result: YogaType = {
        "id": "",
        "name": "Vapee",
        "present": False,
        "strength": 0.0,
        "details": "Vapee Yoga not formed.",
        "type": "Positive",
    }

    panarapas = {2, 5, 8, 11}
    apoklimas = {3, 6, 9, 12}

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    in_panarapas = occupied_houses.issubset(panarapas)
    in_apoklimas = occupied_houses.issubset(apoklimas)

    if in_panarapas or in_apoklimas:
        result["present"] = True
        result["strength"] = 1.0

        details_list = []
        if in_panarapas:
            details_list.append("All planets are in Panarapa houses (2, 5, 8, 11).")
        if in_apoklimas:
            details_list.append("All planets are in Apoklima houses (3, 6, 9, 12).")

        result["details"] = "Vapee Yoga is formed. " + " or ".join(details_list)
    else:
        result["details"] = (
            f"Vapee Yoga not formed. All planets are not in Panarapa or Apoklima houses. Occupied houses: {sorted(list(occupied_houses))}"
        )

    return result


@register_yoga("Samudra")
def Samudra(yoga: Yoga) -> YogaType:
    """
    All planets occupy six even houses
    """
    result: YogaType = {
        "id": "",
        "name": "Samudra",
        "present": False,
        "strength": 0.0,
        "details": "Samudra Yoga not formed.",
        "type": "Positive",
    }

    even_houses = {2, 4, 6, 8, 10, 12}
    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        result["details"] = "Could not locate all classical planets."
        return result

    occupied_houses = set(planet_locations.values())

    if occupied_houses.issubset(even_houses):
        result["present"] = True
        result["strength"] = 1.0

        planets_by_house = {}
        for p, h in planet_locations.items():
            if h not in planets_by_house:
                planets_by_house[h] = []
            planets_by_house[h].append(p)

        details_list = []
        for h in sorted(list(even_houses)):
            planets_str = ", ".join(planets_by_house.get(h, []))
            if planets_str:
                details_list.append(f"House {h}: {planets_str}")

        result["details"] = (
            f"Samudra Yoga is formed. All planets are in even houses. Planet positions: {'; '.join(details_list)}"
        )
    else:
        outside_planets = []
        for planet, house in planet_locations.items():
            if house not in even_houses:
                outside_planets.append(f"{planet} in house {house}")
        result["details"] = (
            f"Samudra Yoga not formed. All planets must be in even houses. Planets in odd houses: {', '.join(outside_planets)}"
        )

    return result


@register_yogas("Vallaki", "Damni", "Pasa", "Kedara", "Sula", "Yuga", "Gola")
def SankhyaYogas(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Sankhya Yogas are based on the number of houses occupied by the seven classical planets.

    - Vallaki (Veena): Planets occupy 7 different houses.
    - Damni (Damini): Planets occupy 6 different houses.
    - Pasa (Pasha): Planets occupy 5 different houses.
    - Kedara: Planets occupy 4 different houses.
    - Sula (Shula): Planets occupy 3 different houses.
    - Yuga: Planets occupy 2 different houses.
    - Gola: Planets occupy 1 single house.
    """
    yoga_definitions = {
        "Vallaki": {"house_count": 7, "type": "Positive"},
        "Damni": {"house_count": 6, "type": "Positive"},
        "Pasa": {"house_count": 5, "type": "Positive"},
        "Kedara": {"house_count": 4, "type": "Positive"},
        "Sula": {"house_count": 3, "type": "Neutral"},
        "Yuga": {"house_count": 2, "type": "Negative"},
        "Gola": {"house_count": 1, "type": "Positive"},
    }

    results: Dict[str, YogaType] = {
        name: {
            "id": "",
            "name": name,
            "present": False,
            "strength": 0.0,
            "details": f"Initial state for {name} Yoga.",
            "type": definition["type"],
        }
        for name, definition in yoga_definitions.items()
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        missing_planets = [p for p, h in planet_locations.items() if h is None]
        for name in results:
            results[name]["details"] = (
                f"Could not locate all classical planets. Missing: {', '.join(missing_planets)}"
            )
        return results

    occupied_houses = set(planet_locations.values())
    num_occupied_houses = len(occupied_houses)

    active_yoga_name = None
    for name, definition in yoga_definitions.items():
        if num_occupied_houses == definition["house_count"]:
            active_yoga_name = name
            break

    for name in yoga_definitions:
        if name == active_yoga_name:
            results[name]["present"] = True
            results[name]["strength"] = 1.0

            planets_by_house = {}
            for p, h in planet_locations.items():
                planets_by_house.setdefault(h, []).append(p)

            details_list = []
            for h in sorted(list(occupied_houses)):
                planets_str = ", ".join(planets_by_house.get(h, []))
                details_list.append(f"House {h}: {planets_str}")

            results[name]["details"] = (
                f"{name} Yoga formed: The 7 classical planets occupy {num_occupied_houses} house(s). "
                f"Positions: {'; '.join(details_list)}"
            )
        else:
            required_count = yoga_definitions[name]["house_count"]
            results[name]["details"] = (
                f"Condition for {name} Yoga not met. "
                f"It requires planets in {required_count} houses, but they occupy {num_occupied_houses}."
            )

    return results


@register_yogas("Rajju", "Musala", "Nala")
def RasiGunaYogas(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Yogas based on all planets occupying signs of a certain modality.
    - Rajju: All planets in movable (cardinal) signs.
    - Musala: All planets in fixed signs.
    - Nala: All planets in dual (mutable) signs.
    """
    MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
    FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
    DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}

    yoga_definitions = {
        "Rajju": {"signs": MOVABLE_SIGNS, "type": "Neutral", "modality": "movable"},
        "Musala": {"signs": FIXED_SIGNS, "type": "Positive", "modality": "fixed"},
        "Nala": {"signs": DUAL_SIGNS, "type": "Negative", "modality": "dual"},
    }

    results: Dict[str, YogaType] = {
        name: {
            "id": "",
            "name": name,
            "present": False,
            "strength": 0.0,
            "details": f"Condition for {name} Yoga not met.",
            "type": definition["type"],
        }
        for name, definition in yoga_definitions.items()
    }

    planet_locations = {p: yoga.get_house_of_planet(p) for p in CLASSICAL_PLANETS}

    if any(h is None for h in planet_locations.values()):
        missing_planets = [p for p, h in planet_locations.items() if h is None]
        details = f"Could not locate all classical planets. Missing: {', '.join(missing_planets)}"
        for name in results:
            results[name]["details"] = details
        return results

    occupied_rashis = {
        yoga.get_rashi_of_house(h) for h in planet_locations.values() if h is not None
    }

    active_yoga = None
    for name, definition in yoga_definitions.items():
        if occupied_rashis.issubset(definition["signs"]):
            active_yoga = name
            break

    for name, definition in yoga_definitions.items():
        if name == active_yoga:
            results[name]["present"] = True
            results[name]["strength"] = 1.0
            results[name]["details"] = (
                f"{name} Yoga formed: All planets are in {definition['modality']} signs. "
                f"Occupied signs: {', '.join(sorted(list(occupied_rashis)))}."
            )
        else:
            results[name]["details"] = (
                f"{name} Yoga not formed. All planets must be in {definition['modality']} signs. "
                f"Occupied signs: {', '.join(sorted(list(occupied_rashis)))}."
            )

    return results


@register_yogas("Srik", "Sarpa")
def SrikSarpa(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Srik: All the benefics occupy kendras
    Sarpa: All the malefics occupy kendras
    """
    results: Dict[str, YogaType] = {
        "Srik": {
            "id": "",
            "name": "Srik",
            "present": False,
            "strength": 0.0,
            "details": "Srik Yoga not formed.",
            "type": "Positive",
        },
        "Sarpa": {
            "id": "",
            "name": "Sarpa",
            "present": False,
            "strength": 0.0,
            "details": "Sarpa Yoga not formed.",
            "type": "Negative",
        },
    }

    KENDRA_HOUSES = {1, 4, 7, 10}

    # Srik Yoga
    benefic_locations = {p: yoga.get_house_of_planet(p) for p in BENEFIC_PLANETS}
    if any(h is None for h in benefic_locations.values()):
        results["Srik"]["details"] = "Could not locate all benefic planets."
    else:
        benefics_in_kendra = all(h in KENDRA_HOUSES for h in benefic_locations.values())
        if benefics_in_kendra:
            results["Srik"]["present"] = True
            results["Srik"]["strength"] = 1.0
            pos_str = ", ".join([f"{p} in h{h}" for p, h in benefic_locations.items()])
            results["Srik"]["details"] = (
                f"Srik Yoga formed. All benefics in Kendra houses: {pos_str}."
            )
        else:
            outside = [
                f"{p} in h{h}"
                for p, h in benefic_locations.items()
                if h not in KENDRA_HOUSES
            ]
            results["Srik"]["details"] = (
                f"Srik Yoga not formed. Benefics outside Kendras: {', '.join(outside)}."
            )

    # Sarpa Yoga
    malefic_locations = {p: yoga.get_house_of_planet(p) for p in MALEFIC_PLANETS}
    if any(h is None for h in malefic_locations.values()):
        results["Sarpa"]["details"] = "Could not locate all malefic planets."
    else:
        malefics_in_kendra = all(h in KENDRA_HOUSES for h in malefic_locations.values())
        if malefics_in_kendra:
            results["Sarpa"]["present"] = True
            results["Sarpa"]["strength"] = 1.0
            pos_str = ", ".join([f"{p} in h{h}" for p, h in malefic_locations.items()])
            results["Sarpa"]["details"] = (
                f"Sarpa Yoga formed. All malefics in Kendra houses: {pos_str}."
            )
        else:
            outside = [
                f"{p} in h{h}"
                for p, h in malefic_locations.items()
                if h not in KENDRA_HOUSES
            ]
            results["Sarpa"]["details"] = (
                f"Sarpa Yoga not formed. Malefics outside Kendras: {', '.join(outside)}."
            )

    return results


@register_yogas("Duryoga", "Daridra")
def DuryogaDaridra(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Duryoga: The lord of the 10th is situated in the 6th, 8th or 12th
    Daridra: The lord of the 11th is situated in the 6th, 8th or 12th
    """
    results: Dict[str, YogaType] = {
        "Duryoga": {
            "id": "",
            "name": "Duryoga",
            "present": False,
            "strength": 0.0,
            "details": "Duryoga not formed.",
            "type": "Negative",
        },
        "Daridra": {
            "id": "",
            "name": "Daridra",
            "present": False,
            "strength": 0.0,
            "details": "Daridra yoga not formed.",
            "type": "Negative",
        },
    }
    L10 = yoga.get_lord_of_house(10)
    L11 = yoga.get_lord_of_house(11)

    L10H = yoga.get_house_of_planet(L10)
    L11H = yoga.get_house_of_planet(L11)

    if L10H in [6, 8, 12]:
        results["Duryoga"]["present"] = True
        results["Duryoga"]["strength"] = 1.0
        results["Duryoga"]["details"] = (
            f"Duryoga formed. Lord of 10th ({L10}) is in the {L10H} house."
        )
    else:
        results["Duryoga"]["details"] = (
            f"Duryoga not formed. Lord of 10th ({L10}) is in the {L10H} house not in 6th, 8th or 12th."
        )

    if L11H in [6, 8, 12]:
        results["Daridra"]["present"] = True
        results["Daridra"]["strength"] = 1.0
        results["Daridra"]["details"] = (
            f"Daridra formed. Lord of 11th ({L11}) is in the {L11H} house."
        )
    else:
        results["Daridra"]["details"] = (
            f"Daridra not formed. Lord of 11th ({L11}) is in the {L11H} house not in 6th, 8th or 12th."
        )

    return results
