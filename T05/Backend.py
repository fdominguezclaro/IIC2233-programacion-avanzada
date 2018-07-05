import os
import random
from math import sqrt, atan, degrees, sin, cos

import Buildings
import Champions
import FLabel
import Subdito
import funciones
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QProgressBar, QLabel

constantes = funciones.leer_constantes()


class Compra:
    def __init__(self, habilidad, valor):
        self.habilidad = habilidad
        self.valor = valor


class Move:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class SendLabel:
    def __init__(self, label, objeto):
        self.label = label
        self.objeto = objeto


class WeakSubdito(QObject):
    mover = pyqtSignal(Move)
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, team, posx, posy):
        super().__init__()
        self.team = team
        self.subdito = Subdito.WeakSubdito(team, constantes)
        self.subdito_label = FLabel.FLabel(parent, self)
        self.subdito_label.setGeometry(30, 30, 30, 30)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/subditos/1')
        self.pixmap = self.pixmap.scaled(30, 30)
        self.subdito_label.setPixmap(self.pixmap)
        self.subdito_label.setStyleSheet('background:transparent')
        self.subdito_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.muerto.connect(parent.sumar_puntos)
        self.position = [posx, posy]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)
        self.estado_caminar = 1
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(50)
        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(posx, posy - 7, 40, 9)
        self.pbar.setValue(self.subdito.health_bar)
        self.pbar.show()
        self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))

    def actualizar_vida(self):
        self.pbar.setValue(self.subdito.health_bar)
        if self.subdito.health <= 0:
            self.subdito_label.close()
            self.pbar.close()
            self.muerto.emit('weak')

    def run(self):
        if self.team == 1:
            self.position[0] = self.subdito_label.x() + self.subdito.speed
            self.position[1] = self.subdito_label.y() + self.subdito.speed
            self.caminar()
            self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))
        else:
            self.position[0] = self.subdito_label.x() - self.subdito.speed
            self.position[1] = self.subdito_label.y() - self.subdito.speed
            self.caminar()
            self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))

        self.pbar.move(self.subdito_label.x(), self.subdito_label.y() - 7)

    def caminar(self):
        string = '/uis/Sprites/subditos/' + str(self.estado_caminar)
        pixmap = QPixmap(os.getcwd() + string)
        pixmap = pixmap.scaled(40, 40)
        self.subdito_label.setPixmap(pixmap)
        self.estado_caminar += 1
        if self.estado_caminar == 4:
            self.estado_caminar = 1

        self.pbar.move(self.subdito_label.x(), self.subdito_label.y() - 7)

    def mouse_arriba(self):
        self.mouse_arriba_senal.emit(SendLabel(self.subdito_label, self.subdito_label))

    def mouse_fuera(self):
        self.mouse_fuera_senal.emit(SendLabel(False, False))


class StrongSubdito(QObject):
    mover = pyqtSignal(Move)
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, team, posx, posy):
        super().__init__()
        self.team = team
        self.subdito = Subdito.StrongSubdito(team, constantes)
        self.subdito_label = FLabel.FLabel(parent, self)
        self.subdito_label.setGeometry(posx, posy, 35, 35)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/subditos/1')
        self.pixmap = self.pixmap.scaled(35, 35)
        self.subdito_label.setPixmap(self.pixmap)
        self.subdito_label.setStyleSheet('background:transparent')
        self.subdito_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.muerto.connect(parent.sumar_puntos)
        self.position = [posx, posy]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000)
        self.estado_caminar = 1
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(50)
        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(posx, posy - 7, 40, 9)
        self.pbar.setValue(self.subdito.health_bar)
        self.pbar.show()
        self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))

    def actualizar_vida(self):
        self.pbar.setValue(self.subdito.health_bar)
        if self.subdito.health <= 0:
            self.subdito_label.close()
            self.pbar.close()
            self.muerto.emit('strong')

    def run(self):
        if self.team == 1:
            self.position[0] = self.subdito_label.x() + self.subdito.speed
            self.position[1] = self.subdito_label.y() + self.subdito.speed
            self.caminar()
            self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))
        else:
            self.position[0] = self.subdito_label.x() - self.subdito.speed
            self.position[1] = self.subdito_label.y() - self.subdito.speed
            self.caminar()
            self.mover.emit(Move(self.subdito_label, self.position[0], self.position[1]))

        self.pbar.move(self.subdito_label.x(), self.subdito_label.y() - 7)

    def mouse_arriba(self):
        self.mouse_arriba_senal.emit(SendLabel(self.subdito_label, self.subdito_label))

    def mouse_fuera(self):
        self.mouse_fuera_senal.emit(SendLabel(False, False))

    def caminar(self):
        string = '/uis/Sprites/subditos/' + str(self.estado_caminar)
        pixmap = QPixmap(os.getcwd() + string)
        pixmap = pixmap.scaled(40, 40)
        self.subdito_label.setPixmap(pixmap)
        self.estado_caminar += 1
        if self.estado_caminar == 4:
            self.estado_caminar = 1

        self.pbar.move(self.subdito_label.x(), self.subdito_label.y() - 7)


