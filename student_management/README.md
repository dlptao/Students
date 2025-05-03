# Hệ Thống Quản Lý Học Sinh & Lớp Học

Hệ thống quản lý học sinh và lớp học được xây dựng bằng FastAPI, cung cấp các API để quản lý thông tin học sinh và lớp học.

## Tính Năng

- Xác thực người dùng (Authentication)
- Phân quyền người dùng (Authorization)
  - Giáo viên: Quản lý lớp học và học sinh
  - Học sinh: Xem thông tin lớp học
- Quản lý lớp học
  - Tạo lớp học mới
  - Xem danh sách lớp học
  - Cập nhật thông tin lớp học
  - Xóa lớp học
- Quản lý học sinh
  - Thêm học sinh mới
  - Xem danh sách học sinh
  - Cập nhật thông tin học sinh
  - Xóa học sinh

## Cài Đặt

1. Clone repository:
```bash
git clone <repository-url>
cd student_management
```

2. Tạo môi trường ảo và cài đặt dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Cấu hình database:
- Tạo database MySQL
- Cập nhật thông tin kết nối trong file `backend/app/core/config.py`

4. Tạo bảng database:
```bash
python backend/create_tables.py
```

5. Chạy server:
```bash
uvicorn backend.app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/auth/register`: Đăng ký tài khoản mới
- `POST /api/auth/login`: Đăng nhập

### Lớp Học
- `POST /api/classes/`: Tạo lớp học mới (Giáo viên)
- `GET /api/classes/`: Lấy danh sách lớp học
- `GET /api/classes/{class_id}`: Xem chi tiết lớp học
- `PUT /api/classes/{class_id}`: Cập nhật thông tin lớp học (Giáo viên)
- `DELETE /api/classes/{class_id}`: Xóa lớp học (Giáo viên)

### Học Sinh
- `POST /api/students/`: Thêm học sinh mới (Giáo viên)
- `GET /api/students/`: Lấy danh sách học sinh
- `GET /api/students/{student_id}`: Xem chi tiết học sinh
- `PUT /api/students/{student_id}`: Cập nhật thông tin học sinh (Giáo viên)
- `DELETE /api/students/{student_id}`: Xóa học sinh (Giáo viên)

## Cấu Trúc Dự Án

```
backend/
├── app/
│   ├── api/
│   │   ├── auth_api.py
│   │   ├── class_api.py
│   │   └── student_api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── dependencies/
│   │   └── dependencies.py
│   ├── models/
│   │   └── models.py
│   ├── repositories/
│   │   ├── class_repository.py
│   │   ├── student_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── services/
│   │   ├── class_service.py
│   │   ├── student_service.py
│   │   └── user_service.py
│   └── main.py
├── create_tables.py
└── requirements.txt
```

## Công Nghệ Sử Dụng

- FastAPI: Framework web
- SQLAlchemy: ORM
- MySQL: Database
- JWT: Xác thực
- Pydantic: Validation
- Python 3.8+

## Bảo Mật

- Xác thực bằng JWT token
- Mật khẩu được mã hóa bằng bcrypt
- Phân quyền dựa trên vai trò người dùng
- Kiểm tra quyền truy cập cho từng thao tác

## Phát Triển

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy Phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết. 