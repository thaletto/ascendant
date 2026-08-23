"""Declarative rule data and the evaluator shared by yoga registries."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from ascendant.types import HOUSES, PLANETS, PLANETS_LAGNA, RASHIS, YogaType
from ascendant.yoga.base import Yoga, register_yoga

YogaClassification = Literal["Positive", "Neutral", "Negative"]


@dataclass(frozen=True, slots=True)
class PlanetInKendraFrom:
    """Require ``planet`` in houses 1, 4, 7, or 10 from ``reference``."""

    planet: PLANETS
    reference: PLANETS_LAGNA


@dataclass(frozen=True, slots=True)
class PlanetInSigns:
    """Require ``planet`` to occupy one of ``signs``."""

    planet: PLANETS
    signs: frozenset[RASHIS]


Condition = PlanetInKendraFrom | PlanetInSigns


@dataclass(frozen=True, slots=True)
class KendraStrength:
    """Score a planet by its relative Kendra from a reference placement."""

    planet: PLANETS
    reference: PLANETS_LAGNA
    scores: tuple[tuple[int, float], ...]
    exalted_sign: RASHIS | None = None
    exaltation_multiplier: float = 1.0
    only_when_present: bool = True
    default_score: float = 0.0


@dataclass(frozen=True, slots=True)
class YogaRule:
    """Data required to evaluate one named Yoga."""

    name: str
    classification: YogaClassification
    conditions: tuple[Condition, ...]
    detail_template: str
    strength: KendraStrength


_YOGA_RULES: dict[str, YogaRule] = {}
YOGA_RULES = MappingProxyType(_YOGA_RULES)


def register_rule(rule: YogaRule) -> None:
    """Register rule data through the existing yoga extension seam."""
    if rule.name in _YOGA_RULES:
        raise ValueError(f'Yoga rule "{rule.name}" is already registered')
    _YOGA_RULES[rule.name] = rule

    def evaluate(yoga: Yoga) -> YogaType:
        return evaluate_rule(yoga, rule)

    _ = register_yoga(rule.name)(evaluate)


def evaluate_rule(yoga: Yoga, rule: YogaRule) -> YogaType:
    """Evaluate one declarative rule against a calculated natal chart."""
    placements: dict[PLANETS_LAGNA, tuple[HOUSES, RASHIS]] = {}

    def placement(body: PLANETS_LAGNA) -> tuple[HOUSES, RASHIS]:
        if body not in placements:
            house = yoga.get_house_of_planet(body)
            placements[body] = (house, yoga.get_rashi_of_house(house))
        return placements[body]

    present = all(
        _condition_matches(condition, yoga, placement) for condition in rule.conditions
    )
    strength_rule = rule.strength
    planet_house, planet_sign = placement(strength_rule.planet)
    reference_house, _ = placement(strength_rule.reference)
    relative_house = (planet_house - reference_house + 12) % 12 + 1
    score = dict(strength_rule.scores).get(
        relative_house,
        strength_rule.default_score,
    )
    if strength_rule.only_when_present and not present:
        score = 0.0
    if present and planet_sign == strength_rule.exalted_sign:
        score *= strength_rule.exaltation_multiplier

    details = rule.detail_template.format(
        planet=strength_rule.planet,
        planet_house=planet_house,
        planet_sign=planet_sign,
        reference=strength_rule.reference,
        reference_house=reference_house,
    )
    return {
        "id": "",
        "name": rule.name,
        "present": present,
        "strength": min(1.0, score),
        "details": details,
        "type": rule.classification,
    }


def _condition_matches(
    condition: Condition,
    yoga: Yoga,
    placement: Callable[[PLANETS_LAGNA], tuple[HOUSES, RASHIS]],
) -> bool:
    if isinstance(condition, PlanetInKendraFrom):
        reference_house, _ = placement(condition.reference)
        return yoga.planet_in_kendra_from(reference_house, condition.planet)
    _, sign = placement(condition.planet)
    return sign in condition.signs
