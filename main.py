# main.py
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from player_manager import PlayerManager
from formation_manager import FormationManager
from match_schedule import MatchScheduleManager
from repository import fetch_players, fetch_matches
from statistics import StatisticsManager
import sys


class AppController:
    def __init__(self):
        print("✅ AppController init")  # debug

        self.main_win = MainWindow()
        self.player_manager = PlayerManager(go_back_callback=self.show_main)
        self.formation_manager = FormationManager(go_back_callback=self.show_main)
        self.match_schedule = MatchScheduleManager(go_back_callback=self.show_main)
        self.statistics = StatisticsManager(go_back_callback=self.show_main)

        self.connect_buttons()

    def connect_buttons(self):
        print("✅ Connecting buttons...")  # debug
        self.main_win.btn_player.clicked.connect(self.show_player_manager)
        self.main_win.btn_formation.clicked.connect(self.show_formation_manager)
        self.main_win.btn_schedule.clicked.connect(self.show_match_manager)
        self.main_win.btn_statistics.clicked.connect(self.show_statistics)

    def show_main(self):
        print("🟨 show_main called")  # debug
        self.player_manager.hide()
        self.formation_manager.hide()
        self.match_schedule.hide()
        self.statistics.hide()
        self.main_win.show()

    def show_player_manager(self):
        print("➡️ Show: Quản lý cầu thủ")  # debug
        self.main_win.hide()
        # self.player_manager.load_players()  # gọi tại đây
        # QTimer.singleShot(100, self.player_manager.load_players)  # 100ms delay
        self.player_manager.show()

    def show_formation_manager(self):
        print("➡️ Show: Quản lý đội hình")  # debug
        self.main_win.hide()
        self.formation_manager.show()

    def show_match_manager(self):
        print("➡️ Show: Lịch thi đấu")  # debug
        self.main_win.hide()
        self.match_schedule.show()

    def show_statistics(self):
        print("➡️ Show: Thống kê")  # debug
        self.main_win.hide()
        players = fetch_players()
        matches = fetch_matches()
        self.statistics.update_statistics(matches, players)
        self.statistics.show()


if __name__ == "__main__":
    print("🚀 App started")  # debug
    app = QApplication(sys.argv)
    controller = AppController()
    controller.main_win.show()
    sys.exit(app.exec_())
