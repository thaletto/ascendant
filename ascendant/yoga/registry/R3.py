# pyright: strict
from ascendant.const import (
    BENEFIC_PLANETS,
    BENEFIC_SIGNS,
    FIXED_SIGNS,
    MALEFIC_PLANETS,
    MOVABLE_SIGNS,
    RASHI_LORD_MAP,
)
from ascendant.types import HOUSES, PLANETS, RASHIS, YogaType
from ascendant.yoga.base import Yoga, register_yoga


def get_navamsa_lord(yoga: Yoga, planet_name: PLANETS) -> str | None:
    """Helper to get the Lord of the Navamsa occupied by a planet"""
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if not d9_chart:
        return None
    for house_data in d9_chart.values():
        for planet in house_data["planets"]:
            if planet["name"] == planet_name:
                # Found planet in D9
                # Sign of this house in D9
                sign = house_data["sign"]
                return RASHI_LORD_MAP.get(sign)
    return None


def get_navamsa_sign(yoga: Yoga, planet_name: PLANETS) -> RASHIS | None:
    """Helper to get the Navamsa Sign occupied by a planet"""
    d9_chart = yoga.__chart__.get_varga_chakra_chart(9)
    if not d9_chart:
        return None
    for house_data in d9_chart.values():
        for planet in house_data["planets"]:
            if planet["name"] == planet_name:
                return house_data["sign"]
    return None


@register_yoga("Bhratruvriddhi")
def bhratruvriddhi(yoga: Yoga) -> YogaType:
    """
    The third Lord, or Mars, or the third house are joined or aspected by benefics or strong.
    """
    result: YogaType = {
        "id": "",
        "name": "Bhratruvriddhi",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    third_lord = yoga.get_lord_of_house(3)
    third_lord_condition = False

    third_lord_planet = yoga.get_planet_by_name(third_lord)

    if third_lord_planet["name"] == "Lagna":
        raise ValueError(f"Invalid planet name: {third_lord}")

    is_strong, _ = yoga.is_planet_powerful(third_lord_planet)
    third_lord_house = yoga.get_house_of_planet(third_lord)

    joined_benefics = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", third_lord_house)
        if p["name"] in BENEFIC_PLANETS and p["name"] != third_lord
    ]
    benefic_aspect = yoga.is_house_benefic_aspected(third_lord_house)

    if is_strong or joined_benefics or benefic_aspect:
        third_lord_condition = True

    mars_condition = False
    mars_planet = yoga.get_planet_by_name("Mars")
    if mars_planet["name"] == "Lagna":
        raise ValueError(f"Invalid planet name: {mars_planet}")

    is_strong, _ = yoga.is_planet_powerful(mars_planet)
    house_mars = yoga.get_house_of_planet("Mars")
    joined_benefics = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", house_mars)
        if p["name"] in BENEFIC_PLANETS and p["name"] != "Mars"
    ]
    benefic_aspect = yoga.is_house_benefic_aspected(house_mars)

    if is_strong or joined_benefics or benefic_aspect:
        mars_condition = True

    third_house_condition = False
    planets_in_3 = yoga.planets_in_relative_house("Lagna", 3)
    benefics_in_3 = [p["name"]
                     for p in planets_in_3 if p["name"] in BENEFIC_PLANETS]
    h3_aspected = yoga.is_house_benefic_aspected(3)

    if benefics_in_3 or h3_aspected:
        third_house_condition = True

    if third_lord_condition or mars_condition or third_house_condition:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "3rd Lord/Mars/3rd House is strong or associated with benefics."
        )
    else:
        result["details"] = (
            "3rd Lord, Mars, and 3rd House lack strength or benefic association."
        )

    return result


@register_yoga("Sodaranasa")
def sodaranasa(yoga: Yoga) -> YogaType:
    """
    Mars and the third Lord occupies the eighth (third, fifth or seventh) house and are aspected by malefic.
    """
    result: YogaType = {
        "id": "",
        "name": "Sodaranasa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    third_lord = yoga.get_lord_of_house(3)
    if not third_lord:
        result["details"] = "Lord of 3rd not found."
        return result

    third_lord_house = yoga.get_house_of_planet(third_lord)
    mars_house = yoga.get_house_of_planet("Mars")

    target_houses = [3, 5, 7, 8]

    if third_lord_house not in target_houses or mars_house not in target_houses:
        result["details"] = f"Mars ({mars_house}) or 3rd Lord ({third_lord_house}) not in 3, 5, 7, 8."
        return result

    def is_aspected_by_malefic(house: HOUSES) -> bool:
        for malefic in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic)
            if aspects:
                for aspect in aspects:
                    for aspect_house in aspect["aspect_houses"]:
                        if house in aspect_house:
                            return True
        return False

    mars_aspected = is_aspected_by_malefic(mars_house)
    third_lord_aspected = is_aspected_by_malefic(third_lord_house)

    if mars_aspected and third_lord_aspected:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Mars and 3rd Lord in 3/5/7/8 aspected by malefics."
    else:
        result["details"] = "Mars or L3 lack malefic aspect required."

    return result


