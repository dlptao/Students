# app/api/class.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import ClassCreate, ClassUpdate, ClassOut, ClassWithStudents, DeleteResponse
from app.models.models import User
from app.services.class_service import (
    create_new_class, get_all_classes, get_class_by_id,
    update_class_info, delete_class_info
)
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.post("/", response_model=ClassOut)
def create_new_class_endpoint(
    class_in: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_new_class(db, class_in, current_user)

@router.get("/", response_model=List[ClassOut])
def read_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_classes(db, current_user, skip, limit)

@router.get("/{class_id}", response_model=ClassWithStudents)
def read_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_class_by_id(db, class_id, current_user)

@router.put("/{class_id}", response_model=ClassOut)
def update_class_endpoint(
    class_id: int,
    class_in: ClassUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_class_info(db, class_id, class_in, current_user)

@router.delete("/{class_id}", response_model=DeleteResponse)
def delete_class_endpoint(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_class_info(db, class_id, current_user)
    return DeleteResponse(message="Đã xóa lớp học thành công")