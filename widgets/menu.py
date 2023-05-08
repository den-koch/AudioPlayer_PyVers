from PyQt5.QtWidgets import QMenu


class MyMenu(QMenu):

    def add_actions(self):
        self.addAction("New Playlist")
        self.addAction("Files")
        self.addAction("Folder")
        self.setStyleSheet("""
        QMenu {
            color: rgb(180, 180, 180);
            background-color: qlineargradient(spread:pad, x1:0.517, y1:1, x2:0.493, y2:0, 
            stop:0 rgba(49, 49, 49, 207), stop:1 rgba(72, 72, 72, 255)); 
            border: 2px solid rgb(100, 100, 100);}
        QMenu::item:selected { 
            background-color: rgb(80, 80, 80);}
        """)
