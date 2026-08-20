from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    owner_id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    name: str
    description: str | None = None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)