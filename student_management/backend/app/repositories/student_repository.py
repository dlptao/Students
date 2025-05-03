from sqlalchemy.orm import Session
from app.models.models import Student
from typing import List, Optional

def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    return db.query(Student).offset(skip).limit(limit).all()

def get_class_students(db: Session, class_id: int, skip: int = 0, limit: int = 100) -> List[Student]:
    return db.query(Student).filter(Student.class_id == class_id).offset(skip).limit(limit).all()

def create_student(db: Session, name: str, class_id: int) -> Student:
    db_student = Student(name=name, class_id=class_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, name: str, class_id: int) -> Optional[Student]:
    db_student = get_student(db, student_id)
    if db_student:
        db_student.name = name
        db_student.class_id = class_id
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int) -> bool:
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False 