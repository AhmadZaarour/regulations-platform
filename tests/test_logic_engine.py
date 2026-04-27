from app.logic.engine import run_egress_stair_engine


def test_engine_flags_two_stairs_issue() -> None:
    result = run_egress_stair_engine(
        {
            "building_use": "residential",
            "floors_above_grade": 6,
            "total_units": 24,
            "sprinklered": True,
            "stair_count_proposed": 1,
        }
    )

    applies_codes = {item["code"] for item in result["applies"]}

    assert "EGRESS-STAIR-001" in applies_codes
    assert "EGRESS-STAIR-002" in applies_codes
