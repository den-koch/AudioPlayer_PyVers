""" Custom tree view widget"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeView

class MyTreeView(QTreeView):

    def mousePressEvent(self, event):
        """ Mouse press/click events """
        if event.button() == QtCore.Qt.LeftButton:
            self.clearSelection()
        elif event.button() == QtCore.Qt.RightButton:
            index = self.indexAt(event.pos())
            if not index.isValid():
                return
            if index.parent().data() is None:
                self.edit(index)
                self.setCurrentIndex(index)

        QTreeView.mousePressEvent(self, event)
