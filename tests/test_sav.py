from ascendant import Ascendant
from ascendant.horoscope import HoroscopeData
from ascendant.sav import Ashtakavarga
from ascendant.sav.constants import ASHTAKAVARGA_PLANET_ORDER, RASHIS_ORDER
from tests.horoscope import my_horoscope


def test_ashtakavarga_checksums_and_entity_scope() -> None:
    result = Ashtakavarga(my_horoscope).calculate()

    assert result["totals"] == {
        "Sun": 48,
        "Moon": 49,
        "Mars": 39,
        "Mercury": 54,
        "Jupiter": 56,
        "Venus": 52,
        "Saturn": 39,
        "Lagna": 49,
        "sarva": 337,
    }
    assert set(result["bhinna"]) == {*ASHTAKAVARGA_PLANET_ORDER, "Lagna"}
    assert set(result["sarva"]) == set(RASHIS_ORDER)
    assert sum(result["sarva"].values()) == 337


def test_ashtakavarga_returns_stable_fixture_values() -> None:
    result = Ashtakavarga(my_horoscope).calculate()

    assert [result["sarva"][sign] for sign in RASHIS_ORDER] == [
        29, 30, 30, 24, 27, 30, 31, 29, 32, 25, 21, 29
    ]
    for planet in ASHTAKAVARGA_PLANET_ORDER:
        assert set(result["reduced"][planet]) == set(RASHIS_ORDER)
        pinda = result["shodhya_pinda"][planet]
        assert pinda["shodhya_pinda"] == (
            pinda["rashi_pinda"] + pinda["graha_pinda"]
        )


def test_ashtakavarga_counts_first_and_twelfth_sign_boundaries() -> None:
    calculator = Ashtakavarga(my_horoscope)
    calculator._positions = {entity: 0 for entity in calculator._positions}

    sun_scores = calculator._calculate_bhinna()["Sun"]

    assert sun_scores["Aries"] == 3
    assert sun_scores["Pisces"] == 3


def test_ascendant_exposes_same_ashtakavarga_result() -> None:
    astro = Ascendant(
        1990, 1, 1, 12, 0, 0, 28.6139, 77.2090, "+5:30"
    )

    assert astro.get_sav() == astro.ashtakavarga_module.calculate()


def test_ashtakavarga_supports_ayanamsa_and_negative_utc() -> None:
    horoscope = HoroscopeData(
        year=1990,
        month=1,
        day=31,
        hour=23,
        minute=30,
        second=0,
        utc="-4:00",
        latitude=40.7128,
        longitude=-74.0060,
        ayanamsa="Raman",
        house_system="Whole Sign",
    )

    result = Ashtakavarga(horoscope).calculate()

    assert result["totals"]["sarva"] == 337
