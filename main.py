""" Hello world
here it is
here we go again
"""
import os
import sys

from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from modules import *


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

        # Add Widgets / Widgets settings

        self.tree_model = QtGui.QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()
        self.main_ui.treeView_Playlist.setModel(self.tree_model)

        self.menu_open = QMenu()
        self.menu_open.setStyleSheet(menu_style)
        self.menu_open.addAction("Files")
        self.menu_open.addAction("Folder")
        self.main_ui.pushButton_Open_file.setMenu(self.menu_open)

        # Define Widgets signals

        self.main_ui.pushButton_Play.clicked.connect(self.play_track)
        self.main_ui.pushButton_Pause.clicked.connect(self.pause_track)
        self.main_ui.pushButton_Stop.clicked.connect(self.stop_playing)
        self.main_ui.pushButton_Previous_track.clicked.connect(self.previous_track)
        self.main_ui.pushButton_Next_track.clicked.connect(self.next_track)
        self.main_ui.pushButton_Delete_file.clicked.connect(self.delete_file)
        self.menu_open.triggered.connect(self.open_file)
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

    def open_file(self, action: object):
        print(action)
        print('Action: ', action.text())

        if action.text() == "Folder":
            file_name = QFileDialog.getExistingDirectory(self, caption="Open folder...", directory=os.getcwd())
            file_in_dir = os.listdir(file_name)

            music_files=[]
            for file in file_in_dir:
                # print(file.rsplit('.')[0])
                if file.endswith(file_filter_for_dir):
                    music_files.append(file)
            print(music_files)
            # self.add_folder(file_name)

        else:
            files, _ = QFileDialog.getOpenFileNames(self, caption="Open file(-s)...", directory=os.getcwd(),
                                                    filter=" ".join(file_filter_for_files))  # options=QFileDialog.DontUseNativeDialog

            for file in files:
                file = file.split("/")
                self.add_songs(file[-2], file[-1].rsplit('.')[0])

    def add_songs(self, folder: str, name: str):
        print(folder, name)
        new_folder = QtGui.QStandardItem(folder)
        new_name = QtGui.QStandardItem(name)
        new_folder.appendRow(new_name)
        self.root_node.appendRow(new_folder)

    def add_folder(self, folder: str):
        print(folder)

    def add_music(self):

        america = QtGui.QStandardItem("Jr")
        abx = QtGui.QStandardItem("abx")
        america.appendRow(abx)
        usa = QtGui.QStandardItem("yes")
        yes = QtGui.QStandardItem("usa")
        usa.appendRow(yes)
        hallo = QtGui.QStandardItem("hallo")
        usa.appendRow(hallo)
        self.root_node.appendRow(america)
        self.root_node.appendRow(usa)

        # self.main_ui.treeView_Playlist.expandAll()

    def get_track(self, val):
        # index = self.main_ui.treeView_Playlist.selectedIndexes()[0]
        # crawler = index.model().itemFromIndex(index)
        # print(crawler)
        print(self.main_ui.treeView_Playlist.selectedIndexes(),
              self.main_ui.treeView_Playlist.selectedIndexes()[0].data())
        for ix in self.main_ui.treeView_Playlist.selectedIndexes():
            text = ix.data()  # or ix.data()
            print(text)
            row_index = ix.row()
            print(row_index)
        # print(self.main_ui.treeView_Playlist.selectedItems())

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