class Character(QObject):
    mover = pyqtSignal(Move)
    att_image = pyqtSignal(Move)
    look_mouse = pyqtSignal()
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    mostrar_tienda = pyqtSignal()

    def __init__(self, parent, champion):
        super().__init__()

        self.nombre = champion
        if champion == 'arthas':
            self.champion = Champions.Arthas(2, constantes)
        elif champion == 'chau':
            self.champion = Champions.Chau(2, constantes)
        elif champion == 'hernan':
            self.champion = Champions.Hernan(2, constantes)

        self.jugador_label = QLabel(parent)
        self.jugador_label.setGeometry(40, 40, 40, 40)
        self.pixmap = QPixmap('uis/Sprites/' + str(self.nombre) + '/1.png')
        self.pixmap = self.pixmap.scaled(40, 40)
        self.jugador_label.setPixmap(self.pixmap)

        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(900, 600, 40, 9)
        self.pbar.setValue(self.champion.health_bar)

        self.jugador_label.setStyleSheet('background:transparent')
        self.jugador_label.setVisible(True)
        self.jugador_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.att_image.connect(parent.actualizar_imagen)
        self.look_mouse.connect(parent.actualizar_imagen)
        self.position = [900, 600]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(10)
        self.mover.emit(Move(self.jugador_label, self.position[0], self.position[1]))
        self.estado_caminar = 1
        self.estado_atacar = 1
        self.target = SendLabel(False, False)
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(50)
        self.angulo = 0

    def actualizar_vida(self):
        self.pbar.setValue(self.champion.health_bar)
        if self.champion.health <= 0:
            self.jugador_label.close()
            self.pbar.close()

    def set_target(self, targ):
        self.target = targ

    def mouse_arriba(self):
        pass

    def mouse_fuera(self):
        pass

    @staticmethod
    def distance(x1, y1, x2, y2):
        dist = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        return dist

    def attack(self):
        if self.target.objeto:

            if self.target.objeto.nombre == 'shop':
                self.mostrar_tienda.emit()
            else:
                if self.target.label and self.target.objeto.team != 2:

                    # Ahora tengo que ver si alguna de las esquinas entre ambos objetos estan en rango de ataquedd
                    # (hipotenusa de un triangulo)
                    # Ademas tome en cuenta la distancia de los puntos medios de los lados de cada uno

                    d1 = self.distance(self.jugador_label.x() + self.jugador_label.width(),
                                       self.jugador_label.y() + self.jugador_label.height(), self.target.label.x(),
                                       self.target.label.y())
                    d2 = self.distance(self.jugador_label.x(), self.jugador_label.y() + self.jugador_label.height(),
                                       self.target.label.x() + self.target.label.width(), self.target.label.y())
                    d3 = self.distance(self.jugador_label.x() + self.jugador_label.width(), self.jugador_label.y(),
                                       self.target.label.x(), self.target.label.y() + self.target.label.height())
                    d4 = self.distance(self.jugador_label.x(), self.jugador_label.y(),
                                       self.target.label.x() + self.target.label.width(),
                                       self.target.label.y() + self.target.label.height())

                    d5 = self.distance(self.jugador_label.x() + (self.jugador_label.width() / 2),
                                       self.jugador_label.y() + self.jugador_label.height(),
                                       self.target.label.x() + (self.target.label.width() / 2), self.target.label.y())
                    d6 = self.distance(self.jugador_label.x() + self.jugador_label.width(),
                                       self.jugador_label.y() + (self.jugador_label.height() / 2),
                                       self.target.label.x(),
                                       self.target.label.y() + (self.target.label.height() / 2))
                    d7 = self.distance(self.jugador_label.x() + (self.jugador_label.width() / 2),
                                       self.jugador_label.y(),
                                       self.target.label.x() + (self.target.label.width() / 2),
                                       self.target.label.y() + self.target.label.height())
                    d8 = self.distance(self.jugador_label.x(),
                                       self.jugador_label.y() + (self.jugador_label.height() / 2),
                                       self.target.label.x() + self.target.label.width(),
                                       self.target.label.y() + (self.target.label.height()) / 2)

                    if d1 <= self.champion.att_range or d2 <= self.champion.att_range or d3 <= self.champion.att_range \
                            or d4 <= self.champion.att_range or d5 <= self.champion.att_range or d6 <= self.champion. \
                            att_range or d7 <= self.champion.att_range or d8 <= self.champion.att_range:
                        self.target.objeto.health -= self.champion.strengh

                        string = '/uis/Sprites/' + str(self.nombre) + '/att' + str(self.estado_atacar)
                        pixmap = QPixmap(os.getcwd() + string)
                        pixmap = pixmap.scaled(40, 40)
                        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angulo))
                        self.jugador_label.setPixmap(pixmap)
                        self.estado_atacar += 1
                        if self.estado_atacar == 4:
                            self.estado_atacar = 1

                        self.att_image.emit(Move(self.jugador_label, self.jugador_label.x(), self.jugador_label.y()))

    def upgrade(self, compra):
        if compra.habilidad == 'frostmourne':
            self.champion.strengh += compra.valor
        if compra.habilidad == 'ballesta':
            self.champion.att_range += compra.valor
        if compra.habilidad == 'boots':
            self.champion.speed += compra.valor
        if compra.habilidad == 'objeto':
            self.champion.poder += compra.valor
        if compra.habilidad == 'armadura':
            self.champion.att_speed += compra.valor
        if compra.habilidad == 'carta':
            habilidad = random.choice(['frostmourne', 'ballesta', 'boots', 'objeto', 'armadura'])
            self.upgrade(Compra(habilidad, compra.valor))

    def run(self):
        pass

    def caminar(self):
        string = '/uis/Sprites/' + str(self.nombre) + '/' + str(self.estado_caminar)
        pixmap = QPixmap(os.getcwd() + string)
        pixmap = pixmap.scaled(40, 40)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angulo))
        self.jugador_label.setPixmap(pixmap)
        self.estado_caminar += 1
        if self.estado_caminar == 4:
            self.estado_caminar = 1

        self.pbar.move(self.jugador_label.x(), self.jugador_label.y() - 7)

    def move_left(self):
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x() - (self.champion.speed * cos(self.angulo)),
                             self.jugador_label.y() + (self.champion.speed * sin(self.angulo))))
        self.caminar()

    def move_right(self):
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x() + (self.champion.speed * cos(self.angulo)),
                             self.jugador_label.y() - (self.champion.speed * sin(self.angulo))))
        self.caminar()

    def move_front(self):
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x() + (self.champion.speed * cos(self.angulo)),
                             self.jugador_label.y() + (self.champion.speed * sin(self.angulo))))
        self.caminar()

    def move_back(self):
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x() - (self.champion.speed * cos(self.angulo)),
                             self.jugador_label.y() - (self.champion.speed * sin(self.angulo))))
        self.caminar()

    def look(self, mouse):
        distx = mouse.x - self.jugador_label.x()
        disty = mouse.y - self.jugador_label.y()

        try:
            self.angulo = degrees(atan(disty / distx))
        except:
            pass

        if distx < 0:
            self.angulo += 180

        if distx > 0 > disty:
            self.angulo += 360

        self.rota()

    def rota(self):
        string = '/uis/Sprites/' + str(self.nombre) + '/' + str(self.estado_caminar)
        pixmap = QPixmap(os.getcwd() + string)
        pixmap = pixmap.scaled(40, 40)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angulo))
        self.jugador_label.setPixmap(pixmap)
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x(), self.jugador_label.y()))


