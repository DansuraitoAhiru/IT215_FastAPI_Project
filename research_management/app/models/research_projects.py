from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base 

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="projects")  # thể hiện qh User 1-N Project

    # cascade="all" cho phép các thao tác trên User (cha) được lan xuống Assignment (con)
    # delete-orphan nghĩa là nếu một object con không còn thuộc về object cha, SQLAlchemy sẽ xóa object con đó khỏi database
    members = relationship("ResearchMember", back_populates="project", cascade="all, delete-orphan")   # Thể hiện qh Project 1-N Member
    tasks = relationship("ResearchTask", back_populates="project",cascade="all, delete-orphan")      # qh Project 1-N Task