@register_yoga("Ekabhagini")
def ekabhagini(yoga: Yoga) -> YogaType:
    """
    Mercury, the Lord of the third house, and Mars join the third house, the Moon and Saturn respectively.
    """
    result: YogaType = {
        "id": "",
        "name": "Ekabhagini",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    mercury_house = yoga.get_house_of_planet("Mercury")
    if mercury_house != 3:
        result["details"] = "Mercury not in 3rd house."
        return result

    third_lord = yoga.get_lord_of_house(3)

    third_lord_house = yoga.get_house_of_planet(third_lord)
    moon_house = yoga.get_house_of_planet("Moon")

    if third_lord_house != moon_house:
        result["details"] = f"3rd Lord ({third_lord}) not with Moon."
        return result

    mars_house = yoga.get_house_of_planet("Mars")
    saturn_house = yoga.get_house_of_planet("Saturn")
    if mars_house != saturn_house:
        result["details"] = "Mars not with Saturn."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "Mercury in 3rd, L3 with Moon, Mars with Saturn."
    return result


@register_yoga("Dwadasa Sahodara")
def dwadasa_sahodara(yoga: Yoga) -> YogaType:
    """
    The third Lord is in a kendra and exalted Mars joins Jupiter in a thrikona from the third Lord.
    """
    result: YogaType = {
        "id": "",
        "name": "Dwadasa Sahodara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    third_lord = yoga.get_lord_of_house(3)
    third_lord_house = yoga.get_house_of_planet(third_lord)

    if not yoga.planet_in_kendra_from(1, third_lord):
        result["details"] = "3rd Lord not in Kendra."
        return result

    mars_planet = yoga.get_planet_by_name("Mars")

    if mars_planet["name"] == "Lagna":
        raise ValueError("Mars not found.")
    if "Exalted" not in mars_planet["inSign"]:
        result["details"] = "Mars not exalted."
        return result

    mars_house = yoga.get_house_of_planet("Mars")
    jupiter_house = yoga.get_house_of_planet("Jupiter")
    if mars_house != jupiter_house:
        result["details"] = "Mars not with Jupiter."
        return result

    trikona_houses = [(third_lord_house - 1 + i - 1) % 12 + 1 for i in [1, 5, 9]]
    if mars_house not in trikona_houses:
        result["details"] = "Mars/Jupiter not in Trikona from 3rd Lord."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in Kendra; Exalted Mars with Jupiter in Trikona from L3."
    return result


@register_yoga("Sapthasankhya Sahodara")
def sapthasankhya_sahodara(yoga: Yoga) -> YogaType:
    """
    Lord of the twelfth house joins Mars, and the Moon is in the third with Jupiter, devoid of association with or aspect of Venus.
    """
    result: YogaType = {
        "id": "",
        "name": "Sapthasankhya Sahodara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    twelfth_lord = yoga.get_lord_of_house(12)
    twelfth_lord_house = yoga.get_house_of_planet(twelfth_lord)
    mars_house = yoga.get_house_of_planet("Mars")

    if twelfth_lord_house != mars_house:
        result["details"] = "12th Lord not with Mars."
        return result

    moon_house = yoga.get_house_of_planet("Moon")
    jupiter_house = yoga.get_house_of_planet("Jupiter")

    if moon_house != 3 or jupiter_house != 3:
        result["details"] = "Moon or Jupiter not in 3rd house."
        return result

    venus_house = yoga.get_house_of_planet("Venus")
    if venus_house == 3:
        result["details"] = "Venus conjoined with Moon/Jupiter."
        return result

    venus_aspects = yoga.__chart__.graha_drishti(n=1, planet="Venus")
    if venus_aspects:
        for aspect in venus_aspects[0]["aspect_houses"]:
            if 3 in aspect:
                result["details"] = "Venus aspects 3rd house."
                return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L12 with Mars; Moon/Jup in 3rd without Venus influence."
    return result


@register_yoga("Parakrama")
def parakrama(yoga: Yoga) -> YogaType:
    """
    The Lord of the third house joins a benefic navamsa being aspected by (or conjoined with) benefic planets, and Mars occupies benefic signs.
    """
    result: YogaType = {
        "id": "",
        "name": "Parakrama",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    third_lord = yoga.get_lord_of_house(3)

    third_lord_navamsa_sign = get_navamsa_sign(yoga, third_lord)
    if not third_lord_navamsa_sign or third_lord_navamsa_sign not in BENEFIC_SIGNS:
        result["details"] = "3rd Lord Navamsa is not benefic."
        return result

    third_lord_house = yoga.get_house_of_planet(third_lord)

    joined_benefics = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", third_lord_house)
        if p["name"] in BENEFIC_PLANETS and p["name"] != third_lord
    ]
    aspected_by_benefic = False
    for benefic_planet in BENEFIC_PLANETS:
        if benefic_planet == third_lord:
            continue
        aspects = yoga.__chart__.graha_drishti(n=1, planet=benefic_planet)
        if aspects:
            for aspect in aspects[0]["aspect_houses"]:
                if third_lord_house in aspect:
                    aspected_by_benefic = True
                    break

    if not (joined_benefics or aspected_by_benefic):
        result["details"] = "3rd Lord not aspected/conjoined by benefics."
        return result

    mars_house = yoga.get_house_of_planet("Mars")
    mars_sign = yoga.get_rashi_of_house(mars_house)
    if mars_sign not in BENEFIC_SIGNS:
        result["details"] = "Mars not in benefic sign."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in benefic D9/aspected by benefics; Mars in benefic sign."
    return result


@register_yoga("Yuddha Praveena")
def yuddha_praveena(yoga: Yoga) -> YogaType:
    """
    The Lord of the navamsa joined by the planet that owns the navamsa in which the third Lord is placed, joins its own vargas.
    """
    result: YogaType = {
        "id": "",
        "name": "Yuddha Praveena",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    third_lord = yoga.get_lord_of_house(3)

    if (third_lord_navamsa_sign := get_navamsa_sign(yoga, third_lord)) is None:
        raise ValueError(f"Could not find Navamsa of {third_lord}.")

    if (first_dispositor := RASHI_LORD_MAP.get(third_lord_navamsa_sign)) is None:
        raise ValueError(f"No lord found for Navamsa {third_lord_navamsa_sign}.")

    if (first_dispositor_navamsa_sign := get_navamsa_sign(yoga, first_dispositor)) is None:
        raise ValueError(f"Could not find Navamsa of {first_dispositor}.")

    if (second_dispositor := RASHI_LORD_MAP.get(first_dispositor_navamsa_sign)) is None:
        raise ValueError(f"No lord found for Navamsa {first_dispositor_navamsa_sign}.")

    second_dispositor_house = yoga.get_house_of_planet(second_dispositor)

    second_dispositor_rashi_sign = yoga.get_rashi_of_house(second_dispositor_house)

    if (second_dispositor_navamsa_sign := get_navamsa_sign(yoga, second_dispositor)) is None:
        raise ValueError(f"Could not find Navamsa of {second_dispositor}.")

    own_rashi = RASHI_LORD_MAP.get(second_dispositor_rashi_sign) == second_dispositor
    own_navamsa = RASHI_LORD_MAP.get(second_dispositor_navamsa_sign) == second_dispositor

    if own_rashi or own_navamsa:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Target Planet {second_dispositor} is in own Rasi or Navamsa."
    else:
        result["details"] = f"Target Planet {second_dispositor} not in own vargas."

    return result


@register_yoga("Yuddhatpoorvadridhachitta")
def yuddhatpoorvadridhachitta(yoga: Yoga) -> YogaType:
    """
    The exalted Lord of the third house joins malefics in movable Rasis or Navamsas.
    """
    result: YogaType = {
        "id": "",
        "name": "Yuddhatpoorvadridhachitta",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    third_lord = yoga.get_lord_of_house(3)

    third_lord_planet = yoga.get_planet_by_name(third_lord)

    if third_lord_planet["name"] == "Lagna":
        raise ValueError("Planet of Lord of house 3 not found")

    if "Exalted" not in third_lord_planet["inSign"]:
        result["details"] = "L3 not exalted."
        return result

    third_lord_house = yoga.get_house_of_planet(third_lord)

    malefics_with_l3 = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", third_lord_house)
        if p["name"] in MALEFIC_PLANETS and p["name"] != third_lord
    ]
    if not malefics_with_l3:
        result["details"] = "L3 not with Malefics."
        return result

    rasi_sign = yoga.get_rashi_of_house(third_lord_house)
    navamsa_sign = get_navamsa_sign(yoga, third_lord)

    if rasi_sign in MOVABLE_SIGNS or navamsa_sign in MOVABLE_SIGNS:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Exalted L3 joins malefics in Movable Rasi/Navamsa."
    else:
        result["details"] = "L3 not in Movable Rasi/Navamsa."

    return result


@register_yoga("Yuddhatpaschaddrudha")
def yuddhatpaschaddrudha(yoga: Yoga) -> YogaType:
    """
    The Lord of the third house occupies a fixed Rasi, a fixed Navamsa and a cruel Shahtiamsa, and the Lord of the Rasi so occupied is in debility.
    """
    result: YogaType = {
        "id": "",
        "name": "Yuddhatpaschaddrudha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    third_lord = yoga.get_lord_of_house(3)

    third_lord_house = yoga.get_house_of_planet(third_lord)

    rasi_sign = yoga.get_rashi_of_house(third_lord_house)

    if rasi_sign not in FIXED_SIGNS:
        result["details"] = "L3 not in Fixed Rasi."
        return result

    navamsa_sign = get_navamsa_sign(yoga, third_lord)
    if navamsa_sign not in FIXED_SIGNS:
        result["details"] = "L3 not in Fixed Navamsa."
        return result

    d60_chart = yoga.__chart__.get_varga_chakra_chart(60)
    if not d60_chart:
        result["details"] = "Could not generate D60 chart."
        return result

    l3_found_in_d60 = False
    for house_data in d60_chart.values():
        for planet in house_data["planets"]:
            if planet["name"] == third_lord:
                l3_found_in_d60 = True
                break
        if l3_found_in_d60:
            break

    if not l3_found_in_d60:
        result["details"] = f"L3 ({third_lord}) not found in D60 chart."
        return result

    if (lord_of_occupied_rasi := RASHI_LORD_MAP.get(rasi_sign)) is None:
        raise ValueError("Lord of occupied rasi not found")

    dispositor_planet = yoga.get_planet_by_name(lord_of_occupied_rasi)
    if dispositor_planet["name"] == "Lagna":
        raise ValueError("Lord of occupied rasi not found")

    if "Debilitated" not in dispositor_planet["inSign"]:
        result["details"] = f"Dispositor ({lord_of_occupied_rasi}) is not debilitated."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in Fixed signs/D60; Dispositor debilitated."
    return result


@register_yoga("Satkathadisravana")
def satkathadisravana(yoga: Yoga) -> YogaType:
    """
    The third house is a benefic sign aspected by benefic planets and the third Lord joins a benefic amsa.
    """
    result: YogaType = {
        "id": "",
        "name": "Satkathadisravana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    third_house_sign = yoga.get_rashi_of_house(3)
    if third_house_sign not in BENEFIC_SIGNS:
        result["details"] = "3rd House not a benefic sign."
        return result

    if not yoga.is_house_benefic_aspected(3):
        result["details"] = "3rd House not aspected by benefics."
        return result

    third_lord = yoga.get_lord_of_house(3)

    third_lord_navamsa_sign = get_navamsa_sign(yoga, third_lord)
    if third_lord_navamsa_sign not in BENEFIC_SIGNS:
        result["details"] = "3rd Lord not in Benefic Amsa."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "3rd House benefic/aspected; L3 in benefic Navamsa."
    return result


@register_yoga("Uttama Griha")
def uttama_griha(yoga: Yoga) -> YogaType:
    """
    The Lord of the fourth house joins benefics in a kendra or thrikona.
    """
    result: YogaType = {
        "id": "",
        "name": "Uttama Griha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    fourth_lord = yoga.get_lord_of_house(4)
    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

    target_houses = [1, 4, 5, 7, 9, 10]
    if fourth_lord_house not in target_houses:
        result["details"] = "L4 not in Kendra/Thrikona."
        return result

    joined_benefics = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", fourth_lord_house)
        if p["name"] in BENEFIC_PLANETS and p["name"] != fourth_lord
    ]
    if not joined_benefics:
        result["details"] = "L4 not joined by benefics."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "4th Lord joins benefics in Kendra or Trikona."
    return result


@register_yoga("Vichitra Saudha Prakara")
def vichitra_saudha_prakara(yoga: Yoga) -> YogaType:
    """
    The Lords of the fourth and tenth are conjoined together with Saturn and Mars.
    """
    result: YogaType = {
        "id": "",
        "name": "Vichitra Saudha Prakara",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    fourth_lord = yoga.get_lord_of_house(4)
    tenth_lord = yoga.get_lord_of_house(10)

    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)
    tenth_lord_house = yoga.get_house_of_planet(tenth_lord)
    saturn_house = yoga.get_house_of_planet("Saturn")
    mars_house = yoga.get_house_of_planet("Mars")

    if not (fourth_lord_house == tenth_lord_house == saturn_house == mars_house):
        result["details"] = "L4, L10, Saturn, and Mars are not conjoined."
        return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L4, L10, Saturn, and Mars are conjoined."
    return result


@register_yoga("Ayatna Griha Prapta Yoga")
def ayatna_griha_prapta_yoga(yoga: Yoga) -> YogaType:
    """
    Lords of Lagna and the seventh house occupies Lagna or the fourth house, aspected by benefics.
    or
    The Lord of the ninth is posited in a kendra and the Lord of the fourth is in exaltation, moolathrikona or own house.
    """
    result: YogaType = {
        "id": "",
        "name": "Ayatna Griha Prapta Yoga",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Condition 1 Failure Reason
    c1_fail = "L1 or L7 missing"

    lagna_lord = yoga.get_lord_of_house(1)
    seventh_lord = yoga.get_lord_of_house(7)
    cond1_met = False

    if lagna_lord and seventh_lord:
        lagna_lord_house = yoga.get_house_of_planet(lagna_lord)
        seventh_lord_house = yoga.get_house_of_planet(seventh_lord)
        allowed = [1, 4]

        if lagna_lord_house not in allowed or seventh_lord_house not in allowed:
            c1_fail = "L1/L7 not in 1/4"
        elif not (
            yoga.is_house_benefic_aspected(lagna_lord_house)
            and yoga.is_house_benefic_aspected(seventh_lord_house)
        ):
            c1_fail = "L1/L7 houses not aspected by benefics"
        else:
            cond1_met = True

    if cond1_met:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L1/L7 in 1/4 aspected by benefics."
        return result

    # Condition 2 Failure Reason
    condition_two_failure = "L9 or L4 missing"

    ninth_lord = yoga.get_lord_of_house(9)
    fourth_lord = yoga.get_lord_of_house(4)
    cond2_met = False

    if ninth_lord and fourth_lord:
        if not yoga.planet_in_kendra_from(1, ninth_lord):
            condition_two_failure = "L9 not in Kendra"
        else:
            fourth_lord_planet = yoga.get_planet_by_name(fourth_lord)
            if fourth_lord_planet["name"] == "Lagna":
                raise ValueError("Lord of 4th house not found.")
            valid_status = ["Exalted", "Moola Trikona", "Own"]
            if any(s in fourth_lord_planet["inSign"] for s in valid_status):
                cond2_met = True
            else:
                condition_two_failure = "L4 not Exalted/MT/Own"

    if cond2_met:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L9 in Kendra and L4 Strong."
        return result

    result["details"] = f"{c1_fail}; {condition_two_failure}."
    return result


@register_yoga("Grihanasa")
def grihanasa(yoga: Yoga) -> YogaType:
    """
    The Lord of the fourth is in the twelfth house aspected by a malefic.
    or
    The Lord of the navamsa occupied by the Lord of the fourth is disposed in the eleventh house.
    """
    result: YogaType = {
        "id": "",
        "name": "Grihanasa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    fourth_lord = yoga.get_lord_of_house(4)
    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

    # Condition 1
    condition_one = False
    if fourth_lord_house == 12:
        aspected = False
        for malefic in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic)
            if aspects:
                for aspect in aspects[0]["aspect_houses"]:
                    if fourth_lord_house in aspect:
                        aspected = True
                        break
        if aspected:
            condition_one = True

    # Condition 2
    condition_two = False
    fourth_lord_navamsa_sign = get_navamsa_sign(yoga, fourth_lord)
    if fourth_lord_navamsa_sign:
        fourth_lord_navamsa_lord = RASHI_LORD_MAP.get(fourth_lord_navamsa_sign)
        if fourth_lord_navamsa_lord:
            if yoga.get_house_of_planet(fourth_lord_navamsa_lord) == 11:
                condition_two = True

    if condition_one or condition_two:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "L4 in 12th aspected by malefic OR Dispositor of L4's Navamsa in 11th."
        )
    else:
        result["details"] = (
            "L4 not in 12th malefic-aspected; D9 Dispositor not in 11th."
        )

    return result


@register_yoga("Bandhu Pujya")
def bandhu_pujya(yoga: Yoga) -> YogaType:
    """
    The benefic Lord of the fourth is aspected by another benefic and Mercury is situated in Lagna.
    or
    The fourth house or the fourth Lord has the association or aspect of Jupiter.
    """
    result: YogaType = {
        "id": "",
        "name": "Bandhu Pujya",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    fourth_lord = yoga.get_lord_of_house(4)

    # Condition 1
    condition_one = False
    if fourth_lord in BENEFIC_PLANETS:
        mercury_house = yoga.get_house_of_planet("Mercury")
        if mercury_house == 1:
            # Check aspect by another benefic on L4
            fourth_lord_house = yoga.get_house_of_planet(fourth_lord)
            aspected = False
            for benefic_planet in BENEFIC_PLANETS:
                if benefic_planet == fourth_lord:
                    continue
                aspects = yoga.__chart__.graha_drishti(n=1, planet=benefic_planet)
                for aspect in aspects:
                    if any(h == fourth_lord_house for group in aspect["aspect_houses"] for h in group):
                        aspected = True
            if aspected:
                condition_one = True

    # Condition 2: Jupiter Assoc/Aspect 4th House or 4th Lord
    condition_two = False
    jupiter_house = yoga.get_house_of_planet("Jupiter")
    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

    # Assoc
    if jupiter_house == 4 or jupiter_house == fourth_lord_house:
        condition_two = True
    else:
        # Aspect
        aspects = yoga.__chart__.graha_drishti(n=1, planet="Jupiter")
        if aspects:
            for aspect in aspects[0]["aspect_houses"]:
                if 4 in aspect or fourth_lord_house in aspect:
                    condition_two = True
                    break

    if condition_one or condition_two:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "Benefic L4 aspected by benefic with Merc in 1 OR Jup assoc with 4H/L4."
        )
    else:
        result["details"] = "No specific benefic association with 4H/L4."

    return result


@register_yoga("Bandhubhisthyaktha")
def bandhubhisthyaktha(yoga: Yoga) -> YogaType:
    """
    The fourth Lord is associated with malefics or occupies evil shashtiamsas or joins inimical or debilitation signs.
    """
    result: YogaType = {
        "id": "",
        "name": "Bandhubhisthyaktha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    fourth_lord = yoga.get_lord_of_house(4)

    fourth_lord_planet = yoga.get_planet_by_name(fourth_lord)

    if fourth_lord_planet["name"] == "Lagna":
        raise ValueError("Planet of Lord of house 4 not found")

    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

    # 1. Associated with malefics
    malefics_with_l4 = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", fourth_lord_house)
        if p["name"] in MALEFIC_PLANETS and p["name"] != fourth_lord
    ]

    # 2. Inimical or Debilitation
    # simplified check using inSign
    bad_sign = any(s in fourth_lord_planet["inSign"] for s in ["Debilitated", "Enemy"])

    # 3. Evil Shashtiamsa (Skipped precise deity check, assuming covered if above not met but rare)
    # Ideally checking D60 chart positions if we knew which were evil.

    if malefics_with_l4 or bad_sign:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L4 associated with Malefics OR in Enemy/Debilitated sign."
    else:
        result["details"] = "L4 strong and free from malefic association."

    return result


@register_yoga("Matrudeerghayur")
def matrudeerghayur(yoga: Yoga) -> YogaType:
    """
    A benefic occupies the fourth, the fourth Lord is exalted, and the Moon is strong.
    or
    The Lord of the navamsa occupied by the fourth Lord is strong and occupy a kendra from Lagna as well as Chandra Lagna.
    """
    result: YogaType = {
        "id": "",
        "name": "Matrudeerghayur",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    fourth_lord = yoga.get_lord_of_house(4)

    # Cond 1
    condition_one = False
    planets_in_4 = yoga.planets_in_relative_house("Lagna", 4)
    benefic_in_4 = any(p["name"] in BENEFIC_PLANETS for p in planets_in_4)

    fourth_lord_planet = yoga.get_planet_by_name(fourth_lord)

    if fourth_lord_planet["name"] == "Lagna":
        raise ValueError("Planet of Lord of house 4 not found")

    fourth_lord_exalted = "Exalted" in fourth_lord_planet["inSign"]

    moon_planet = yoga.get_planet_by_name("Moon")

    if moon_planet["name"] == "Lagna":
        raise ValueError("Moon not found")
    moon_strong, _ = yoga.is_planet_powerful(moon_planet)

    if benefic_in_4 and fourth_lord_exalted and moon_strong:
        condition_one = True

    # Cond 2
    condition_two = False
    fourth_lord_navamsa_sign = get_navamsa_sign(yoga, fourth_lord)
    target_lord = None
    if fourth_lord_navamsa_sign:
        target_lord = RASHI_LORD_MAP.get(fourth_lord_navamsa_sign)

    if target_lord:
        target_lord_planet = yoga.get_planet_by_name(target_lord)
        if target_lord_planet["name"] == "Lagna":
            raise ValueError("Planet of Lord of house 4 not found")
        target_lord_strong, _ = yoga.is_planet_powerful(target_lord_planet)

        in_kendra_lagna = yoga.planet_in_kendra_from(1, target_lord)

        # Kendra from chandra Lagna
        moon_house = yoga.get_house_of_planet("Moon")
        in_kendra_moon = False
        target_lord_house = yoga.get_house_of_planet(target_lord)
        if moon_house and target_lord_house:
            relative_position = (target_lord_house - moon_house) % 12 + 1
            if relative_position in [1, 4, 7, 10]:
                in_kendra_moon = True

        if target_lord_strong and in_kendra_lagna and in_kendra_moon:
            condition_two = True

    if condition_one or condition_two:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "Benefic in 4, L4 Exalted, Moon Strong OR L4's D9 Lord strong in Kendras."
        )
    else:
        result["details"] = "Conditions for Matrudeerghayur not met."

    return result


@register_yoga("Matrunasa")
def matrunasa(yoga: Yoga) -> YogaType:
    """
    The Moon is hemmed in between, associated with or aspected by evil planets.
    or
    The planet owning the navamsa, in which the Lord of the navamsa occupied by the fourth Lord is situated is disposed in the sixth, eighth or twelfth house.
    """
    result: YogaType = {
        "id": "",
        "name": "Matrunasa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    # Cond 1: Moon afflicted
    condition_one = False
    moon_house = yoga.get_house_of_planet("Moon")
    if moon_house:
        # Associated
        assoc_malefics = [
            p["name"]
            for p in yoga.planets_in_relative_house("Lagna", moon_house)
            if p["name"] in MALEFIC_PLANETS
        ]
        # Aspected
        aspected_malefic = False
        for malefic_planet in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
            if aspects:
                for aspect in aspects[0]["aspect_houses"]:
                    if moon_house in aspect:
                        aspected_malefic = True
        # Hemmed (Papakartari) - check 2nd and 12th from Moon
        hemmed = False
        previous_house = (moon_house - 2) % 12 + 1
        next_house = (moon_house) % 12 + 1
        # Simple check: Malefics in prev and next
        mal_prev = any(
            p["name"] in MALEFIC_PLANETS
            for p in yoga.planets_in_relative_house("Lagna", previous_house)
        )
        mal_next = any(
            p["name"] in MALEFIC_PLANETS
            for p in yoga.planets_in_relative_house("Lagna", next_house)
        )
        if mal_prev and mal_next:
            hemmed = True

        if assoc_malefics or aspected_malefic or hemmed:
            condition_one = True

    # Cond 2: Deep Navamsa Lord Check
    # "The planet owning the navamsa (P2), in which the Lord of the navamsa occupied by the fourth Lord (P1) is situated is disposed in the 6, 8, or 12 house."
    # L4 -> D9_Sign1 -> Lord(D9_Sign1) = P1
    # P1 -> D9_Sign2 -> Lord(D9_Sign2) = P2
    # P2 in 6, 8, 12 (D1)

    condition_two = False
    fourth_lord = yoga.get_lord_of_house(4)
    if fourth_lord:
        first_navamsa_sign = get_navamsa_sign(yoga, fourth_lord)
        if first_navamsa_sign:
            first_dispositor = RASHI_LORD_MAP.get(first_navamsa_sign)
            if first_dispositor:
                second_navamsa_sign = get_navamsa_sign(yoga, first_dispositor)
                if second_navamsa_sign:
                    second_dispositor = RASHI_LORD_MAP.get(second_navamsa_sign)
                    if second_dispositor:
                        second_dispositor_house = yoga.get_house_of_planet(second_dispositor)
                        if second_dispositor_house in [6, 8, 12]:
                            condition_two = True

    if condition_one or condition_two:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = (
            "Moon afflicted OR L4's 'Grand-Dispositor' (Navamsa) in 6/8/12."
        )
    else:
        result["details"] = "Moon not afflicted; Dispositor chain safe."

    return result


@register_yoga("Matrugami")
def matrugami(yoga: Yoga) -> YogaType:
    """
    The Moon or Venus joins a kendra in conjunction with or aspected by a malefic, and an evil planet occupies the fourth house.
    """
    result: YogaType = {
        "id": "",
        "name": "Matrugami",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    # "Evil planet occupies 4th"
    if not any(
        p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", 4)
    ):
        result["details"] = "No malefic in 4th house."
        return result

    candidates: list[PLANETS] = []
    if yoga.planet_in_kendra_from(1, "Moon"):
        candidates.append("Moon")
    if yoga.planet_in_kendra_from(1, "Venus"):
        candidates.append("Venus")

    match_found = False
    for planet in candidates:
        planet_house = yoga.get_house_of_planet(planet)
        # Check malefic association/aspect
        assoc = any(
            p["name"] in MALEFIC_PLANETS and p["name"] != planet
            for p in yoga.planets_in_relative_house("Lagna", planet_house)
        )
        if assoc:
            match_found = True
            break
        # Aspect
        for malefic_planet in MALEFIC_PLANETS:
            if malefic_planet == planet:
                continue
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
            if aspects:
                for aspect in aspects[0]["aspect_houses"]:
                    if planet_house in aspect:
                        match_found = True
                        break
        if match_found:
            break

    if match_found:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Malefic in 4th; Moon/Venus in Kendra is afflicted."
    else:
        result["details"] = "No afflicted Moon/Venus in Kendra with Malefic in 4th."

    return result


@register_yoga("Sahodareesangama")
def sahodareesangama(yoga: Yoga) -> YogaType:
    """
    The Lord of the seventh house and Venus are in conjunction in the fourth house and are aspected by or associated with malefics or are in cruel shashtiamsas.
    """
    result: YogaType = {
        "id": "",
        "name": "Sahodareesangama",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    seventh_lord = yoga.get_lord_of_house(7)

    seventh_lord_house = yoga.get_house_of_planet(seventh_lord)
    venus_house = yoga.get_house_of_planet("Venus")

    if seventh_lord_house != 4 or venus_house != 4:
        result["details"] = "L7 and Venus not in 4th."
        return result

    # Check affiliation
    afflicted = any(
        p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", 4)
    )

    if not afflicted:
        # Aspected
        for malefic_planet in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
            if aspects:
                for aspect in aspects[0]["aspect_houses"]:
                    if 4 in aspect:
                        afflicted = True
                        break

    if afflicted:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L7 and Venus in 4th afflicted by Malefics."
    else:
        result["details"] = "L7 and Venus in 4th but not afflicted."

    return result


@register_yoga("Kapata")
def kapata(yoga: Yoga) -> YogaType:
    """
    The fourth house is joined by a malefic and the fourth Lord is associated with or aspected by malefics or is hemmed in between malefic.
    or
    The fourth house is occupied by Saturn, Rahu and the malefic tenth Lord, who in turn is aspected by malefics.
    or
    The fourth Lord joins Saturn and Rahu and is aspected by malefics.
    """
    result: YogaType = {
        "id": "",
        "name": "Kapata",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Neutral",
    }

    fourth_lord = yoga.get_lord_of_house(4)
    fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

    # Cond 1
    condition_one = False
    condition_one_details = ""
    malefics_in_fourth = [
        p["name"]
        for p in yoga.planets_in_relative_house("Lagna", 4)
        if p["name"] in MALEFIC_PLANETS
    ]
    if malefics_in_fourth:
        # Check L4 affliction
        fourth_lord_afflicted = False
        affliction_type = ""
        # Assoc
        assoc_malefics = [
            p["name"]
            for p in yoga.planets_in_relative_house("Lagna", fourth_lord_house)
            if p["name"] in MALEFIC_PLANETS and p["name"] != fourth_lord
        ]
        if assoc_malefics:
            fourth_lord_afflicted = True
            affliction_type = f"associated with malefics ({', '.join(assoc_malefics)})"

        # Aspected
        if not fourth_lord_afflicted:
            for malefic_planet in MALEFIC_PLANETS:
                if malefic_planet == fourth_lord:
                    continue
                aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
                if aspects:
                    for aspect in aspects[0]["aspect_houses"]:
                        if fourth_lord_house in aspect:
                            fourth_lord_afflicted = True
                            affliction_type = f"aspected by {malefic_planet}"
                            break
        # Hemmed
        if not fourth_lord_afflicted:
            previous_house = (fourth_lord_house - 2) % 12 + 1
            next_house = fourth_lord_house % 12 + 1
            m_prev = [
                p["name"]
                for p in yoga.planets_in_relative_house("Lagna", previous_house)
                if p["name"] in MALEFIC_PLANETS
            ]
            m_next = [
                p["name"]
                for p in yoga.planets_in_relative_house("Lagna", next_house)
                if p["name"] in MALEFIC_PLANETS
            ]
            if m_prev and m_next:
                fourth_lord_afflicted = True
                affliction_type = f"hemmed between malefics ({', '.join(m_prev)} and {', '.join(m_next)})"

        if fourth_lord_afflicted:
            condition_one = True
            condition_one_details = f"4th House contains malefics ({', '.join(malefics_in_fourth)}) AND 4th Lord is {affliction_type}."

    # Cond 2
    condition_two = False
    condition_two_details = ""
    planets_4 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 4)]
    tenth_lord = yoga.get_lord_of_house(10)
    if "Saturn" in planets_4 and "Rahu" in planets_4 and tenth_lord in planets_4:
        if tenth_lord in MALEFIC_PLANETS:
            # Check if L10 aspected by malefics
            tenth_lord_house = 4
            l10_aspected = False
            aspector = ""
            for malefic_planet in MALEFIC_PLANETS:
                if malefic_planet == tenth_lord or malefic_planet in planets_4:
                    continue
                aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
                if aspects:
                    for aspect in aspects[0]["aspect_houses"]:
                        if tenth_lord_house in aspect:
                            l10_aspected = True
                            aspector = malefic_planet
                            break
            if l10_aspected:
                condition_two = True
                condition_two_details = f"4th House has Saturn, Rahu, and Malefic 10th Lord ({tenth_lord}) who is aspected by {aspector}."

    # Cond 3
    condition_three = False
    condition_three_details = ""
    fourth_lord_neighbor_planets = [p["name"]
                                    for p in yoga.planets_in_relative_house("Lagna", fourth_lord_house)]
    if "Saturn" in fourth_lord_neighbor_planets and "Rahu" in fourth_lord_neighbor_planets and fourth_lord in fourth_lord_neighbor_planets:
        # Check aspect
        aspected = False
        aspector = ""
        for malefic_planet in MALEFIC_PLANETS:
            # Need to be careful not to count Saturn/Rahu if they are the ones joining, but assuming outside aspect
            if malefic_planet in fourth_lord_neighbor_planets:
                continue
            actions = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
            if actions:
                for aspect in actions[0]["aspect_houses"]:
                    if fourth_lord_house in aspect:
                        aspected = True
                        aspector = malefic_planet
                        break
        if aspected:
            condition_three = True
            condition_three_details = (
                f"4th Lord joins Saturn and Rahu, and is aspected by {aspector}."
            )

    if condition_one or condition_two or condition_three:
        result["present"] = True
        result["strength"] = 1.0
        details_list: list[str] = []
        if condition_one:
            details_list.append(condition_one_details)
        if condition_two:
            details_list.append(condition_two_details)
        if condition_three:
            details_list.append(condition_three_details)
        result["details"] = " OR ".join(details_list)
    else:
        result["details"] = (
            "Kapata: 4th House/Lord not sufficiently afflicted by Saturn/Rahu/Malefics."
        )

    return result


@register_yoga("Nishkapata")
def nishkapata(yoga: Yoga) -> YogaType:
    """
    The fourth house is occupied by a benefic, or a planet in exaltation, friendly or own house, or the fourth house is a benefic sign.
    or
    Lord of Lagna joins the fourth house in conjunction with or aspected by a benefic or occupy Parvata or Uttamamsa.
    """
    result: YogaType = {
        "id": "",
        "name": "Nishkapata",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    # Cond 1
    condition_one = False
    condition_one_details = ""
    # 4th house occupied by benefic
    fourth_house_planets = yoga.planets_in_relative_house("Lagna", 4)
    benefics_in_4 = [p["name"]
                     for p in fourth_house_planets if p["name"] in BENEFIC_PLANETS]

    if benefics_in_4:
        condition_one = True
        condition_one_details = f"4th House occupied by benefics ({', '.join(benefics_in_4)})."
    else:
        # occupied by planet in exalt/friend/own
        strong_planets: list[str] = []
        for p in fourth_house_planets:
            statuses = [s for s in ["Exalted",
                                    "Friend", "Own"] if s in p["inSign"]]
            if statuses:
                strong_planets.append(f"{p['name']} ({statuses[0]})")

        if strong_planets:
            condition_one = True
            condition_one_details = (
                f"4th House occupied by strong planets: {', '.join(strong_planets)}."
            )

    if not condition_one:
        # 4th house is benefic sign
        fourth_house_sign = yoga.get_rashi_of_house(4)
        if fourth_house_sign in BENEFIC_SIGNS:
            condition_one = True
            condition_one_details = f"4th House ({fourth_house_sign}) is a Benefic Sign."

    # Cond 2
    condition_two = False
    condition_two_details = ""
    lagna_lord = yoga.get_lord_of_house(1)
    if lagna_lord and yoga.get_house_of_planet(lagna_lord) == 4:
        # Conj aspected by benefic
        has_benefic_assoc = False
        assoc_type = ""

        # Conj
        if benefics_in_4:
            has_benefic_assoc = True
            assoc_type = f"conjoined with benefics ({', '.join(benefics_in_4)})"

        # Aspect
        if not has_benefic_assoc and yoga.is_house_benefic_aspected(4):
            has_benefic_assoc = True
            assoc_type = "aspected by a benefic"

        if has_benefic_assoc:
            condition_two = True
            condition_two_details = f"L1 is in 4th House {assoc_type}."

    if condition_one or condition_two:
        result["present"] = True
        result["strength"] = 1.0
        details_list: list[str] = []
        if condition_one:
            details_list.append(condition_one_details)
        if condition_two:
            details_list.append(condition_two_details)
        result["details"] = " OR ".join(details_list)
    else:
        result["details"] = (
            "Nishkapata: 4th House not benefic/strong, and L1 not in 4th with benefic influence."
        )

    return result


@register_yoga("Matru Satrutwa")
def matru_satrutwa(yoga: Yoga) -> YogaType:
    """
    Mercury, being the Lord of Lagna and the fourth house, must join with or be aspected by a malefic.
    """
    result: YogaType = {
        "id": "",
        "name": "Matru Satrutwa",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Negative",
    }

    lagna_lord = yoga.get_lord_of_house(1)
    fourth_lord = yoga.get_lord_of_house(4)

    if lagna_lord == "Mercury" and fourth_lord == "Mercury":
        afflicted = False
        mercury_house = yoga.get_house_of_planet("Mercury")
        # Joined Malefic
        if any(
            p["name"] in MALEFIC_PLANETS
            for p in yoga.planets_in_relative_house("Lagna", mercury_house)
        ):
            afflicted = True
        # Aspected Malefic
        if not afflicted:
            for malefic_planet in MALEFIC_PLANETS:
                aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic_planet)
                if aspects:
                    for aspect in aspects[0]["aspect_houses"]:
                        if mercury_house in aspect:
                            afflicted = True
                            break
        if afflicted:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = "Mercury as L1/L4 is afflicted by Malefic."
        else:
            result["details"] = "Mercury is L1/L4 but not afflicted."
    else:
        result["details"] = "Mercury is not Lord of both 1st and 4th."

    return result


@register_yoga("Matru Sneha")
def matru_sneha(yoga: Yoga) -> YogaType:
    """
    The first and fourth house have a common Lord, or the Lords of the first and fourth house must be temporal or natural friends or aspected by benefics.
    """
    result: YogaType = {
        "id": "",
        "name": "Matru Sneha",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    lagna_lord = yoga.get_lord_of_house(1)
    fourth_lord = yoga.get_lord_of_house(4)

    if not lagna_lord or not fourth_lord:
        return result

    condition_met = False
    if lagna_lord == fourth_lord:
        condition_met = True
    else:
        # Check aspected by benefics
        lagna_lord_house = yoga.get_house_of_planet(lagna_lord)
        fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

        lagna_lord_benefic_aspected = False
        fourth_lord_benefic_aspected = False

        # Check aspect
        if yoga.is_house_benefic_aspected(lagna_lord_house):
            lagna_lord_benefic_aspected = True
        if yoga.is_house_benefic_aspected(fourth_lord_house):
            fourth_lord_benefic_aspected = True

        if lagna_lord_benefic_aspected and fourth_lord_benefic_aspected:
            condition_met = True

    if condition_met:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L1/L4 same or both aspected by benefics."
    else:
        result["details"] = (
            "L1/L4 different and not both benefic aspected (Friendship check omitted)."
        )

    return result


@register_yoga("Vahana")
def vahana(yoga: Yoga) -> YogaType:
    """
    The Lord of Lagna joins the fourth, eleventh or the ninth house.
    or
    The fourth Lord is exalted and the Lord of the exaltation sign occupies a kendra or trikona.
    """
    result: YogaType = {
        "id": "",
        "name": "Vahana",
        "present": False,
        "strength": 0.0,
        "details": "",
        "type": "Positive",
    }

    lagna_lord = yoga.get_lord_of_house(1)
    if lagna_lord:
        lagna_lord_house = yoga.get_house_of_planet(lagna_lord)
        if lagna_lord_house in [4, 9, 11]:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L1 in {lagna_lord_house}."
            return result

    fourth_lord = yoga.get_lord_of_house(4)

    fourth_lord_planet = yoga.get_planet_by_name(fourth_lord)

    if fourth_lord_planet["name"] == "Lagna":
        raise ValueError("Planet of Fourth Lord not found")
    if "Exalted" in fourth_lord_planet["inSign"]:
        # Lord of Exaltation Sign
        fourth_lord_house = yoga.get_house_of_planet(fourth_lord)

        exalt_sign = yoga.get_rashi_of_house(fourth_lord_house)
        dispositor = RASHI_LORD_MAP.get(exalt_sign)
        if dispositor:
            if yoga.planet_in_kendra_from(1, dispositor) or yoga.planet_in_trikona_from(
                1, dispositor
            ):
                result["present"] = True
                result["strength"] = 1.0
                result["details"] = "L4 Exalted and Dispositor in Kendra/Trikona."
                return result

    result["details"] = "Vahana yoga conditions not met."
    return result
