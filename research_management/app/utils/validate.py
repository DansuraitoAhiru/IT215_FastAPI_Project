from typing import Any
from fastapi import HTTPException, status

def validate_space(info: Any):
    if not info or not info.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Thông tin không được để trống")
    return info.strip()


def validate_pass(password: str):
    password = validate_space(password)
    if len(password) < 6:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Mật khẩu phải có ít nhất 6 ký tự")
    return password