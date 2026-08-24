from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials   # 1 thư viện để lấy Bearer token từ Header
from app.models.users import User, UserRole
from app.core.security import decode_access_token
from app.db.database import get_db
from sqlalchemy.orm import Session

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # tokenUrl là bắt buộc, khai báo cho FastAPI biết endpoint đăng nhập/lấy token

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

security = HTTPBearer()

# HTTPAuthorizationCredentials là class của FastAPI dùng để chứa thông tin lấy từ header
# Depends(security) bảo FastAPI: chạy HTTPBearer() để lấy thông tin từ header Authorization
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials   # credentials là thuộc tính, để lấy phần token bên trong object HTTPAuthor
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token không hợp lệ")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email hoặc mật khẩu bị sai")

    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tài khoản không hoạt động")
    return user


def require_admin(user: User=Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Phải có sự cho phép của admin, tài khoản này chưa tày đâu")
    return user