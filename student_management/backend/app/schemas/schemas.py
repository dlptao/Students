# app/schemas/schemas.py
from pydantic import BaseModel
from typing import Optional

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

class ClassCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ClassOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    teacher_id: int

    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    name: str
    class_id: int

class StudentOut(BaseModel):
    id: int
    name: str
    class_id: int

    class Config:
        orm_mode = True