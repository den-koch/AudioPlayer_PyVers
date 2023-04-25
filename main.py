import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.Equalizer import EqualizerBar
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("design.ui", self)

        # Define Widgets
        self.pushButton_Play = self.findChild(QPushButton, "pushButton_Play")
        self.pushButton_Pause = self.findChild(QPushButton, "pushButton_Pause")
        self.pushButton_Stop = self.findChild(QPushButton, "pushButton_Stop")
        self.pushButton_Previous_track = self.findChild(QPushButton, "pushButton_Previous_track")
        self.pushButton_Next_track = self.findChild(QPushButton, "pushButton_Next_track")
        self.pushButton_Open_file = self.findChild(QPushButton, "pushButton_Open_file")
        
        self.gridLayout_Equalizer = self.findChild(QGridLayout, "gridLayout")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