class ChampionEnemigo(QObject):
    mover = pyqtSignal(Move)
    att_image = pyqtSignal(Move)
    look_mouse = pyqtSignal()
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, champion):
        super().__init__()

        self.nombre = champion
        if champion == 'arthas':
            self.champion = Champions.Arthas(2, constantes)
        elif champion == 'chau':
            self.champion = Champions.Chau(2, constantes)
        elif champion == 'hernan':
            self.champion = Champions.Hernan(2, constantes)

        self.jugador_label = QLabel(parent)
        self.jugador_label.setGeometry(40, 40, 40, 40)
        self.pixmap = QPixmap('uis/Sprites/' + str(self.nombre) + '/1.png')
        self.pixmap = self.pixmap.scaled(40, 40)
        self.jugador_label.setPixmap(self.pixmap)

        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(40, 37, 40, 9)
        self.pbar.setValue(self.champion.health_bar)

        self.jugador_label.setStyleSheet('background:transparent')
        self.jugador_label.setVisible(True)
        self.jugador_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.muerto.connect(parent.sumar_puntos)
        self.att_image.connect(parent.actualizar_imagen)
        self.look_mouse.connect(parent.actualizar_imagen)
        self.position = [40, 40]
        self.mover.emit(Move(self.jugador_label, self.jugador_label.x(), self.jugador_label.y()))
        self.estado_caminar = 1
        self.estado_atacar = 1
        self.target = SendLabel(False, False)
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(50)
        self.angulo = 0

    def actualizar_vida(self):
        self.pbar.setValue(self.champion.health_bar)
        if self.champion.health <= 0:
            self.jugador_label.close()
            self.pbar.close()
            self.muerto.emit('champion')

    def set_target(self, targ):
        self.target = targ

    def mouse_arriba(self):
        pass

    def mouse_fuera(self):
        pass

    @staticmethod
    def distance(x1, y1, x2, y2):
        dist = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        return dist

    def attack(self):
        if self.target.objeto:

            if self.target.objeto.nombre == 'shop':
                self.mostrar_tienda.emit()
            else:
                if self.target.label and self.target.objeto.team != 2:

                    # Ahora tengo que ver si alguna de las esquinas entre ambos objetos estan en rango de ataquedd
                    # (hipotenusa de un triangulo)
                    # Ademas tome en cuenta la distancia de los puntos medios de los lados de cada uno

                    d1 = self.distance(self.jugador_label.x() + self.jugador_label.width(),
                                       self.jugador_label.y() + self.jugador_label.height(), self.target.label.x(),
                                       self.target.label.y())
                    d2 = self.distance(self.jugador_label.x(), self.jugador_label.y() + self.jugador_label.height(),
                                       self.target.label.x() + self.target.label.width(), self.target.label.y())
                    d3 = self.distance(self.jugador_label.x() + self.jugador_label.width(), self.jugador_label.y(),
                                       self.target.label.x(), self.target.label.y() + self.target.label.height())
                    d4 = self.distance(self.jugador_label.x(), self.jugador_label.y(),
                                       self.target.label.x() + self.target.label.width(),
                                       self.target.label.y() + self.target.label.height())

                    d5 = self.distance(self.jugador_label.x() + (self.jugador_label.width() / 2),
                                       self.jugador_label.y() + self.jugador_label.height(),
                                       self.target.label.x() + (self.target.label.width() / 2), self.target.label.y())
                    d6 = self.distance(self.jugador_label.x() + self.jugador_label.width(),
                                       self.jugador_label.y() + (self.jugador_label.height() / 2),
                                       self.target.label.x(),
                                       self.target.label.y() + (self.target.label.height() / 2))
                    d7 = self.distance(self.jugador_label.x() + (self.jugador_label.width() / 2),
                                       self.jugador_label.y(),
                                       self.target.label.x() + (self.target.label.width() / 2),
                                       self.target.label.y() + self.target.label.height())
                    d8 = self.distance(self.jugador_label.x(),
                                       self.jugador_label.y() + (self.jugador_label.height() / 2),
                                       self.target.label.x() + self.target.label.width(),
                                       self.target.label.y() + (self.target.label.height()) / 2)

                    if d1 <= self.champion.att_range or d2 <= self.champion.att_range or d3 <= self.champion.att_range \
                            or d4 <= self.champion.att_range or d5 <= self.champion.att_range or d6 <= self.champion. \
                            att_range or d7 <= self.champion.att_range or d8 <= self.champion.att_range:
                        self.target.objeto.health -= self.champion.strengh

                        string = '/uis/Sprites/' + str(self.nombre) + '/att' + str(self.estado_atacar)
                        pixmap = QPixmap(os.getcwd() + string)
                        pixmap = pixmap.scaled(40, 40)
                        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angulo))
                        self.jugador_label.setPixmap(pixmap)
                        self.estado_atacar += 1
                        if self.estado_atacar == 4:
                            self.estado_atacar = 1

                        self.att_image.emit(Move(self.jugador_label, self.jugador_label.x(), self.jugador_label.y()))

    def caminar(self):
        string = '/uis/Sprites/' + str(self.nombre) + '/' + str(self.estado_caminar)
        pixmap = QPixmap(os.getcwd() + string)
        pixmap = pixmap.scaled(40, 40)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angulo))
        self.jugador_label.setPixmap(pixmap)
        self.estado_caminar += 1
        if self.estado_caminar == 4:
            self.estado_caminar = 1

        self.pbar.move(self.jugador_label.x(), self.jugador_label.y() - 7)

    def move_left(self):
        self.position[0] = self.jugador_label.x()
        self.position[1] = self.jugador_label.y()
        self.position[0] -= self.champion.speed
        self.mover.emit(Move(self.jugador_label, self.position[0], self.position[1]))

    def move_right(self):
        self.position[0] = self.jugador_label.x()
        self.position[1] = self.jugador_label.y()
        self.position[0] += self.champion.speed
        self.mover.emit(Move(self.jugador_label, self.position[0], self.position[1]))

    def move_front(self):
        self.position[0] = self.jugador_label.x()
        self.position[1] = self.jugador_label.y()
        self.position[1] -= self.champion.speed
        self.mover.emit(Move(self.jugador_label, self.position[0], self.position[1]))

    def move_back(self):
        self.position[0] = self.jugador_label.x()
        self.position[1] = self.jugador_label.y()
        self.position[1] += self.champion.speed
        self.mover.emit(Move(self.jugador_label, self.position[0], self.position[1]))


