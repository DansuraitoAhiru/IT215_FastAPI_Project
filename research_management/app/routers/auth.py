from fastapi import APIRouter, status
from app.services.auth_service import register_service, login_service
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, TokenResponse, RegisterResponse, LoginRequest
from fastapi import Depends, Request
from app.utils.responses import create_response
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.dependency import security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: Request, user: RegisterRequest, db: Session=Depends(get_db)):  # Depends là 1 hàm có nv tự chạy hàm truyền vào trước, lấy kết quả của nó rồi đưa kết quả vào lại parameter cho tôi
    new_user = register_service(user, db)
    data = RegisterResponse.model_validate(new_user)
    return create_response(request, 201, "Đăng ký tài khoản thành công", data.model_dump(), None)


@router.post("/login", response_model=TokenResponse)
# def login(data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):   # FastAPI hãy tự tạo OAuth2PasswordRequestForm và inject nó vào form_data
def login(data: LoginRequest, db: Session=Depends(get_db)):
    token = login_service(data, db)
    return {
        "access_token": token,
        "token_type": "bearer"
    }