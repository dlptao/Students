from fastapi import APIRouter, HTTPException
import pymysql.cursors  # Dùng DictCursor để trả về dữ liệu dưới dạng từ điển

from database import get_connection

# Khởi tạo router cho lớp học
classroom_router = APIRouter()

# API lấy danh sách lớp học (KHÔNG dùng response_model để tránh lỗi validate)
@classroom_router.get("/")
def get_classrooms():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM classrooms")
        classrooms = cursor.fetchall()
        return classrooms
    finally:
        cursor.close()
        conn.close()

# API thêm lớp học mới
@classroom_router.post("/")
def create_classroom(classroom: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO classrooms (name, description) VALUES (%s, %s)",
            (classroom["name"], classroom["description"])
        )
        conn.commit()
        return classroom
    finally:
        cursor.close()
        conn.close()

# API sửa lớp học
@classroom_router.put("/{classroom_id}")
def update_classroom(classroom_id: int, classroom: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE classrooms SET name = %s, description = %s WHERE id = %s",
            (classroom["name"], classroom["description"], classroom_id)
        )
        conn.commit()
        return classroom
    finally:
        cursor.close()
        conn.close()

# API xóa lớp học
@classroom_router.delete("/{classroom_id}")
def delete_classroom(classroom_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM classrooms WHERE id = %s", (classroom_id,))
        conn.commit()
        return {"message": "Classroom deleted successfully"}
    finally:
        cursor.close()
        conn.close()
