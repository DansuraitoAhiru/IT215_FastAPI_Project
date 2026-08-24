from fastapi import APIRouter, Depends
from app.dependencies.dependency import get_current_user
from app.schemas.user import UserResponse
from app.utils.responses import create_response
from app.dependencies.dependency import require_admin
from app.services.user_service import get_users_services
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.get("/me", response_model=UserResponse)
def get_me(user = Depends(get_current_user)):
    return user


@router.get("", response_model=list[UserResponse])
def get_users(db: Session=Depends(get_db), keyword: str | None=None, is_active: bool | None=None, current_user=Depends(require_admin)):
    return get_users_services(db, keyword, is_active)