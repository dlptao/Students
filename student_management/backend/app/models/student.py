from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    # Quan hệ ORM
    classroom = relationship("Classroom")
    creator = relationship("User")
