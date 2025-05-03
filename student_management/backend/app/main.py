# app/main.py
from fastapi import FastAPI
from app.api import auth_api, class_api, student_api

app = FastAPI(title="Quản lý học sinh & lớp học")

app.include_router(auth_api.router)
app.include_router(class_api.router)
app.include_router(student_api.router)