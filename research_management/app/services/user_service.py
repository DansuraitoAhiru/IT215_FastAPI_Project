from app.schemas.user import UserCreate, UserUpdate
from app.models.users import User
from sqlalchemy.orm import Session
from app.dependencies.dependency import require_admin
from fastapi import HTTPException, status

def get_users_services(db: Session, keyword: str | None = None, is_active: bool | None=None):
    query = db.query(User)

    if keyword:
        query = query.filter(User.full_name.ilike(f"%{keyword}%") | User.email.ilike(f"%{keyword}%"))
    if is_active is not None:    # chỉ để ktra sự tồn tại, ko quan tâm gtri là True hay False
        query = query.filter(User.is_active == is_active)

    users = query.all()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Không tìm thấy tài khoản")
    return users