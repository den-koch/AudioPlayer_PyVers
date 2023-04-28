""" Hello world
here it is
here we go again
"""
import os
import sys

from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


# from tree_view import *


# from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
# from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    """Class Main window"""

    def __init__(self):
        QMainWindow.__init__(self)

        # Load UI file

        self.main_ui = uic.loadUi("design.ui", self)
        # self.main_ui = Ui_MainWindow()
        # self.main_ui.setupUi(self)

        # Main Window settings

        self.setWindowTitle("Audio Player PyVerse")
        self.setFixedWidth(self.geometry().width())

        # Define Widgets signals

        self.main_ui.pushButton_Play.clicked.connect(self.play_track)
        self.main_ui.pushButton_Pause.clicked.connect(self.pause_track)
        self.main_ui.pushButton_Stop.clicked.connect(self.stop_playing)
        self.main_ui.pushButton_Previous_track.clicked.connect(self.previous_track)
        self.main_ui.pushButton_Next_track.clicked.connect(self.next_track)
        self.main_ui.pushButton_Open_file.clicked.connect(self.add_music)  # self.open_file
        self.main_ui.pushButton_Open_file.clicked.connect(self.open_file)
        self.main_ui.pushButton_Delete_file.clicked.connect(self.delete_file)

        self.main_ui.slider_Volume.valueChanged.connect(self.change_volume)

        self.main_ui.treeView_Playlist.doubleClicked.connect(self.get_track)

        # self.slider_Duration.

    def play_track(self):
        self.main_ui.EqualizerWidget.set_timer.start()

    def pause_track(self):
        self.main_ui.EqualizerWidget.set_timer.stop()

    def stop_playing(self):
        pass

    def previous_track(self):
        pass

    def next_track(self):
        pass

    def open_file(self):
        file_filter = "All supported (*.mp3 *.mp4 *.wav *.m4a *.flac *.wma)"
        files, _ = QFileDialog.getOpenFileNames(self, caption="Open file...", directory=os.getcwd(),
                                                filter=file_filter)  # options=QFileDialog.DontUseNativeDialog
        if files:
            for file in files:
                print(file)
                # self.add_music(os.path.split(file)[1], os.path.split(os.path.split(file)[0])[1])

    def add_music(self):
        tree_model = QtGui.QStandardItemModel()
        root_node = tree_model.invisibleRootItem()

        america = QtGui.QStandardItem("Jr")
        abx = QtGui.QStandardItem("abx")
        america.appendRow(abx)
        usa = QtGui.QStandardItem("yes")
        yes = QtGui.QStandardItem("usa")
        usa.appendRow(yes)
        hallo = QtGui.QStandardItem("hallo")
        usa.appendRow(hallo)
        root_node.appendRow(america)
        root_node.appendRow(usa)
        self.main_ui.treeView_Playlist.setModel(tree_model)
        # self.main_ui.treeView_Playlist.expandAll()

    def get_track(self, val):
        print("parent", val.parent().data())
        print("child", val.data())

    def delete_file(self):
        pass

    def change_volume(self):
        print(self.slider_Volume.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
