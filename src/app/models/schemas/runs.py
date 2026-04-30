from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class EgressStairsInput(BaseModel):
    building_use: Literal["residential"]
    floors_above_grade: int = Field(ge=1, le=200)
    total_units: int = Field(ge=0, le=10000)
    sprinklered: bool | None = None
    stair_count_proposed: int | None = Field(default=None, ge=0, le=50)


class RunCreateResponse(BaseModel):
    run_id: int
    job_id: str
    status: str


class RunResultResponse(BaseModel):
    id: int
    status: str
    project_type: str
    input_data: dict[str, Any]
    result: dict[str, Any] | None
    error_message: str | None
    rq_job_id: str | None
    created_at: str | None
    started_at: str | None
    finished_at: str | None


class RunListItem(BaseModel):
    id: int
    status: str
    project_type: str
    created_at: str | None
    finished_at: str | None


class RunListResponse(BaseModel):
    items: list[RunListItem]
