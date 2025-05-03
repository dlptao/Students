from sqlalchemy.orm import Session
from app.models.models import Class
from typing import List, Optional

def get_class(db: Session, class_id: int) -> Optional[Class]:
    return db.query(Class).filter(Class.id == class_id).first()

def get_classes(db: Session, skip: int = 0, limit: int = 100) -> List[Class]:
    return db.query(Class).offset(skip).limit(limit).all()

def get_teacher_classes(db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> List[Class]:
    return db.query(Class).filter(Class.teacher_id == teacher_id).offset(skip).limit(limit).all()

def create_class(db: Session, name: str, description: str, teacher_id: int) -> Class:
    db_class = Class(name=name, description=description, teacher_id=teacher_id)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def update_class(db: Session, class_id: int, name: str, description: str) -> Optional[Class]:
    db_class = get_class(db, class_id)
    if db_class:
        db_class.name = name
        db_class.description = description
        db.commit()
        db.refresh(db_class)
    return db_class

def delete_class(db: Session, class_id: int) -> bool:
    db_class = get_class(db, class_id)
    if db_class:
        db.delete(db_class)
        db.commit()
        return True
    return False 