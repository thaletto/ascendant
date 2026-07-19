from typing import Final

GREG_CAL: Final[int]
SUN: Final[int]
MOON: Final[int]
MARS: Final[int]
MERCURY: Final[int]
JUPITER: Final[int]
VENUS: Final[int]
SATURN: Final[int]
MEAN_NODE: Final[int]
SIDM_LAHIRI: Final[int]
SIDM_LAHIRI_1940: Final[int]
SIDM_LAHIRI_VP285: Final[int]
SIDM_LAHIRI_ICRC: Final[int]
SIDM_RAMAN: Final[int]
SIDM_KRISHNAMURTI: Final[int]
SIDM_KRISHNAMURTI_VP291: Final[int]
FLG_SWIEPH: Final[int]
FLG_SPEED: Final[int]
FLG_SIDEREAL: Final[int]

def julday(year: int, month: int, day: int, hour: float, cal: int = ...) -> float: ...
def set_sid_mode(sid_mode: int, t0: float = ..., ayan_t0: float = ...) -> None: ...
def calc_ut(
    tjdut: float, planet: int, flags: int = ...
) -> tuple[tuple[float, float, float, float, float, float], int]: ...
def houses_ex(
    tjdut: float, lat: float, lon: float, hsys: bytes = ..., flags: int = ...
) -> tuple[tuple[float, ...], tuple[float, ...]]: ...
