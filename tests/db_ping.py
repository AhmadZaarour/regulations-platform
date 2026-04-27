from sqlalchemy import text

from app.db.session import SessionLocal


def main() -> None:
    db = SessionLocal()
    try:
        print(db.execute(text("select 1")).scalar())
    finally:
        db.close()


if __name__ == "__main__":
    main()
