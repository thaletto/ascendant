from typing import List, Tuple
from ascendant.const import FIXED, MOVABLE
from ascendant.utils import isSignOdd
from ascendant.types import ALLOWED_DIVISIONS, HOUSES, PLANETS


def aspect_offsets_for_planet(planet_name: PLANETS) -> List[int]:
    """Returns the house offsets for a planet's aspects (e.g., 7th house aspect is an offset of 6)."""
    # All planets aspect the 7th house from their position.
    offsets: List[int] = [6]
    if planet_name == "Mars":
        # Mars also aspects the 4th and 8th houses.
        offsets += [3, 7]
    elif planet_name == "Jupiter" or planet_name == "Rahu":
        # Jupiter and Rahu also aspect the 5th and 9th houses.
        offsets += [4, 8]
    elif planet_name == "Saturn":
        # Saturn also aspects the 3rd and 10th houses.
        offsets += [2, 9]
    return offsets


def get_divisional_target(
    longitude: float, division: ALLOWED_DIVISIONS
) -> Tuple[HOUSES, float]:
    """Map an absolute longitude into a target sign/degree for a varga"""

    # Fast path for D1
    if division == 1:
        sign_index = int(longitude // 30)  # [0, 11]
        degree_in_target = longitude % 30  # [0, 30]
        return sign_index, degree_in_target

    sign_index = int(longitude // 30)  # [0, 11]
    pos_in_sign = longitude % 30  # [0, 30]
    part_size = 30.0 / division  # size of each part
    part_index = int(pos_in_sign // part_size)
    offset_in_part = pos_in_sign - (part_index * part_size)
    degree_in_target = (offset_in_part / part_size) * 30.0

    # Default target sign, same as D1
    target_sign = sign_index

    # =====D2=====
    if division == 2:
        target_sign = (
            (sign_index * 2 + part_index)
            if sign_index <= 5
            else ((sign_index - 6) * 2 + part_index)
        )

    # =====D3=====
    elif division == 3:
        target_sign = (sign_index + [0, 4, 8][part_index]) % 12

    # =====D4=====
    elif division == 4:
        target_sign = (sign_index + [0, 3, 6, 9][part_index]) % 12

    # =====D7=====
    elif division == 7:
        target_sign = (
            (sign_index + part_index) % 12
            if isSignOdd(sign_index)
            else (sign_index + 6 + part_index) % 12
        )

    # =====D9=====
    elif division == 9:
        if sign_index in MOVABLE:
            start = sign_index
        elif sign_index in FIXED:
            start = (sign_index + 8) % 12
        else:
            start = (sign_index + 4) % 12
        target_sign = (start + part_index) % 12

    # =====D10=====
    elif division == 10:
        start = sign_index if isSignOdd(sign_index) else (sign_index + 8) % 12
        target_sign = (start + part_index) % 12

    # =====D12=====
    elif division == 12:
        target_sign = (sign_index + part_index) % 12

    # =====D16=====
    elif division == 16:
        start = 0 if sign_index in MOVABLE else 4 if sign_index in FIXED else 8
        target_sign = (start + part_index) % 12

    # =====D20=====
    elif division == 20:
        start = 0 if sign_index in MOVABLE else 8 if sign_index in FIXED else 4
        target_sign = (start + part_index) % 12

    # =====D24=====
    elif division == 24:
        start = 4 if isSignOdd(sign_index) else 3
        target_sign = (start + part_index) % 12

    # =====D27=====
    elif division == 27:
        start = (
            0
            if sign_index in [0, 4, 8]
            else 3
            if sign_index in [1, 5, 9]
            else 6
            if sign_index in [2, 6, 10]
            else 9
        )
        target_sign = (start + part_index) % 12

    # =====D30=====
    elif division == 30:
        if isSignOdd(sign_index):
            targets, edges = [0, 10, 8, 2, 6], [5, 10, 18, 25]
        else:
            targets, edges = [1, 5, 11, 9, 7], [5, 12, 20, 25]
        for i, edge in enumerate(edges):
            if pos_in_sign < edge:
                target_sign = targets[i]
                break
        else:
            target_sign = targets[-1]

    # =====D40=====
    elif division == 40:
        target_sign = ((0 if isSignOdd(sign_index) else 6) + part_index) % 12

    # =====D45=====
    elif division == 45:
        start = 0 if sign_index in MOVABLE else 4 if sign_index in FIXED else 8
        target_sign = (start + part_index) % 12

    # =====D60=====
    elif division == 60:
        target_sign = (sign_index + part_index) % 12

    return target_sign, degree_in_target
