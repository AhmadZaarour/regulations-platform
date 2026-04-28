FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

RUN pip install --upgrade pip \
  && pip install -e . \
  && pip install "SQLAlchemy>=2.0" "psycopg[binary]" alembic rq redis python-jose "passlib[argon2]" argon2-cffi

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]