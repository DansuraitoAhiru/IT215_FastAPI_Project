from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str


class MemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: str


class MemberUpdate(BaseModel):
    role: str | None = None


class MemberResponse(MemberBase):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)