# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Menu_principal.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MenuPrincipal(QDialog):
    def setupUi(self, MenuPrincipal):
        MenuPrincipal.setObjectName("MenuPrincipal")
        MenuPrincipal.resize(374, 173)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MenuPrincipal)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.jugar = QtWidgets.QPushButton(MenuPrincipal)
        self.jugar.setObjectName("jugar")
        self.verticalLayout.addWidget(self.jugar)
        self.borrar_hist = QtWidgets.QPushButton(MenuPrincipal)
        self.borrar_hist.setObjectName("borrar_hist")
        self.verticalLayout.addWidget(self.borrar_hist)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(MenuPrincipal)
        QtCore.QMetaObject.connectSlotsByName(MenuPrincipal)

    def retranslateUi(self, MenuPrincipal):
        _translate = QtCore.QCoreApplication.translate
        MenuPrincipal.setWindowTitle(_translate("MenuPrincipal", "Menu Principal"))
        self.jugar.setText(_translate("MenuPrincipal", "Jugar"))
        self.borrar_hist.setText(_translate("MenuPrincipal", "Borrar historial"))
        self.jugar.connect(self.imprimir)

    def imprimir(self):
        print('Hola')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_MenuPrincipal()
    ex.show()
    sys.exit(app.exec())