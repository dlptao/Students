# app/schemas/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Class schemas
class ClassBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    teacher_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ClassWithStudents(ClassOut):
    students: List['StudentOut']

# Student schemas
class StudentBase(BaseModel):
    name: str
    class_id: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Delete response schemas
class DeleteResponse(BaseModel):
    message: str
    status: str = "success"

# Update forward references
ClassWithStudents.update_forward_refs()