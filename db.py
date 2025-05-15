# database.py
import pymysql

def connect_db():
    try:
        print("🛠️ Đang tạo kết nối tới MySQL...")
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="123",
            database="doibong",
        )
        print("✅ Kết nối thành công!")
        return conn
    except Exception as e:
        print("❌ Lỗi kết nối:")
        raise




# Thêm các hàm update_player, delete_player, search_player sau đó
