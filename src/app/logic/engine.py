from __future__ import annotations

from app.logic.classifiers import classify_project
from app.logic.rules import (
    evaluate_min_exit_stairs,
    evaluate_proposed_stair_count,
)
from app.logic.types import ProjectInput, RuleEvaluation


def run_egress_stair_engine(data: ProjectInput) -> dict[str, list[RuleEvaluation]]:
    classification = classify_project(data)

    evaluations = [
        evaluate_min_exit_stairs(classification),
        evaluate_proposed_stair_count(classification),
    ]

    return {
        "applies": [r for r in evaluations if r["status"] == "applies"],
        "maybe": [r for r in evaluations if r["status"] == "maybe"],
        "not_applicable": [r for r in evaluations if r["status"] == "not_applicable"],
    }
