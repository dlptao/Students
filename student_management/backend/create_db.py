from app.core.database import Base, engine
from app.models import user, classroom, student

print("🔄 Đang tạo bảng...")
Base.metadata.create_all(bind=engine)
print("✅ Tạo bảng thành công.")
