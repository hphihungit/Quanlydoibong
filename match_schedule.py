
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QDateTimeEdit,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QDateTime
from db import connect_db


class MatchScheduleManager(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.setWindowTitle("Lịch thi đấu & Kết quả")
        self.setFixedSize(1100, 800)
        self.go_back_callback = go_back_callback

        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        main_layout = QVBoxLayout()

        title = QLabel("🗓 TRẬN ĐẤU")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # Nhập thông tin trận đấu
        self.opponent_input = QLineEdit()
        self.opponent_input.setPlaceholderText("Đối thủ")

        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setDisplayFormat("dd/MM/yyyy HH:mm")

        self.result_input = QComboBox()
        self.result_input.addItems(["Thắng", "Hòa", "Thua"])

        self.team_score_input = QLineEdit()
        self.team_score_input.setPlaceholderText("Bàn thắng đội nhà")

        self.opponent_score_input = QLineEdit()
        self.opponent_score_input.setPlaceholderText("Bàn thắng đội khách")

        self.location_input = QComboBox()
        self.location_input.addItems(["Old Sanford", "Away"])

        self.tournament_input = QComboBox()
        self.tournament_input.addItems(["EPL", "Giao hữu", "Champions League"])

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.opponent_input)
        input_layout.addWidget(self.datetime_input)
        input_layout.addWidget(self.result_input)
        input_layout.addWidget(self.team_score_input)
        input_layout.addWidget(self.opponent_score_input)
        input_layout.addWidget(self.location_input)
        input_layout.addWidget(self.tournament_input)

        main_layout.addLayout(input_layout)

        # Nút lưu
        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Thêm trận đấu")
        save_btn.clicked.connect(self.add_match)
        update_btn = QPushButton("📝 Cập nhật")
        update_btn.clicked.connect(self.update_match)
        clear_btn = QPushButton("🧹 Clear Form")
        clear_btn.clicked.connect(self.clear_inputs)
        back_btn = QPushButton("⬅ Quay lại")
        back_btn.clicked.connect(self.go_back)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(back_btn)
        main_layout.addLayout(button_layout)

        # Bảng hiển thị danh sách trận đấu
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Đối thủ", "Thời gian", "Kết quả", "Bàn thắng đội nhà",
            "Bàn thắng đội khách", "Địa điểm", "Giải đấu"
        ])
        main_layout.addWidget(self.table)

        self.table.cellClicked.connect(self.load_selected_match)
        self.selected_match_id = None  # để lưu ID trận được chọn

        self.setLayout(main_layout)

        self.load_matches()

    def add_match(self):
        opponent = self.opponent_input.text()
        match_time = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        result = self.result_input.currentText()
        team_score = self.team_score_input.text()
        opponent_score = self.opponent_score_input.text()
        location = self.location_input.currentText()
        tournament = self.tournament_input.currentText()

        if not opponent or not location or not team_score or not opponent_score:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO matchs (opponent, match_time, result, team_score, opponent_score, location, tournament)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (opponent, match_time, result, team_score, opponent_score, location, tournament))
            self.conn.commit()
            QMessageBox.information(self, "Thành công", "Đã thêm trận đấu.")
            self.clear_inputs()
            self.load_matches()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm trận đấu:\n{e}")
            print(str(e))

    def load_matches(self):
        self.table.setRowCount(0)
        self.cursor.execute("SELECT * FROM matchs ORDER BY match_time DESC")
        for row_data in self.cursor.fetchall():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, data in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def load_selected_match(self, row, column):
        self.selected_match_id = self.table.item(row, 0).text()
        self.opponent_input.setText(self.table.item(row, 1).text())
        datetime_str = self.table.item(row, 2).text()
        self.datetime_input.setDateTime(QDateTime.fromString(datetime_str, "yyyy-MM-dd HH:mm:ss"))
        self.result_input.setCurrentText(self.table.item(row, 3).text())
        self.team_score_input.setText(self.table.item(row, 4).text())
        self.opponent_score_input.setText(self.table.item(row, 5).text())
        self.location_input.setCurrentText(self.table.item(row, 6).text())
        self.tournament_input.setCurrentText(self.table.item(row, 7).text())

    def update_match(self):
        if not self.selected_match_id:
            QMessageBox.warning(self, "Chưa chọn trận", "Vui lòng chọn một trận để cập nhật.")
            return

        opponent = self.opponent_input.text()
        match_time = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        result = self.result_input.currentText()
        team_score = self.team_score_input.text()
        opponent_score = self.opponent_score_input.text()
        location = self.location_input.currentText()
        tournament = self.tournament_input.currentText()

        if not opponent or not location or not team_score or not opponent_score:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            self.cursor.execute("""
                UPDATE matchs
                SET opponent=%s, match_time=%s, result=%s,
                    team_score=%s, opponent_score=%s,
                    location=%s, tournament=%s
                WHERE id=%s
            """, (opponent, match_time, result, team_score, opponent_score, location, tournament, self.selected_match_id))
            self.conn.commit()
            QMessageBox.information(self, "Thành công", "Cập nhật trận đấu thành công.")
            self.clear_inputs()
            self.load_matches()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật trận đấu:\n{e}")
            print(str(e))


    def clear_inputs(self):
        self.opponent_input.clear()
        self.team_score_input.clear()
        self.opponent_score_input.clear()
        self.result_input.setCurrentIndex(0)
        self.location_input.setCurrentIndex(0)
        self.tournament_input.setCurrentIndex(0)
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.selected_match_id = None

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()

