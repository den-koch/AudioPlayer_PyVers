""" Custom equalizer class """

import random
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5 import QtCore
from PyQt5.Equalizer import EqualizerBar


class MyEqualizer(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3',
                                          '#B02A8F', '#CA4678', '#E06461', '#F1824C',
                                          '#FCA635', '#FCCC25', '#EFF821'])
        self.equalizer.setBackgroundColor("transparent")

        self.grid_layout = QGridLayout(self)
        self.grid_layout.addWidget(self.equalizer)

        self.set_timer = QtCore.QTimer()
        self.set_timer.setInterval(100)
        self.set_timer.timeout.connect(self.update_values)

    def update_values(self):
        """ Equalizer movements """
        self.equalizer.setValues([
            min(100, value + random.randint(0, 50) if random.randint(0, 5) > 2 else value)
            for value in self.equalizer.values()])
