import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# Import các router
from users import user_router
from students import student_router
from classrooms import classroom_router

# Load biến môi trường từ file .env
load_dotenv()

# Kiểm tra biến môi trường
print("✅ DB_HOST:", os.getenv("DB_HOST"))
print("✅ SECRET_KEY:", os.getenv("SECRET_KEY"))

# Cấu hình kết nối cơ sở dữ liệu
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Tạo engine và session cho SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Khởi tạo base class cho ORM models
Base: DeclarativeMeta = declarative_base()

# Hàm khởi tạo session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    description="API quản lý học sinh sử dụng FastAPI và MySQL"
)

# Cấu hình CORS cho phép frontend truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Đổi thành ["http://localhost:5173"] nếu dùng Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(student_router, prefix="/students", tags=["Students"])
app.include_router(classroom_router, prefix="/classrooms", tags=["Classrooms"])

# Route mặc định
@app.get("/")
def home():
    return {"message": "Student Management with FastAPI + MySQL"}

# Tùy chỉnh Swagger UI để hỗ trợ Bearer Token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Gán schema tùy chỉnh cho app
app.openapi = custom_openapi

# Tạo cơ sở dữ liệu nếu chưa có
Base.metadata.create_all(bind=engine)
