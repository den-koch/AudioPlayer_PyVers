""" Main app file """
import os
import sys
import json
import time
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from widgets import settings
from widgets.menu import MyMenu


from gui import Ui_AudioPlayer


class AudioPlayer(QMainWindow):
    """ Main app cLass

    Attributes
    ----------
    playlists_folder : dict
        keys: playlists names
        values: QMediaPlaylist object

    playlists_media : dict
        keys: playlists names
        values: list of media path

    current_playlist: object
        currently playing QMediaPlaylist object """

    def __init__(self):
        QMainWindow.__init__(self)

        # Load UI file

        # self.main_ui = uic.loadUi("design.ui", self)
        self.main_ui = Ui_AudioPlayer()
        self.main_ui.setupUi(self)

        # Main Window settings

        self.setWindowTitle("Audio Player PyVerse")
        self.setFixedWidth(self.geometry().width())

        # Add Widgets and Variables

        self.status_label = QLabel("Status: ...")
        self.track_label = QLabel("Track: ...")
        self.player = QMediaPlayer(volume=20)
        self.menu_open = MyMenu()
        self.menu_open.add_actions()

        self.tree_model = QtGui.QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()

        self.playlists_media = {}
        self.playlists_folder = {}
        self.current_playlist = None

        self.__init_settings()
        self.__init_ui()

    def __init_settings(self):
        """ Init some widgets settings """
        self.main_ui.pushButton_Open_file.setMenu(self.menu_open)
        self.main_ui.statusBar.addPermanentWidget(self.status_label, 1)
        self.main_ui.statusBar.addPermanentWidget(self.track_label, 2)
        self.main_ui.treeView_Playlist.setModel(self.tree_model)
        self.main_ui.treeView_Playlist.expandAll()

    def __init_ui(self):
        """ Connect widgets events """
        self.main_ui.pushButton_Play.clicked.connect(self.play_track)
        self.main_ui.pushButton_Pause.clicked.connect(self.pause_track)
        self.main_ui.pushButton_Stop.clicked.connect(self.stop_track)
        self.main_ui.pushButton_Previous_track.clicked.connect(self.previous_track)
        self.main_ui.pushButton_Next_track.clicked.connect(self.next_track)
        self.main_ui.pushButton_Delete_file.clicked.connect(self.delete_track)
        self.menu_open.triggered.connect(self.open_file)
        self.main_ui.actionExit.triggered.connect(self.close)
        self.main_ui.menuMain.triggered.connect(self.open_file)
        self.main_ui.actionAbout.triggered.connect(lambda: os.startfile(f"{os.getcwd()}\\README.md"))
        self.main_ui.actionHelp.triggered.connect(lambda: os.startfile(f"{os.getcwd()}\\info\\HELP.md"))

        self.main_ui.treeView_Playlist.doubleClicked.connect(self.select_track)
        self.main_ui.slider_Volume.valueChanged.connect(self.change_volume)
        self.main_ui.slider_Volume.sliderReleased.connect(self.slider_released)
        self.main_ui.slider_Duration.actionTriggered.connect(self.media_rewind)
        self.player.currentMediaChanged.connect(self.media_changed)
        self.player.durationChanged.connect(self.track_duration)
        self.player.positionChanged.connect(self.track_position)
        self.tree_model.dataChanged.connect(self.rename_playlist)

    def rename_playlist(self, index):
        """ Rename the playlist """
        index_id = self.main_ui.treeView_Playlist.selectedIndexes()[0].row()
        previous_name = list(self.playlists_folder.keys())[index_id]

        if index.data() in self.playlists_folder:
            self.tree_model.setData(index, previous_name)

        else:
            self.playlists_folder[index.data()] = self.playlists_folder.pop(previous_name)
            self.playlists_media[index.data()] = self.playlists_media.pop(previous_name)

            for item in list(self.playlists_folder.keys())[index_id:-1]:
                self.playlists_folder[item] = self.playlists_folder.pop(item)
                self.playlists_media[item] = self.playlists_media.pop(item)

    def media_rewind(self):
        """ Rewind the track """
        self.player.setPosition(self.main_ui.slider_Duration.sliderPosition() * 1000)

    def track_position(self, position):
        """ Show the current track time position """
        self.main_ui.label_Start.setText((time.strftime('%H:%M:%S', time.gmtime(position / 1000))))
        self.main_ui.slider_Duration.setValue(int(position / 1000))

    def track_duration(self, duration):
        """ Set track time duration """
        self.main_ui.label_End.setText((time.strftime('%H:%M:%S', time.gmtime(duration / 1000))))
        self.main_ui.slider_Duration.setMaximum(int(duration / 1000))

    def media_changed(self, media):
        """ Set label track name text """
        if not media.isNull():
            self.track_label.setText(f"Track: {media.canonicalUrl().fileName().rsplit('.')[0]}")
        else:
            self.current_playlist.setCurrentIndex(0)

    def select_track(self):
        """ Set the selected track to playback """
        index = self.main_ui.treeView_Playlist.selectedIndexes()[0]
        if index.parent().data() is not None:
            self.current_playlist = self.playlists_folder[index.parent().data()]
            self.player.setPlaylist(self.current_playlist)
            self.current_playlist.setCurrentIndex(index.row())
            self.player.play()
            self.status_label.setText("Status: Playing")
            self.track_label.setText(f"Track: {index.data()}")
            self.main_ui.EqualizerWidget.set_timer.start()

    def play_track(self):
        """ Play the track """
        if self.current_playlist is not None:
            self.player.play()
            self.status_label.setText("Status: Playing")
            self.main_ui.EqualizerWidget.set_timer.start()

    def pause_track(self):
        """ Pause the track """
        if self.current_playlist is not None:
            self.player.pause()
            self.status_label.setText("Status: Paused")
            self.main_ui.EqualizerWidget.set_timer.stop()

    def stop_track(self):
        """ Stop playing music """
        if self.current_playlist is not None:
            self.player.stop()
            self.status_label.setText("Status: Stopped")
            self.main_ui.EqualizerWidget.set_timer.stop()

    def previous_track(self):
        """ Skip to the previous track """
        if self.current_playlist is not None:
            if self.current_playlist.currentIndex() == 0:
                self.current_playlist.setCurrentIndex(self.current_playlist.mediaCount() - 1)
            else:
                self.current_playlist.previous()
            self.player.play()

    def next_track(self):
        """ Skip to the next track """
        if self.current_playlist is not None:
            self.current_playlist.next()
            self.player.play()

    def delete_track(self):
        """ Delete selected track/playlist """
        index = self.main_ui.treeView_Playlist.selectedIndexes()
        if not index:
            return
        playlist_key = index[0].parent().data()
        if playlist_key is None:
            if self.current_playlist == self.playlists_folder[index[0].data()]:
                self.player.stop()
                self.main_ui.EqualizerWidget.set_timer.stop()
                self.status_label.setText("Status: ...")
                self.track_label.setText("Track: ...")
                self.current_playlist = None
            del self.playlists_folder[index[0].data()]
            del self.playlists_media[index[0].data()]
        else:
            self.playlists_folder[playlist_key].removeMedia(index[0].row())
            self.playlists_media[playlist_key].pop(index[0].row())

        self.tree_model.removeRow(index[0].row(), index[0].parent())

    def change_volume(self):
        """ Change music volume """
        self.player.setVolume(self.main_ui.slider_Volume.value())
        self.main_ui.label_Volume.setText(f"Volume: {self.main_ui.slider_Volume.value()}%")
        if not self.main_ui.slider_Volume.isSliderDown():
            self.slider_released()

    def slider_released(self):
        """Set volume tooltip and text"""
        self.main_ui.slider_Volume.setToolTip(f"{self.main_ui.slider_Volume.value()}%")
        self.main_ui.label_Volume.setText("Volume")

    def open_file(self, action):
        """ Open files from device """

        if action.text() == "New Playlist":
            counter = 1
            while f"new playlist {counter}" in self.playlists_folder:
                counter += 1
            new_playlist = QMediaPlaylist(self.player)
            new_folder = QtGui.QStandardItem(f"new playlist {counter}")
            self.playlists_media[new_folder.text()] = []
            self.playlists_folder[new_folder.text()] = new_playlist
            self.root_node.appendRow(new_folder)

        elif action.text() == "Files":
            files, _ = QFileDialog.getOpenFileNames(self, caption="Open file(-s)...",
                                                    directory=os.getcwd(),
                                                    filter=" ".join(settings.file_filter_files))
            if files:
                if self.main_ui.treeView_Playlist.selectedIndexes():
                    self.add_songs(files)
                else:
                    self.add_songs_new_folder(files)

        elif action.text() == "Folder":
            dir_path = QFileDialog.getExistingDirectory(self, caption="Open folder...",
                                                        directory=os.getcwd())
            dir_name = os.path.split(dir_path)[-1]

            if dir_name not in self.playlists_media:
                files_in_dir = os.listdir(dir_path) if dir_path else []
                music_files = []
                for file in files_in_dir:
                    if file.endswith(settings.file_filter_dir):
                        music_files.append(f"{dir_path}/{file}")

                if music_files:
                    self.add_folder(dir_name, music_files)

        print(self.playlists_folder)
        print(self.playlists_media)

    def add_media(self, folder, files: list, playlist):
        """ Add media to the playlist """
        self.playlists_folder[folder.text()] = playlist
        for file in files:
            self.playlists_media[folder.text()].append(file)
            playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            new_name = QtGui.QStandardItem(file.split("/")[-1].rsplit('.')[0])
            folder.appendRow(new_name)

    def add_songs(self, files: list):
        """ Add multiple media to an existing playlist """
        index = self.main_ui.treeView_Playlist.selectedIndexes()[0]
        if index.parent().data() is None:
            folder = index.model().itemFromIndex(index)
        else:
            folder = index.parent().model().itemFromIndex(index.parent())
        self.add_media(folder, files, self.playlists_folder[folder.text()])
        self.main_ui.treeView_Playlist.expand(index)

    def add_songs_new_folder(self, files: list):
        """ Add multiple media from a folder to the new playlist """
        folder_name = files[0].split("/")[-2]
        if folder_name not in self.playlists_folder:
            new_playlist = QMediaPlaylist(self.player)
            new_folder = QtGui.QStandardItem(folder_name)
            self.playlists_media[folder_name] = []
            self.add_media(new_folder, files, new_playlist)
            self.root_node.appendRow(new_folder)

    def add_folder(self, folder_name: str, files: list):
        """ Add a new entire folder as the new playlist """
        if folder_name not in self.playlists_folder:
            new_playlist = QMediaPlaylist(self.player)
            new_folder = QtGui.QStandardItem(folder_name)
            self.playlists_media[folder_name] = []
            self.add_media(new_folder, files, new_playlist)
            self.root_node.appendRow(new_folder)

    def openEvent(self):
        """Loading the last session data"""

        with open("playlists.json", 'r', encoding='utf8') as open_file:
            playlists = json.load(open_file)

        for folder, files in playlists.items():
            self.add_folder(folder, files)

    def closeEvent(self, event):
        """Saving the current session data before closing"""

        with open("playlists.json", "w", encoding='utf8') as save_file:
            json.dump(self.playlists_media, save_file, indent=4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    audio_player = AudioPlayer()
    audio_player.openEvent()
    audio_player.show()
    sys.exit(app.exec_())
