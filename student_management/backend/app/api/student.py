# app/api/student.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import StudentCreate, StudentOut
from app.models.models import Student
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

@router.post("/", response_model=StudentOut)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Chỉ giáo viên được phép tạo học sinh")
    new_student = Student(name=student_in.name, class_id=student_in.class_id)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student