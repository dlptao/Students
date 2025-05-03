# app/api/student.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import StudentCreate, StudentUpdate, StudentOut, DeleteResponse
from app.models.models import User
from app.services.student_service import (
    create_new_student, get_all_students, get_student_by_id,
    update_student_info, delete_student_info
)
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

@router.post("/", response_model=StudentOut)
def create_new_student_endpoint(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_new_student(db, student_in, current_user)

@router.get("/", response_model=List[StudentOut])
def read_students(
    skip: int = 0,
    limit: int = 100,
    class_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_students(db, current_user, class_id, skip, limit)

@router.get("/{student_id}", response_model=StudentOut)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_student_by_id(db, student_id, current_user)

@router.put("/{student_id}", response_model=StudentOut)
def update_student_endpoint(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_student_info(db, student_id, student_in, current_user)

@router.delete("/{student_id}", response_model=DeleteResponse)
def delete_student_endpoint(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_student_info(db, student_id, current_user)
    return DeleteResponse(message="Đã xóa học sinh thành công")