from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QGridLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

from db import connect_db

formations = {
    "4-4-2": {
        (0, 1): "ST1", (0, 3): "ST2",
        (1, 0): "LM", (1, 1): "CM1", (1, 3): "CM2", (1, 4): "RM",
        (2, 0): "LB", (2, 1): "CB1", (2, 3): "CB2", (2, 4): "RB",
        (3, 2): "GK"
    },
    "4-3-3": {
        (0, 1): "LW", (0, 2): "ST", (0, 3): "RW",
        (1, 1): "CM1", (1, 2): "CM2", (1, 3): "CDM",
        (2, 0): "LB", (2, 1): "CB1", (2, 3): "CB2", (2, 4): "RB",
        (3, 2): "GK"
    },
    "3-5-2": {
        (0, 1): "ST1", (0, 3): "ST2",
        (1, 0): "LM", (1, 1): "CM1", (1, 2): "CAM", (1, 3): "CM2", (1, 4): "RM",
        (2, 1): "CB1", (2, 2): "CB2", (2, 3): "CB3",
        (3, 2): "GK"
    }
}

class FormationManager(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.setWindowTitle("Quản lý đội hình")
        self.setFixedSize(700, 600)
        self.go_back_callback = go_back_callback

        self.main_layout = QVBoxLayout()

        title = QLabel("📋 QUẢN LÝ ĐỘI HÌNH")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.formation_selector = QComboBox()
        self.formation_selector.addItems(formations.keys())
        self.formation_selector.currentTextChanged.connect(self.update_formation)
        self.main_layout.addWidget(self.formation_selector)

        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.grid_layout = QGridLayout()
        self.position_boxes = {}

        self.grid_container = QWidget()
        self.grid_container.setLayout(self.grid_layout)
        self.grid_container.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.grid_container)
        center_layout.addStretch()

        self.main_layout.addLayout(center_layout)

        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Lưu đội hình")
        clear_btn = QPushButton("🧹 Làm mới")
        load_btn = QPushButton("📥 Tải đội hình")
        back_btn = QPushButton("⬅ Quay lại")

        save_btn.clicked.connect(self.save_formation)
        clear_btn.clicked.connect(self.clear_formation)
        load_btn.clicked.connect(self.load_formation)
        back_btn.clicked.connect(self.go_back)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(back_btn)
        self.main_layout.addLayout(button_layout)

        self.setLayout(self.main_layout)

        self.update_formation(self.formation_selector.currentText())

    def load_formation_from_db(self, formation_name):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT position, player_name FROM formations WHERE name = %s", (formation_name,)
        )
        result = cursor.fetchall()
        conn.close()
        return {position: player for position, player in result}

    def fetch_players(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM players")
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result

    def update_formation(self, formation_name):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.position_boxes.clear()
        formation = formations[formation_name]
        players = self.fetch_players()
        saved_data = self.load_formation_from_db(formation_name)

        for (row, col), position in formation.items():
            combo = QComboBox()
            combo.addItems([f"-- {position} --"] + players)
            self.position_boxes[position] = combo

            if position in saved_data:
                index = combo.findText(saved_data[position])
                if index != -1:
                    combo.setCurrentIndex(index)

            self.grid_layout.addWidget(combo, row, col)

    def save_formation(self):
        selected_players = set()
        formation_name = self.formation_selector.currentText()
        data = {}

        for position, combo in self.position_boxes.items():
            player = combo.currentText()
            if player.startswith("--"):
                continue
            if player in selected_players:
                QMessageBox.warning(self, "Trùng cầu thủ", f"Cầu thủ {player} đã được chọn 2 lần!")
                return
            selected_players.add(player)
            data[position] = player

        self.save_formation_to_db(formation_name, data)
        QMessageBox.information(self, "Thành công", "Đội hình đã được lưu thành công!")

    def save_formation_to_db(self, formation_name, data):
        conn = connect_db()
        cursor = conn.cursor()

        # Xóa đội hình cũ trước khi lưu
        cursor.execute("DELETE FROM formations WHERE name = %s", (formation_name,))

        for position, player in data.items():
            cursor.execute(
                "INSERT INTO formations (name, position, player_name) VALUES (%s, %s, %s)",
                (formation_name, position, player)
            )

        conn.commit()
        conn.close()

    def clear_formation(self):
        for combo in self.position_boxes.values():
            combo.setCurrentIndex(0)  # Reset all ComboBoxes to the first item

    def load_formation(self):
        formation_name = self.formation_selector.currentText()
        saved_data = self.load_formation_from_db(formation_name)

        for position, combo in self.position_boxes.items():
            if position in saved_data:
                index = combo.findText(saved_data[position])
                if index != -1:
                    combo.setCurrentIndex(index)

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()



