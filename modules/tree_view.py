""" Tree view settings"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeView
from main import *


class MyTreeView(QTreeView):

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:
            self.clearSelection()
        else:
            print("left click !")
        QTreeView.mousePressEvent(self, event)
