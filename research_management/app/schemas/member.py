from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal

class AddMemberRequest(BaseModel):
    user_id: int


class MemberUpdate(BaseModel):
    role: Literal["OWNER", "MEMBER"] | None = None


class MemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)