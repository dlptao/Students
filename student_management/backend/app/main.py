# app/main.py
from fastapi import FastAPI
from app.api import auth, class_api, student

app = FastAPI(title="Quản lý học sinh & lớp học")

app.include_router(auth.router)
app.include_router(class_api.router)
app.include_router(student.router)