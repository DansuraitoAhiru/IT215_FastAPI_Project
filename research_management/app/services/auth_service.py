from app.models.users import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def register_service(user: RegisterRequest, db: Session):
    try:
        exist = db.query(User).filter(User.email == user.email).first()
        if exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email đã tồn tại")

        hashed = hash_password(user.password)
        new_user = User(
            email = user.email,
            password_hash = hashed,
            full_name = user.full_name
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))


def login_serive(data: LoginRequest, db: Session):
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email hoặc mật khẩu sai")
        if not user.is_active:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Tài khoản không hoạt động")
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sai email hoặc mật khẩu")

        token = create_access_token(
            email = data.email,
            role= user.role
        ) 
        return token
    except HTTPException:
        db.rollback()
        raise
    except Exception as error:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))