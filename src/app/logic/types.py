from __future__ import annotations

from typing import Literal, TypedDict

RuleStatus = Literal["applies", "maybe", "not_applicable"]


class ProjectInput(TypedDict, total=False):
    building_use: str
    floors_above_grade: int
    total_units: int
    sprinklered: bool
    stair_count_proposed: int


class ClassificationResult(TypedDict, total=False):
    building_use: str
    is_residential: bool
    is_multistory: bool
    floors_above_grade: int
    total_units: int
    sprinklered: bool
    stair_count_proposed: int
    occupant_load_estimate: int


class RuleEvaluation(TypedDict):
    code: str
    title: str
    status: RuleStatus
    why: list[str]
    missing_inputs: list[str]
    checklist: list[str]
