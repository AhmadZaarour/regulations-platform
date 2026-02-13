from fastapi import APIRouter

router = APIRouter()


@router.post("/login")  # type: ignore[misc]
def login() -> dict[str, str]:
    return {"message": "login endpoint wired"}