class Tower(QObject):
    mover = pyqtSignal(Move)
    attack = pyqtSignal()
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, team, pos):
        super().__init__()
        self.tower_building = Buildings.Tower(pos, team, constantes)
        self.nombre = 'tower'
        self.team = team
        self.tower_label = FLabel.FLabel(parent, self)
        self.tower_label.setGeometry(80, 80, 80, 80)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/buildings/tower.png')
        self.pixmap = self.pixmap.scaled(80, 80)
        self.tower_label.setPixmap(self.pixmap)
        self.tower_label.setStyleSheet('background:transparent')
        self.position = pos
        self.tower_label.setVisible(True)
        self.tower_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.mover.emit(Move(self.tower_label, self.position[0], self.position[1]))
        self.muerto.connect(parent.sumar_puntos)

        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(pos[0] + 9, pos[1] - 5, 70, 9)
        self.pbar.setValue(self.tower_building.health)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(100)

    def run(self):
        self.pbar.setValue(self.tower_building.health_bar)
        if self.tower_building.health <= 0:
            self.tower_label.close()
            self.pbar.close()
            self.muerto.emit('tower')
            # Ahora la torre ataca a la unidad mas cercana
            # No alcanze a hacerlo....

    def mouse_arriba(self):
        self.mouse_arriba_senal.emit(SendLabel(self.tower_label, self.tower_building))

    def mouse_fuera(self):
        self.mouse_fuera_senal.emit(SendLabel(False, False))

    def atacar(self):
        pass


