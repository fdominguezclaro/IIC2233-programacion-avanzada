import os
import pickle
import socket
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QObject


class Client(QObject):
    loggin_back = pyqtSignal(list)
    imprimeprueba = pyqtSignal(list)
    manda_canciones = pyqtSignal(dict)
    cancion_sonando = pyqtSignal(dict)
    actualiza_puntos = pyqtSignal()
    ocupado = pyqtSignal(str)
    actualiza_respuestas = pyqtSignal(list)
    chat = pyqtSignal(list)
    puntajes = pyqtSignal(list)

    def __init__(self, parent, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()
        self.name = None
        self.loggin_back.connect(parent.revisar_usuario)
        self.imprimeprueba.connect(parent.imprimeprueba)
        self.manda_canciones.connect(parent.recibir_canciones)
        self.cancion_sonando.connect(parent.cancion_sonando)
        self.puntajes.connect(parent.puntajes_lista)
        self.ocupado.connect(parent.ocupado)
        self.actualiza_respuestas.connect(parent.actualiza_respuestas)
        self.puntos = 0
        self.actualiza_puntos.connect(parent.actualiza_puntos)
        self.chat.connect(parent.chat_1)

        # Compruebo si existe el directorio songs
        if not os.path.exists('Songs'):
            # Creo el directorio
            os.makedirs('Songs')

    def start(self):
        self.connect_to_server()
        self.listen()

    def terminar(self):
        """

        Mando senal de temrminar el thread en el server
        """
        self.send(['terminar', self.name])

    def connect_to_server(self):
        """
        El método connnect_to_server() creará la conexión al servidor.
        """
        self.socket_client.connect((self.host, self.port))

        print("Cliente conectado exitosamente al servidor...")

    def listen(self):
        """
        El método listen() inicilizará el thread que escuchará los mensajes del servidor.
        """
        listen_thread = Thread(target=self.listen_thread, daemon=True)
        listen_thread.start()

    def listen_thread(self):
        """
        La función listen_thread() será lanzada como thread el cual se encarga de escuchar al servidor.
        """
        while True:
            response_bytes_length = self.socket_client.recv(4)
            response_length = int.from_bytes(response_bytes_length, byteorder="big")
            response = b""

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            while len(response) < response_length:
                response += self.socket_client.recv(8388608)

            try:
                resp = pickle.loads(response)

            except EOFError as err:
                print('Desconectado... ', err)

            if resp[0] == 'cancion':

                for cancion in resp[1]:
                    with open('Songs/' + cancion[0], 'wb') as s:
                        s.write(cancion[1])

                self.send(['listo'])

            if resp[0] == 'loggin':
                if resp[2] == -1:
                    self.puntos = 0
                    self.name = resp[1]
                    self.loggin_back.emit([self.name, -1])

                else:
                    self.puntos = int(resp[2])
                    self.name = resp[1]
                    self.loggin_back.emit([self.name, self.puntos])

            if resp[0] == 'usuario ocupado':
                self.ocupado.emit(resp[1])

            if resp[0] == 'lista canciones':
                self.canciones = resp[1]
                self.manda_canciones.emit(self.canciones)

            if resp[0] == 'canciones actuales':
                self.canciones_actuales = resp[1]
                self.cancion_sonando.emit(self.canciones_actuales)

            if resp[0] == 'actualizar respuestas':
                self.actualiza_respuestas.emit(resp[1])

            if resp[0] == 'puntajes':
                self.puntajes.emit(resp[1:])

            if resp[0] == 'chat':
                self.chat.emit(resp)

    def send(self, message):
        """
        El método send() enviará mensajes al servidor
        """

        msg_bytes = pickle.dumps(message)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.socket_client.sendall(msg_length)
        self.socket_client.sendall(msg_bytes)

    def loggin(self, usuario):
        self.usuario = usuario
        self.send(['loggin', self.usuario])

    def suma_puntos(self, lista):
        self.puntos += ((20 - lista[0]) * 100)
        self.actualiza_puntos.emit()
        self.send(['buena', self.name, self.puntos, lista[1], lista[0]])


if __name__ == "__main__":
    client = Client()
