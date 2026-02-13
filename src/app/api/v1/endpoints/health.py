from fastapi import APIRouter

router = APIRouter()


@router.get("/health")  # type: ignore[misc]
def health() -> dict[str, str]:
    return {"status": "ok"}