class Nexo(QObject):
    mover = pyqtSignal(Move)
    attack = pyqtSignal()
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, team, pos):
        super().__init__()
        self.nexo_building = Buildings.Nexo(team, constantes)
        self.nombre = 'nexo'
        self.team = team
        self.nexo_label = FLabel.FLabel(parent, self)
        self.nexo_label.setGeometry(80, 80, 80, 80)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/buildings/nexo.png')
        self.pixmap = self.pixmap.scaled(80, 80)
        self.nexo_label.setPixmap(self.pixmap)
        self.nexo_label.setStyleSheet('background:transparent')
        self.position = pos
        self.nexo_label.setVisible(True)
        self.nexo_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.mover.emit(Move(self.nexo_label, self.position[0], self.position[1]))
        self.muerto.connect(parent.sumar_puntos)
        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(pos[0] + 4, pos[1] - 5, 75, 9)
        self.pbar.setValue(self.nexo_building.health_bar)
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(100)

    def actualizar_vida(self):
        self.pbar.setValue(self.nexo_building.health_bar)
        if self.nexo_building.health <= 0:
            self.nexo_label.close()
            self.pbar.close()
            self.muerto.emit('nexo')

    def mouse_arriba(self):
        self.mouse_arriba_senal.emit(SendLabel(self.nexo_label, self.nexo_building))

    def mouse_fuera(self):
        self.mouse_fuera_senal.emit(SendLabel(False, False))


