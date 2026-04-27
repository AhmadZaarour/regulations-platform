from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me")  # type: ignore[misc]
def get_me(current_user: User = Depends(get_current_user)) -> dict[str, str]:
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }
