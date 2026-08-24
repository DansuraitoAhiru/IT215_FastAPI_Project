from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.users import UserRole
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)
    full_name: str = Field(min_length=1, max_length=50)

class RegisterResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str