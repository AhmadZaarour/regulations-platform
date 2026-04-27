from __future__ import annotations

from app.logic.types import ClassificationResult, ProjectInput

DEFAULT_OCCUPANTS_PER_UNIT = 3


def classify_project(data: ProjectInput) -> ClassificationResult:
    building_use = data.get("building_use", "").lower()
    floors = data.get("floors_above_grade", 0)
    total_units = data.get("total_units", 0)

    return {
        "building_use": building_use,
        "is_residential": building_use == "residential",
        "is_multistory": floors > 1,
        "floors_above_grade": floors,
        "total_units": total_units,
        "sprinklered": bool(data.get("sprinklered", False)),
        "stair_count_proposed": data.get("stair_count_proposed", 0),
        "occupant_load_estimate": total_units * DEFAULT_OCCUPANTS_PER_UNIT,
    }
