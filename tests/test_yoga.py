"""Behavior tests for public yoga evaluation."""

from __future__ import annotations

from ascendant import Ascendant


def test_yoga_results_have_a_consistent_public_contract(
    astrology: Ascendant,
) -> None:
    yogas = astrology.get_yogas()

    assert yogas
    assert len({yoga["id"] for yoga in yogas}) == len(yogas)
    for yoga in yogas:
        assert set(yoga) == {
            "id", "name", "present", "strength", "details", "type"
        }
        assert isinstance(yoga["present"], bool)
        assert yoga["strength"] >= 0
        assert yoga["type"] in {"Positive", "Neutral", "Negative"}
