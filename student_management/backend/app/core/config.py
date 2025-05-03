# app/core/config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:12345@localhost:3306/student_clean")
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60