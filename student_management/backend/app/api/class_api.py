# app/api/class.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import ClassCreate, ClassOut
from app.models.models import Class
from app.dependencies.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api/classes", tags=["classes"])

@router.post("/", response_model=ClassOut)
def create_class(class_in: ClassCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Chỉ giáo viên được phép tạo lớp")
    new_class = Class(name=class_in.name, description=class_in.description, teacher_id=user.id)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class