import sys
from math import ceil, sqrt
from random import choice

import Backend
from PyQt5 import QtCore
from PyQt5 import uic, Qt
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog


class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Compra:
    def __init__(self, habilidad, valor):
        self.habilidad = habilidad
        self.valor = valor


class Attack:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Estas clases del principio son solo los uis cargadaos para usarlos en el MainWindow
class ChooseChampion(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/ChooseChampion.ui", self)


class Shop(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Shop.ui", self)


class Pausa(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Pausa.ui", self)


class MainMenu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/MainMenu.ui", self)


class MainWindow(QMainWindow):
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    move_up = pyqtSignal()
    move_down = pyqtSignal()
    mouse = pyqtSignal(Mouse)
    attack = pyqtSignal()
    comprar = pyqtSignal(Compra)

    def __init__(self):
        super().__init__()
        uic.loadUi("uis/MainWindow.ui", self)
        self.pausa = False
        self.subditos = []
        self.menu = self.menuBar().addMenu('Menu')
        self.pausa = self.menuBar().addMenu('Pausa')
        self.tienda = self.menuBar().addMenu('Tienda')
        mennu = self.menu.addAction('Menu')
        mennu.triggered.connect(self.initGui)
        pausa = self.pausa.addAction('Pausa')
        pausa.triggered.connect(self.pausear)
        tienda = self.tienda.addAction('Tienda')
        tienda.triggered.connect(self.mostrar_tienda)
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.ventanapause = Pausa()
        self.ventanapause.seguirjugando.clicked.connect(self.despausear)
        self.tienda_window = Shop()
        self.tienda_window.frostmourne.clicked.connect(self.comprarfrost)
        self.tienda_window.ballesta.clicked.connect(self.comprarball)
        self.tienda_window.boots.clicked.connect(self.comprarboots)
        self.tienda_window.objeto_magico.clicked.connect(self.comprarobjeto)
        self.tienda_window.armadura.clicked.connect(self.comprararmadura)
        self.tienda_window.carta.clicked.connect(self.comprarcarta)
        self.initGui()

    def initGui(self):
        self.mainmenu = MainMenu()
        self.choose = ChooseChampion()
        self.choose.chau.clicked.connect(self.jugar_chau)
        self.choose.hernan.clicked.connect(self.jugar_hernan)
        self.choose.arthas.clicked.connect(self.jugar_arthas)
        self.mainmenu.jugar.clicked.connect(self.showchoosechampion)
        self.mainmenu.borrar_hist.clicked.connect(self.borrar_historial)
        self.mainmenu.show()

    def start(self, champion):

        self.personalidad = choice(['noob', 'normal', 'ragequitter'])
        self.champion1name = choice(['arthas', 'chau', 'hernan'])
        self.champion = Backend.Character(self, champion)
        self.champion.mostrar_tienda.connect(self.mostrar_tienda)
        self.comprar.connect(self.champion.upgrade)
        self.attack.connect(self.champion.attack)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.aparece_subdito)
        self.timer.start(10000)
        self.act_labels = QTimer(self)
        self.act_labels.timeout.connect(self.actualizar_labels)
        self.act_labels.start(50)
        self.setMouseTracking(True)
        self.choose.hide()

        self.champion1 = Backend.ChampionEnemigo(self, self.champion1name)
        self.tower1 = Backend.Tower(self, 1, [(self.width / 2) - 190, (self.height / 2) - 180])
        self.tower1.mouse_arriba_senal.connect(self.champion.set_target)
        self.tower1.mouse_fuera_senal.connect(self.champion.set_target)
        self.inhibidor1 = Backend.Inhibidor(self, 1, [(self.width / 2) - 340, (self.height / 2) - 240])
        self.inhibidor1.mouse_arriba_senal.connect(self.champion.set_target)
        self.inhibidor1.mouse_fuera_senal.connect(self.champion.set_target)
        self.nexo1 = Backend.Nexo(self, 1, [(self.width / 2) - 510, (self.height / 2) - 330])
        self.nexo1.mouse_arriba_senal.connect(self.champion.set_target)
        self.nexo1.mouse_fuera_senal.connect(self.champion.set_target)

        self.tower2 = Backend.Tower(self, 2, [(self.width / 2) + 110, (self.height / 2)])
        self.tower2.mouse_arriba_senal.connect(self.champion.set_target)
        self.tower2.mouse_fuera_senal.connect(self.champion.set_target)
        self.inhibidor2 = Backend.Inhibidor(self, 2, [(self.width / 2) + 240, (self.height / 2) + 80])
        self.inhibidor2.mouse_arriba_senal.connect(self.champion.set_target)
        self.inhibidor2.mouse_fuera_senal.connect(self.champion.set_target)
        self.nexo2 = Backend.Nexo(self, 2, [(self.width / 2) + 420, (self.height / 2) + 240])
        self.nexo2.mouse_arriba_senal.connect(self.champion.set_target)
        self.nexo2.mouse_fuera_senal.connect(self.champion.set_target)
        self.tienda2 = Backend.Tienda(self, [(self.width / 2) + 460, (self.height / 2) + 150])
        self.tienda2.mouse_arriba_tienda_senal.connect(self.champion.set_target)
        self.tienda2.mouse_fuera_tienda_senal.connect(self.champion.set_target)

        self.move_down.connect(self.champion.move_back)
        self.move_up.connect(self.champion.move_front)
        self.move_right.connect(self.champion.move_right)
        self.move_left.connect(self.champion.move_left)
        self.mouse.connect(self.champion.look)
        self.show()

    def actualizar_labels(self):
        self.speed.setStyleSheet('QLabel { color: red }')
        self.att.setStyleSheet('QLabel { color: red }')
        self.magic.setStyleSheet('QLabel { color: red }')
        self.deff.setStyleSheet('QLabel { color: red }')

        self.speed.setText('speed: ' + str(self.champion.champion.speed))
        self.att.setText('att: ' + str(self.champion.champion.strengh))
        self.magic.setText('magic: ' + str(self.champion.champion.poder))
        self.deff.setText('def: ' + str(self.champion.champion.att_speed))

    def showchoosechampion(self):
        self.choose.show()
        self.mainmenu.hide()

    def jugar_chau(self):
        self.start('chau')

    def jugar_hernan(self):
        self.start('hernan')

    def jugar_arthas(self):
        self.start('arthas')

    def mostrar_tienda(self):

        distancia1 = sqrt(((self.champion.jugador_label.x() + self.champion.jugador_label.width() -
                            self.tienda2.shop_label.x()) ** 2) + ((self.champion.jugador_label.y() +
                                                                   self.champion.jugador_label.height() -
                                                                   self.tienda2.shop_label.y()) ** 2))
        distancia2 = sqrt(((self.champion.jugador_label.x() - self.tienda2.shop_label.x() -
                            self.tienda2.shop_label.width()) ** 2) + ((self.champion.jugador_label.y() +
                                                                       self.champion.jugador_label.height() -
                                                                       self.tienda2.shop_label.y()) ** 2))
        distancia3 = sqrt(((self.champion.jugador_label.x() + self.champion.jugador_label.width() -
                            self.tienda2.shop_label.x()) ** 2) + ((self.champion.jugador_label.y() -
                                                                   self.tienda2.shop_label.y()) ** 2))
        distancia4 = sqrt(((self.champion.jugador_label.x() - self.tienda2.shop_label.x() -
                            self.tienda2.shop_label.width()) ** 2) + ((self.champion.jugador_label.y() -
                                                                       self.tienda2.shop_label.y() -
                                                                       self.tienda2.shop_label.height()) ** 2))

        if distancia1 <= 50 or distancia2 <= 50 or distancia3 <= 50 or distancia4 <= 50:
            self.tienda_window.frostmourne_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.froustmourne_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.froustmourne_upgrade))
            self.tienda_window.ballesta_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.ballesta_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.ballesta_upgrade))
            self.tienda_window.boots_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.boots_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.boots_upgrade))
            self.tienda_window.objeto_magico_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.objeto_magico_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.objeto_magico_upgrade))
            self.tienda_window.armadura_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.armadura_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.armadura_upgrade))
            self.tienda_window.carta_label.setText(
                'Precio: ' + str(self.tienda2.shop_building.carta_cost) + '\nUpgrade: ' + str(
                    self.tienda2.shop_building.carta_upgrade))
            self.tienda_window.puntos.setText('Puntos disponibles: ' + str(self.champion.champion.puntos))
            self.tienda_window.show()

    def comprarfrost(self):
        """
        Esta funcion se activa al comprar frostmourne de la tienda, le manda una senal a champion para que actualice sus
         atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos.
        """
        self.comprar.emit(Compra('frostmourne', self.tienda2.shop_building.froustmourne_upgrade))
        self.tienda2.shop_building.froustmourne_cost += int(self.tienda2.shop_building.froustmourne_cost / 2)
        self.tienda2.shop_building.froustmourne_upgrade += ceil(0.1 * self.tienda2.shop_building.froustmourne_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def comprarball(self):
        """
        Esta funcion se activa al comprar ballesta de la tienda , le manda una senal a champion para que actualice sus
         atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos.
        """
        self.comprar.emit(Compra('ballesta', self.tienda2.shop_building.ballesta_upgrade))
        self.tienda2.shop_building.ballesta_cost += int(self.tienda2.shop_building.ballesta_cost / 2)
        self.tienda2.shop_building.ballesta_upgrade += ceil(0.1 * self.tienda2.shop_building.ballesta_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def comprarboots(self):
        """
        Esta funcion se activa al comprar boots de la tienda , le manda una senal a champion para que actualice sus
         atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos.
        """
        self.comprar.emit(Compra('boots', self.tienda2.shop_building.boots_upgrade))
        self.tienda2.shop_building.boots_cost += int(self.tienda2.shop_building.boots_cost / 2)
        self.tienda2.shop_building.boots_upgrade += ceil(0.1 * self.tienda2.shop_building.boots_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def comprarobjeto(self):
        """
        Esta funcion se activa al comprar objeto_magico de la tienda, le manda una senal a champion para que actualice 
        sus atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos. 
        """
        self.comprar.emit(Compra('objeto', self.tienda2.shop_building.objeto_magico_upgrade))
        self.tienda2.shop_building.objeto_magico_cost += int(self.tienda2.shop_building.objeto_magico_cost / 2)
        self.tienda2.shop_building.objeto_magico_upgrade += ceil(0.1 * self.tienda2.shop_building.objeto_magico_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def comprararmadura(self):
        """
        Esta funcion se activa al comprar armadura de la tienda, le manda una senal a champion para que actualice sus
         atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos. 
        """
        self.comprar.emit(Compra('armadura', self.tienda2.shop_building.armadura_upgrade))
        self.tienda2.shop_building.armadura_cost += int(self.tienda2.shop_building.armadura_cost / 2)
        self.tienda2.shop_building.armadura_upgrade += ceil(0.1 * self.tienda2.shop_building.armadura_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def comprarcarta(self):
        """
        Esta funcion se activa al comprar carta de la tienda, le manda una senal a champion para que actualice sus
         atributos, y luego muestea de nuevo la tienda con el nuevo precio de los objetos. 
        """
        self.comprar.emit(Compra('carta', self.tienda2.shop_building.carta_upgrade))
        self.tienda2.shop_building.carta_cost += int(self.tienda2.shop_building.carta_cost / 2)
        self.tienda2.shop_building.carta_upgrade += ceil(0.1 * self.tienda2.shop_building.carta_upgrade)
        self.tienda_window.close()
        self.mostrar_tienda()

    def aparece_subdito(self):
        # Aparecen subditos pero solo caminan, si quieren pongan un return antes de la funcion para que no funcione
        self.subdito1 = Backend.WeakSubdito(self, 1, 30, 80)
        self.subditos.append(self.subdito1)
        self.subdito5 = Backend.StrongSubdito(self, 1, 100, 120)
        self.subditos.append(self.subdito5)

        self.subdito11 = Backend.WeakSubdito(self, 2, 980, 580)
        self.subditos.append(self.subdito11)
        self.subdito55 = Backend.StrongSubdito(self, 2, 1035, 580)
        self.subditos.append(self.subdito55)

    def pausear(self):
        if self.pausa:
            self.pausa = False
            self.ventanapause.show()
        else:
            self.pausa = True

    def despausear(self):
        self.pause = False
        self.ventanapause.close()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Qt.Key_P:
            self.pausear()

        if self.pausa:
            if key == Qt.Qt.Key_W:
                self.move_up.emit()
            if key == Qt.Qt.Key_S:
                self.move_down.emit()
            if key == Qt.Qt.Key_A:
                self.move_left.emit()
            if key == Qt.Qt.Key_D:
                self.move_right.emit()

    def setMouseTracking(self, flag):
        """
        Esta funcion es para hacer que todos los objetos tengan activado el mousetracking...
        la saque de https://stackoverflow.com/questions/25368295/qwidgetmousemoveevent-not-firing-when-
        cursor-over-child-widget"""

        def recursion(padre):
            for hijo in padre.findChildren(QtCore.QObject):
                try:
                    hijo.setMouseTracking(flag)
                except:
                    pass
                recursion(hijo)

        QMainWindow.setMouseTracking(self, flag)
        recursion(self)

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        self.mouse.emit(Mouse(x, y))

    def sumar_puntos(self, tipo):
        if tipo == 'weak':
            self.champion.champion.puntos += 1
        if tipo == 'strongh':
            self.champion.champion.puntos += 5
        if tipo == 'tower' or tipo == 'inhibidor':
            self.champion.champion.puntos += 15

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.attack.emit()

    @staticmethod
    def borrar_historial():
        with open('partidas_guardadas.txt', 'w'):
            pass

    @staticmethod
    def actualizar_imagen(move):
        lab = move.label
        lab.move(move.x, move.y)

        if move.label.x() < 0:
            lab.move(0, move.label.y())

        if move.label.x() > 1135:
            lab.move(1135, move.label.y())

        if move.label.y() < 10:
            lab.move(10, move.label.y())

        if move.label.y() > 700:
            lab.move(700, move.label.y())


if __name__ == "__main__":
    def hook(tipo, traceback):
        print(tipo)
        print(traceback)


    sys.__excepthook__ = hook

    app = QApplication(sys.argv)
    menu = MainWindow()
    sys.exit(app.exec())