class Inhibidor(QObject):
    mover = pyqtSignal(Move)
    attack = pyqtSignal()
    mouse_arriba_senal = pyqtSignal(SendLabel)
    mouse_fuera_senal = pyqtSignal(SendLabel)
    muerto = pyqtSignal(str)

    def __init__(self, parent, team, pos):
        super().__init__()
        self.inhibidor_building = Buildings.Inhibidor(team, constantes)
        self.nombre = 'inhibidor'
        self.team = team
        self.inhibidor_label = FLabel.FLabel(parent, self)
        self.inhibidor_label.setGeometry(80, 80, 80, 80)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/buildings/inhibidor.png')
        self.pixmap = self.pixmap.scaled(80, 80)
        self.inhibidor_label.setPixmap(self.pixmap)
        self.inhibidor_label.setStyleSheet('background:transparent')
        self.position = pos
        self.inhibidor_label.setVisible(True)
        self.inhibidor_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.mover.emit(Move(self.inhibidor_label, self.position[0], self.position[1]))
        self.muerto.connect(parent.sumar_puntos)
        self.pbar = QProgressBar(parent)
        self.pbar.setGeometry(pos[0] + 9, pos[1] - 5, 70, 9)
        self.pbar.setValue(self.inhibidor_building.health_bar)
        self.lifetimer = QTimer(self)
        self.lifetimer.timeout.connect(self.actualizar_vida)
        self.lifetimer.start(100)

    def actualizar_vida(self):
        self.pbar.setValue(self.inhibidor_building.health_bar)
        if self.inhibidor_building.health <= 0:
            self.inhibidor_label.close()
            self.pbar.close()
            self.muerto.emit('inhibidor')

    def mouse_arriba(self):
        self.mouse_arriba_senal.emit(SendLabel(self.inhibidor_label, self.inhibidor_building))

    def mouse_fuera(self):
        self.mouse_fuera_senal.emit(SendLabel(False, False))


class Tienda(QObject):
    mover = pyqtSignal(Move)
    mouse_arriba_tienda_senal = pyqtSignal(SendLabel)
    mouse_fuera_tienda_senal = pyqtSignal(SendLabel)

    def __init__(self, parent, pos):
        super().__init__()
        self.shop_building = Buildings.Shop(pos, constantes)
        self.nombre = 'tower'
        self.shop_label = FLabel.FLabel(parent, self)
        self.shop_label.setGeometry(80, 80, 80, 80)
        self.pixmap = QPixmap(os.getcwd() + '/uis/Sprites/buildings/tienda.png')
        self.pixmap = self.pixmap.scaled(80, 80)
        self.shop_label.setPixmap(self.pixmap)
        self.shop_label.setStyleSheet('background:transparent')
        self.position = pos
        self.shop_label.setVisible(True)
        self.shop_label.show()
        self.mover.connect(parent.actualizar_imagen)
        self.mover.emit(Move(self.shop_label, self.position[0], self.position[1]))

    def mouse_arriba(self):
        self.mouse_arriba_tienda_senal.emit(SendLabel(self.shop_label, self.shop_building))

    def mouse_fuera(self):
        self.mouse_fuera_tienda_senal.emit(SendLabel(False, False))
