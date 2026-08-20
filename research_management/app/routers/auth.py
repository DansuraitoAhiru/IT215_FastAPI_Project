from fastapi import APIRouter
from app.services.auth_service import register_service, login_serive
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from fastapi import Depends, Request
from app.utils.responses import create_response
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(request: Request, user: RegisterRequest, db: Session=Depends(get_db)):
    new_user = register_service(user, db)
    return create_response(request, 200, "Đăng ký tài khoản thành công", jsonable_encoder(new_user), None)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session=Depends(get_db)):
    token = login_serive(data, db)
    return {
        "access_token": token,
        "token_type": "bearer"
    }