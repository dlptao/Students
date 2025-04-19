from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pymysql.cursors  # ✅ Dùng DictCursor

from database import get_connection  # Sử dụng kết nối của bạn với PyMySQL

# Load biến môi trường từ file .env
load_dotenv()

user_router = APIRouter()

# Lấy biến môi trường
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Schemas
class UserRegister(BaseModel):
    username: str
    password: str
    role: str  # 'teacher' hoặc 'student'

class UserLogin(BaseModel):
    username: str
    password: str

# Hàm tạo JWT token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Hàm đăng ký
@user_router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_password = bcrypt.hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (user.username, hashed_password, user.role)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    finally:
        cursor.close()
        conn.close()

# API Đăng nhập
@user_router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # Dùng DictCursor để trả về dict
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        result = cursor.fetchone()

        if not result or not bcrypt.verify(user.password, result["password"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_token({"sub": result["username"], "role": result["role"]})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        cursor.close()
        conn.close()
