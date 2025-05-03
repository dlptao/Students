# Tạo file create_tables.py
from app.models.models import Base
from app.dependencies.dependencies import engine

Base.metadata.create_all(bind=engine)