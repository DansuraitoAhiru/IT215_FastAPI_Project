from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DB_URL

Base = declarative_base()  # tạo ra một class cơ sở (base class) chưa được định nghĩa, Base = lớp cha chung của các Model SQLAlchemy
engine = create_engine(DB_URL)  # engine là cầu nối giữa Python và Database

SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db    # Đưa db cho FastAPI sử dụng, nhưng chưa kết thúc hàm
    finally:
        db.close()