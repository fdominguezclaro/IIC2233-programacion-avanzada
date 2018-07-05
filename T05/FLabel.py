from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class FLabel(QLabel):
    enter = pyqtSignal()
    out = pyqtSignal()

    def __init__(self, parent, objeto=None):
        self.parent = parent
        super().__init__(parent)
        self.enter.connect(objeto.mouse_arriba)
        self.out.connect(objeto.mouse_fuera)

    def enterEvent(self, event):
        self.enter.emit()

    def leaveEvent(self, event):
        self.out.emit()
