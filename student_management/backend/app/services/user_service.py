# app/services/user_service.py
from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_username, create_user
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.schemas import UserCreate
from fastapi import HTTPException, status

def register_user(db: Session, user_in: UserCreate):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    password_hash = get_password_hash(user_in.password)
    return create_user(db, user_in.username, password_hash, user_in.role)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user