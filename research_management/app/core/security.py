import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": email,
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token không hợp lệ")