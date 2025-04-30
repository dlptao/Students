from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Student Management API with SQLAlchemy is running!"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])