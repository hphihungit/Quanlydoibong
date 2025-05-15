import pandas as pd
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StatisticsManager(QWidget):
    def __init__(self, go_back_callback=None):
        super().__init__()
        self.setWindowTitle("Thống kê đội bóng")
        self.setFixedSize(800, 800)
        self.go_back_callback = go_back_callback

        layout = QVBoxLayout()

        # Tiêu đề
        title = QLabel("📊 THỐNG KÊ ĐỘI BÓNG")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Biểu đồ tổng hợp trận đấu
        layout.addWidget(QLabel("\n📈 Biểu đồ thống kê trận đấu:"))
        self.match_chart = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.match_chart)

        # Thống kê cầu thủ
        layout.addWidget(QLabel("\n🧍‍♂️ Thống kê theo cầu thủ:"))
        self.best_scorer_label = QLabel()
        self.top_assist_label = QLabel()
        self.best_scorer_label.setStyleSheet("font-size: 14px;")
        self.top_assist_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.best_scorer_label)
        layout.addWidget(self.top_assist_label)

        # Biểu đồ cầu thủ ghi bàn
        layout.addWidget(QLabel("\n📊 Biểu đồ top cầu thủ ghi bàn:"))
        self.goals_chart = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.goals_chart)

        # Nút quay lại
        back_btn = QPushButton("⬅ Quay lại")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        # Nút tải về file Excel
        download_btn = QPushButton("📥 Tải về Excel")
        download_btn.clicked.connect(self.download_excel)
        layout.addWidget(download_btn)

        self.setLayout(layout)


    def update_statistics(self, matches, players, home_stadium="Old Sanford"):
        self.matches = matches  # Lưu dữ liệu matches vào đối tượng
        self.players = players  # Lưu dữ liệu players vào đối tượng

        wins = losses = draws = goals_scored = goals_conceded = clean_sheets = 0
        home_wins = away_wins = 0

        for match in matches:
            result = match.get("result")
            if result == "win":
                wins += 1
                if match.get("location") == home_stadium:
                    home_wins += 1
                else:
                    away_wins += 1
            elif result == "loss":
                losses += 1
            else:
                draws += 1

            goals_scored += match.get("team_score", 0)
            goals_conceded += match.get("opponent_score", 0)

            if match.get("opponent_score", 1) == 0:
                clean_sheets += 1

        # Cập nhật biểu đồ thống kê trận đấu
        self.update_match_chart(
            wins, losses, draws, goals_scored, goals_conceded,
            clean_sheets, home_wins, away_wins
        )

        # Tìm cầu thủ ghi nhiều bàn / kiến tạo nhất
        if players:
            max_goal = max(players, key=lambda x: x.get("goals", 0))
            max_assist = max(players, key=lambda x: x.get("assists", 0))

            self.best_scorer_label.setText(
                f"⚽ Cầu thủ ghi nhiều bàn nhất: {max_goal['name']} ({max_goal['goals']})"
            )
            self.top_assist_label.setText(
                f"🎯 Cầu thủ kiến tạo nhiều nhất: {max_assist['name']} ({max_assist['assists']})"
            )

            self.update_goal_chart(players)

    def update_match_chart(self, wins, losses, draws, goals_scored, goals_conceded,
                           clean_sheets, home_wins, away_wins):
        labels = [
            "Thắng", "Hòa", "Thua", "Bàn thắng", "Bàn thua",
            "Giữ sạch lưới", "Thắng sân nhà", "Thắng sân khách"
        ]
        values = [
            wins, draws, losses, goals_scored, goals_conceded,
            clean_sheets, home_wins, away_wins
        ]
        colors = ["#4CAF50", "#FFC107", "#F44336", "#2196F3", "#FF9800", "#9C27B0", "#3F51B5", "#009688"]

        fig = self.match_chart.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.bar(labels, values, color=colors)
        ax.set_title("Tổng hợp chỉ số trận đấu")
        ax.set_ylabel("Số lượng")
        ax.tick_params(axis='x', rotation=30)
        fig.tight_layout()
        self.match_chart.draw()

    def update_goal_chart(self, players, top_n=7):
        sorted_players = sorted(players, key=lambda x: x.get("goals", 0), reverse=True)[:top_n]
        names = [p["name"] for p in sorted_players]
        goals = [p.get("goals", 0) for p in sorted_players]

        fig = self.goals_chart.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.barh(names, goals, color="skyblue")
        ax.set_xlabel("Số bàn thắng")
        ax.set_title(f"Top {top_n} cầu thủ ghi bàn")
        ax.invert_yaxis()
        fig.tight_layout()
        self.goals_chart.draw()

    def export_statistics_to_excel(self, matches, players, file_path):
        # Xác định sân nhà để phân biệt thắng sân nhà/sân khách
        home_stadium = "Old Sanford"

        # Tính toán thống kê trận đấu
        wins = losses = draws = goals_scored = goals_conceded = clean_sheets = 0
        home_wins = away_wins = 0

        for match in matches:
            result = match.get("result")
            if result == "win":
                wins += 1
                if match.get("location") == home_stadium:
                    home_wins += 1
                else:
                    away_wins += 1
            elif result == "loss":
                losses += 1
            else:
                draws += 1

            goals_scored += match.get("team_score", 0)
            goals_conceded += match.get("opponent_score", 0)

            if match.get("opponent_score", 1) == 0:
                clean_sheets += 1

        # Ghi thống kê trận đấu vào DataFrame
        match_stats = {
            "Thống kê": [
                "Thắng", "Hòa", "Thua", "Bàn thắng", "Bàn thua",
                "Giữ sạch lưới", "Thắng sân nhà", "Thắng sân khách"
            ],
            "Số lượng": [
                wins, draws, losses, goals_scored, goals_conceded,
                clean_sheets, home_wins, away_wins
            ]
        }
        df_matches = pd.DataFrame(match_stats)

        # Ghi thống kê cầu thủ vào DataFrame
        player_stats = {
            "Cầu thủ": [player["name"] for player in players],
            "Số bàn thắng": [player.get("goals", 0) for player in players],
            "Số kiến tạo": [player.get("assists", 0) for player in players]
        }
        df_players = pd.DataFrame(player_stats)

        # Xuất ra file Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df_matches.to_excel(writer, sheet_name='Thống kê trận đấu', index=False)
            df_players.to_excel(writer, sheet_name='Thống kê cầu thủ', index=False)

    def download_excel(self):
        if not hasattr(self, 'matches') or not hasattr(self, 'players'):
            print("Chưa có dữ liệu thống kê để tải về.")
            return

        # Mở hộp thoại để chọn đường dẫn lưu file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu file Excel", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            # Xuất thống kê ra file Excel
            self.export_statistics_to_excel(self.matches, self.players, file_path)

    def go_back(self):
        if self.go_back_callback:
            self.go_back_callback()



