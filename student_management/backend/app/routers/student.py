from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.student import Student

router = APIRouter()

@router.get("/me", response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
