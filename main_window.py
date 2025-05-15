# ui/main_window.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMainWindow
)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống quản lý đội bóng đá")
        self.setFixedSize(400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        title = QLabel("🏆 QUẢN LÝ ĐỘI BÓNG ĐÁ")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Các nút được định danh rõ ràng
        self.btn_player = QPushButton("Quản lý cầu thủ")
        self.btn_formation = QPushButton("Quản lý đội hình")
        self.btn_schedule = QPushButton("Trận đấu")
        self.btn_statistics = QPushButton("Thống kê")
        self.btn_coach = QPushButton("Quản lý HLV / Ban huấn luyện")

        for btn in [self.btn_player, self.btn_formation, self.btn_schedule, self.btn_statistics, self.btn_coach]:
            btn.setFixedHeight(50)
            btn.setStyleSheet("font-size: 16px;")
            layout.addWidget(btn)

        self.central_widget.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
