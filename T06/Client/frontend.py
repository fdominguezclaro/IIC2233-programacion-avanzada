import os
import random
from functools import partial

import client
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QListWidgetItem

interfaz = uic.loadUiType('interfaz.ui')


class MainWindow(interfaz[0], interfaz[1]):
    loggin = pyqtSignal(str)
    send = pyqtSignal(list)
    puntos = pyqtSignal(list)
    terminar = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.setupUi(self)
        self.canciones = {}
        self.genero_actual = ''
        self.client = client.Client(self, host, port)
        self.ingresar.clicked.connect(self.ingresar_user)
        self.terminar.connect(self.client.terminar)
        self.puntos.connect(self.client.suma_puntos)
        self.puntajes_b.clicked.connect(self.puntajes_ver)
        self.volver.clicked.connect(self.vermenu_principal)
        self.texto_send.clicked.connect(self.send_chat)
        self.indice_actual = 0
        self.timer = 20
        self.response_time = 0
        self.cancion_actual = ['', '']
        self.botones_opciones_list = [self.boton_op1, self.boton_op2, self.boton_op3, self.boton_op4]
        self.cancion = None
        self.loggin.connect(self.client.loggin)
        self.b_salir_sala.clicked.connect(self.salir_sala)
        self.send.connect(self.client.send)
        self.botones = {}
        self.labels = {}
        self.insala = False
        self.play = False

        # Para hacer solo una vez click
        self.click = True
        self.cancion_op1 = ''
        self.cancion_op2 = ''
        self.cancion_op3 = ''
        self.cancion_op4 = ''

        self.correct = []
        self.wrong = []

        self.initGui()

    def initGui(self):
        self.stackedWidget.setCurrentIndex(0)
        self.boton_op1.clicked.connect(partial(self.botones_opciones, 0))
        self.boton_op2.clicked.connect(partial(self.botones_opciones, 1))
        self.boton_op3.clicked.connect(partial(self.botones_opciones, 2))
        self.boton_op4.clicked.connect(partial(self.botones_opciones, 3))

        # Tiempo que se demora en adivinar
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.tiempo_respuesta)
        self.qtimer.start(1000)

        self.show()

    @staticmethod
    def boton_salas(boton):
        print('el boton ' + boton.text + ' hizo click')

    def setindex(self, index):
        self.indice_actual = index
        if index == 1:
            self.mostrar_botones()

        else:
            self.esconder_botones()
        self.stackedWidget.setCurrentIndex(self.indice_actual)

    def ingresar_user(self):
        if self.lineedit_enter_user.text() is not None:
            self.loggin.emit(self.lineedit_enter_user.text())

    def ocupado(self, usuario):
        QMessageBox.information(self, '', 'Este usuario ya esta conectado: ' + usuario)

    def revisar_usuario(self, lista_usuario):
        self.label_puntos = lista_usuario[1]
        if lista_usuario[1] == -1:
            self.label_puntos = 0
            QMessageBox.information(self, '', 'Usuario creado: ' + lista_usuario[0] + ', bienvenido')
        else:
            QMessageBox.information(self, '', 'Bienvenido de nuevo: ' + lista_usuario[0])

        self.nombre_usuario_ms.setText('Nombre usuario: ' + lista_usuario[0])
        self.nombre_usuario_ms_2.setText('Puntos: ' + str(self.client.puntos))
        self.nombre_usuario_s.setText('Nombre usuario: ' + lista_usuario[0])
        self.nombre_usuario_s_2.setText('Puntos: ' + str(self.client.puntos))

        self.setindex(1)

    def imprimeprueba(self, list):
        print(list)

    def ingresar_sala(self, genero):
        # self.esconder_botones()
        self.pedir_canciones(genero)

        # Seteo en que genero de sala esta
        self.insala = True
        self.click = True
        self.genero_actual = genero
        self.actualizar_botones_sala(genero)
        self.setindex(2)

        # reseteo el tiempo de respuesta
        self.response_time = 0

        self.label_sala.setText(genero)

    def salir_sala(self):
        self.insala = False
        self.timer = 0
        self.play = True
        self.chat.clear()
        self.cancion.stop()
        self.setindex(1)

    def pedir_canciones(self, genero):
        """
        Esta funcion pide las canciones que no tiene al servidor
        """

        lista_canciones = os.listdir('Songs/')
        if 'Icon\r' in lista_canciones:
            lista_canciones.remove('Icon\r')
        self.send.emit(['pedir canciones', genero, lista_canciones])

    def actualizar_botones_sala(self, genero):

        """
        Actualiza los botones de las distintas opciones

        """
        artistas = []
        for cancion in self.canciones[genero]:
            separado = cancion.split(' - ')
            artistas.append(separado)
        random.shuffle(artistas)

        self.boton_op1.setText(artistas[0][0])
        self.boton_op2.setText(artistas[1][0])
        self.boton_op3.setText(artistas[2][0])
        self.boton_op4.setText(artistas[3][0])
        self.cancion_op1 = artistas[0][1]
        self.cancion_op2 = artistas[1][1]
        self.cancion_op3 = artistas[2][1]
        self.cancion_op4 = artistas[3][1]

    def recibir_canciones(self, diccionario):
        """
        cuando se instancia el client, este recibe los nombre de las canciones del server, y manda una senal para aqui,
        asi el frontend guarda las canciones en un diccionario
        """
        self.canciones = diccionario
        self.crear_botones_salas()

    def crear_botones_salas(self):
        """
        Creo los botones y labels respectivos de cada sala. Trate de meterlos en un V y H layout, pero como es una
        pagina del stacked widget no me resulto, entonces tuve que agregarlos a mano y luego cerrarlos y abrirlos
        manualmente
        """
        posv = 120
        for genero in self.canciones.keys():
            label = QLabel(self)
            label.setText('artistas')
            label.setGeometry(150, posv, 400, 20)

            boton = QPushButton(self)
            boton.setText('artistas boton')
            boton.setGeometry(10, posv, 100, 20)
            boton.clicked.connect(partial(self.ingresar_sala, genero))

            self.labels[genero] = label
            self.botones[genero] = boton

            posv += 50

    def cancion_sonando(self, canciones_sonando):
        """
        Esta funcion se va actualizando cada cierto rato para ir poniendo play a la cancion correspondiente. Para esto
        compara la cancion que esta sonando actualmente en la sala y la compara con self.cancion_actual
        :param canciones_sonando: dict
        """

        if self.insala:

            if self.timer == 0:
                self.cancion.stop()

            if self.cancion_actual[0] != canciones_sonando[self.genero_actual][0]:
                self.respuestas.clear()
                self.click = True
                if self.cancion is not None:
                    self.cancion.stop()

                # Reseteo el response time
                self.response_time = 0

                self.cancion_actual = canciones_sonando[self.genero_actual]

                # Tiempo que le queda a la cancion

                self.timer = canciones_sonando[self.genero_actual][1]
                self.cancion = QSound('Songs/' + self.cancion_actual[0], self)
                self.cancion.play()
                self.play = False

            else:
                # Esta parte lo puse porque fue la unica manera que encontre de arreglar cuando se ingresa a la misma
                # sala de manera seguida, por lo que estaba sonando la misma cancion
                if self.play:
                    self.cancion.play()
                    self.play = False

            self.timer = canciones_sonando[self.genero_actual][1]
            self.tiempo_restante.setText('Tiempo restante: ' + str(self.timer))

    def botones_opciones(self, numero_boton):
        """
        Esta funcion recibe la respuesta del usuario, recibiendo ademas el artista que fue seleccionado.
        """

        if self.click:
            self.mala = True
            if numero_boton == 0:
                if self.cancion_op1 == self.cancion_actual[0].split(' - ')[1]:
                    self.mala = False
                    self.puntos.emit([self.response_time, self.genero_actual])

            elif numero_boton == 1:
                if self.cancion_op2 == self.cancion_actual[0].split(' - ')[1]:
                    self.mala = False
                    self.puntos.emit([self.response_time, self.genero_actual])

            elif numero_boton == 2:
                if self.cancion_op3 == self.cancion_actual[0].split(' - ')[1]:
                    self.mala = False
                    self.puntos.emit([self.response_time, self.genero_actual])

            elif numero_boton == 3:
                if self.cancion_op4 == self.cancion_actual[0].split(' - ')[1]:
                    self.mala = False
                    self.puntos.emit([self.response_time, self.genero_actual])

            if self.mala:
                self.send.emit(['mala', self.client.name, self.client.puntos, self.genero_actual, self.response_time])
                self.mala = True

        self.click = False

    def mostrar_botones(self):

        for genero in self.canciones.keys():
            artistas = self.get_artistas(genero)
            self.labels[genero].setText(artistas[0] + ' // ' + artistas[1])
            self.labels[genero].show()
            self.botones[genero].setText(genero)
            self.botones[genero].show()

    def esconder_botones(self):
        for genero in self.canciones.keys():
            self.labels[genero].hide()
            self.botones[genero].hide()

    def actualiza_puntos(self):
        self.nombre_usuario_ms_2.setText('Puntos: ' + str(self.client.puntos))
        self.nombre_usuario_s_2.setText('Puntos: ' + str(self.client.puntos))

    def get_artistas(self, genero):
        artista = self.canciones[genero]
        artistas = []
        for nombre in artista:
            nombre_artista = nombre.split('-')[0]
            artistas.append(nombre_artista)
        return artistas

    def tiempo_respuesta(self):
        if self.response_time >= 20:
            self.response_time = 0

        self.response_time += 1

    def puntajes_ver(self):
        self.setindex(3)
        self.send.emit(['puntajes'])

    def vermenu_principal(self):
        self.setindex(1)

    def puntajes_lista(self, lista):
        """

        Actualizo el Qlistwidget de los puntajes de jugadores
        """
        diccionario = lista[0]
        puntajes = []
        for usuario in diccionario.keys():
            puntajes.append([usuario, diccionario[usuario]])

        puntajes = sorted(puntajes, key=lambda x: int(x[1]), reverse=True)

        for puntos in puntajes:
            item = QListWidgetItem(puntos[0] + ': ' + str(puntos[1]))
            self.rank_jugadores.addItem(item)

        buenas = sorted(lista[1], key=lambda x: int(x[1]), reverse=True)
        malas = sorted(lista[2], key=lambda x: int(x[1]), reverse=True)

        sala = buenas[0]
        sala1 = malas[0]

        self.rank_aciertos.setText(str(sala[0] + ': ' + str(sala[1])))

        self.rank_aciertosmalos.setText(str(sala1[0] + ': ' + str(sala1[1])))

    def actualiza_respuestas(self, lista):
        aprobados = []
        reprobados = []
        for usuario in lista:
            if usuario[0] == 'buena':
                aprobados.append([usuario[1], usuario[4]])
            elif usuario[0] == 'mala':
                reprobados.append([usuario[1]])

        aprobados = sorted(aprobados, key=lambda x: x[1], reverse=True)

        item = QListWidgetItem('Respuestas correctas:')
        self.respuestas.addItem(item)
        for usuario in aprobados:
            item = QListWidgetItem(usuario[0] + ': ' + str(usuario[1]))
            self.respuestas.addItem(item)

        item = QListWidgetItem('Reprobados:')
        self.respuestas.addItem(item)
        for usuario in reprobados:
            item = QListWidgetItem(usuario[0])
            self.respuestas.addItem(item)

    def send_chat(self):
        chat2 = self.texto.text()
        user = self.client.name
        self.send.emit(['chat', user, chat2, self.genero_actual])

    def chat_1(self, lista):
        user = lista[1]
        chat3 = lista[2]
        genero = lista[3]

        if genero == self.genero_actual:
            item = QListWidgetItem(user + ': ' + chat3)
            self.chat.addItem(item)
            self.texto.setText('')

    def closeEvent(self, event):
        self.terminar.emit()
        event.accept()
