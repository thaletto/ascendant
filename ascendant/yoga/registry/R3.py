from typing import Dict, List, Optional
from ascendant.const import (
    BENEFIC_PLANETS,
    MALEFIC_PLANETS,
    RASHI_LORD_MAP,
    CLASSICAL_PLANETS,
    MOVABLE_SIGNS,
    FIXED_SIGNS,
    BENEFIC_SIGNS,
)
from ascendant.types import YogaType, PLANETS
from ascendant.yoga.base import Yoga, register_yoga, register_yogas
from ascendant.utils import isSignOdd, getSignName

# Helper constants (Removed local definitions)


def get_navamsa_lord(yoga: Yoga, planet_name: PLANETS) -> Optional[str]:
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

def get_navamsa_sign(yoga: Yoga, planet_name: PLANETS) -> Optional[str]:
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
def Bhratruvriddhi(yoga: Yoga) -> YogaType:
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

    l3 = yoga.get_lord_of_house(3)
    l3_cond = False
    
    if l3:
        p_l3 = yoga.get_planet_by_name(l3)
        if p_l3:
            is_strong, _ = yoga.isPlanetPowerful(p_l3)
            house_l3 = yoga.get_house_of_planet(l3)
            joined_benefics = [
                p["name"] for p in yoga.planets_in_relative_house("Lagna", house_l3) 
                if p["name"] in BENEFIC_PLANETS and p["name"] != l3
            ]
            benefic_aspect = yoga.is_house_benefic_aspected(house_l3)

            if is_strong or joined_benefics or benefic_aspect:
                l3_cond = True

    mars_cond = False
    p_mars = yoga.get_planet_by_name("Mars")
    if p_mars:
         is_strong, _ = yoga.isPlanetPowerful(p_mars)
         house_mars = yoga.get_house_of_planet("Mars")
         joined_benefics = [
                p["name"] for p in yoga.planets_in_relative_house("Lagna", house_mars) 
                if p["name"] in BENEFIC_PLANETS and p["name"] != "Mars"
         ]
         benefic_aspect = yoga.is_house_benefic_aspected(house_mars)
         
         if is_strong or joined_benefics or benefic_aspect:
             mars_cond = True

    h3_cond = False
    planets_in_3 = yoga.planets_in_relative_house("Lagna", 3)
    benefics_in_3 = [p["name"] for p in planets_in_3 if p["name"] in BENEFIC_PLANETS]
    h3_aspected = yoga.is_house_benefic_aspected(3)
    
    if benefics_in_3 or h3_aspected:
        h3_cond = True
        
    if l3_cond or mars_cond or h3_cond:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "3rd Lord/Mars/3rd House is strong or associated with benefics."
    else:
        result["details"] = "3rd Lord, Mars, and 3rd House lack strength or benefic association."

    return result


@register_yoga("Sodaranasa")
def Sodaranasa(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3:
        result["details"] = "Lord of 3rd not found."
        return result
        
    h_l3 = yoga.get_house_of_planet(l3)
    h_mars = yoga.get_house_of_planet("Mars")
    
    target_houses = [3, 5, 7, 8]
    
    if h_l3 not in target_houses or h_mars not in target_houses:
        result["details"] = f"Mars ({h_mars}) or 3rd Lord ({h_l3}) not in 3, 5, 7, 8."
        return result
        
    def is_aspected_by_malefic(planet_name, house):
        for malefic in MALEFIC_PLANETS:
             aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic)
             if aspects:
                 for asp in aspects:
                     for h_dict in asp["aspect_houses"]:
                         if house in h_dict:
                             return True
        return False
    
    mars_aspected = is_aspected_by_malefic("Mars", h_mars)
    l3_aspected = is_aspected_by_malefic(l3, h_l3)
    
    if mars_aspected and l3_aspected:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Mars and 3rd Lord in 3/5/7/8 aspected by malefics."
    else:
        result["details"] = "Mars or L3 lack malefic aspect required."
        
    return result


