import pymysql
import os
from dotenv import load_dotenv

# Tải cấu hình từ .env
load_dotenv()

def get_connection():
    """Kết nối đến cơ sở dữ liệu MySQL và trả về đối tượng kết nối."""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),  # Chuyển đổi cổng sang kiểu int
        cursorclass=pymysql.cursors.DictCursor  # Trả về kết quả dưới dạng từ điển
    )
