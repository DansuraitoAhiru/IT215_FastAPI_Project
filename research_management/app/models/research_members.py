from datetime import datetime
from enum import Enum   # tạo một tập hợp các giá trị cố định
from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base 

class MemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class ResearchMember(Base):
    __tablename__ = "research_members"

    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(SQLEnum(MemberRole), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("ResearchProject", back_populates="members")  # qh Project 1-N Member
    user = relationship("User", back_populates="members")       # qh User 1-N Member