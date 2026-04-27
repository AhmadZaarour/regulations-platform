# src/app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, db_health, health, users
from app.api.v1.endpoints.runs import router as runs_router

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(db_health.router, prefix="/db-health", tags=["db-health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(runs_router, prefix="/runs", tags=["runs"])
