from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from db import connect_db

from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
from datetime import datetime


class PlayerManager(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.setWindowTitle("Quản lý cầu thủ")
        self.setFixedSize(1300, 800)
        self.go_back_callback = go_back_callback

        layout = QVBoxLayout()

        title = QLabel("⚽ QUẢN LÝ CẦU THỦ")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Bảng cầu thủ
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Họ tên", "Ngày sinh", "Vị trí", "Quốc tịch",
            "Số áo", "Chiều cao", "Cân nặng", "Ghi bàn", "Kiến tạo"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.load_selected_player)
        layout.addWidget(self.table)

        # Form
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.birthday_input = QLineEdit()
        self.position_input = QLineEdit()
        self.country_input = QLineEdit()
        self.shirt_number_input = QLineEdit()
        self.height_input = QLineEdit()
        self.weight_input = QLineEdit()
        self.goals_input = QLineEdit()
        self.assists_input = QLineEdit()

        form_layout.addRow("Họ tên:", self.name_input)
        # form_layout.addRow("Ngày sinh (YYYY-MM-DD):", self.birthday_input)

        self.birthday_input = QDateEdit()
        self.birthday_input.setDisplayFormat("dd/MM/yyyy")
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDate(QDate.currentDate())  # đặt ngày hiện tại làm mặc định

        form_layout.addRow("Ngày sinh (dd/MM/yyyy):", self.birthday_input)

        form_layout.addRow("Vị trí:", self.position_input)
        form_layout.addRow("Quốc tịch:", self.country_input)
        form_layout.addRow("Số áo:", self.shirt_number_input)
        form_layout.addRow("Chiều cao:", self.height_input)
        form_layout.addRow("Cân nặng:", self.weight_input)
        form_layout.addRow("Số bàn thắng:", self.goals_input)
        form_layout.addRow("Số kiến tạo:", self.assists_input)

        layout.addLayout(form_layout)

        # Nút thao tác
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm")
        update_btn = QPushButton("Cập nhật")
        delete_btn = QPushButton("Xóa")
        clear_btn = QPushButton("Clear")
        back_btn = QPushButton("⬅ Quay lại")

        add_btn.clicked.connect(self.add_player)
        update_btn.clicked.connect(self.update_player)
        delete_btn.clicked.connect(self.delete_player)
        clear_btn.clicked.connect(self.clear_form)
        back_btn.clicked.connect(self.go_back)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(back_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.selected_player_id = None
        self.load_players()

    def load_players(self):
        self.table.setRowCount(0)
        try:
            print("🔗 Đang kết nối CSDL...")
            try:
                conn = connect_db()
                print("✅ Đã kết nối DB")
            except Exception as e:
                print("❌ Lỗi khi connect_db():", e)

            try:
                cursor = conn.cursor()
                print("✅ Đã tạo cursor")
            except Exception as e:
                print("❌ Lỗi khi tạo cursor:", e)
            print("✅ Kết nối thành công, thực hiện truy vấn...")
            cursor.execute(
                "SELECT * FROM players"
            )
            rows = cursor.fetchall()
            print(f"📥 Số dòng lấy được: {len(rows)}")

            for row_data in rows:
                print(f"📄 Dòng: {row_data}")
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, data in enumerate(row_data):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

            cursor.close()
            conn.close()
            print("✅ Load dữ liệu xong")
        except Exception as e:
            print("❌ Lỗi:", e)
            import traceback
            traceback.print_exc()
            # QMessageBox.critical(self, "Lỗi khi tải dữ liệu", str(e))

    def load_selected_player(self, row, _col):
        # Lưu id vào biến selected_player_id
        self.selected_player_id = self.table.item(row, 0).text()

        # Cập nhật các trường thông tin cầu thủ từ bảng
        self.name_input.setText(self.table.item(row, 1).text())

        # Lấy giá trị ngày sinh từ bảng và chuyển đổi thành QDate
        birthday_str = self.table.item(row, 2).text()
        birthday_date = QDate.fromString(birthday_str, "dd/MM/yyyy")
        self.birthday_input.setDate(birthday_date)

        self.position_input.setText(self.table.item(row, 3).text())
        self.country_input.setText(self.table.item(row, 4).text())
        self.shirt_number_input.setText(self.table.item(row, 5).text())
        self.height_input.setText(self.table.item(row, 6).text())
        self.weight_input.setText(self.table.item(row, 7).text())
        self.goals_input.setText(self.table.item(row, 8).text())
        self.assists_input.setText(self.table.item(row, 9).text())

    def add_player(self):
        try:
            # Chuyển đổi chuỗi ngày sinh từ định dạng dd/MM/yyyy thành yyyy-MM-dd
            birthday_str = self.birthday_input.text()
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y").date()

            conn = connect_db()
            cursor = conn.cursor()
            sql = """
                INSERT INTO players
                (name, birthday, position, country, shirt_number, height, weight, goals, assists)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                self.name_input.text(), birthday, self.position_input.text(),
                self.country_input.text(), int(self.shirt_number_input.text()),
                float(self.height_input.text()), float(self.weight_input.text()),
                int(self.goals_input.text()), int(self.assists_input.text())
            )
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm cầu thủ.")
            self.load_players()
            self.clear_form()
        except ValueError:
            QMessageBox.critical(self, "Lỗi định dạng", "Ngày sinh phải ở định dạng dd/MM/yyyy.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi thêm cầu thủ", str(e))

    def delete_player(self):
        if not self.selected_player_id:
            QMessageBox.warning(self, "Chọn cầu thủ", "Vui lòng chọn cầu thủ để xóa.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players WHERE id=%s", (self.selected_player_id,))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Xóa thành công", "Đã xóa cầu thủ.")
            self.load_players()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi xóa cầu thủ", str(e))

    def update_player(self):
        if not self.selected_player_id:
            QMessageBox.warning(self, "Chọn cầu thủ", "Vui lòng chọn cầu thủ để cập nhật.")
            return
        try:
            # Chuyển đổi ngày sinh thành định dạng đúng để cập nhật
            birthday_str = self.birthday_input.text()
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y").date()

            conn = connect_db()
            cursor = conn.cursor()

            # SQL để cập nhật cầu thủ
            sql = """
                UPDATE players SET
                name=%s, birthday=%s, position=%s, country=%s,
                shirt_number=%s, height=%s, weight=%s, goals=%s, assists=%s
                WHERE id=%s
            """
            data = (
                self.name_input.text(), birthday, self.position_input.text(),
                self.country_input.text(), int(self.shirt_number_input.text()),
                float(self.height_input.text()), float(self.weight_input.text()),
                int(self.goals_input.text()), int(self.assists_input.text()),
                self.selected_player_id  # Dùng selected_player_id để cập nhật
            )

            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()

            # Hiển thị thông báo thành công và tải lại danh sách cầu thủ
            QMessageBox.information(self, "Thành công", "Đã cập nhật cầu thủ.")
            self.load_players()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi cập nhật", str(e))

    def clear_form(self):
        self.name_input.clear()
        self.birthday_input.clear()
        self.position_input.clear()
        self.country_input.clear()
        self.shirt_number_input.clear()
        self.height_input.clear()
        self.weight_input.clear()
        self.goals_input.clear()
        self.assists_input.clear()
        self.selected_player_id = None

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()

