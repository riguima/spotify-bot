import sys

from PySide6.QtWidgets import QApplication

from spotify_bot.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
