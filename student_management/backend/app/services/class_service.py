from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.class_repository import (
    get_class, get_classes, get_teacher_classes,
    create_class, update_class, delete_class
)
from app.schemas.schemas import ClassCreate, ClassUpdate
from app.models.models import User

def create_new_class(db: Session, class_in: ClassCreate, teacher: User):
    if teacher.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên được phép tạo lớp"
        )
    return create_class(
        db=db,
        name=class_in.name,
        description=class_in.description,
        teacher_id=teacher.id
    )

def get_all_classes(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    if current_user.role == "teacher":
        return get_teacher_classes(db, current_user.id, skip, limit)
    return get_classes(db, skip, limit)

def get_class_by_id(db: Session, class_id: int, current_user: User):
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

def update_class_info(db: Session, class_id: int, class_in: ClassUpdate, current_user: User):
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

def delete_class_info(db: Session, class_id: int, current_user: User):
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