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


@register_yoga("Grihanasa")
def Grihanasa(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    h_l4 = yoga.get_house_of_planet(l4)
    
    # Condition 1
    cond1 = False
    if h_l4 == 12:
        aspected = False
        for malefic in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=malefic)
            if aspects:
                for asp in aspects[0]["aspect_houses"]:
                    if h_l4 in asp:
                        aspected = True
                        break
        if aspected:
            cond1 = True

    # Condition 2
    cond2 = False
    n_l4 = get_navamsa_sign(yoga, l4)
    if n_l4:
        lord_n_l4 = RASHI_LORD_MAP.get(n_l4)
        if lord_n_l4:
             if yoga.get_house_of_planet(lord_n_l4) == 11:
                 cond2 = True
                 
    if cond1 or cond2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L4 in 12th aspected by malefic OR Dispositor of L4's Navamsa in 11th."
    else:
        result["details"] = "L4 not in 12th malefic-aspected; D9 Dispositor not in 11th."
        
    return result


@register_yoga("Bandhu Pujya")
def Bandhu_Pujya(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    
    # Condition 1
    cond1 = False
    if l4 in BENEFIC_PLANETS:
        h_mercury = yoga.get_house_of_planet("Mercury")
        if h_mercury == 1:
             # Check aspect by another benefic on L4
             h_l4 = yoga.get_house_of_planet(l4)
             aspected = False
             for ben in BENEFIC_PLANETS:
                 if ben == l4: continue
                 aspects = yoga.__chart__.graha_drishti(n=1, planet=ben)
                 for asp in aspects:
                     if any(h == h_l4 for group in asp["aspect_houses"] for h in group):
                         aspected = True
             if aspected:
                 cond1 = True
                 
    # Condition 2: Jupiter Assoc/Aspect 4th House or 4th Lord
    cond2 = False
    h_ju = yoga.get_house_of_planet("Jupiter")
    h_l4 = yoga.get_house_of_planet(l4)
    
    # Assoc
    if h_ju == 4 or h_ju == h_l4:
        cond2 = True
    else:
        # Aspect
        aspects = yoga.__chart__.graha_drishti(n=1, planet="Jupiter")
        if aspects:
            for asp in aspects[0]["aspect_houses"]:
                if 4 in asp or h_l4 in asp:
                    cond2 = True
                    break
                    
    if cond1 or cond2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Benefic L4 aspected by benefic with Merc in 1 OR Jup assoc with 4H/L4."
    else:
        result["details"] = "No specific benefic association with 4H/L4."
        
    return result


@register_yoga("Bandhubhisthyaktha")
def Bandhubhisthyaktha(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    
    p_l4 = yoga.get_planet_by_name(l4)
    h_l4 = yoga.get_house_of_planet(l4)
    
    # 1. Associated with malefics
    malefics_with_l4 = [
        p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l4)
        if p["name"] in MALEFIC_PLANETS and p["name"] != l4
    ]
    
    # 2. Inimical or Debilitation
    # simplified check using inSign
    bad_sign = any(s in p_l4["inSign"] for s in ["Debilitated", "Enemy"])
    
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
def Matrudeerghayur(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    
    # Cond 1
    cond1 = False
    planets_in_4 = yoga.planets_in_relative_house("Lagna", 4)
    benefic_in_4 = any(p["name"] in BENEFIC_PLANETS for p in planets_in_4)
    
    p_l4 = yoga.get_planet_by_name(l4)
    l4_exalted = "Exalted" in p_l4["inSign"]
    
    p_moon = yoga.get_planet_by_name("Moon")
    moon_strong, _ = yoga.isPlanetPowerful(p_moon)
    
    if benefic_in_4 and l4_exalted and moon_strong:
        cond1 = True
        
    # Cond 2
    cond2 = False
    n_l4 = get_navamsa_sign(yoga, l4)
    target_lord = None
    if n_l4:
        target_lord = RASHI_LORD_MAP.get(n_l4)
        
    if target_lord:
        p_target = yoga.get_planet_by_name(target_lord)
        t_strong, _ = yoga.isPlanetPowerful(p_target)
        
        in_kendra_lagna = yoga.planet_in_kendra_from(1, target_lord)
        
        # Kendra from Chandra Lagna
        h_moon = yoga.get_house_of_planet("Moon")
        in_kendra_moon = False
        t_house = yoga.get_house_of_planet(target_lord)
        if h_moon and t_house:
             rel = (t_house - h_moon) % 12 + 1
             if rel in [1, 4, 7, 10]:
                 in_kendra_moon = True
                 
        if t_strong and in_kendra_lagna and in_kendra_moon:
            cond2 = True
            
    if cond1 or cond2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Benefic in 4, L4 Exalted, Moon Strong OR L4's D9 Lord strong in Kendras."
    else:
        result["details"] = "Conditions for Matrudeerghayur not met."
        
    return result


@register_yoga("Matrunasa")
def Matrunasa(yoga: Yoga) -> YogaType:
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
    cond1 = False
    h_moon = yoga.get_house_of_planet("Moon")
    if h_moon:
        # Associated
        assoc_malefics = [p["name"] for p in yoga.planets_in_relative_house("Lagna", h_moon) if p["name"] in MALEFIC_PLANETS]
        # Aspected
        aspected_malefic = False
        for mal in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
            if aspects:
                for asp in aspects[0]["aspect_houses"]:
                    if h_moon in asp:
                        aspected_malefic = True
        # Hemmed (Papakartari) - check 2nd and 12th from Moon
        hemmed = False
        prev_h = (h_moon - 2) % 12 + 1
        next_h = (h_moon) % 12 + 1
        # Simple check: Malefics in prev and next
        mal_prev = any(p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", prev_h))
        mal_next = any(p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", next_h))
        if mal_prev and mal_next:
            hemmed = True
            
        if assoc_malefics or aspected_malefic or hemmed:
            cond1 = True
        
    # Cond 2: Deep Navamsa Lord Check
    # "The planet owning the navamsa (P2), in which the Lord of the navamsa occupied by the fourth Lord (P1) is situated is disposed in the 6, 8, or 12 house."
    # L4 -> D9_Sign1 -> Lord(D9_Sign1) = P1
    # P1 -> D9_Sign2 -> Lord(D9_Sign2) = P2
    # P2 in 6, 8, 12 (D1)
    
    cond2 = False
    l4 = yoga.get_lord_of_house(4)
    if l4:
        n1 = get_navamsa_sign(yoga, l4)
        if n1:
            p1 = RASHI_LORD_MAP.get(n1)
            if p1:
                n2 = get_navamsa_sign(yoga, p1)
                if n2:
                    p2 = RASHI_LORD_MAP.get(n2)
                    if p2:
                        h_p2 = yoga.get_house_of_planet(p2)
                        if h_p2 in [6, 8, 12]:
                            cond2 = True
                            
    if cond1 or cond2:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Moon afflicted OR L4's 'Grand-Dispositor' (Navamsa) in 6/8/12."
    else:
         result["details"] = "Moon not afflicted; Dispositor chain safe."
         
    return result


@register_yoga("Matrugami")
def Matrugami(yoga: Yoga) -> YogaType:
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
    if not any(p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", 4)):
        result["details"] = "No malefic in 4th house."
        return result
        
    candidates = []
    if yoga.planet_in_kendra_from(1, "Moon"): candidates.append("Moon")
    if yoga.planet_in_kendra_from(1, "Venus"): candidates.append("Venus")
    
    match_found = False
    for planet in candidates:
        h_p = yoga.get_house_of_planet(planet)
        # Check malefic association/aspect
        assoc = any(p["name"] in MALEFIC_PLANETS and p["name"] != planet for p in yoga.planets_in_relative_house("Lagna", h_p))
        if assoc:
            match_found = True
            break
        # Aspect
        for mal in MALEFIC_PLANETS:
            if mal == planet: continue
            aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
            if aspects:
                for asp in aspects[0]["aspect_houses"]:
                     if h_p in asp:
                         match_found = True
                         break
        if match_found: break
        
    if match_found:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "Malefic in 4th; Moon/Venus in Kendra is afflicted."
    else:
        result["details"] = "No afflicted Moon/Venus in Kendra with Malefic in 4th."
        
    return result


@register_yoga("Sahodareesangama")
def Sahodareesangama(yoga: Yoga) -> YogaType:
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
    
    l7 = yoga.get_lord_of_house(7)
    if not l7: return result
    
    h_l7 = yoga.get_house_of_planet(l7)
    h_ven = yoga.get_house_of_planet("Venus")
    
    if h_l7 != 4 or h_ven != 4:
        result["details"] = "L7 and Venus not in 4th."
        return result
        
    # Check affiliation
    afflicted = False
    # Associated
    assoc = any(p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", 4))
    if assoc: afflicted = True
    
    if not afflicted:
        # Aspected
        for mal in MALEFIC_PLANETS:
            aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
            if aspects:
                for asp in aspects[0]["aspect_houses"]:
                    if 4 in asp:
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
def Kapata(yoga: Yoga) -> YogaType:
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
    
    l4 = yoga.get_lord_of_house(4)
    if not l4: return result
    h_l4 = yoga.get_house_of_planet(l4)
    
    # Cond 1
    c1 = False
    c1_details = ""
    mal_in_4 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 4) if p["name"] in MALEFIC_PLANETS]
    if mal_in_4:
        # Check L4 affliction
        l4_afflicted = False
        affliction_type = ""
        # Assoc
        assoc_malefics = [p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l4) if p["name"] in MALEFIC_PLANETS and p["name"] != l4]
        if assoc_malefics:
            l4_afflicted = True
            affliction_type = f"associated with malefics ({', '.join(assoc_malefics)})"
        
        # Aspected
        if not l4_afflicted:
            for mal in MALEFIC_PLANETS:
                if mal == l4: continue
                aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
                if aspects:
                     for asp in aspects[0]["aspect_houses"]:
                         if h_l4 in asp:
                             l4_afflicted = True
                             affliction_type = f"aspected by {mal}"
                             break
        # Hemmed
        if not l4_afflicted:
            prev_h = (h_l4 - 2) % 12 + 1
            next_h = h_l4 % 12 + 1
            m_prev = [p["name"] for p in yoga.planets_in_relative_house("Lagna", prev_h) if p["name"] in MALEFIC_PLANETS]
            m_next = [p["name"] for p in yoga.planets_in_relative_house("Lagna", next_h) if p["name"] in MALEFIC_PLANETS]
            if m_prev and m_next:
                 l4_afflicted = True
                 affliction_type = f"hemmed between malefics ({', '.join(m_prev)} and {', '.join(m_next)})"
                 
        if l4_afflicted:
            c1 = True
            c1_details = f"4th House contains malefics ({', '.join(mal_in_4)}) AND 4th Lord is {affliction_type}."
            
    # Cond 2
    c2 = False
    c2_details = ""
    planets_4 = [p["name"] for p in yoga.planets_in_relative_house("Lagna", 4)]
    l10 = yoga.get_lord_of_house(10)
    if "Saturn" in planets_4 and "Rahu" in planets_4 and l10 in planets_4:
        if l10 in MALEFIC_PLANETS:
             # Check if L10 aspected by malefics
             h_l10 = 4 
             l10_aspected = False
             aspector = ""
             for mal in MALEFIC_PLANETS:
                 if mal == l10 or mal in planets_4: continue
                 aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
                 if aspects:
                     for asp in aspects[0]["aspect_houses"]:
                         if h_l10 in asp:
                             l10_aspected = True
                             aspector = mal
                             break
             if l10_aspected:
                 c2 = True
                 c2_details = f"4th House has Saturn, Rahu, and Malefic 10th Lord ({l10}) who is aspected by {aspector}."
                 
    # Cond 3
    c3 = False
    c3_details = ""
    p_l4_neighbors = [p["name"] for p in yoga.planets_in_relative_house("Lagna", h_l4)]
    if "Saturn" in p_l4_neighbors and "Rahu" in p_l4_neighbors and l4 in p_l4_neighbors:
        # Check aspect
        aspected = False
        aspector = ""
        for mal in MALEFIC_PLANETS:
            # Need to be careful not to count Saturn/Rahu if they are the ones joining, but assuming outside aspect
            if mal in p_l4_neighbors: continue 
            actions = yoga.__chart__.graha_drishti(n=1, planet=mal)
            if actions:
                for asp in actions[0]["aspect_houses"]:
                    if h_l4 in asp:
                        aspected = True
                        aspector = mal
                        break
        if aspected:
            c3 = True
            c3_details = f"4th Lord joins Saturn and Rahu, and is aspected by {aspector}."
            
    if c1 or c2 or c3:
        result["present"] = True
        result["strength"] = 1.0
        details_list = []
        if c1: details_list.append(c1_details)
        if c2: details_list.append(c2_details)
        if c3: details_list.append(c3_details)
        result["details"] = " OR ".join(details_list)
    else:
        result["details"] = "Kapata: 4th House/Lord not sufficiently afflicted by Saturn/Rahu/Malefics."
        
    return result


@register_yoga("Nishkapata")
def Nishkapata(yoga: Yoga) -> YogaType:
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
    c1 = False
    c1_details = ""
    # 4th house occupied by benefic
    planets_4_objs = yoga.planets_in_relative_house("Lagna", 4)
    benefics_in_4 = [p["name"] for p in planets_4_objs if p["name"] in BENEFIC_PLANETS]
    
    if benefics_in_4:
        c1 = True
        c1_details = f"4th House occupied by benefics ({', '.join(benefics_in_4)})."
    else:
        # occupied by planet in exalt/friend/own
        strong_planets = []
        for p in planets_4_objs:
            statuses = [s for s in ["Exalted", "Friend", "Own"] if s in p["inSign"]]
            if statuses:
                strong_planets.append(f"{p['name']} ({statuses[0]})")
        
        if strong_planets:
            c1 = True
            c1_details = f"4th House occupied by strong planets: {', '.join(strong_planets)}."
            
    if not c1:
        # 4th house is benefic sign
        s4 = yoga.get_rashi_of_house(4)
        if s4 in BENEFIC_SIGNS:
            c1 = True
            c1_details = f"4th House ({s4}) is a Benefic Sign."
            
    # Cond 2
    c2 = False
    c2_details = ""
    l1 = yoga.get_lord_of_house(1)
    if l1 and yoga.get_house_of_planet(l1) == 4:
         # Conj aspected by benefic
         has_benefic_assoc = False
         assoc_type = ""
         
         # Conj
         if benefics_in_4:
             has_benefic_assoc = True
             assoc_type = f"conjoined with benefics ({', '.join(benefics_in_4)})"
             
         # Aspect
         if not has_benefic_assoc:
             if yoga.is_house_benefic_aspected(4):
                 has_benefic_assoc = True
                 assoc_type = "aspected by a benefic"
                 
         if has_benefic_assoc:
             c2 = True
             c2_details = f"L1 is in 4th House {assoc_type}."
             
    if c1 or c2:
        result["present"] = True
        result["strength"] = 1.0
        details_list = []
        if c1: details_list.append(c1_details)
        if c2: details_list.append(c2_details)
        result["details"] = " OR ".join(details_list)
    else:
        result["details"] = "Nishkapata: 4th House not benefic/strong, and L1 not in 4th with benefic influence."
        
    return result


@register_yoga("Matru Satrutwa")
def Matru_Satrutwa(yoga: Yoga) -> YogaType:
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
    
    l1 = yoga.get_lord_of_house(1)
    l4 = yoga.get_lord_of_house(4)
    
    if l1 == "Mercury" and l4 == "Mercury":
        afflicted = False
        h_mer = yoga.get_house_of_planet("Mercury")
        # Joined Malefic
        if any(p["name"] in MALEFIC_PLANETS for p in yoga.planets_in_relative_house("Lagna", h_mer)):
            afflicted = True
        # Aspected Malefic
        if not afflicted:
            for mal in MALEFIC_PLANETS:
                aspects = yoga.__chart__.graha_drishti(n=1, planet=mal)
                if aspects:
                    for asp in aspects[0]["aspect_houses"]:
                        if h_mer in asp:
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
def Matru_Sneha(yoga: Yoga) -> YogaType:
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
    
    l1 = yoga.get_lord_of_house(1)
    l4 = yoga.get_lord_of_house(4)
    
    if not l1 or not l4: return result
    
    cond = False
    if l1 == l4:
        cond = True
    else:
        # Check aspected by benefics
        h_l1 = yoga.get_house_of_planet(l1)
        h_l4 = yoga.get_house_of_planet(l4)
        
        l1_ben = False
        l4_ben = False
        
        # Check aspect
        if yoga.is_house_benefic_aspected(h_l1): l1_ben = True
        if yoga.is_house_benefic_aspected(h_l4): l4_ben = True
        
        if l1_ben and l4_ben:
             cond = True
             
    if cond:
        result["present"] = True
        result["strength"] = 1.0
        result["details"] = "L1/L4 same or both aspected by benefics."
    else:
        result["details"] = "L1/L4 different and not both benefic aspected (Friendship check omitted)."
        
    return result


@register_yoga("Vahana")
def Vahana(yoga: Yoga) -> YogaType:
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
    
    l1 = yoga.get_lord_of_house(1)
    if l1:
        h_l1 = yoga.get_house_of_planet(l1)
        if h_l1 in [4, 9, 11]:
            result["present"] = True
            result["strength"] = 1.0
            result["details"] = f"L1 in {h_l1}."
            return result
            
    l4 = yoga.get_lord_of_house(4)
    if l4:
        p_l4 = yoga.get_planet_by_name(l4)
        if "Exalted" in p_l4["inSign"]:
             # Lord of Exaltation Sign
             exalt_sign = yoga.get_rashi_of_house(yoga.get_house_of_planet(l4))
             disp = RASHI_LORD_MAP.get(exalt_sign)
             if disp:
                 if yoga.planet_in_kendra_from(1, disp) or yoga.planet_in_trikona_from(1, disp):
                     result["present"] = True
                     result["strength"] = 1.0
                     result["details"] = "L4 Exalted and Dispositor in Kendra/Trikona."
                     return result
                     
    result["details"] = "Vahana yoga conditions not met."
    return result
