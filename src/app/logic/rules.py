from __future__ import annotations

from app.logic.requirement_cards import REQUIREMENT_CARDS
from app.logic.types import ClassificationResult, RuleEvaluation


def evaluate_min_exit_stairs(classification: ClassificationResult) -> RuleEvaluation:
    why: list[str] = []
    missing_inputs: list[str] = []

    if "floors_above_grade" not in classification:
        missing_inputs.append("floors_above_grade")

    if not classification.get("is_residential", False):
        return {
            "code": "EGRESS-STAIR-001",
            "title": REQUIREMENT_CARDS["EGRESS-STAIR-001"]["title"],
            "status": "not_applicable",
            "why": ["Current MVP slice only evaluates residential buildings"],
            "missing_inputs": missing_inputs,
            "checklist": [],
        }

    floors = classification.get("floors_above_grade", 0)

    if floors >= 4:
        why.extend(
            [
                "Building use is residential",
                "Building has 4 or more floors above grade",
            ]
        )
        return {
            "code": "EGRESS-STAIR-001",
            "title": REQUIREMENT_CARDS["EGRESS-STAIR-001"]["title"],
            "status": "applies",
            "why": why,
            "missing_inputs": missing_inputs,
            "checklist": REQUIREMENT_CARDS["EGRESS-STAIR-001"]["checklist"],
        }

    why.append("Building has fewer than 4 floors above grade")
    return {
        "code": "EGRESS-STAIR-001",
        "title": REQUIREMENT_CARDS["EGRESS-STAIR-001"]["title"],
        "status": "maybe",
        "why": why,
        "missing_inputs": missing_inputs,
        "checklist": REQUIREMENT_CARDS["EGRESS-STAIR-001"]["checklist"],
    }


def evaluate_proposed_stair_count(classification: ClassificationResult) -> RuleEvaluation:
    why: list[str] = []
    missing_inputs: list[str] = []

    floors = classification.get("floors_above_grade")
    stair_count = classification.get("stair_count_proposed")

    if floors is None:
        missing_inputs.append("floors_above_grade")
    if stair_count is None:
        missing_inputs.append("stair_count_proposed")

    if floors is None or stair_count is None:
        return {
            "code": "EGRESS-STAIR-002",
            "title": REQUIREMENT_CARDS["EGRESS-STAIR-002"]["title"],
            "status": "maybe",
            "why": ["More project inputs are needed to evaluate proposed stair count"],
            "missing_inputs": missing_inputs,
            "checklist": REQUIREMENT_CARDS["EGRESS-STAIR-002"]["checklist"],
        }

    if floors >= 4 and stair_count < 2:
        why.extend(
            [
                "Building has 4 or more floors above grade",
                "Only one stair is currently proposed",
            ]
        )
        return {
            "code": "EGRESS-STAIR-002",
            "title": REQUIREMENT_CARDS["EGRESS-STAIR-002"]["title"],
            "status": "applies",
            "why": why,
            "missing_inputs": [],
            "checklist": REQUIREMENT_CARDS["EGRESS-STAIR-002"]["checklist"],
        }

    return {
        "code": "EGRESS-STAIR-002",
        "title": REQUIREMENT_CARDS["EGRESS-STAIR-002"]["title"],
        "status": "not_applicable",
        "why": ["No obvious stair count issue detected from current inputs"],
        "missing_inputs": [],
        "checklist": [],
    }
