# app/api/student.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import StudentCreate, StudentUpdate, StudentOut, DeleteResponse
from app.models.models import User
from app.repositories.student_repository import (
    get_student, get_students, get_class_students,
    create_student, update_student, delete_student
)
from app.repositories.class_repository import get_class
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

@router.post("/", response_model=StudentOut)
def create_new_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép thêm học sinh"
        )
    
    # Kiểm tra xem lớp học có tồn tại và thuộc về giáo viên này không
    db_class = get_class(db, student_in.class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lớp học"
        )
    if db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền thêm học sinh vào lớp học này"
        )
    
    return create_student(
        db=db,
        name=student_in.name,
        class_id=student_in.class_id
    )

@router.get("/", response_model=List[StudentOut])
def read_students(
    skip: int = 0,
    limit: int = 100,
    class_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if class_id:
        # Kiểm tra quyền truy cập lớp học
        db_class = get_class(db, class_id)
        if db_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy lớp học"
            )
        if current_user.role == "teacher" and db_class.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Không có quyền xem danh sách học sinh của lớp này"
            )
        return get_class_students(db, class_id, skip, limit)
    return get_students(db, skip, limit)

@router.get("/{student_id}", response_model=StudentOut)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học sinh"
        )
    
    # Kiểm tra quyền truy cập
    db_class = get_class(db, db_student.class_id)
    if current_user.role == "teacher" and db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xem thông tin học sinh này"
        )
    return db_student

@router.put("/{student_id}", response_model=StudentOut)
def update_student_info(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép cập nhật thông tin học sinh"
        )
    
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học sinh"
        )
    
    # Kiểm tra quyền cập nhật
    db_class = get_class(db, db_student.class_id)
    if db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền cập nhật thông tin học sinh này"
        )
    
    # Kiểm tra lớp học mới nếu có thay đổi
    if student_in.class_id != db_student.class_id:
        new_class = get_class(db, student_in.class_id)
        if new_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy lớp học mới"
            )
        if new_class.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Không có quyền chuyển học sinh vào lớp học này"
            )
    
    return update_student(
        db=db,
        student_id=student_id,
        name=student_in.name,
        class_id=student_in.class_id
    )

@router.delete("/{student_id}", response_model=DeleteResponse)
def delete_student_info(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép xóa học sinh"
        )
    
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy học sinh"
        )
    
    # Kiểm tra quyền xóa
    db_class = get_class(db, db_student.class_id)
    if db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xóa học sinh này"
        )
    
    delete_student(db, student_id)
    return DeleteResponse(message="Đã xóa học sinh thành công")