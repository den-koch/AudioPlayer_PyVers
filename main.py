import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(self)

        uic.loadUi("design.ui", self)

        # Define Widgets



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
