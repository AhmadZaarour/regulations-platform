from app.api.health import health


def test_health_has_ok_status() -> None:
    result = health()
    assert result["status"] == "ok"
    assert "app" in result
    assert "env" in result
