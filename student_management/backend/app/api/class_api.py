# app/api/class.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import ClassCreate, ClassUpdate, ClassOut, ClassWithStudents, DeleteResponse
from app.models.models import User
from app.repositories.class_repository import (
    get_class, get_classes, get_teacher_classes,
    create_class, update_class, delete_class
)
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.post("/", response_model=ClassOut)
def create_new_class(
    class_in: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép tạo lớp"
        )
    return create_class(
        db=db,
        name=class_in.name,
        description=class_in.description,
        teacher_id=current_user.id
    )

@router.get("/", response_model=List[ClassOut])
def read_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "teacher":
        return get_teacher_classes(db, current_user.id, skip, limit)
    return get_classes(db, skip, limit)

@router.get("/{class_id}", response_model=ClassWithStudents)
def read_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_class = get_class(db, class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lớp học"
        )
    if current_user.role == "teacher" and db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập lớp học này"
        )
    return db_class

@router.put("/{class_id}", response_model=ClassOut)
def update_class_info(
    class_id: int,
    class_in: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép cập nhật thông tin lớp"
        )
    db_class = get_class(db, class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lớp học"
        )
    if db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền cập nhật lớp học này"
        )
    return update_class(
        db=db,
        class_id=class_id,
        name=class_in.name,
        description=class_in.description
    )

@router.delete("/{class_id}", response_model=DeleteResponse)
def delete_class_info(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép xóa lớp học"
        )
    db_class = get_class(db, class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy lớp học"
        )
    if db_class.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xóa lớp học này"
        )
    delete_class(db, class_id)
    return DeleteResponse(message="Đã xóa lớp học thành công")