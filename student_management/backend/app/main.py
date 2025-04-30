from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

<<<<<<< HEAD
@app.get("/")
def root():
    return {"message": "Student Management API with SQLAlchemy is running!"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
=======
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
>>>>>>> b63faba1984b7b66cebd04181b5af4a956cd5c3c
