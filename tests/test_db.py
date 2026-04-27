from sqlalchemy import text

from app.db.session import SessionLocal


def test_db_connection() -> None:
    db = SessionLocal()
    try:
        assert db.execute(text("select 1")).scalar() == 1
    finally:
        db.close()
