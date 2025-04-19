from fastapi import APIRouter, HTTPException, Depends
import pymysql.cursors
import logging

from database import get_connection
from auth import require_teacher  # Dùng để phân quyền

# Cấu hình logger để ghi lại log lỗi
logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.DEBUG)

# Khởi tạo router cho lớp học
classroom_router = APIRouter()

# ✅ API lấy danh sách lớp học – ai cũng có thể xem (học sinh và giáo viên)
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

# ✅ API thêm lớp học mới – chỉ giáo viên được phép
@classroom_router.post("/")
def create_classroom(classroom: dict, user: dict = Depends(require_teacher)):
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

# ✅ API sửa lớp học – chỉ giáo viên được phép
@classroom_router.put("/{classroom_id}")
def update_classroom(classroom_id: int, classroom: dict, user: dict = Depends(require_teacher)):
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

# ✅ API xóa lớp học – chỉ giáo viên được phép
@classroom_router.delete("/{classroom_id}")
def delete_classroom(classroom_id: int, user: dict = Depends(require_teacher)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Kiểm tra lớp học có tồn tại không
        cursor.execute("SELECT * FROM classrooms WHERE id = %s", (classroom_id,))
        classroom = cursor.fetchone()
        if not classroom:
            logger.error(f"Classroom with id {classroom_id} not found")
            raise HTTPException(status_code=404, detail="Classroom not found")

        # Xóa lớp học (sẽ không gặp lỗi khóa ngoại nếu đã thay đổi cấu trúc bảng)
        cursor.execute("DELETE FROM classrooms WHERE id = %s", (classroom_id,))
        conn.commit()

        if cursor.rowcount == 0:
            logger.error(f"No classroom was deleted with id {classroom_id}")
            raise HTTPException(status_code=500, detail="Failed to delete classroom")

        logger.info(f"Classroom with id {classroom_id} deleted successfully")
        return {"message": "Classroom deleted successfully"}
    
    except pymysql.MySQLError as e:
        # Bắt lỗi MySQL và trả về lỗi rõ ràng
        logger.error(f"MySQL error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"MySQL error: {str(e)}")
    
    except Exception as e:
        # Bắt các lỗi khác và trả về thông báo lỗi chung
        logger.error(f"Error deleting classroom with id {classroom_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting classroom: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()
