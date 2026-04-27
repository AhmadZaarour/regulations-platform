from __future__ import annotations

from typing import TypedDict


class RequirementCard(TypedDict):
    title: str
    checklist: list[str]


REQUIREMENT_CARDS: dict[str, RequirementCard] = {
    "EGRESS-STAIR-001": {
        "title": "Minimum number of exit stairs",
        "checklist": [
            "Confirm the minimum number of exit stairs required for the building is provided",
            "Check whether stair separation requirements apply",
            "Verify stairs serve all required floors continuously",
        ],
    },
    "EGRESS-STAIR-002": {
        "title": "Proposed stair count appears insufficient",
        "checklist": [
            "Review the number of stairs shown in plans",
            "Confirm whether a second exit stair is required",
            "Flag this issue for design review before submission",
        ],
    },
}