@register_yoga("Ekabhagini")
def Ekabhagini(yoga: Yoga) -> YogaType:
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
    
    h_mercury = yoga.get_house_of_planet("Mercury")
    if h_mercury != 3:
        result["details"] = "Mercury not in 3rd house."
        return result
        
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    h_l3 = yoga.get_house_of_planet(l3)
    h_moon = yoga.get_house_of_planet("Moon")
    if h_l3 != h_moon:
        result["details"] = f"3rd Lord ({l3}) not with Moon."
        return result
        
    h_mars = yoga.get_house_of_planet("Mars")
    h_saturn = yoga.get_house_of_planet("Saturn")
    if h_mars != h_saturn:
        result["details"] = "Mars not with Saturn."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "Mercury in 3rd, L3 with Moon, Mars with Saturn."
    return result


@register_yoga("Dwadasa Sahodara")
def Dwadasa_Sahodara(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    h_l3 = yoga.get_house_of_planet(l3)
    
    if not yoga.planet_in_kendra_from(1, l3):
        result["details"] = "3rd Lord not in Kendra."
        return result
        
    p_mars = yoga.get_planet_by_name("Mars")
    if "Exalted" not in p_mars["inSign"]:
        result["details"] = "Mars not exalted."
        return result
        
    h_mars = yoga.get_house_of_planet("Mars")
    h_ju = yoga.get_house_of_planet("Jupiter")
    if h_mars != h_ju:
        result["details"] = "Mars not with Jupiter."
        return result
        
    trikona_houses = [(h_l3 - 1 + i - 1) % 12 + 1 for i in [1, 5, 9]]
    if h_mars not in trikona_houses:
        result["details"] = "Mars/Jupiter not in Trikona from 3rd Lord."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in Kendra; Exalted Mars with Jupiter in Trikona from L3."
    return result


@register_yoga("Sapthasankhya Sahodara")
def Sapthasankhya_Sahodara(yoga: Yoga) -> YogaType:
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
    
    l12 = yoga.get_lord_of_house(12)
    if not l12: return result
    h_l12 = yoga.get_house_of_planet(l12)
    h_mars = yoga.get_house_of_planet("Mars")
    
    if h_l12 != h_mars:
        result["details"] = "12th Lord not with Mars."
        return result
        
    h_moon = yoga.get_house_of_planet("Moon")
    h_ju = yoga.get_house_of_planet("Jupiter")
    
    if h_moon != 3 or h_ju != 3:
         result["details"] = "Moon or Jupiter not in 3rd house."
         return result
         
    h_venus = yoga.get_house_of_planet("Venus")
    if h_venus == 3:
        result["details"] = "Venus conjoined with Moon/Jupiter."
        return result
        
    venus_aspects = yoga.__chart__.graha_drishti(n=1, planet="Venus")
    if venus_aspects:
        for asp in venus_aspects[0]["aspect_houses"]:
            if 3 in asp:
                result["details"] = "Venus aspects 3rd house."
                return result

    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L12 with Mars; Moon/Jup in 3rd without Venus influence."
    return result


@register_yoga("Parakrama")
def Parakrama(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    
    nl3_sign = get_navamsa_sign(yoga, l3)
    if not nl3_sign or nl3_sign not in BENEFIC_SIGNS:
        result["details"] = "3rd Lord Navamsa is not benefic."
        return result
        
    h_l3 = yoga.get_house_of_planet(l3)
    joined_benefics = [
        p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l3) 
        if p["name"] in BENEFIC_PLANETS and p["name"] != l3
    ]
    aspected_by_benefic = False
    for ben in BENEFIC_PLANETS:
        if ben == l3: continue
        aspects = yoga.__chart__.graha_drishti(n=1, planet=ben)
        if aspects:
            for asp in aspects[0]["aspect_houses"]:
                if h_l3 in asp:
                    aspected_by_benefic = True
                    break
    
    if not (joined_benefics or aspected_by_benefic):
        result["details"] = "3rd Lord not aspected/conjoined by benefics."
        return result
        
    mars_sign = yoga.get_rashi_of_house(yoga.get_house_of_planet("Mars"))
    if mars_sign not in BENEFIC_SIGNS:
        result["details"] = "Mars not in benefic sign."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in benefic D9/aspected by benefics; Mars in benefic sign."
    return result


@register_yoga("Yuddha Praveena")
def Yuddha_Praveena(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    
    n_l3 = get_navamsa_sign(yoga, l3)
    if not n_l3: 
        result["details"] = "Could not find Navamsa of L3."
        return result
        
    p1 = RASHI_LORD_MAP.get(n_l3)
    if not p1: return result
    
    n_p1 = get_navamsa_sign(yoga, p1)
    if not n_p1:
        result["details"] = f"Could not find Navamsa of {p1}."
        return result
        
    p2 = RASHI_LORD_MAP.get(n_p1)
    if not p2: return result
    
    p2_rasi_sign = yoga.get_rashi_of_house(yoga.get_house_of_planet(p2))
    p2_navamsa_sign = get_navamsa_sign(yoga, p2)
    
    own_rasi = RASHI_LORD_MAP.get(p2_rasi_sign) == p2
    own_navamsa = RASHI_LORD_MAP.get(p2_navamsa_sign) == p2
    
    if own_rasi or own_navamsa:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = f"Target Planet {p2} is in own Rasi or Navamsa."
    else:
        result["details"] = f"Target Planet {p2} not in own vargas."
        
    return result


@register_yoga("Yuddhatpoorvadridhachitta")
def Yuddhatpoorvadridhachitta(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    
    p_l3 = yoga.get_planet_by_name(l3)
    if not p_l3: return result
    
    if "Exalted" not in p_l3["inSign"]:
         result["details"] = "L3 not exalted."
         return result
         
    h_l3 = yoga.get_house_of_planet(l3)
    malefics_with_l3 = [
        p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l3)
        if p["name"] in MALEFIC_PLANETS and p["name"] != l3
    ]
    if not malefics_with_l3:
        result["details"] = "L3 not with Malefics."
        return result
        
    rasi_sign = yoga.get_rashi_of_house(h_l3)
    navamsa_sign = get_navamsa_sign(yoga, l3)
    
    if rasi_sign in MOVABLE_SIGNS or navamsa_sign in MOVABLE_SIGNS:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Exalted L3 joins malefics in Movable Rasi/Navamsa."
    else:
        result["details"] = "L3 not in Movable Rasi/Navamsa."
        
    return result


@register_yoga("Yuddhatpaschaddrudha")
def Yuddhatpaschaddrudha(yoga: Yoga) -> YogaType:
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
    
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    
    h_l3 = yoga.get_house_of_planet(l3)
    rasi_sign = yoga.get_rashi_of_house(h_l3)
    if rasi_sign not in FIXED_SIGNS:
        result["details"] = "L3 not in Fixed Rasi."
        return result
        
    navamsa_sign = get_navamsa_sign(yoga, l3)
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
            if planet["name"] == l3:
                l3_found_in_d60 = True
                break
        if l3_found_in_d60: break
    
    if not l3_found_in_d60:
        result["details"] = f"L3 ({l3}) not found in D60 chart."
        return result

    lord_of_occupied_rasi = RASHI_LORD_MAP.get(rasi_sign)
    if not lord_of_occupied_rasi: return result
    
    p_lord = yoga.get_planet_by_name(lord_of_occupied_rasi)
    if not p_lord or "Debilitated" not in p_lord["inSign"]:
         result["details"] = f"Dispositor ({lord_of_occupied_rasi}) is not debilitated."
         return result
         
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L3 in Fixed signs/D60; Dispositor debilitated."
    return result


@register_yoga("Satkathadisravana")
def Satkathadisravana(yoga: Yoga) -> YogaType:
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
    
    h3_sign = yoga.get_rashi_of_house(3)
    if h3_sign not in BENEFIC_SIGNS:
        result["details"] = "3rd House not a benefic sign."
        return result
        
    if not yoga.is_house_benefic_aspected(3):
        result["details"] = "3rd House not aspected by benefics."
        return result
        
    l3 = yoga.get_lord_of_house(3)
    if not l3: return result
    
    n_l3 = get_navamsa_sign(yoga, l3)
    if n_l3 not in BENEFIC_SIGNS:
        result["details"] = "3rd Lord not in Benefic Amsa."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "3rd House benefic/aspected; L3 in benefic Navamsa."
    return result


@register_yoga("Uttama Griha")
def Uttama_Griha(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    h_l4 = yoga.get_house_of_planet(l4)
    
    target_houses = [1, 4, 5, 7, 9, 10]
    if h_l4 not in target_houses:
        result["details"] = "L4 not in Kendra/Thrikona."
        return result
        
    joined_benefics = [
        p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l4)
        if p["name"] in BENEFIC_PLANETS and p["name"] != l4
    ]
    if not joined_benefics:
        result["details"] = "L4 not joined by benefics."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "4th Lord joins benefics in Kendra or Trikona."
    return result


@register_yoga("Vichitra Saudha Prakara")
def Vichitra_Saudha_Prakara(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    l10 = yoga.get_lord_of_house(10)
    if not l4 or not l10: return result
    
    h_l4 = yoga.get_house_of_planet(l4)
    h_l10 = yoga.get_house_of_planet(l10)
    h_sat = yoga.get_house_of_planet("Saturn")
    h_mar = yoga.get_house_of_planet("Mars")
    
    if not (h_l4 == h_l10 == h_sat == h_mar):
        result["details"] = "L4, L10, Saturn, and Mars are not conjoined."
        return result
        
    result["present"] = True
    result["strength"] = 1.0
    result["details"] = "L4, L10, Saturn, and Mars are conjoined."
    return result


@register_yoga("Ayatna Griha Prapta Yoga")
def Ayatna_Griha_Prapta_Yoga(yoga: Yoga) -> YogaType:
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
    
    l1 = yoga.get_lord_of_house(1)
    l7 = yoga.get_lord_of_house(7)
    cond1_met = False
    
    if l1 and l7:
        h_l1 = yoga.get_house_of_planet(l1)
        h_l7 = yoga.get_house_of_planet(l7)
        allowed = [1, 4]
        
        if h_l1 not in allowed or h_l7 not in allowed:
            c1_fail = "L1/L7 not in 1/4"
        elif not (yoga.is_house_benefic_aspected(h_l1) and yoga.is_house_benefic_aspected(h_l7)):
            c1_fail = "L1/L7 houses not aspected by benefics"
        else:
            cond1_met = True

    if cond1_met:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L1/L7 in 1/4 aspected by benefics."
        return result
        
    # Condition 2 Failure Reason
    c2_fail = "L9 or L4 missing"
    
    l9 = yoga.get_lord_of_house(9)
    l4 = yoga.get_lord_of_house(4)
    cond2_met = False
    
    if l9 and l4:
        if not yoga.planet_in_kendra_from(1, l9):
             c2_fail = "L9 not in Kendra"
        else:
             p_l4 = yoga.get_planet_by_name(l4)
             valid_status = ["Exalted", "Moola Trikona", "Own"]
             if any(s in p_l4["inSign"] for s in valid_status):
                 cond2_met = True
             else:
                 c2_fail = "L4 not Exalted/MT/Own"
                 
    if cond2_met:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L9 in Kendra and L4 Strong."
        return result
    
    result["details"] = f"{c1_fail}; {c2_fail}."
    return result
