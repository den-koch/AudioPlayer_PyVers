""" Unit tests File """
import sys
import unittest
from PyQt5.QtWidgets import QApplication
import main


class MainWindowTest(unittest.TestCase):
    """ Main unit tests class"""

    def setUp(self):
        self.window = main.AudioPlayer()

        self.folders = ["music 2.0", "music", "new playlist 1"]
        self.music = ['D:/KPI/4семестр/ІПЗ-курсова/music 2.0/John Denver - Take Me Home, Country Roads.mp3',
                      'D:/KPI/4семестр/ІПЗ-курсова/music 2.0/The Beatles - Yesterday.mp3',
                      'D:/KPI/4семестр/ІПЗ-курсова/music/Metallica - Enter Sandman.mp3',
                      'D:/KPI/4семестр/ІПЗ-курсова/music/AC-DC - Hells Bells.mp3']

    def test_defaults(self):
        """ Test default app settings """
        self.assertFalse(self.window.playlists_folder)
        self.assertFalse(self.window.playlists_media)
        self.assertEqual(self.window.main_ui.slider_Volume.value(), 20)
        self.assertEqual(self.window.main_ui.slider_Duration.value(), 0)
        self.assertEqual(self.window.main_ui.label_Start.text(), "00:00:00")
        self.assertEqual(self.window.main_ui.label_End.text(), "00:00:00")

    def test_add_files(self):
        """ Test the files add functions """
        self.window.add_folder(self.folders[0], self.music[:2])
        self.assertIn(self.folders[0], self.window.playlists_folder)
        self.assertIn(self.music[:2], self.window.playlists_media.values())
        self.window.add_songs_new_folder(self.music[2:])
        self.assertIn(self.folders[1], self.window.playlists_folder)
        self.assertIn(self.music[2:], self.window.playlists_media.values())

    def test_volume_slider(self):
        """ Test the volume slider """
        self.window.main_ui.slider_Volume.setValue(50)
        self.assertEqual(self.window.player.volume(), 50)
        self.assertEqual(self.window.main_ui.slider_Volume.toolTip(), "50%")

    def test_track_duration(self):
        """ Test the track duration label """
        self.window.track_duration(226427)
        self.assertEqual(self.window.main_ui.slider_Duration.maximum(), int(226427 / 1000))
        self.assertEqual(self.window.main_ui.label_End.text(), "00:03:46")

    def test_media_position(self):
        """ Test the media rewind slider """
        self.window.main_ui.slider_Duration.setSliderPosition(56)
        self.assertEqual(self.window.player.position(), 56000)
        self.assertEqual(self.window.main_ui.label_Start.text(), "00:00:56")


app = QApplication(sys.argv)

if __name__ == "__main__":
    unittest.main()
