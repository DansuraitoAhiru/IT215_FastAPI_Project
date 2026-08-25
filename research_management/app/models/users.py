from datetime import datetime
from enum import Enum   # tạo một tập hợp các giá trị cố định
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base 

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):     # khi Model kế thừa Base, SQLAlchemy mới biết class đó là một ORM model và quản lý nó để ánh xạ với database
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255),nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    projects = relationship("ResearchProject", back_populates="owner")  # thể hiện qh User 1-N Project
    members = relationship("ResearchMember", back_populates="user")     # Thể hiện qh User 1-N Member
    tasks = relationship("ResearchTask", back_populates="assignee")     # Thể hiện qh User 1-N Tasks