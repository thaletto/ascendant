from typing import Dict, List, Sequence, cast

from ascendant.const import (
    BENEFIC_PLANETS,
    CLASSICAL_PLANETS,
    DEEP_EXALTATION_POINTS,
    MALEFIC_PLANETS,
    RASHI_LORD_MAP,
)
from ascendant.types import HOUSES, PLANETS, YogaType
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
    if (Ju_house := yoga.get_house_of_planet("Jupiter")) is not None and Ju_house != 1:
        result["details"] = "Jupiter is not in Asc"
        return result

    if (Mo_house := yoga.get_house_of_planet("Moon")) is not None and Mo_house != 7:
        result["details"] = "Moon is not in 7th house"
        return result

    if (Su_house := yoga.get_house_of_planet("Sun")) is not None and Su_house != 2:
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
        if (d9_chart := yoga.__chart__.get_varga_chakra_chart(9)) is None:
            raise ValueError("D9 chart not found")

        all_benefics_A = benefics_in_5 + benefics_in_6 + benefics_in_7
        all_benefics_names_A = [p["name"] for p in all_benefics_A]

        dignified_benefics = 0
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
    if (lagna_house := yoga.get_house_of_planet("Lagna")) is None:
        return result
    lagna_rashi = yoga.get_rashi_of_house(lagna_house)
    fixed_signs = ["Taurus", "Leo", "Scorpio", "Aquarius"]
    if lagna_rashi not in fixed_signs:
        result["details"] = f"Lagna sign '{lagna_rashi}' is not a fixed sign."
        return result

    # Condition 2: Lords of 1st and 11th interchange houses
    if (lord_of_1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Lord of 1st house not found")
    if (lord_of_11 := yoga.get_lord_of_house(11)) is None:
        raise ValueError("Lord of 11th house not found")

    house_of_lord_1 = yoga.get_house_of_planet(lord_of_1)
    house_of_lord_11 = yoga.get_house_of_planet(lord_of_11)
    if not (house_of_lord_1 == 11 and house_of_lord_11 == 1):
        result["details"] = (
            f"Lords of 1st ({lord_of_1} in {house_of_lord_1}) and 11th ({lord_of_11} in {house_of_lord_11}) do not interchange houses."
        )
        return result

    # Condition 3: Lords of 2nd and 10th interchange houses
    if (lord_of_2 := yoga.get_lord_of_house(2)) is None:
        raise ValueError("Lord of 2nd house not found")
    if (lord_of_10 := yoga.get_lord_of_house(10)) is None:
        raise ValueError("Lord of 10th house not found")

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
    if (lord_of_9 := yoga.get_lord_of_house(9)) is None:
        raise ValueError("Lord of 9th house not found")
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
    if (lagna_house := yoga.get_house_of_planet("Lagna")) is None:
        return result
    lagna_rashi = yoga.get_rashi_of_house(lagna_house)
    fixed_signs = ["Taurus", "Leo", "Scorpio", "Aquarius"]
    if lagna_rashi not in fixed_signs:
        result["details"] = f"Lagna sign '{lagna_rashi}' is not a fixed sign."
        return result

    # Condition 2: Lagna aspected by Lord of 6th
    if (lord_of_6 := yoga.get_lord_of_house(6)) is None:
        raise ValueError("Lord of 6th house not found")
    try:
        aspects = yoga.__chart__.graha_drishti(n=1, planet=lord_of_6)
        if aspects is None:
            raise ValueError("Graha drishti of L6 is not found")
        aspect_houses = aspects[0].get("aspect_houses", [])
        if not any(lagna_house in house_dict for house_dict in aspect_houses):
            result["details"] = f"Lagna is not aspected by 6th lord ({lord_of_6})."
            return result
    except (KeyError, IndexError, TypeError):
        result["details"] = f"Could not get aspects for {lord_of_6}."
        return result

    # Condition 3: Navamsa Lords of L6 and L9 cojoined with Sun
    L6 = lord_of_6
    if (L9 := yoga.get_lord_of_house(9)) is None:
        raise ValueError("Lord of 9th house not found")

    if (D9 := yoga.__chart__.get_varga_chakra_chart(9)) is None:
        raise ValueError("D9 chart not found")

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

    if (house_nsl6 := yoga.get_house_of_planet(NSL6)) is None:
        raise ValueError("House of NSL6 not found")

    if (house_nsl9 := yoga.get_house_of_planet(NSL9)) is None:
        raise ValueError("House of NSL9 not found")

    if (house_sun := yoga.get_house_of_planet("Sun")) is None:
        raise ValueError("House of Sun not found")

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
    if (lord_of_6 := yoga.get_lord_of_house(6)) is None:
        raise ValueError("Lord of 6th not found")
    if (p6 := yoga.get_planet_by_name(lord_of_6)) is None or p6["name"] == "Lagna":
        raise ValueError(f"Could not find planet object for {lord_of_6}")
    if "Debilitated" not in p6["inSign"]:
        result["details"] = f"Lord of 6th ({lord_of_6}) is not debilitated."
        return result

    # Condition 2: Lord of 10th is in deep exaltation
    if (lord_of_10 := yoga.get_lord_of_house(10)) is None:
        raise ValueError("Lord of 10th not found")
    if (p10 := yoga.get_planet_by_name(lord_of_10)) is None or p10["name"] == "Lagna":
        raise ValueError(f"Could not find planet object for {lord_of_10}")
    p10_name = p10["name"]
    if p10_name not in DEEP_EXALTATION_POINTS:
        result["details"] = f"{p10_name} does not have a deep exaltation point."
        return result

    exaltation_info = DEEP_EXALTATION_POINTS[p10_name]
    if (p10_house := yoga.get_house_of_planet(p10_name)) is None:
        result["details"] = f"Could not determine house of {p10_name}."
        return result
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
    if (lord_of_11 := yoga.get_lord_of_house(11)) is None:
        raise ValueError("Could not determine lord of 11th.")
    if (p11 := yoga.get_planet_by_name(lord_of_11)) is None:
        raise ValueError(f"Could not find planet object for {lord_of_11}. ")

    p11_name = p11["name"]
    if p11_name not in DEEP_EXALTATION_POINTS:
        result["details"] = f"{p11_name} does not have a deep exaltation point."
        return result

    exaltation_info = DEEP_EXALTATION_POINTS[p11_name]
    if (p11_house := yoga.get_house_of_planet(p11_name)) is None:
        raise ValueError(f"Could not determine house of {p11_name}.")
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

    if (lord_of_1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Could not determine lord of Lagna.")

    if (base_house := yoga.get_house_of_planet(lord_of_1)) is None:
        raise ValueError(f"Could not find house of Lagna lord ({lord_of_1}).")

    if (target_house := yoga.get_house_of_planet("Venus")) is None:
        raise ValueError("Could not determine house of Venus.")

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
    if (lord_of_10 := yoga.get_lord_of_house(10)) is None:
        raise ValueError("Could not determine lord of 10th.")
    if (house_of_l10 := yoga.get_house_of_planet(lord_of_10)) is None:
        raise ValueError("Could not determine house of 10th lord.")

    if house_of_l10 not in [3, 7, 11]:
        result["details"] = (
            f"10th lord ({lord_of_10}) is in house {house_of_l10}, not in a Kama Trikona (3, 7, 11)."
        )
        return result

    # Condition 2: Lord of Lagna and Jupiter are in association
    if (lord_of_1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Could not determine lord of Lagna.")
    if (house_of_l1 := yoga.get_house_of_planet(lord_of_1)) is None:
        raise ValueError("Could not determine house of Lagna lord.")
    if (house_of_ju := yoga.get_house_of_planet("Jupiter")) is None:
        raise ValueError("Could not determine house of Jupiter.")
    if house_of_l1 != house_of_ju:
        result["details"] = "Lagna lord and Jupiter are not in the same house."
        return result

    # Condition 3: Sun is exalted
    if (sun_planet := yoga.get_planet_by_name("Sun")) is None or sun_planet["name"] == "Lagna":
        raise ValueError("Sun is not found")
    if "Exalted" not in sun_planet["inSign"]:
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

    if (l9 := yoga.get_lord_of_house(9)) is None:
        raise ValueError("Could not determine lord of 9th house")

    if (l10 := yoga.get_lord_of_house(10)) is None:
        raise ValueError("Could not determine lord of 10th house")

    # Condition: l9, l10 and NL9L must be in the 2nd house
    house_of_l9 = yoga.get_house_of_planet(l9)
    house_of_l10 = yoga.get_house_of_planet(l10)

    if house_of_l9 != 2 or house_of_l10 != 2:
        result["details"] = (
            f"9th lord ({l9} in {house_of_l9}) and 10th lord ({l10} in {house_of_l10}) are not both in the 2nd house."
        )
        return result

    # Find Navamsa lord of L9's Navamsa sign (NL9L)
    if (d9_chart := yoga.__chart__.get_varga_chakra_chart(9)) is None:
        raise ValueError("Navamsa chart is not found")
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
    if (l9 := yoga.get_lord_of_house(9)) is None:
        raise ValueError("Could not determine lord of 9th house")
    if (h_l9 := yoga.get_house_of_planet(l9)) is None:
        raise ValueError("Could not determine house of 9th lord")
    if (h_ju := yoga.get_house_of_planet("Jupiter")) is None:
        raise ValueError("Could not determine house of Jupiter")

    kendra_from_l9 = [((h_l9 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]
    if h_ju not in kendra_from_l9:
        result["details"] = "Jupiter is not in a Kendra from the 9th lord."
        return result

    # Condition 2: Venus in Kendra from 11th lord
    if (l11 := yoga.get_lord_of_house(11)) is None:
        raise ValueError("Could not determine lord of 11th house")
    if (h_l11 := yoga.get_house_of_planet(l11)) is None:
        raise ValueError("Could not determine house of 11th lord")
    if (h_ve := yoga.get_house_of_planet("Venus")) is None:
        raise ValueError("Could not determine house of Venus")

    kendra_from_l11 = [((h_l11 - 1 + offset - 1) % 12) + 1 for offset in kendra_offsets]
    if h_ve not in kendra_from_l11:
        result["details"] = "Venus is not in a Kendra from the 11th lord."
        return result

    # Condition 3: Mercury in Kendra from Lagna lord OR 10th lord
    if (l1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Could not determine lord of 1st house")
    if (l10 := yoga.get_lord_of_house(10)) is None:
        raise ValueError("Could not determine lord of 10th house")
    if (h_l1 := yoga.get_house_of_planet(l1)) is None:
        raise ValueError("Could not determine house of 1st lord")
    if (h_l10 := yoga.get_house_of_planet(l10)) is None:
        raise ValueError("Could not determine house of 10th lord")
    if (h_me := yoga.get_house_of_planet("Mercury")) is None:
        raise ValueError("Could not determine house of Mercury")


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
    if (l5 := yoga.get_lord_of_house(5)) is None or (l11 := yoga.get_lord_of_house(11)) is None:
        raise ValueError("Could not determine lord of 5th or 11th.")

    if (h_l5 := yoga.get_house_of_planet(l5)) is None or (h_l11 := yoga.get_house_of_planet(l11)) is None:
        raise ValueError("Could not determine house of lord of 5th or 11th.")

    # Condition 1: Lords of 5th and 11th interchange their houses
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
    if (p_ju := yoga.get_planet_by_name("Jupiter")) is None or p_ju["name"] == "Lagna":
        raise ValueError("Jupiter is not found")
    if "Moola Trikona" not in p_ju["inSign"]:
        result["details"] = "Jupiter is not in Moolatrikona."
        return result

    if (l2 := yoga.get_lord_of_house(2)) is None:
        raise ValueError("Lord of 2nd house is not found")

    h_ju = yoga.get_house_of_planet("Jupiter")
    h_l2 = yoga.get_house_of_planet(l2)
    if h_ju != h_l2:
        result["details"] = "Jupiter is not in conjunction with the 2nd lord."
        return result

    # Condition 2: Lord of Lagna is in exaltation
    if (l1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Lord of Lagna is not found")

    if (p_l1 := yoga.get_planet_by_name(l1)) is None or p_l1["name"] == "Lagna":
        raise ValueError("Lord of Lagna is not found")
    if "Exalted" not in p_l1["inSign"]:
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

    if (h_su := yoga.get_house_of_planet("Sun")) is None:
        result["details"] = "Could not locate Sun."
        return result
    if (h_mo := yoga.get_house_of_planet("Moon")) is None:
        result["details"] = "Could not locate Moon."
        return result
    if (h_ma := yoga.get_house_of_planet("Mars")) is None:
        result["details"] = "Could not locate Mars."
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

    planet_locations: dict[PLANETS, HOUSES] = {
        p: h
        for p in CLASSICAL_PLANETS
        if (h := yoga.get_house_of_planet(p)) is not None
    }
    if not all(planet_locations.values()):
        missing = [p for p, h in planet_locations.items() if h is None]
        result["details"] = (
            f"Could not locate all classical planets: {', '.join(missing)}."
        )
        return result

    # Check if all planets are in the same house
    occupied_houses = {p for p in planet_locations.values() if p is not None}
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
    if (h_su := yoga.get_house_of_planet("Sun")) is None:
        raise ValueError("Could not locate Sun.")

    target_house_from_sun = ((h_su - 1 + 4) % 12) + 1
    if the_house == target_house_from_sun:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"All classical planets ({', '.join(planets_in_the_house)}) are in house {the_house}, which is the 5th from the Sun (in house {h_su})."
        )
        return result

    # Case 3: 5th house from Moon
    if (h_mo := yoga.get_house_of_planet("Moon")) is None:
        raise ValueError("Could not locate Moon.")

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

    occupied_houses = {h for h in planet_locations.values() if h is not None}

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

    occupied_houses = {h for h in planet_locations.values() if h is not None}

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

    occupied_houses = {h for h in planet_locations.values() if h is not None}
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
    results: Dict[str, YogaType] = {
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

    occupied_houses = {h for h in planet_locations.values() if h is not None}

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

    occupied_houses = {h for h in planet_locations.values() if h is not None}

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

    occupied_houses = {h for h in planet_locations.values() if h is not None}
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

    occupied_rashis: set[str] = {
        r
        for h in planet_locations.values()
        if h is not None
        if (r := yoga.get_rashi_of_house(cast(HOUSES, h))) is not None
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
    if (L10 := yoga.get_lord_of_house(10)) is None:
        return results
    if (L11 := yoga.get_lord_of_house(11)) is None:
        return results

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


@register_yogas("Harsha", "Sarala", "Vimala")
def HarshaSaralaVimala(yoga: Yoga) -> Dict[str, YogaType]:
    """
    The lords of the 6th occupy the 6th
    The lords of the 8th occupy the 8th
    The lords of the 12th occupy the 12th
    """
    results: Dict[str, YogaType] = {
        "Harsha": {
            "id": "",
            "name": "Harsha",
            "present": False,
            "strength": 0.0,
            "details": "Harsha Yoga not formed.",
            "type": "Positive",
        },
        "Sarala": {
            "id": "",
            "name": "Sarala",
            "present": False,
            "strength": 0.0,
            "details": "Sarala Yoga not formed.",
            "type": "Positive",
        },
        "Vimala": {
            "id": "",
            "name": "Vimala",
            "present": False,
            "strength": 0.0,
            "details": "Vimala Yoga not formed.",
            "type": "Positive",
        },
    }
    if (L6 := yoga.get_lord_of_house(6)) is None:
        return results
    if (L8 := yoga.get_lord_of_house(8)) is None:
        return results
    if (L12 := yoga.get_lord_of_house(12)) is None:
        return results

    L6H = yoga.get_house_of_planet(L6)
    L8H = yoga.get_house_of_planet(L8)
    L12H = yoga.get_house_of_planet(L12)

    if L6H == 6:
        results["Harsha"]["present"] = True
        results["Harsha"]["strength"] = 1.0
        results["Harsha"]["details"] = (
            f"Harsha formed. Lord of 6th ({L6}) is in the 6th house."
        )
    else:
        results["Harsha"]["details"] = (
            f"Harsha not formed. Lord of 6th ({L6}) is in the {L6H} house not in 6th."
        )

    if L8H == 8:
        results["Sarala"]["present"] = True
        results["Sarala"]["strength"] = 1.0
        results["Sarala"]["details"] = (
            f"Sarala formed. Lord of 8th ({L8}) is in the 8th house."
        )
    else:
        results["Sarala"]["details"] = (
            f"Sarala not formed. Lord of 8th ({L8}) is in the {L8H} house not in 8th."
        )

    if L12H == 12:
        results["Vimala"]["present"] = True
        results["Vimala"]["strength"] = 1.0
        results["Vimala"]["details"] = (
            f"Vimala formed. Lord of 12th ({L12}) is in the 12th house."
        )
    else:
        results["Vimala"]["details"] = (
            f"Vimala not formed. Lord of 12th ({L12}) is in the {L12H} house not in 12th."
        )

    return results


@register_yoga("SareeraSoukhya")
def SareeraSoukhya(yoga: Yoga) -> YogaType:
    """
    The lord of Lagna, Jupiter or Venus should occupy a quadrant
    """
    result: YogaType = {
        "id": "",
        "name": "SareeraSoukhya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    if (LAsc := yoga.get_lord_of_house(1)) is None:
        result["details"] = "SareeraSoukhya not formed. Lord of Lagna is not found."
        return result
    if (LJu := yoga.get_lord_of_planet("Jupiter")) is None:
        result["details"] = "SareeraSoukhya not formed. Lord of Jupiter is not found."
        return result
    if (LVe := yoga.get_lord_of_planet("Venus")) is None:
        result["details"] = "SareeraSoukhya not formed. Lord of Venus is not found."
        return result

    LAscH = yoga.get_house_of_planet(LAsc)
    LJuH = yoga.get_house_of_planet(LJu)
    LVeH = yoga.get_house_of_planet(LVe)

    if LAscH in [1, 4, 7, 10] or LJuH in [1, 4, 7, 10] or LVeH in [1, 4, 7, 10]:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"SareeraSoukhya formed. Lord of Lagna ({LAsc}), Lord of Jupiter ({LJu}), Lord of Venus ({LVe}) is in the {LAscH}, {LJuH}, {LVeH} house respectively."
        )
    else:
        result["details"] = (
            f"SareeraSoukhya not formed. Lord of Lagna ({LAsc}) or Lord of Jupiter ({LJu}) or Lord of Venus ({LVe}) is not in the kendra."
        )

    return result


@register_yogas("Dehapushti", "Dehakashta")
def DehapushtiDehakashta(yoga: Yoga) -> Dict[str, YogaType]:
    """
    Dehapushti: Lord of Lagna in a movable sign and aspected by a benefic
    Dehakashta: Lord of Langa must join a malefic or occupy the 8th house
    """
    results: Dict[str, YogaType] = {
        "Dehapushti": {
            "id": "",
            "name": "Dehapushti",
            "present": False,
            "strength": 0.0,
            "details": "Dehapushti Yoga not formed.",
            "type": "Positive",
        },
        "Dehakashta": {
            "id": "",
            "name": "Dehakashta",
            "present": False,
            "strength": 0.0,
            "details": "Dehakashta Yoga not formed.",
            "type": "Negative",
        },
    }

    if (LAsc := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Invalid Lagna planet")
    if (LAscH := yoga.get_house_of_planet(LAsc)) is None:
        raise ValueError("Invalid Lagna house")
    LAscPlanet = yoga.get_planet_by_name(LAsc)
    if LAscPlanet is None or LAscPlanet["name"] == "Lagna":
        raise ValueError("Invalid Lagna planet")
    LAscAspected = yoga.is_house_benefic_aspected(LAscH)
    LAscCojoins = yoga.planets_in_relative_house(LAsc, 1)

    if LAscPlanet["sign"]["name"] in ["Aries", "Cancer", "Libra", "Capricorn"]:
        if LAscAspected:
            results["Dehapushti"]["present"] = True
            results["Dehapushti"]["strength"] = 1.0
            results["Dehapushti"]["details"] = (
                f"Lord of Lagna ({LAsc}) is in the movable sign ({LAscPlanet['sign']['name']}) and aspected by a benefic"
            )
        else:
            results["Dehapushti"]["details"] = (
                f"Lord of Lagna ({LAsc}) is in the movable sign ({LAscPlanet['sign']['name']}) and not aspected by a benefic"
            )
    else:
        results["Dehapushti"]["details"] = (
            f"Lord of Lagna ({LAsc}) is not in the movalble sign and not aspected by a benefic"
        )

    if LAscH == 8:
        results["Dehakashta"]["present"] = True
        results["Dehakashta"]["strength"] = 1.0
        results["Dehakashta"]["details"] = f"Lord of Lagna ({LAsc}) is in the 8th house"
    elif any(p in MALEFIC_PLANETS for p in LAscCojoins):
        results["Dehakashta"]["present"] = True
        results["Dehakashta"]["strength"] = 1.0
        results["Dehakashta"]["details"] = (
            f"Lord of Lagna ({LAsc}) is in the {LAscH} house and cojoined by a malefic"
        )
    else:
        results["Dehakashta"]["details"] = (
            f"Lord of Lagna ({LAsc}) is not in the 8th house and not cojoined by a malefic"
        )

    return results


@register_yoga("Rogagrastha")
def Rogagrastha(yoga: Yoga) -> YogaType:
    """
    Lord of Lagna occupies Lagna in conjunction with the lord of 6th or 8th or 12th house.
    Or weak lord of Lagna joins a trine or a quadrant.

    This is a Negative Yoga
    """
    result: YogaType = {
        "id": "",
        "name": "Rogagrastha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not determine Lord of Lagna"
        return result

    h_l1 = yoga.get_house_of_planet(l1)

    # Condition 1: Lord of Lagna occupies Lagna...
    condition1 = False
    details1 = ""
    if h_l1 == 1:
        # ...in conjunction with the lord of 6th or 8th or 12th house.
        l6 = yoga.get_lord_of_house(6)
        l8 = yoga.get_lord_of_house(8)
        l12 = yoga.get_lord_of_house(12)

        planets_in_1 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 1)]

        conjoined = []
        if l6 and l6 in planets_in_1:
            conjoined.append(f"6th Lord ({l6})")
        if l8 and l8 in planets_in_1:
            conjoined.append(f"8th Lord ({l8})")
        if l12 and l12 in planets_in_1:
            conjoined.append(f"12th Lord ({l12})")

        if conjoined:
            condition1 = True
            details1 = f"Lagna Lord ({l1}) is in Lagna with {', '.join(conjoined)}."

    # Condition 2: Weak lord of Lagna joins a trine or a quadrant.
    condition2 = False
    details2 = ""

    p_l1 = yoga.get_planet_by_name(l1)
    if p_l1 is None or p_l1["name"] == "Lagna":
        raise ValueError("Invalid Lagna planet")
    if p_l1:
        # Note: isPlanetPowerful returns (bool, strength)
        is_powerful, _ = yoga.isPlanetPowerful(p_l1)
        if not is_powerful:
            # Weak lord of Lagna
            # Check if in Trine (1, 5, 9) or Quadrant (1, 4, 7, 10).
            # Combined: 1, 4, 5, 7, 9, 10
            if h_l1 in [1, 4, 5, 7, 9, 10]:
                condition2 = True
                details2 = (
                    f"Weak Lagna Lord ({l1}) is in house {h_l1} (Trine/Quadrant)."
                )

    if condition1:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = details1
        return result

    if condition2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = details2
        return result

    result["details"] = (
        "Lagna Lord is not in Lagna with 6/8/12 lords, nor is it weak in Trine/Quadrant."
    )
    return result


@register_yoga("Krisanga")
def Krisanga(yoga: Yoga) -> YogaType:
    """
    The Lagna Sign occupies a dry sign (Aries, Leo, Sagittarius, Taurus, Virgo, Capricorn)
    or the Lagna lord is dry planet (Sun, Mars, Saturn and Mercury).

    This is a Negative Yoga
    """
    result: YogaType = {
        "id": "",
        "name": "Krisanga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    dry_signs = ["Aries", "Leo", "Sagittarius", "Taurus", "Virgo", "Capricorn"]
    dry_planets = ["Sun", "Mars", "Saturn", "Mercury"]

    # Condition 1
    if (lagna_house := yoga.get_house_of_planet("Lagna")) is None:
        raise ValueError("Invalid Lagna house")
    lagna_sign = yoga.get_rashi_of_house(lagna_house)

    if lagna_sign in dry_signs:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Lagna Sign ({lagna_sign}) is a dry sign."
        return result

    # Condition 2
    l1 = yoga.get_lord_of_house(1)
    if l1 and l1 in dry_planets:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Lagna Lord ({l1}) is a dry planet."
        return result

    result["details"] = "Lagna Sign is not dry and Lagna Lord is not a dry planet."
    return result


@register_yoga("Dehasthoulya")
def Dehasthoulya(yoga: Yoga) -> YogaType:
    """
    Lord of Lagna and the planet, in whose Navamasa the lord of Lagna is placed, should occupy watery signs.
    or
    The Lagna must be occupied by Jupiter or he must aspect the Lagna from a watery sign.
    or
    The Ascendant must fall in a watery sign in conjunction with benefics or the Ascendant lord must be a watery sign.

    This is a Negative Yoga
    """
    result: YogaType = {
        "id": "",
        "name": "Dehasthoulya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    watery_signs = ["Cancer", "Scorpio", "Pisces"]
    benefics = ["Jupiter", "Venus", "Mercury", "Moon"]

    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not determine Lord of Lagna"
        return result

    if (h_l1 := yoga.get_house_of_planet(l1)) is None:
        raise ValueError("Invalid Lagna house")
    # Note: get_rashi_of_house returns the sign of the house number in Rashi chart
    sign_l1 = yoga.get_rashi_of_house(h_l1)

    # Helper to check if a sign is watery
    def is_watery(sign):
        return sign in watery_signs

    # Condition 1: Lord of Lagna and [Navamsa Lord of L1] occupy watery signs.
    cond1 = False
    details1 = ""
    if is_watery(sign_l1):
        # Find Navamsa Lord of L1
        d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
        if d9_chart is None:
            raise ValueError("Invalid Navamsa chart")
        navamsa_lord_l1 = None
        for data in d9_chart.values():
            for planet in data["planets"]:
                if planet["name"] == l1:
                    navamsa_sign_l1 = planet["sign"]["name"]
                    from ascendant.const import RASHI_LORD_MAP

                    navamsa_lord_l1 = RASHI_LORD_MAP.get(navamsa_sign_l1)
                    break
            if navamsa_lord_l1:
                break

        if navamsa_lord_l1:
            if (h_nl1 := yoga.get_house_of_planet(navamsa_lord_l1)) is None:
                raise ValueError("Invalid Navamsa Lord house")
            sign_nl1 = yoga.get_rashi_of_house(h_nl1)
            if is_watery(sign_nl1):
                cond1 = True
                details1 = f"Lagna Lord ({l1}) and its Navamsa dispositor ({navamsa_lord_l1}) are in watery signs."

    # Condition 2: Lagna occupied by Jupiter OR Jupiter aspects Lagna from a watery sign.
    cond2 = False
    details2 = ""
    # Check if Jupiter in Lagna (House 1)
    if (h_ju := yoga.get_house_of_planet("Jupiter")) is None:
        raise ValueError("Invalid Jupiter house")
    if h_ju == 1:
        cond2 = True
        details2 = "Jupiter is in Lagna."
    else:
        # Check aspect
        # Jupiter aspects 5, 7, 9 houses from itself.
        # So if Lagna (1) is 5, 7, or 9 from Jupiter...
        # Relative house of 1 from Jupiter should be 5, 7, 9.
        rel_1_from_ju = yoga.relative_house("Jupiter", "Lagna")
        if rel_1_from_ju in [5, 7, 9]:
            # AND Jupiter must be in a watery sign
            sign_ju = yoga.get_rashi_of_house(h_ju)
            if is_watery(sign_ju):
                cond2 = True
                details2 = f"Jupiter aspects Lagna from a watery sign ({sign_ju})."

    # Condition 3: Ascendant in watery sign + benefics OR Ascendant lord is in watery sign.
    cond3 = False
    details3 = ""

    # Part B: Ascendant lord must be a watery sign (interpreted as "in a watery sign")
    if is_watery(sign_l1):
        cond3 = True
        details3 = f"Lagna Lord ({l1}) is in a watery sign ({sign_l1})."
    else:
        # Part A: Ascendant in watery sign in conjunction with benefics
        lagna_sign = yoga.get_rashi_of_house(1)
        if is_watery(lagna_sign):
            # Check benefics in Lagna
            planets_in_1 = yoga.planets_in_relative_house("Lagna", 1)
            has_benefic = any(p["name"] in benefics for p in planets_in_1)
            if has_benefic:
                cond3 = True
                details3 = f"Ascendant is in watery sign ({lagna_sign}) with benefics."

    if cond1:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = details1
        return result
    if cond2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = details2
        return result
    if cond3:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = details3
        return result

    result["details"] = "None of the conditions for Dehasthoulya Yoga are met."
    return result


@register_yoga("Sada Sanchara")
def SadaSanchara(yoga: Yoga) -> YogaType:
    """
    The lord of either the Lagna or the sign occupied by Lagna lord must be movable sign.

    This is a Positive Yoga
    """
    result: YogaType = {
        "id": "",
        "name": "Sada Sanchara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    movable_signs = ["Aries", "Cancer", "Libra", "Capricorn"]

    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not determine Lord of Lagna"
        return result

    if (h_l1 := yoga.get_house_of_planet(l1)) is None:
        raise ValueError("Invalid Lagna Lord house")
    if (sign_l1 := yoga.get_rashi_of_house(h_l1)) is None:
        raise ValueError("Invalid Lagna Lord sign")

    # Condition 1: Lord of Lagna is in a movable sign
    if sign_l1 in movable_signs:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Lagna Lord ({l1}) is in a movable sign ({sign_l1})."
        return result

    # Condition 2: Lord of the sign occupied by Lagna Lord (dispositor) is in a movable sign

    dispositor_l1 = RASHI_LORD_MAP.get(sign_l1)

    if dispositor_l1:
        if (h_disp := yoga.get_house_of_planet(dispositor_l1)) is None:
            raise ValueError("Invalid dispositor house")
        if (sign_disp := yoga.get_rashi_of_house(h_disp)) is None:
            raise ValueError("Invalid dispositor sign")

        if sign_disp in movable_signs:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"Dispositor of Lagna Lord ({dispositor_l1}) is in a movable sign ({sign_disp})."
            )
            return result

    result["details"] = "Neither Lagna Lord nor its dispositor are in movable signs."
    return result


@register_yoga("Dhana")
def Dhana(yoga: Yoga) -> YogaType:
    """
    Multiple conditions involved 5th, 11th, and specific planet positions.
    Check details for specific condition met.

    This is a positive yoga.
    """
    result: YogaType = {
        "id": "",
        "name": "Dhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Helper function to check if a planet is in a specific house
    def check_planet_house(planet, house):
        return yoga.get_house_of_planet(planet) == house

    # Helper for aspect/conjunction
    def joined_or_aspected(planet_name, *others):
        chart = yoga.__chart__
        if chart is None:
            raise ValueError("Invalid chart")

        phouse = yoga.get_house_of_planet(planet_name)
        if phouse is None:
            return False

        planets_in_same_house = [
            p["name"] for p in yoga.planets_in_relative_house("Lagna", phouse)
        ]

        aspects_all = chart.graha_drishti(n=1)
        if not aspects_all:
            return False

        satisfied_count = 0

        for other in others:
            is_joined = other in planets_in_same_house
            is_aspected = False

            aspect_list = chart.graha_drishti(n=1, planet=other)
            if aspect_list:
                aspect = aspect_list[0]
                if any(phouse in h for h in aspect.get("aspect_houses", [])):
                    is_aspected = True

            if is_joined or is_aspected:
                satisfied_count += 1

        return satisfied_count == len(others)

    # 1. The 5th from the Ascendant happen to be a sign of Venus, and Venus and Saturn are situated in the 5th and 11th respectively.
    sign_5 = yoga.get_rashi_of_house(5)
    rashi_lord_5 = None
    if sign_5:
        from ascendant.const import RASHI_LORD_MAP

        rashi_lord_5 = RASHI_LORD_MAP.get(sign_5)

    if rashi_lord_5 == "Venus":
        if check_planet_house("Venus", 5) and check_planet_house("Saturn", 11):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "5th is Venus sign, Venus in 5th, Saturn in 11th."
            return result

    # 2. Mercury occupies his own sign which should be in the 5th from Lagna and the Moon and Mars should be in 11th.
    if rashi_lord_5 == "Mercury":  # 5th is Mercury sign
        if (
            check_planet_house("Mercury", 5)
            and check_planet_house("Moon", 11)
            and check_planet_house("Mars", 11)
        ):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Mercury in own sign in 5th, Moon and Mars in 11th."
            return result

    # 3. Saturn should occupy his own sign which should be in the 5th from Lagna, and Mercury and Mars should be positioned in 11th.
    if rashi_lord_5 == "Saturn":
        if (
            check_planet_house("Saturn", 5)
            and check_planet_house("Mercury", 11)
            and check_planet_house("Mars", 11)
        ):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Saturn in own sign in 5th, Mercury and Mars in 11th."
            return result

    # 4. The Sun must occupy his 5th identical with his own sign and Jupiter and Moon should be in 11th.
    # "Sun must occupy his 5th identical with his own sign" -> Sun is in 5th house, and 5th house sign is Leo (Sun's sign).
    if rashi_lord_5 == "Sun":
        if (
            check_planet_house("Sun", 5)
            and check_planet_house("Jupiter", 11)
            and check_planet_house("Moon", 11)
        ):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Sun in own sign in 5th, Jupiter and Moon in 11th."
            return result

    # 5. The 5th from the Lagna happens to be a house of Jupiter with Jupiter there and Mars and the Moon in the 11th.
    if rashi_lord_5 == "Jupiter":
        if (
            check_planet_house("Jupiter", 5)
            and check_planet_house("Mars", 11)
            and check_planet_house("Moon", 11)
        ):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Jupiter in own sign in 5th, Mars and Moon in 11th."
            return result

    # 6. The Sun is in Lagna, identical with Leo, and aspected or joined by Mars and Jupiter.
    lagna_sign = yoga.get_rashi_of_house(1)
    if lagna_sign == "Leo" and check_planet_house("Sun", 1):
        if joined_or_aspected("Sun", "Mars", "Jupiter"):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                "Sun in Lagna (Leo), aspected/joined by Mars and Jupiter."
            )
            return result

    # 7. The Moon is in Lagna identical with Cancer and aspected by Jupiter and Mars. (Text says aspected but usually implies joined too, keeping strict to text? "aspected by". Let's use joined_or_aspected for safety as usually implied).
    # Text: "aspected by Jupiter and Mars"
    if lagna_sign == "Cancer" and check_planet_house("Moon", 1):
        # Checking aspect/join for safety
        if joined_or_aspected("Moon", "Jupiter", "Mars"):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                "Moon in Lagna (Cancer), aspected/joined by Jupiter and Mars."
            )
            return result

    # 8. Mars should be in Lagna identical with Aries or Scorpio and joined or aspected by the Moon.
    if (lagna_sign == "Aries" or lagna_sign == "Scorpio") and check_planet_house(
        "Mars", 1
    ):
        if joined_or_aspected("Mars", "Moon"):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"Mars in Lagna ({lagna_sign}), aspected/joined by Moon."
            )
            return result

    # 9. Mercury should be in Lagna identical with his own sign and joined or aspected by Saturn or Venus.
    # Note: "joined or aspected by Saturn OR Venus".
    if (lagna_sign == "Gemini" or lagna_sign == "Virgo") and check_planet_house(
        "Mercury", 1
    ):
        # Special check for OR condition
        saturn_rel = joined_or_aspected("Mercury", "Saturn")
        venus_rel = joined_or_aspected("Mercury", "Venus")
        if saturn_rel or venus_rel:
            result["present"] = True
            result["strength"] = 1.0
            with_planet = "Saturn" if saturn_rel else "Venus"
            if saturn_rel and venus_rel:
                with_planet = "Saturn and Venus"
            result["details"] = (
                f"Mercury in Lagna ({lagna_sign}), aspected/joined by {with_planet}."
            )
            return result

    # 10. Jupiter should be in Lagna identical with his own sign and joined or aspected by Mercury and Mars.
    if (lagna_sign == "Sagittarius" or lagna_sign == "Pisces") and check_planet_house(
        "Jupiter", 1
    ):
        if joined_or_aspected("Jupiter", "Mercury", "Mars"):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"Jupiter in Lagna ({lagna_sign}), aspected/joined by Mercury and Mars."
            )
            return result

    # 11. Venus should be in Lagna identical with his own sign and joined or aspected by Saturn and Mercury.
    if (lagna_sign == "Taurus" or lagna_sign == "Libra") and check_planet_house(
        "Venus", 1
    ):
        if joined_or_aspected("Venus", "Saturn", "Mercury"):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"Venus in Lagna ({lagna_sign}), aspected/joined by Saturn and Mercury."
            )
            return result

    result["details"] = "No Dhana Yoga conditions met."
    return result


@register_yoga("Bahudravyarjana")
def Bahudravyarjana(yoga: Yoga) -> YogaType:
    """
    Lord of the Lagna in the 2nd, lord of the 2nd in the 11th and the lord of 11th in the Lagna.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Bahudravyarjana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Lord of Lagna in 2nd
    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not find Lord of Lagna"
        return result
    h_l1 = yoga.get_house_of_planet(l1)

    if h_l1 != 2:
        result["details"] = f"Lord of Lagna ({l1}) is in {h_l1}, not 2nd."
        return result

    # Lord of 2nd in 11th
    l2 = yoga.get_lord_of_house(2)
    if not l2:
        result["details"] = "Could not find Lord of 2nd"
        return result
    h_l2 = yoga.get_house_of_planet(l2)

    if h_l2 != 11:
        result["details"] = f"Lord of 2nd ({l2}) is in {h_l2}, not 11th."
        return result

    # Lord of 11th in Lagna (1st)
    l11 = yoga.get_lord_of_house(11)
    if not l11:
        result["details"] = "Could not find Lord of 11th"
        return result
    h_l11 = yoga.get_house_of_planet(l11)

    if h_l11 != 1:
        result["details"] = f"Lord of 11th ({l11}) is in {h_l11}, not 1st."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = f"L1 ({l1}) in 2nd, L2 ({l2}) in 11th, L11 ({l11}) in Lagna."
    return result


@register_yoga("Anthya Vayasi Dhana")
def AnthyaVayasiDhana(yoga: Yoga) -> YogaType:
    """
    The planets owning the sign in which the lords of the 2nd and 1st together with a natural benefic are placed,
    should be strongly disposed in Lagna.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Anthya Vayasi Dhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    if not l1 or not l2:
        result["details"] = "Could not find Lord of 1st or 2nd."
        return result

    if (h_l1 := yoga.get_house_of_planet(l1)) is None:
        raise ValueError("Invalid Lagna Lord house")
    if (h_l2 := yoga.get_house_of_planet(l2)) is None:
        raise ValueError("Invalid 2nd Lord house")

    # Check L1 and L2 in same house
    if h_l1 != h_l2:
        result["details"] = f"L1 ({l1}) and L2 ({l2}) are not in the same house."
        return result

    # Check for additional Natural Benefic in the same house
    planets_in_house = yoga.planets_in_relative_house("Lagna", h_l1)
    benefics_in_house = [
        p["name"]
        for p in planets_in_house
        if p["name"] in BENEFIC_PLANETS and p["name"] != l1 and p["name"] != l2
    ]

    if not benefics_in_house:
        result["details"] = (
            f"L1 ({l1}) and L2 ({l2}) are together but not with a separate Natural Benefic."
        )
        return result

    # Find the lord of this house (the dispositor)
    if (sign_of_house := yoga.get_rashi_of_house(h_l1)) is None:
        raise ValueError("Invalid dispositor sign")
    dispositor = RASHI_LORD_MAP.get(sign_of_house)

    if not dispositor:
        result["details"] = "Could not determine dispositor."
        return result

    # Dispositor must be "strongly disposed in Lagna"
    # 1. In Lagna
    h_disp = yoga.get_house_of_planet(dispositor)
    if h_disp != 1:
        result["details"] = f"Dispositor ({dispositor}) is in {h_disp}, not Lagna (1)."
        return result

    # 2. Strong
    p_disp = yoga.get_planet_by_name(dispositor)
    if p_disp is None or p_disp["name"] == "Lagna":
        raise ValueError(f"Invalid dispositor: {dispositor}")
    is_strong, _ = yoga.isPlanetPowerful(p_disp)

    if not is_strong:
        result["details"] = f"Dispositor ({dispositor}) is in Lagna but not strong."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = (
        f"L1 ({l1}) and L2 ({l2}) joined {benefics_in_house[0]} in {sign_of_house}. "
        f"Dispositor {dispositor} is strong in Lagna."
    )
    return result


@register_yoga("Balya Dhana")
def BalyaDhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Balya Dhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    chart = yoga.__chart__
    if chart is None:
        result["details"] = "Invalid chart."
        return result

    # Lords of 2nd and 10th
    l2 = yoga.get_lord_of_house(2)
    l10 = yoga.get_lord_of_house(10)
    if not l2 or not l10:
        result["details"] = "Could not find Lord of 2nd or 10th."
        return result

    h2 = yoga.get_house_of_planet(l2)
    h10 = yoga.get_house_of_planet(l10)

    # Conjunction
    if h2 != h10:
        result["details"] = "L2 and L10 are not conjoined."
        return result

    if h2 not in {1, 4, 7, 10}:
        result["details"] = "L2 and L10 are not conjoined in a Kendra."
        return result

    # Lagna lord
    l1 = yoga.get_lord_of_house(1)
    if not l1:
        result["details"] = "Could not find Lagna lord."
        return result

    # Navamsa lord of Lagna lord
    d9 = chart.get_varga_chakra_chart(9)
    if not d9:
        result["details"] = "Navamsa chart not found."
        return result

    nl1 = None
    for house in d9.values():
        for p in house.get("planets", []):
            if p.get("name") == l1:
                sign = p["sign"]["name"]
                nl1 = RASHI_LORD_MAP.get(sign)
                break
        if nl1:
            break

    if not nl1:
        result["details"] = "Could not find Navamsa lord of Lagna lord."
        return result

    # Aspect check
    is_aspected = False
    drishti = chart.graha_drishti(n=1, planet=nl1)
    if drishti:
        for aspect in drishti:
            for houses in aspect.get("aspect_houses", []):
                if h2 in houses:
                    is_aspected = True
                    break

    # Allow conjunction as sambandha
    if not is_aspected:
        if yoga.get_house_of_planet(nl1) == h2:
            is_aspected = True

    if not is_aspected:
        result["details"] = f"Not aspected by NL1 ({nl1})."
        return result

    result.update(
        present=True,
        strength=1.0,
        details=(
            f"L2 ({l2}) and L10 ({l10}) conjoined in Kendra ({h2}), "
            f"aspected/joined by NL1 ({nl1})."
        ),
    )
    return result


@register_yoga("Bhratrumooladdhanaprapti")
def Bhratrumooladdhanaprapti(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Bhratrumooladdhanaprapti",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    chart = yoga.__chart__
    if chart is None:
        result["details"] = "Invalid chart."
        return result

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    l3 = yoga.get_lord_of_house(3)

    if not l1 or not l2 or not l3:
        result["details"] = "Could not find lords of 1, 2, or 3."
        return result

    h1 = yoga.get_house_of_planet(l1)
    h2 = yoga.get_house_of_planet(l2)
    h3 = yoga.get_house_of_planet(l3)

    # ---------- Condition 1 ----------
    # L1 & L2 in 3rd, aspected by benefics
    if h1 == 3 and h2 == 3:
        drishti = chart.graha_drishti(n=1)
        if drishti:
            for aspect in drishti:
                if aspect.get("planet") in BENEFIC_PLANETS:
                    for houses in aspect.get("aspect_houses", []):
                        if 3 in houses:
                            result.update(
                                present=True,
                                strength=1.0,
                                details=(
                                    f"L1 ({l1}) and L2 ({l2}) in 3rd house, "
                                    "aspected by benefics."
                                ),
                            )
                            return result

    # ---------- Condition 2 ----------
    # L3 + Jupiter in 2nd, joined/aspected by powerful L1
    if h3 == 2 and yoga.get_house_of_planet("Jupiter") == 2:
        p_l1 = yoga.get_planet_by_name(l1)
        if not p_l1 or p_l1["name"] == "Lagna":
            raise ValueError("L1 not found or is Lagna")
        l1_powerful, _ = yoga.isPlanetPowerful(p_l1)

        if l1_powerful:
            joined = yoga.get_house_of_planet(l1) == 2
            aspected = False

            drishti_l1 = chart.graha_drishti(n=1, planet=l1)
            if drishti_l1:
                for aspect in drishti_l1:
                    for houses in aspect.get("aspect_houses", []):
                        if 2 in houses:
                            aspected = True
                            break

            if joined or aspected:
                result.update(
                    present=True,
                    strength=1.0,
                    details=(
                        f"L3 ({l3}) and Jupiter in 2nd house, "
                        f"joined/aspected by powerful L1 ({l1})."
                    ),
                )
                return result

    result["details"] = "Neither condition satisfied."
    return result


@register_yoga("Matrumooladdhana")
def Matrumooladdhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Matrumooladdhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    chart = yoga.__chart__
    if chart is None:
        result["details"] = "Invalid chart."
        return result

    l2 = yoga.get_lord_of_house(2)
    l4 = yoga.get_lord_of_house(4)
    if not l2 or not l4:
        result["details"] = "Could not find lords of 2 or 4."
        return result

    h2 = yoga.get_house_of_planet(l2)
    h4 = yoga.get_house_of_planet(l4)

    # Conjunction
    if h2 == h4:
        result.update(
            present=True,
            strength=1.0,
            details=f"L2 ({l2}) is joined with L4 ({l4}).",
        )
        return result

    # Aspect
    drishti = chart.graha_drishti(n=1, planet=l4)
    if drishti:
        for aspect in drishti:
            for houses in aspect.get("aspect_houses", []):
                if h2 in houses:
                    result.update(
                        present=True,
                        strength=1.0,
                        details=f"L2 ({l2}) is aspected by L4 ({l4}).",
                    )
                    return result

    result["details"] = f"L2 ({l2}) is neither joined nor aspected by L4 ({l4})."
    return result


@register_yoga("Putramooladdhana")
def Putramooladdhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Putramooladdhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    l5 = yoga.get_lord_of_house(5)

    if not l1 or not l2 or not l5:
        result["details"] = "Could not find lords of Lagna, 2nd or 5th."
        return result

    # Strength checks
    p_l1 = yoga.get_planet_by_name(l1)
    p_l2 = yoga.get_planet_by_name(l2)
    if not p_l1 or p_l1["name"] == "Lagna" or not p_l2 or p_l2["name"] == "Lagna":
        raise ValueError("Invalid planet data")

    l1_strong, _ = yoga.isPlanetPowerful(p_l1)
    l2_strong, _ = yoga.isPlanetPowerful(p_l2)

    if not l1_strong:
        result["details"] = f"L1 ({l1}) is not strong / Vaiseshikamsa."
        return result

    if not l2_strong:
        result["details"] = f"L2 ({l2}) is not strong."
        return result

    # Conjunction check
    h2 = yoga.get_house_of_planet(l2)
    h5 = yoga.get_house_of_planet(l5)
    h_ju = yoga.get_house_of_planet("Jupiter")

    joined = []
    if h2 == h5:
        joined.append(f"L5 ({l5})")
    if h2 == h_ju:
        joined.append("Jupiter")

    if joined:
        result.update(
            present=True,
            strength=1.0,
            details=f"Strong L2 ({l2}) joined with {' and '.join(joined)}; strong L1 ({l1}).",
        )
        return result

    result["details"] = f"L2 ({l2}) is not joined with L5 ({l5}) or Jupiter."
    return result


@register_yoga("Satrumooladdhana")
def Satrumooladdhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Satrumooladdhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    l6 = yoga.get_lord_of_house(6)

    if not l1 or not l2 or not l6:
        result["details"] = "Could not find lords of Lagna, 2nd or 6th."
        return result

    # Strength checks
    p_l1 = yoga.get_planet_by_name(l1)
    p_l2 = yoga.get_planet_by_name(l2)
    if not p_l1 or p_l1["name"] == "Lagna" or not p_l2 or p_l2["name"] == "Lagna":
        result["details"] = "Planet data missing."
        return result

    l1_strong, _ = yoga.isPlanetPowerful(p_l1)
    l2_strong, _ = yoga.isPlanetPowerful(p_l2)

    if not l1_strong:
        result["details"] = f"L1 ({l1}) is not strong / Vaiseshikamsa."
        return result

    if not l2_strong:
        result["details"] = f"L2 ({l2}) is not strong."
        return result

    # Conjunction check
    h2 = yoga.get_house_of_planet(l2)
    h6 = yoga.get_house_of_planet(l6)
    h_mars = yoga.get_house_of_planet("Mars")

    joined = []
    if h2 == h6:
        joined.append(f"L6 ({l6})")
    if h2 == h_mars:
        joined.append("Mars")

    if joined:
        result.update(
            present=True,
            strength=1.0,
            details=f"Strong L2 ({l2}) joined with {' and '.join(joined)}; strong L1 ({l1}).",
        )
        return result

    result["details"] = f"L2 ({l2}) is not joined with L6 ({l6}) or Mars."
    return result


@register_yoga("Kalatramooladdhana")
def Kalatramooladdhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Kalatramooladdhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    l7 = yoga.get_lord_of_house(7)

    if not l1 or not l2 or not l7:
        result["details"] = "Could not find lords of L1, L2, L7."
        return result

    # Check strength
    p_l1 = yoga.get_planet_by_name(l1)
    p_l2 = yoga.get_planet_by_name(l2)
    if not p_l1 or p_l1["name"] == "Lagna" or not p_l2 or p_l2["name"] == "Lagna":
        result["details"] = "Planet data missing."
        return result

    l1_strong, _ = yoga.isPlanetPowerful(p_l1)
    l2_strong, _ = yoga.isPlanetPowerful(p_l2)

    if not l1_strong:
        result["details"] = f"L1 ({l1}) is not powerful."
        return result
    if not l2_strong:
        result["details"] = f"L2 ({l2}) is not strong."
        return result

    if (h2 := yoga.get_house_of_planet(l2)) is None:
        raise ValueError("Invalid 2nd Lord house")

    def is_joined_or_aspected(target_h: int, planet_name: PLANETS) -> bool:
        h_p = yoga.get_house_of_planet(planet_name)
        if h_p == target_h:
            return True
        aspects = yoga.__chart__.graha_drishti(n=1, planet=planet_name) or []
        for aspect in aspects:
            for houses in aspect.get("aspect_houses", []):
                if target_h in houses:
                    return True
        return False

    if is_joined_or_aspected(h2, l7) and is_joined_or_aspected(h2, "Venus"):
        result.update(
            present=True,
            strength=1.0,
            details=f"Strong L2 ({l2}) joined/aspected by L7 ({l7}) AND Venus. Powerful L1 ({l1}).",
        )
        return result

    result["details"] = f"L2 ({l2}) is not related to both L7 ({l7}) and Venus."
    return result


@register_yoga("Amaranantha Dhana")
def AmarananthaDhana(yoga: Yoga) -> YogaType:
    result: YogaType = {
        "id": "",
        "name": "Amaranantha Dhana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    planets_in_2 = yoga.planets_in_relative_house("Lagna", 2)
    if len(planets_in_2) < 2:
        result["details"] = (
            f"Only {len(planets_in_2)} planet(s) in 2nd house (need multiple)."
        )
        return result

    wealth_karakas: List[PLANETS] = [
        cast(PLANETS, p)
        for p in [
            "Jupiter",
            yoga.get_lord_of_house(2),
            yoga.get_lord_of_house(11),
        ]
        if p is not None
    ]
    wealth_karakas = [k for k in wealth_karakas if k]

    strong_wealth = []
    for k in wealth_karakas:
        p = yoga.get_planet_by_name(k)
        if not p or p["name"] == "Lagna":
            continue
        is_strong, _ = yoga.isPlanetPowerful(p)
        in_sign = p.get("inSign") or []
        own_or_exalt = any(s in ["Exalted", "Own"] for s in in_sign)
        if is_strong or own_or_exalt:
            strong_wealth.append(k)

    if len(strong_wealth) >= 2:
        result.update(
            present=True,
            strength=1.0,
            details=f"{len(planets_in_2)} planets in 2nd house. Strong wealth karakas: {', '.join(strong_wealth)}.",
        )
        return result

    result["details"] = "Multiple planets in 2nd, but not enough strong wealth karakas."
    return result


@register_yoga("Ayatnadhanalabha")
def Ayatnadhanalabha(yoga: Yoga) -> YogaType:
    """
    The lord of the Lagna and the 2nd must exchange places.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Ayatnadhanalabha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Parivartana between L1 and L2
    # L1 in 2nd house AND L2 in 1st house

    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)

    if not l1 or not l2:
        result["details"] = "Could not find lords of 1 or 2."
        return result

    h_l1 = yoga.get_house_of_planet(l1)
    h_l2 = yoga.get_house_of_planet(l2)

    if h_l1 == 2 and h_l2 == 1:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"L1 ({l1}) in 2nd and L2 ({l2}) in 1st (Exchange)."
        return result

    result["details"] = f"No exchange. L1 is in {h_l1}, L2 is in {h_l2}."
    return result


@register_yoga("Daridhra")
def Daridhra(yoga: Yoga) -> YogaType:
    """
    Negative yoga conditions for Daridhra.
    """
    result: YogaType = {
        "id": "",
        "name": "Daridhra",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    valid_planets = CLASSICAL_PLANETS  # ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")

    def is_joined_or_aspected(target_house: HOUSES, planet_name: PLANETS) -> bool:
        h_p = yoga.get_house_of_planet(planet_name)
        if h_p == target_house:
            return True
        aspects = yoga.__chart__.graha_drishti(n=1, planet=planet_name) or []
        for aspect in aspects:
            for houses in aspect.get("aspect_houses", []):
                if target_house in houses:
                    return True
        return False

    def has_benefic_influence(house: HOUSES) -> bool:
        for p in yoga.planets_in_relative_house("Lagna", house):
            if p["name"] in BENEFIC_PLANETS:
                return True
        for aspect in yoga.__chart__.graha_drishti(n=1) or []:
            if aspect["planet"] in BENEFIC_PLANETS:
                for houses in aspect.get("aspect_houses", []):
                    if house in houses:
                        return True
        return False

    # Lords of relevant houses
    if (l1 := yoga.get_lord_of_house(1)) is None:
        raise ValueError("Invalid 1st Lord")
    if (l2 := yoga.get_lord_of_house(2)) is None:
        raise ValueError("Invalid 2nd Lord")
    if (l5 := yoga.get_lord_of_house(5)) is None:
        raise ValueError("Invalid 5th Lord")
    if (l6 := yoga.get_lord_of_house(6)) is None:
        raise ValueError("Invalid 6th Lord")
    if (l7 := yoga.get_lord_of_house(7)) is None:
        raise ValueError("Invalid 7th Lord")
    if (l8 := yoga.get_lord_of_house(8)) is None:
        raise ValueError("Invalid 8th Lord")
    if (l12 := yoga.get_lord_of_house(12)) is None:
        raise ValueError("Invalid 12th Lord")

    if (h_l1 := yoga.get_house_of_planet(l1)) is None:
        raise ValueError(f"Invalid planet {l1}")
    if (h_l5 := yoga.get_house_of_planet(l5)) is None:
        raise ValueError(f"Invalid planet {l5}")
    if (h_l6 := yoga.get_house_of_planet(l6)) is None:
        raise ValueError(f"Invalid planet {l6}")

    # Condition 1: L12/L1 exchange with L7 influence
    if h_l1 == 6 and h_l6 == 1:
        if (h_moon := yoga.get_house_of_planet("Moon")) is None:
            raise ValueError("Invalid Moon House")
        cause_l1_l6: list[str] = [
            desc
            for desc in [
                f"L2 ({l2}) affects Moon"
                if is_joined_or_aspected(h_moon, l2)
                else None,
                f"L7 ({l7}) affects Moon"
                if is_joined_or_aspected(h_moon, l7)
                else None,
            ]
            if desc is not None
        ]

        if cause_l1_l6:
            result.update(
                present=True,
                strength=1.0,
                details=f"Exchange L1/L6. Influence: {', '.join(cause_l1_l6)}.",
            )
            return result

    # Condition 2: L6/L1 exchange, Moon influenced by L2/L7
    h_l7 = yoga.get_house_of_planet(l7)
    h_l2 = yoga.get_house_of_planet(l2)
    if h_l7 == 2 and h_l2 == 7:
        result.update(
            present=True,
            strength=1.0,
            details=f"Exchange L2/L7. Influence: L2 ({l2}) affects L7 ({l7}).",
        )
        return result

    # --- Condition 3: Ketu and Moon in Lagna ---
    if yoga.get_house_of_planet("Ketu") == 1 and yoga.get_house_of_planet("Moon") == 1:
        result.update(
            present=True, strength=1.0, details="Ketu and Moon both in Lagna."
        )
        return result

    # --- Condition 4: L1 in 8th influenced by L2/L7 ---
    if h_l1 == 8:
        cause = [
            p for p in [l2, l7] if p in valid_planets and is_joined_or_aspected(8, p)
        ]
        if cause:
            result.update(
                present=True,
                strength=1.0,
                details=f"L1 ({l1}) in 8th. Influenced by: {', '.join(cause)}.",
            )
            return result

    # --- Condition 5: L1 joins 6/8/12 without benefic influence ---
    houses5: dict[str, HOUSES] = {}

    for lord in [l6, l8, l12]:
        if lord in valid_planets:  # only pass valid PLANETS_LAGNA
            house = yoga.get_house_of_planet(lord)
            if house is None:
                raise ValueError(f"Invalid house of lord {lord}")
            houses5[lord] = house


    # Now `houses` only contains keys that are PLANETS_LAGNA
    joined_lords = [
        f"{lord} ({name})" for lord, name in houses5.items() if h_l1 == name
    ]

    if joined_lords and not has_benefic_influence(h_l1):
        result.update(
            present=True,
            strength=1.0,
            details=f"L1 ({l1}) joins {', '.join(joined_lords)}. No benefic influence.",
        )
        return result

    # --- Condition 6: L1 with 6/8/12 lords subjected to malefic aspects ---
    valid_lords: list[PLANETS] = [p for p in [l6, l8, l12] if p in valid_planets]
    associated_houses: list[HOUSES] = [
        h
        for hp in valid_lords
        if (h := yoga.get_house_of_planet(hp)) is not None
    ]

    malefics_affecting = []
    for h in associated_houses:
        planets_in_h = yoga.planets_in_relative_house("Lagna", h)
        malefics_affecting += [
            f"{p['name']} (Conjunction)"
            for p in planets_in_h
            if p["name"] in MALEFIC_PLANETS and p["name"] != l1
        ]
        for aspect in yoga.__chart__.graha_drishti(n=1) or []:
            if aspect["planet"] in MALEFIC_PLANETS:
                for hd in aspect.get("aspect_houses", []):
                    if h in hd:
                        malefics_affecting.append(f"{aspect['planet']} (Aspect)")
    if malefics_affecting:
        result.update(
            present=True,
            strength=1.0,
            details=f"L1 ({l1}) associated with {', '.join([l6, l8, l12])}. Malefic influence: {', '.join(malefics_affecting)}.",
        )
        return result

    # --- Condition 7: L5 joins 6/8/12 without benefic influence ---
    houses: dict[str, HOUSES] = {}

    for lord in (l6, l8, l12):
        if lord in valid_planets:
            house = yoga.get_house_of_planet(lord)
            if house is None:
                raise ValueError(f"Invalid planet {lord}")
            houses[lord] = house

    # Now `houses` only contains keys that are PLANETS_LAGNA
    joined = [f"{lord} ({name})" for name, lord in houses.items() if h_l5 == lord]
    if joined and not has_benefic_influence(h_l5):
        result.update(
            present=True,
            strength=1.0,
            details=f"L5 ({l5}) joins {', '.join(joined)}. No benefic influence.",
        )
        return result

    # --- Condition 8: L5 in 6 or 10 aspected by L2/L6/L7/L8/L12 ---
    if l5 and h_l5 in [6, 10]:
        lords: list[PLANETS] = [p for p in [l2, l6, l7, l8, l12] if p in valid_planets]
        aspectors = [p for p in lords if is_joined_or_aspected(h_l5, p)]
        if aspectors:
            result.update(
                present=True,
                strength=1.0,
                details=f"L5 ({l5}) in {h_l5}. Influenced by: {', '.join(aspectors)}.",
            )
            return result

    # --- Condition 9: Malefics in Lagna influenced by Maraka lords ---
    planets_in_1 = yoga.planets_in_relative_house("Lagna", 1)
    for p in planets_in_1:
        if p["name"] in MALEFIC_PLANETS:
            cause: list[PLANETS] = [
                lord
                for lord in [l2, l7]
                if lord in valid_planets and is_joined_or_aspected(1, lord)
            ]
            if cause:
                result.update(
                    present=True,
                    strength=1.0,
                    details=f"Malefic {p['name']} in Lagna. Influenced by Maraka: {', '.join(cause)}.",
                )
                return result

    # No conditions met
    result["details"] = "No Daridhra conditions met."
    return result


@register_yoga("Yukthi Samanwithavagmi")
def YukthiSamanwithavagmi(yoga: Yoga) -> YogaType:
    """
    1. The second Lord joins a benefic in a kendra or thrikona, or is exalted and combined with Jupiter.
    2. The Lord of speech occupies a kendra, attains paramochha and gains Parvatamsa, while Jupiter or Venus is in Simhasanamsa.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Yukthi Samanwithavagmi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l2 = yoga.get_lord_of_house(2)  # Lord of 2nd (Lord of Speech)
    if not l2:
        return result

    h_l2 = yoga.get_house_of_planet(l2)
    p_l2 = yoga.get_planet_by_name(l2)

    # helper for benefic conjunction
    def has_benefic_conjunction(house, planet_me):
        planets = yoga.planets_in_relative_house("Lagna", house)
        for p in planets:
            if p["name"] in BENEFIC_PLANETS and p["name"] != planet_me:
                return True
        return False

    def is_exalted(planet_obj):
        return "Exalted" in planet_obj.get("inSign", "")

    # Condition 1:
    # A) L2 joins benefic in Kendra/Trikona
    is_in_kt = h_l2 in [1, 4, 7, 10, 5, 9]
    if is_in_kt:
        if has_benefic_conjunction(h_l2, l2):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L2 ({l2}) in Kendra/Trikona ({h_l2}) with Benefic."
            return result

    # B) L2 is exalted and combined with Jupiter
    if is_exalted(p_l2):
        # Combined with Jupiter?
        if yoga.get_house_of_planet("Jupiter") == h_l2:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L2 ({l2}) Exalted and with Jupiter."
            return result

    # Condition 2:
    # L2 in Kendra
    # AND Attains Paramochha (Deep Exaltation) - Proxy: Exalted
    # AND Gains Parvatamsa (Varga strength) - Proxy: isPlanetPowerful
    # AND Jupiter or Venus in Simhasanamsa (Varga strength) - Proxy: Jupiter or Venus is Powerful

    if h_l2 in [1, 4, 7, 10]:
        if is_exalted(p_l2) and p_l2 is not None and p_l2["name"] != "Lagna":
            is_strong_l2, _ = yoga.isPlanetPowerful(p_l2)
            if is_strong_l2:
                # Check Ju or Ve strong
                p_ju = yoga.get_planet_by_name("Jupiter")
                if p_ju is None or p_ju["name"] == "Lagna":
                    raise ValueError("Could not find Jupiter in D9.")
                p_ve = yoga.get_planet_by_name("Venus")
                if p_ve is None or p_ve["name"] == "Lagna":
                    raise ValueError("Could not find Venus in D9.")
                ju_strong = yoga.isPlanetPowerful(p_ju)[0] if p_ju else False
                ve_strong = yoga.isPlanetPowerful(p_ve)[0] if p_ve else False

                if ju_strong or ve_strong:
                    result["present"] = True
                    result["strength"] = 1.0
                    result["details"] = "L2 Exalted/Strong in Kendra. Ju/Ve Strong."
                    return result

    result["details"] = "No Yukthi Samanwithavagmi conditions met."
    return result


@register_yoga("Parihasaka")
def Parihasaka(yoga: Yoga) -> YogaType:
    """
    The Lord of Navamsa occupied by the Sun attains Vaiseshikamsa and joins the second house.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Parihasaka",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # 1. Find Lord of Navamsa occupied by Sun (NSL_Sun)
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if d9_chart is None:
        raise ValueError("Could not find Navamsa chart.")

    # Need to iterate D9 chart to find where Sun is placed
    found_sun = False
    sun_navamsa_sign = None

    for h_num, data in d9_chart.items():
        for planet in data["planets"]:
            if planet["name"] == "Sun":
                sun_navamsa_sign = planet["sign"]["name"]
                found_sun = True
                break
        if found_sun:
            break

    if not found_sun or not sun_navamsa_sign:
        result["details"] = "Could not find Sun in Navamsa chart."
        return result

    nsl_sun = RASHI_LORD_MAP.get(sun_navamsa_sign)
    if not nsl_sun:
        result["details"] = "Could not determine lord of Sun's Navamsa."
        return result

    # 2. Check if NSL_Sun attains Vaiseshikamsa (Strong)
    p_nsl = yoga.get_planet_by_name(nsl_sun)
    if p_nsl is None or p_nsl["name"] == "Lagna":
        raise ValueError("Could not find Navamsa Sun Lord in D9.")
    is_strong, _ = yoga.isPlanetPowerful(p_nsl)

    if not is_strong:
        result["details"] = (
            f"Lord of Sun's Navamsa ({nsl_sun}) is not Strong/Vaiseshikamsa."
        )
        return result

    # 3. Joins the 2nd house
    # "joins the second house" -> In Rashi D1 chart or Navamsa D9?
    # Standard: unless specified "in Navamsa", positions like "joins 2nd house" refer to Rashi.
    # The subject is "The Lord of Navamsa occupied by Sun". This is a planet.
    # So: This planet (NSL_Sun) is in 2nd house (in Rashi).

    h_nsl = yoga.get_house_of_planet(nsl_sun)
    if h_nsl == 2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"Lord of Sun's Navamsa ({nsl_sun}) is Strong and in 2nd House."
        )
        return result

    result["details"] = (
        f"Lord of Sun's Navamsa ({nsl_sun}) is Strong but in {h_nsl} (not 2)."
    )
    return result


@register_yoga("Asatyavadi")
def Asatyavadi(yoga: Yoga) -> YogaType:
    """
    The Lord of the second house occupies the house of Saturn or Mars and malefics join kendras and thrikonas.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Asatyavadi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    # 1. L2 in Saturn's house (Cap/Aqu) OR Mars's house (Ari/Sco)
    l2 = yoga.get_lord_of_house(2)
    if not l2:
        return result

    p_l2 = yoga.get_planet_by_name(l2)
    if not p_l2:
        return result

    sign_of_l2 = p_l2.get("sign", {}).get("name")

    target_signs = ["Capricorn", "Aquarius", "Aries", "Scorpio"]

    if sign_of_l2 not in target_signs:
        result["details"] = f"L2 ({l2}) is in {sign_of_l2}, not in Sat/Mars sign."
        return result

    # CRITICAL: Invalid if L2 is itself Saturn or Mars (Own Sign)
    # The requirement "occupies the house of Saturn or Mars" implies "Staying in someone else's house" (usually malefics).
    # If L2 is Mars and in Aries -> Own house. This is usually good (Swakshetra). Not Asatyavadi (Liar).
    # User clarification: "the first condition is will be invalid if L2 is itself Saturn or Mars"
    # Wait, simple logic: IF L2 == Saturn OR L2 == Mars, checking if they are in their own house means they are Strong.
    # The user logic was: "invalid if L2 is itself Saturn or Mars".
    # Does this mean checking L2 name?
    # "Invalid if L2 IS Saturn or Mars" -> Meaning if L2 is Sat/Mars, this yoga cannot form?
    # Or "Invalid if L2 is in its OWN house"?
    # Context: "L2 in Saturn's house...". If L2 is Saturn, it is in its own house.
    # Usually "Planet in Malefic's house" is bad. "Planet in Own house" is good.
    # So if L2 is Saturn, being in Capricorn is GOOD.
    # So the condition really is: L2 is in Sat/Mars sign AND L2 is NOT the owner of that sign.

    l2_in_own_sign = (l2 == "Saturn" and sign_of_l2 in ["Capricorn", "Aquarius"]) or (
        l2 == "Mars" and sign_of_l2 in ["Aries", "Scorpio"]
    )

    if l2_in_own_sign:
        result["details"] = f"L2 ({l2}) is in own sign {sign_of_l2} (Good)."
        return result

    # 2. Malefics join Kendras and Trikonas
    # "Malefics" -> Plural. "Join Kendras and Trikonas" -> Plural.
    # Implies a general affliction of Kendras/Trikonas by Malefics.
    # Does it mean ALL Kendras/Trikonas have malefics? Or "Some" malefics are in "Some" Kendras/Trikonas?
    # Usually "Malefics in Kendras and Trikonas" means there are malefics present in these pivotal houses.
    # Let's count how many Kendras/Trikonas (1,4,7,10, 5,9) are occupied by Malefics.
    # Or just "Are there Malefics in K/T?"
    # Let's verify if there is SIGNIFICANT malefic presence.
    # Maybe check if at least one Kendra AND at least one Trikona has Malefics?
    # Or simply "Malefics occupy Kendras and Trikonas".
    # I will stick to: At least one Malefic in a Kendra AND At least one Malefic in a Trikona.

    kendras: list[HOUSES] = [1, 4, 7, 10]
    trikonas: list[HOUSES] = [5, 9]

    malefic_in_kendra = False
    for k in kendras:
        planets = yoga.planets_in_relative_house("Lagna", k)
        if any(p["name"] in MALEFIC_PLANETS for p in planets):
            malefic_in_kendra = True
            break

    malefic_in_trikona = False
    for t in trikonas:
        planets = yoga.planets_in_relative_house("Lagna", t)
        if any(p["name"] in MALEFIC_PLANETS for p in planets):
            malefic_in_trikona = True
            break

    if malefic_in_kendra and malefic_in_trikona:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"L2 ({l2}) in {sign_of_l2}. Malefics in Kendras and Trikonas."
        )
        return result

    result["details"] = (
        "L2 matches sign, but Malefics not found in BOTH Kendra and Trikona."
    )
    return result


@register_yoga("Bhaskara")
def Bhaskara(yoga: Yoga) -> YogaType:
    """
    Mercury in the second house from the Sun, the Moon in the eleventh house from Mercury and Jupiter in the fifth or ninth house from the Moon.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Bhaskara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    h_sun = yoga.get_house_of_planet("Sun")
    h_mercury = yoga.get_house_of_planet("Mercury")
    h_moon = yoga.get_house_of_planet("Moon")
    h_jupiter = yoga.get_house_of_planet("Jupiter")

    if None in [h_sun, h_mercury, h_moon, h_jupiter]:
        return result

    def relative_house(h_from, h_to):
        return ((h_to - h_from) % 12) + 1

    rel_merc_sun = relative_house(h_sun, h_mercury)
    if rel_merc_sun != 2:
        result["details"] = f"Mercury in {rel_merc_sun} from Sun (Expected 2)."
        return result

    rel_moon_merc = relative_house(h_mercury, h_moon)
    if rel_moon_merc != 11:
        result["details"] = f"Moon in {rel_moon_merc} from Mercury (Expected 11)."
        return result

    rel_ju_moon = relative_house(h_moon, h_jupiter)
    if rel_ju_moon not in [5, 9]:
        result["details"] = f"Jupiter in {rel_ju_moon} from Moon (Expected 5 or 9)."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = (
        "Mercury 2nd from Sun, Moon 11th from Mercury, Jupiter 5/9 from Moon."
    )
    return result


@register_yoga("Marud")
def Marud(yoga: Yoga) -> YogaType:
    """
    Jupiter in fifth or ninth house from Venus, the Moon in the fifth house from Jupiter and the Sun in a kendra from the Moon.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Marud",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    h_venus = yoga.get_house_of_planet("Venus")
    h_jupiter = yoga.get_house_of_planet("Jupiter")
    h_moon = yoga.get_house_of_planet("Moon")
    h_sun = yoga.get_house_of_planet("Sun")

    if None in [h_venus, h_jupiter, h_moon, h_sun]:
        return result

    def relative_house(h_from, h_to):
        return ((h_to - h_from) % 12) + 1

    # Jupiter in 5 or 9 from Venus
    rel_ju_ve = relative_house(h_venus, h_jupiter)
    if rel_ju_ve not in [5, 9]:
        result["details"] = f"Jupiter in {rel_ju_ve} from Venus (Expected 5 or 9)."
        return result

    # Moon in 5th from Jupiter
    rel_moon_ju = relative_house(h_jupiter, h_moon)
    if rel_moon_ju != 5:
        result["details"] = f"Moon in {rel_moon_ju} from Jupiter (Expected 5)."
        return result

    # Sun in Kendra (1, 4, 7, 10) from Moon
    rel_sun_moon = relative_house(h_moon, h_sun)
    if rel_sun_moon not in [1, 4, 7, 10]:
        result["details"] = f"Sun in {rel_sun_moon} from Moon (Expected Kendra)."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = (
        "Jupiter 5/9 from Venus, Moon 5 from Jupiter, Sun Kendra from Moon."
    )
    return result


@register_yoga("Saraswathi")
def Saraswathi(yoga: Yoga) -> YogaType:
    """
    Jupiter, Venus and Mercury occupy Lagna, second, fourth, fifth, seventh, ninth or tenth house either jointly or severally, Jupiter being in his own, exaltation or friendly sign.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Saraswathi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    allowed_houses = [1, 2, 4, 5, 7, 9, 10]

    h_jupiter = yoga.get_house_of_planet("Jupiter")
    h_venus = yoga.get_house_of_planet("Venus")
    h_mercury = yoga.get_house_of_planet("Mercury")

    # Check positions
    if h_jupiter not in allowed_houses:
        result["details"] = f"Jupiter in {h_jupiter} (Not allowed)."
        return result
    if h_venus not in allowed_houses:
        result["details"] = f"Venus in {h_venus} (Not allowed)."
        return result
    if h_mercury not in allowed_houses:
        result["details"] = f"Mercury in {h_mercury} (Not allowed)."
        return result

    # Check Jupiter strength (Own, Exaltation, Friend)
    # isPlanetPowerful checks Exalted(1.0), MoolaTrikona(0.8), Own(0.7), Friend(0.6).
    # Usually covers the requirement.
    p_jupiter = yoga.get_planet_by_name("Jupiter")
    if not p_jupiter or p_jupiter["name"] == "Lagna":
        raise ValueError("Jupiter not found or is Lagna")
    is_strong, _ = yoga.isPlanetPowerful(p_jupiter)

    if not is_strong:
        # Check specific Relation if isPlanetPowerful is too strict?
        # isPlanetPowerful returns True for Friend, Own, Exalted.
        # But maybe we should check the sign relation directly to be sure.
        relation = p_jupiter.get("inSign")  # e.g. "Friend's Sign", "Own Sign"
        # Since isPlanetPowerful covers Friend, it is likely sufficient.
        result["details"] = (
            f"Benefics in allowed houses, but Jupiter is not strong ({relation})."
        )
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "Ju/Ve/Me in allowed houses. Jupiter is Strong."
    return result


@register_yoga("Budha")
def Budha(yoga: Yoga) -> YogaType:
    """
    Jupiter in Lagna, the Moon in a kendra, Rahu in the second house from the Moon and the Sun and Mars in the third house from Rahu.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Budha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # 1. Jupiter in Lagna
    h_jupiter = yoga.get_house_of_planet("Jupiter")
    if h_jupiter != 1:
        result["details"] = f"Jupiter in {h_jupiter} (Expected 1)."
        return result

    # 2. Moon in Kendra (from Lagna)
    h_moon = yoga.get_house_of_planet("Moon")
    if h_moon not in [1, 4, 7, 10]:
        result["details"] = f"Moon in {h_moon} (Not Kendra)."
        return result

    # 3. Rahu in 2nd from Moon
    h_rahu = yoga.get_house_of_planet("Rahu")

    def relative_house(h_from, h_to):
        return ((h_to - h_from) % 12) + 1

    rel_rahu_moon = relative_house(h_moon, h_rahu)
    if rel_rahu_moon != 2:
        result["details"] = f"Rahu in {rel_rahu_moon} from Moon (Expected 2)."
        return result

    # 4. Sun and Mars in 3rd from Rahu
    h_sun = yoga.get_house_of_planet("Sun")
    h_mars = yoga.get_house_of_planet("Mars")

    rel_sun_rahu = relative_house(h_rahu, h_sun)
    rel_mars_rahu = relative_house(h_rahu, h_mars)

    if rel_sun_rahu != 3 or rel_mars_rahu != 3:
        result["details"] = (
            f"Sun({rel_sun_rahu})/Mars({rel_mars_rahu}) from Rahu (Expected 3)."
        )
        return result

    result["details"] = "Ju in 1, Moon Kendra, Rahu 2 from Moon, Sun+Mars 3 from Rahu."
    return result


@register_yoga("Mooka")
def Mooka(yoga: Yoga) -> YogaType:
    """
    The second Lord joins the eighth with Jupiter.
    Clarification: L2, L8 and Jupiter in the same house.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Mooka",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l2 = yoga.get_lord_of_house(2)
    l8 = yoga.get_lord_of_house(8)

    if not l2 or not l8:
        result["details"] = "Could not find lords of 2 or 8."
        return result

    h_l2 = yoga.get_house_of_planet(l2)
    h_l8 = yoga.get_house_of_planet(l8)
    h_jupiter = yoga.get_house_of_planet("Jupiter")

    # Check conjunction: L2, L8, Jupiter all in same house.
    if h_l2 == h_l8 and h_l8 == h_jupiter:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"L2 ({l2}), L8 ({l8}), Jupiter joined in {h_l2}."
        return result

    result["details"] = f"L2({h_l2}), L8({h_l8}), Ju({h_jupiter}) not in same house."
    return result


@register_yoga("Netranasa")
def Netranasa(yoga: Yoga) -> YogaType:
    """
    The Lords of the tenth and sixth house occupy Lagna with the second Lord, or they are in Neechamsa.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Netranasa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l10 = yoga.get_lord_of_house(10)
    l6 = yoga.get_lord_of_house(6)
    l2 = yoga.get_lord_of_house(2)

    if not l10 or not l6:
        return result

    # Condition 1: L10 + L6 + L2 in Lagna (1)
    if l2:
        h_l10 = yoga.get_house_of_planet(l10)
        h_l6 = yoga.get_house_of_planet(l6)
        h_l2 = yoga.get_house_of_planet(l2)

        if h_l10 == 1 and h_l6 == 1 and h_l2 == 1:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L10 ({l10}), L6 ({l6}), L2 ({l2}) in Lagna."
            return result

    # Condition 2: They (L10 and L6) are in Neechamsa (Debilitated in Navamsa)
    # Check debility in D9 for L10 and L6.
    # How to check "Neechamsa"?
    # IsPlanetPowerful returns details but doesn't explicitly flag Neecha/Debilitated.
    # Planet object has "inSign". Does that refer to Rashi or currently selected chart?
    # When using get_varga_chakra_chart(9), we get planets in D9.
    # But usually "Neechamsa" means the planet is in its Debilitation Sign in Navamsa.

    # We need to know the debilitation sign for each planet.
    # CONST needed: EXALTATION_SIGNS, DEBILITATION_SIGNS
    # Debilitation is usually 180 from Exaltation.
    # Sun: Libra, Moon: Scorpio, Mars: Cancer, Mercury: Pisces, Jupiter: Capricorn, Venus: Virgo, Saturn: Aries.
    debilitation_map = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }

    # Find L10 and L6 in Navamsa
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if not d9_chart:
        raise ValueError("D9 chart not found")

    l10_sign_d9 = None
    l6_sign_d9 = None

    # Scan D9
    for data in d9_chart.values():
        for p in data["planets"]:
            if p["name"] == l10:
                l10_sign_d9 = p["sign"]["name"]
            if p["name"] == l6:
                l6_sign_d9 = p["sign"]["name"]

    if l10_sign_d9 and l6_sign_d9:
        l10_deb = l10_sign_d9 == debilitation_map.get(l10)
        l6_deb = l6_sign_d9 == debilitation_map.get(l6)

        if l10_deb and l6_deb:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = (
                f"L10 ({l10}) and L6 ({l6}) are Neechamsa (Debilitated in D9)."
            )
            return result

    result["details"] = "Conditions for Netranasa not met."
    return result


@register_yoga("Andha")
def Andha(yoga: Yoga) -> YogaType:
    """
    Mercury and the Moon is in the second or the Lords of Lagna and the second join the second house with the Sun.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Andha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    # 1. Mercury and Moon in 2nd
    h_merc = yoga.get_house_of_planet("Mercury")
    h_moon = yoga.get_house_of_planet("Moon")

    if h_merc == 2 and h_moon == 2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Mercury and Moon in 2nd House."
        return result

    # 2. Lords of Lagna (L1) and Second (L2) join the second house with the Sun.
    l1 = yoga.get_lord_of_house(1)
    l2 = yoga.get_lord_of_house(2)
    h_sun = yoga.get_house_of_planet("Sun")

    if l1 and l2:
        h_l1 = yoga.get_house_of_planet(l1)
        h_l2 = yoga.get_house_of_planet(l2)

        # "join the second house with the Sun" -> In 2nd House AND With Sun.
        # Implies Sun is also in 2nd.
        if h_l1 == 2 and h_l2 == 2 and h_sun == 2:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L1 ({l1}), L2 ({l2}), Sun joined in 2nd House."
            return result

    result["details"] = "Andha Yoga conditions not met."
    return result


@register_yoga("Sumukha")
def Sumukha(yoga: Yoga) -> YogaType:
    """
    The Lord of the second house is in a kendra aspected by benefics, or benefics join the second house.
    or
    The Lord of the second house is posited in a kendra which is his exaltation, own or friendly sign and the Lord of the kendra attains Gopuramsa.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Sumukha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }
    if yoga.__chart__ is None:
        raise ValueError("Invalid chart data")
    l2 = yoga.get_lord_of_house(2)
    if not l2:
        return result
    h_l2 = yoga.get_house_of_planet(l2)

    kendras = [1, 4, 7, 10]

    def has_benefic_aspect(house: int) -> bool:
        aspects: Sequence[dict] = cast(
            Sequence[dict], yoga.__chart__.graha_drishti(n=1) or []
        )
        for aspect in aspects:
            if aspect.get("planet") in BENEFIC_PLANETS:
                for house_data in aspect.get("aspect_houses", []):
                    if house in house_data:
                        return True
        return False

    # Cond 1A: L2 in Kendra aspected by benefics
    if h_l2 in kendras:
        if has_benefic_aspect(h_l2):
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L2 ({l2}) in Kendra ({h_l2}) aspected by Benefics."
            return result

    # Cond 1B: Benefics join the second house.
    # "Benefics" -> Plural. At least 2? Or just "There are benefics in 2nd"?
    # Let's say at least one benefic.
    planets_in_2 = yoga.planets_in_relative_house("Lagna", 2)
    benefics_in_2 = [p["name"] for p in planets_in_2 if p["name"] in BENEFIC_PLANETS]
    if benefics_in_2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Benefics in 2nd House: {', '.join(benefics_in_2)}."
        return result

    # Cond 2: L2 in Kendra (Exalt/Own/Friend) AND Lord of that Kendra (L_Kendra) attains Gopuramsa.
    if h_l2 in kendras:
        p_l2 = yoga.get_planet_by_name(l2)
        if not p_l2 or p_l2["name"] == "Lagna":
            raise ValueError("L2 not found or is Lagna")
        relation = p_l2["inSign"]  # e.g. "Friend's Sign"
        valid_relation = False
        if "Exalted" in relation or "Own" in relation or "Friend" in relation:
            valid_relation = True

        if valid_relation:
            # Lord of that Kendra
            l_kendra = yoga.get_lord_of_house(h_l2)
            # Attains Gopuramsa (Use isPlanetPowerful as proxy for now, or check explicit strength if possible)
            # Gopuramsa is a specific Varga strength (4 vargas).
            # "isPlanetPowerful" isn't strictly Gopuramsa.
            # But assume Strong for now.
            if l_kendra:
                p_lk = yoga.get_planet_by_name(l_kendra)
                if not p_lk or p_lk["name"] == "Lagna":
                    raise ValueError("L_Kendra not found or is Lagna")
                is_strong, _ = yoga.isPlanetPowerful(p_lk)
                if is_strong:
                    result["present"] = True
                    result["strength"] = 1.0
                    result["details"] = (
                        f"L2 ({l2}) good in Kendra. Lord ({l_kendra}) is Strong/Gopuramsa."
                    )
                    return result

    result["details"] = "No Sumukha conditions met."
    return result


@register_yoga("Durmukha")
def Durmukha(yoga: Yoga) -> YogaType:
    """
    Malefics occupies the second and its Lord joins an evil planet or is in debilitation.
    or
    The Lord of the second house being evil, joins Gulika or occupies unfriendly and debilitated Navamsa with malefics.
    (Note: Gulika not available. 'Evil' = Malefic.)

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Durmukha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        return result

    # Cond 1: Malefics in 2nd AND (L2 joins Evil OR L2 Debilitated)
    planets_in_2 = yoga.planets_in_relative_house("Lagna", 2)
    malefics_in_2 = [p["name"] for p in planets_in_2 if p["name"] in MALEFIC_PLANETS]

    # Helper to check if L2 is debilitated
    debilitation_map = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }
    if (h_l2 := yoga.get_house_of_planet(l2)) is None:
        raise ValueError(f"Invalid planet {l2}")
    if (sign_l2 := yoga.get_rashi_of_house(h_l2)) is None:
        raise ValueError(f"Invalid house {h_l2}")
    is_l2_debilitated = sign_l2 == debilitation_map.get(l2)

    # Helper to check if L2 joins an "Evil Planet" (Malefic)
    # Get planets in same house as L2
    planets_with_l2 = yoga.planets_in_relative_house("Lagna", h_l2)
    has_evil_with_l2 = any(
        p["name"] in MALEFIC_PLANETS and p["name"] != l2 for p in planets_with_l2
    )

    if malefics_in_2:
        if has_evil_with_l2 or is_l2_debilitated:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Malefics in 2nd. L2 with Malefics or Debilitated."
            return result

    # Cond 2: L2 is Evil (Malefic) AND (Joins Gulika [Skip] OR (In Unfriendly AND Debilitated Navamsa with Malefics))
    # Text says: "occupies unfriendly AND debilitated Navamsa". Both?
    # Usually Debilitated implies Unfriendly (or worse).
    # And "with malefics".
    if l2 in MALEFIC_PLANETS:
        # Check Navamsa
        d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
        if not d9_chart:
            raise ValueError("Navamsa chart not found")
        l2_in_d9 = None
        planets_with_l2_d9 = []

        for data in d9_chart.values():
            p_names = [p["name"] for p in data["planets"]]
            if l2 in p_names:
                l2_in_d9 = data["planets"][0]["sign"]["name"]  # The sign L2 is in
                planets_with_l2_d9 = p_names
                break

        if l2_in_d9:
            # Check Debilitated in D9
            is_deb_d9 = l2_in_d9 == debilitation_map.get(l2)
            # Check Unfriendly?
            # Skip explicit Unfriendly check if we have Debilitated.
            # Check "with malefics" in D9
            has_malefics_in_d9 = any(
                p in MALEFIC_PLANETS and p != l2 for p in planets_with_l2_d9
            )

            if is_deb_d9 and has_malefics_in_d9:
                result["present"] = True
                result["strength"] = 1.0
                result["details"] = (
                    "L2 Malefic and Debilitated in Navamsa with Malefics."
                )
                return result

    result["details"] = "No Durmukha conditions met."
    return result


@register_yoga("Bhojana Soukhya")
def BhojanaSoukhya(yoga: Yoga) -> YogaType:
    """
    The powerful Lord of the second house occupies Vaiseshikamsa
    and has the aspect of Jupiter or Venus.

    [Positive Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Bhojana Soukhya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        result["details"] = "Could not find Lord of 2nd house."
        return result

    # Cast to PLANETS for Pyright
    l2_planet: PLANETS = cast(PLANETS, l2)

    # 1. Check if L2 is powerful / Vaiseshikamsa
    p_l2 = yoga.get_planet_by_name(l2_planet)
    if not p_l2 or p_l2["name"] == "Lagna":
        raise ValueError("L2 not found or is Lagna")

    is_strong, _ = yoga.isPlanetPowerful(p_l2)
    if not is_strong:
        result["details"] = f"L2 ({l2_planet}) is not strong/Vaiseshikamsa."
        return result

    # 2. Check if Jupiter or Venus aspects L2
    if (h_l2 := yoga.get_house_of_planet(l2_planet)) is None:
        raise ValueError(f"Invalid planet {l2_planet}")
    aspecting_planets: List[PLANETS] = []

    for p_name in ["Jupiter", "Venus"]:
        p: PLANETS = cast(PLANETS, p_name)
        try:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=p) or []
            for aspect in aspects:
                for houses in aspect.get("aspect_houses", []):
                    if h_l2 in houses:
                        aspecting_planets.append(p)
        except Exception as e:
            print(f"Error checking aspecting planets: {e}")
            continue

    if aspecting_planets:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"L2 ({l2_planet}) is strong/Vaiseshikamsa and aspected by {', '.join(aspecting_planets)}."
        )
        return result

    result["details"] = (
        f"L2 ({l2_planet}) is strong but not aspected by Jupiter or Venus."
    )
    return result


@register_yoga("Parannabhojana")
def Parannabhojana(yoga: Yoga) -> YogaType:
    """
    The Lord of the second house is in debilitation or in unfriendly navamsas
    and aspected by a debilitated planet.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Parannabhojana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        result["details"] = "Could not find Lord of 2nd house."
        return result

    l2_planet: PLANETS = cast(PLANETS, l2)

    # Debilitation map
    debilitation_map: dict[PLANETS, str] = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }

    # Check L2 Debilitated in Rashi
    if (h_l2 := yoga.get_house_of_planet(l2_planet)) is None:
        raise ValueError(f"Invalid planet {l2_planet}")
    if (sign_l2 := yoga.get_rashi_of_house(h_l2)) is None:
        raise ValueError(f"Invalid house {h_l2}")
    is_l2_deb: bool = sign_l2 == debilitation_map.get(l2_planet)

    # Check Navamsa (D9)
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    l2_in_d9_sign: str | None = None
    if d9_chart:
        for data in d9_chart.values():
            for planet in data["planets"]:
                planet_name = planet["name"]
                if planet_name == l2_planet:
                    l2_in_d9_sign = planet["sign"]["name"]

    is_l2_deb_d9: bool = (
        l2_in_d9_sign == debilitation_map.get(l2_planet) if l2_in_d9_sign else False
    )

    if not (is_l2_deb or is_l2_deb_d9):
        result["details"] = "L2 not debilitated in Rashi or Navamsa."
        return result

    # Check if aspected by a debilitated planet
    debilitated_aspectors: list[PLANETS] = []
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p: PLANETS = cast(PLANETS, p_name)
        if (h_p := yoga.get_house_of_planet(p)) is None:
            raise ValueError(f"Invalid planet {p}")
        if (sign_p := yoga.get_rashi_of_house(h_p)) is None:
            raise ValueError(f"Invalid house {h_p}")
        if sign_p != debilitation_map.get(p):
            continue

        # Debilitated planet, check aspect on L2
        try:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=p) or []
            for aspect in aspects:
                for houses in aspect.get("aspect_houses", []):
                    if h_l2 in houses:
                        debilitated_aspectors.append(p)
        except Exception as e:
            print(f"Error occurred while checking aspect: {e}")
            continue

    if debilitated_aspectors:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            f"L2 debilitated. Aspected by debilitated planets: {', '.join(debilitated_aspectors)}."
        )
        return result

    result["details"] = "L2 debilitated, but not aspected by any debilitated planet."
    return result


@register_yoga("Sraddhannabhuktha")
def Sraddhannabhuktha(yoga: Yoga) -> YogaType:
    """
    Saturn owns the second house, or joins the second Lord, or the second house is aspected by debilitated Saturn.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Sraddhannabhuktha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        result["details"] = "Could not find L2."
        return result

    l2_planet: PLANETS = cast(PLANETS, l2)
    saturn: PLANETS = "Saturn"

    # Cond A: Saturn owns 2nd
    if l2_planet == saturn:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Saturn is L2."
        return result

    # Cond B: Saturn joins L2
    if (h_l2 := yoga.get_house_of_planet(l2_planet)) is None:
        raise ValueError(f"Invalid planet {l2_planet}")
    if (h_saturn := yoga.get_house_of_planet(saturn)) is None:
        raise ValueError(f"Invalid planet {saturn}")
    if h_l2 == h_saturn:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Saturn joins L2 ({l2_planet})."
        return result

    # Cond C: 2nd House aspected by Debilitated Saturn
    # Saturn debilitation = Aries
    sign_saturn: str | None = yoga.get_rashi_of_house(h_saturn) if h_saturn else None
    if sign_saturn == "Aries":
        try:
            aspects: Sequence[dict] = cast(
                Sequence[dict], yoga.__chart__.graha_drishti(n=1, planet=saturn) or []
            )
            for aspect in aspects:
                for houses in aspect.get("aspect_houses", []):
                    if 2 in houses:
                        result["present"] = True
                        result["strength"] = 1.0
                        result["details"] = "2nd House aspected by Debilitated Saturn."
                        return result
        except Exception as e:
            print(f"Error occurred while checking aspects: {e}")

    result["details"] = "No Sraddhannabhuktha conditions met."
    return result


@register_yoga("Vakchalana")
def Vakchalana(yoga: Yoga) -> YogaType:
    """
    A malefic owns the second house, joins a cruel navamsa and the second house is devoid of benefic aspect or association.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "Vakchalana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    l2 = yoga.get_lord_of_house(2)
    if not l2:
        return result

    # 1. Malefic owns 2nd
    if l2 not in MALEFIC_PLANETS:
        result["details"] = f"L2 ({l2}) is not Malefic."
        return result

    # 2. Joins Cruel Navamsa (L2 in D9 in sign owned by Malefic)
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if not d9_chart:
        raise ValueError("D9 chart not found")

    l2_navamsa_lord: PLANETS | None = None
    for house_data in d9_chart.values():
        for p in house_data.get("planets", []):
            if p["name"] == l2:
                sign_name = p.get("sign", {}).get("name")
                if sign_name:
                    l2_navamsa_lord = RASHI_LORD_MAP.get(sign_name)
                break
        if l2_navamsa_lord:
            break

    if not l2_navamsa_lord or l2_navamsa_lord not in MALEFIC_PLANETS:
        result["details"] = (
            f"L2 Navamsa Lord ({l2_navamsa_lord}) is not Malefic (Cruel)."
        )
        return result

    # 3. Second House devoid of benefic aspect or association
    planets_in_2 = yoga.planets_in_relative_house("Lagna", 2)
    has_benefic_assoc = any(p["name"] in BENEFIC_PLANETS for p in planets_in_2)

    def is_house_aspected_by_benefic(house: HOUSES) -> bool:
        for p in BENEFIC_PLANETS:
            aspects_list: Sequence[dict] = cast(
                Sequence[dict], yoga.__chart__.graha_drishti(n=1, planet=p) or []
            )
            for aspect in aspects_list:
                for houses in aspect.get("aspect_houses", []):
                    if house in houses:
                        return True
        return False

    has_benefic_aspect = is_house_aspected_by_benefic(2)

    if not has_benefic_assoc and not has_benefic_aspect:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "L2 Malefic in Cruel Navamsa. 2nd House has no Benefic influence."
        )
        return result

    result["details"] = "L2 Malefic/Cruel Navamsa, but 2nd House has Benefics."
    return result


@register_yoga("VishapraYoga")
def VishapraYoga(yoga: Yoga) -> YogaType:
    """
    The second house is joined and aspected by malefics and the second Lord is in a cruel navamsa aspected by a malefic.

    [Negative Yoga]
    """
    result: YogaType = {
        "id": "",
        "name": "VishapraYoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    # Helper to check if a house is aspected by malefics
    def is_house_aspected_by_malefic(target_house: HOUSES) -> bool:
        for malefic in MALEFIC_PLANETS:
            aspects_list: Sequence[dict] = cast(
                Sequence[dict], yoga.__chart__.graha_drishti(n=1, planet=malefic) or []
            )
            for aspect in aspects_list:
                for houses in aspect.get("aspect_houses", []):
                    if target_house in houses:
                        return True
        return False

    # 1. 2nd House joined AND aspected by malefics
    planets_in_2 = yoga.planets_in_relative_house("Lagna", 2)
    joined_malefic = any(p["name"] in MALEFIC_PLANETS for p in planets_in_2)
    aspected_malefic = is_house_aspected_by_malefic(2)

    if not (joined_malefic and aspected_malefic):
        result["details"] = "2nd House not Joined AND Aspected by Malefics."
        return result

    # 2. L2 in Cruel Navamsa
    l2 = yoga.get_lord_of_house(2)
    if not l2:
        return result

    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if not d9_chart:
        raise ValueError("Navamsa chart not found")

    l2_navamsa_lord: PLANETS | None = None
    for house_data in d9_chart.values():
        for p in house_data.get("planets", []):
            if p["name"] == l2:
                sign_name = p.get("sign", {}).get("name")
                if sign_name:
                    l2_navamsa_lord = RASHI_LORD_MAP.get(sign_name)
                break
        if l2_navamsa_lord:
            break

    if not l2_navamsa_lord or l2_navamsa_lord not in MALEFIC_PLANETS:
        result["details"] = "L2 not in Cruel Navamsa."
        return result

    # 3. L2 aspected by malefic in Rashi chart
    if (h_l2 := yoga.get_house_of_planet(l2)) is None:
        raise ValueError(f"Invalid planet {l2}")
    l2_aspected_by_malefic = is_house_aspected_by_malefic(h_l2)

    if l2_aspected_by_malefic:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "2nd House joined/aspected by malefics. L2 in Cruel Navamsa & aspected by Malefic."
        )
        return result

    result["details"] = "L2 conditions met, but not Aspected by Malefic."
    return result
