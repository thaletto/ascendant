from ascendant.const import BENEFIC_PLANETS, MALEFIC_PLANETS, RASHI_LORD_MAP
from ascendant.types import YogaType
from ascendant.yoga.base import Yoga, register_yoga


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

    # Condition 1: Lagna in fixed sign
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
