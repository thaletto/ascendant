import hashlib
import json

import pytest

from ascendant import Ascendant, HoroscopeData
from ascendant.dasha import Dasha
from ascendant.horoscope import HOUSE_SYSTEM_MAPPING
from ascendant.utils import getHouseSystem


def _digest(value) -> str:
    normalized = json.loads(json.dumps(value, ensure_ascii=False))
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


@pytest.fixture
def astro() -> Ascendant:
    return Ascendant(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        second=0,
        latitude=28.6139,
        longitude=77.2090,
        utc="+5:30",
    )


@pytest.mark.parametrize(
    ("division", "expected"),
    [
        (1, "f68616930868a0f9c39cecd42d350b6e6eac53aa69dafa25dca6334b6a929469"),
        (9, "16767891e99cbfa46e2907fa9d563cf0d1093de8c2f3c5f60ff9c1c349aed261"),
        (10, "1b042d376e212a323cd2bf134569544ca3d71fcd331586b7530fa9d0c90810e7"),
    ],
)
def test_charts_match_vedicastro_021(astro: Ascendant, division: int, expected: str):
    assert _digest(astro.get_chart(division)) == expected


def test_dasha_matches_vedicastro_021(astro: Ascendant):
    assert _digest(astro.get_dasha_timeline()) == (
        "62100a7d9ce5bd175d0f244be2056d3a60f668bf4dba992b9bf63bbbd14906db"
    )


def test_house_system_normalization_is_preserved():
    assert getHouseSystem("whole_sign") == HOUSE_SYSTEM_MAPPING["Whole Sign"]
    assert HoroscopeData(
        1990, 1, 1, 12, 0, 0, "+5:30", 28.6139, 77.2090, house_system="whole_sign"
    ).get_house_system() == HOUSE_SYSTEM_MAPPING["Whole Sign"]


def test_horoscope_data_is_public_advanced_api():
    horoscope = HoroscopeData(
        1990, 1, 1, 12, 0, 0, "+5:30", 28.6139, 77.2090, house_system="Whole Sign"
    )
    assert horoscope.generate_chart().getAngle("Asc").lon == pytest.approx(343.9226400242266)


@pytest.mark.parametrize(
    ("ayanamsa", "ascendant_longitude", "moon_longitude"),
    [
        ("Lahiri", 343.9226400242266, 306.46525775974686),
        ("Lahiri_1940", 343.937409129953, 306.48002686547323),
        ("Lahiri_VP285", 343.916250517218, 306.4588682527382),
        ("Lahiri_ICRC", 343.9229433616497, 306.46556109716994),
        ("Raman", 345.368941349953, 307.91155908547324),
        ("Krishnamurti", 344.019492349953, 306.56211008547325),
        ("Krishnamurti_Senthilathiban", 343.99936676898847, 306.5419845045087),
    ],
)
def test_supported_ayanamsas_match_vedicastro_baseline(
    ayanamsa: str, ascendant_longitude: float, moon_longitude: float
):
    chart = HoroscopeData(
        1990, 1, 1, 12, 0, 0, "+5:30", 28.6139, 77.2090, ayanamsa=ayanamsa
    ).generate_chart()
    assert chart.getAngle("Asc").lon == pytest.approx(ascendant_longitude)
    assert chart.get("Moon").lon == pytest.approx(moon_longitude)


@pytest.mark.parametrize(
    ("house_system", "first_house_longitude"),
    [
        ("Whole Sign", 330.0),
        ("Placidus", 343.9226400242266),
        ("Equal", 343.9226400242266),
        ("Equal 2", 343.9226400242266),
    ],
)
def test_supported_house_systems_match_vedicastro_baseline(
    house_system: str, first_house_longitude: float
):
    chart = HoroscopeData(
        1990, 1, 1, 12, 0, 0, "+5:30", 28.6139, 77.2090, house_system=house_system
    ).generate_chart()
    assert list(chart.houses)[0].lon == pytest.approx(first_house_longitude)


def test_negative_utc_and_lunar_nodes_match_vedicastro_baseline():
    chart = HoroscopeData(
        1990, 1, 1, 12, 0, 0, "-5:00", 40.7128, -74.006, house_system="Whole Sign"
    ).generate_chart()
    assert chart.getAngle("Asc").lon == pytest.approx(356.9442034611048)
    assert chart.get("North Node").isRetrograde() is True
    assert chart.get("South Node").isRetrograde() is True


@pytest.mark.parametrize(
    ("longitude", "expected"),
    [
        (0, {"Nakshatra": "Ashwini", "Pada": 1, "SubLord": "Ketu"}),
        (3.325, {"Nakshatra": "Ashwini", "Pada": 2, "SubLord": "Sun"}),
        (13.332, {"Nakshatra": "Bharani", "Pada": 1, "SubLord": "Mercury"}),
        (359.999, {"Nakshatra": "Ashwini", "Pada": 1, "SubLord": "Saturn"}),
    ],
)
def test_nakshatra_boundaries_match_vedicastro_baseline(longitude, expected):
    horoscope = HoroscopeData(1990, 1, 1, 12, 0, 0, "+5:30", 28.6139, 77.2090)
    data = horoscope.get_rl_nl_sl_data(longitude)
    assert data is not None
    assert {key: data[key] for key in expected} == expected


@pytest.mark.parametrize(
    ("start_date", "direction"),
    [((2000, 1, 31, 0, 0), "forward"), ((2000, 3, 31, 0, 0), "backward")],
)
def test_month_end_dasha_arithmetic_matches_vedicastro_baseline(start_date, direction):
    result = Dasha._compute_new_date(start_date, 1 / 12, direction)
    assert result.isoformat() == "2000-02-29T00:00:00"
