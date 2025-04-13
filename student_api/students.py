from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
import mysql.connector
import os
from jose import JWTError, jwt
from dotenv import load_dotenv

from database import get_connection
from logger import log_exception

# Load .env
load_dotenv()

# Tạo router
student_router = APIRouter()

# Cấu hình JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Cấu hình OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Pydantic models
class StudentCreate(BaseModel):
    name: str
    age: int
    classroom_id: int

class StudentUpdate(StudentCreate):
    pass

class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    classroom_id: int

# Hàm lấy thông tin user từ JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username = payload.get("sub")
        role = payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

# ----------------- CRUD Student -------------------

# Tạo học sinh (chỉ giáo viên)
@student_router.post("/", response_model=dict)
def create_student(student: StudentCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Chỉ giáo viên mới được tạo học sinh")

    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, age, classroom_id) VALUES (%s, %s, %s)",
            (student.name, student.age, student.classroom_id)
        )
        db.commit()
        student_id = cursor.lastrowid
        return {"id": student_id, "message": "Tạo học sinh thành công"}
    except Exception as e:
        log_exception(e)
        raise
    finally:
        cursor.close()
        db.close()

# Lấy danh sách học sinh
@student_router.get("/", response_model=List[StudentOut])
def get_students():
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return students
    finally:
        print('1')
        cursor.close()
        print('2')
        db.close()
        print('3')

# Lấy học sinh theo ID
@student_router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Không tìm thấy học sinh")
        return student
    finally:
        cursor.close()
        db.close()

# Cập nhật học sinh (chỉ giáo viên)
@student_router.put("/{student_id}", response_model=dict)
def update_student(student_id: int, student: StudentUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Chỉ giáo viên mới được cập nhật học sinh")

    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE students SET name=%s, age=%s, classroom_id=%s WHERE id=%s",
            (student.name, student.age, student.classroom_id, student_id)
        )
        db.commit()
        return {"message": "Cập nhật thành công"}
    finally:
        cursor.close()
        db.close()

# Xoá học sinh (chỉ giáo viên)
@student_router.delete("/{student_id}", response_model=dict)
def delete_student(student_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Chỉ giáo viên mới được xoá học sinh")

    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        db.commit()
        return {"message": "Xoá học sinh thành công"}
    finally:
        cursor.close()
        db.close()