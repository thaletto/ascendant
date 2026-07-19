from ascendant import Ascendant


def test_ashtakavarga_has_classical_checksums(astrology: Ascendant) -> None:
    result = astrology.get_sav()

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
    assert set(result["bhinna"]) == {
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
        "Lagna",
    }
    assert len(result["sarva"]) == 12
    assert sum(result["sarva"].values()) == 337


def test_ashtakavarga_exposes_reduced_scores_and_pindas(
    astrology: Ascendant,
) -> None:
    result = astrology.get_sav()

    for planet in result["reduced"]:
        assert len(result["reduced"][planet]) == 12
        assert all(score >= 0 for score in result["reduced"][planet].values())
        pinda = result["shodhya_pinda"][planet]
        assert pinda["shodhya_pinda"] == (
            pinda["rashi_pinda"] + pinda["graha_pinda"]
        )


def test_ashtakavarga_supports_alternate_birth_settings() -> None:
    astrology = Ascendant(
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

    result = astrology.get_sav()

    assert result["totals"]["sarva"] == 337
