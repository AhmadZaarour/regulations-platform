# app/db/session.py
from __future__ import annotations

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
