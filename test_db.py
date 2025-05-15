from db import connect_db

try:
    print("🔍 Đang thử kết nối và lấy cursor...")
    conn = connect_db()
    print("✅ Kết nối thành công!")

    cursor = conn.cursor()
    print("✅ Tạo cursor thành công!")

    cursor.execute(
        "SELECT name, birthday, position, country, shirt_number, height, weight, goals, assists FROM players"
    )
    rows = cursor.fetchall()
    print("📜 Rows:", rows)
    for table in cursor.fetchall():
        print("📄 Table:", table)

    cursor.close()
    conn.close()
    print("✅ Đã đóng kết nối!")
except Exception as e:
    print("❌ Lỗi:", e)
