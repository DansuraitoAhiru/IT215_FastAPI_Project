import os   # là thư viện/module có sẵn của Python, dùng để làm việc với hệ điều hành (Operating System), ở đây dùng để lấy biến từ môi trg
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))