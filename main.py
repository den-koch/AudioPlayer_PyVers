import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("design.ui", self)

        # Define Widgets

        self.pushButton_Play.clicked.connect(self.onStart)
        self.pushButton_Pause.clicked.connect(self.onStop)

    def onStart(self):        
        self.EqualizerWidget._timer.start()
        
    def onStop(self):        
        self.EqualizerWidget._timer.stop()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
