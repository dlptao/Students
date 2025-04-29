from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Đọc thông tin kết nối từ .env hoặc viết trực tiếp
DATABASE_URL = "mysql+pymysql://root:12345@localhost:3306/student_clean"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Hiện câu SQL để debug, có thể tắt bằng False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ⚠️ Đây là Base mà bạn cần import trong create_db.py
Base = declarative_base()
