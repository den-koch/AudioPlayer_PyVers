""" Hello world
here it is
here we go again
"""

import os
import sys
import json
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

from modules import *


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

        # Add Widgets, Variables

        self.player = QMediaPlayer()
        self.url = QUrl()

        self.media_playlists = {}
        self.folder_playlist = {}
        self.counter = 1

        # Widgets settings

        self.tree_model = QtGui.QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()
        self.main_ui.treeView_Playlist.setModel(self.tree_model)
        self.main_ui.treeView_Playlist.expandAll()

        self.menu_open = QMenu()
        self.menu_open.setStyleSheet(menu_style)
        self.menu_open.addAction("New Playlist")
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

        # self.main_ui.treeView_Playlist.doubleClicked.connect(self.get_track)

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

        if action.text() == "New Playlist":
            new_playlist = QMediaPlaylist(self.player)
            new_folder = QtGui.QStandardItem(f"new playlist {self.counter}")
            self.counter += 1
            self.media_playlists[new_folder.text()] = []
            self.folder_playlist[new_folder.text()] = new_playlist
            self.root_node.appendRow(new_folder)

        elif action.text() == "Files":
            files, _ = QFileDialog.getOpenFileNames(self, caption="Open file(-s)...", directory=os.getcwd(),
                                                    filter=" ".join(file_filter_for_files))
            if files:
                if self.main_ui.treeView_Playlist.selectedIndexes():
                    self.add_songs(files)
                else:
                    self.add_songs_new_folder(files)

        else:
            dir_path = QFileDialog.getExistingDirectory(self, caption="Open folder...", directory=os.getcwd())
            dir_name = os.path.split(dir_path)[-1]
            if dir_name in list(self.media_playlists.keys()):
                pass
            else:
                files_in_dir = os.listdir(dir_path) if dir_path else []
                music_files = []
                for file in files_in_dir:
                    if file.endswith(file_filter_for_dir):
                        music_files.append(f"{dir_path}/{file}")

                if music_files:
                    self.add_folder(dir_name, music_files)

        print(self.media_playlists)
        print(self.folder_playlist)
        self.main_ui.treeView_Playlist.expandAll()

    def cycle_add(self, folder, files, playlist):
        for file in files:
            self.media_playlists[folder.text()].append(file)
            self.folder_playlist[folder.text()] = playlist
            playlist.addMedia(QMediaContent(self.url.fromLocalFile(file)))
            file = file.split("/")
            new_name = QtGui.QStandardItem(file[-1].rsplit('.')[0])
            folder.appendRow(new_name)

    def add_songs(self, files: list):
        index = self.main_ui.treeView_Playlist.selectedIndexes()[0]
        if index.parent().data() is None:
            folder = index.model().itemFromIndex(index)
        else:
            folder = index.parent().model().itemFromIndex(index.parent())
        self.cycle_add(folder, files, self.folder_playlist[folder.text()])

    def add_songs_new_folder(self, files: list):
        folder = files[0].split("/")[-2]
        if folder not in list(self.media_playlists.keys()):
            new_playlist = QMediaPlaylist(self.player)
            new_folder = QtGui.QStandardItem(folder)
            self.media_playlists[folder] = []
            self.cycle_add(new_folder, files, new_playlist)
            self.root_node.appendRow(new_folder)

    def add_folder(self, folder: str, files: list):
        new_playlist = QMediaPlaylist(self.player)
        new_folder = QtGui.QStandardItem(folder)
        self.media_playlists[folder] = []
        self.cycle_add(new_folder, files, new_playlist)
        self.root_node.appendRow(new_folder)

    # def get_track(self, val):
    #     print(val)
    #     index = self.main_ui.treeView_Playlist.selectedIndexes()[0]
    #     print(index, index.data())
    #     # crawler = index.model().itemFromIndex(index)
    #     # print(crawler)
    #     print(self.main_ui.treeView_Playlist.selectedIndexes()[0],
    #           self.main_ui.treeView_Playlist.selectedIndexes()[0].data())
    #
    #     for ix in self.main_ui.treeView_Playlist.selectedIndexes():
    #         print(ix.data())
    #         # print(ix.row())
    #
    #     print("parent", val.parent().data())
    #     print("child", val.data())

    def delete_file(self):
        pass

    def change_volume(self):
        print(self.slider_Volume.value())

    def closeEvent(self, event):
        with open("playlists.json", "w") as save_file:
            json.dump(self.media_playlists, save_file, indent=4)

        with open('playlists.json', 'r') as open_file:
            print(json.load(open_file))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
