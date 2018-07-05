import os
import pickle
import socket
import time
from threading import Thread, Lock

import sala


class Server:
    """
    Estas primeras funciones las saque de mi actividad y material de clases, por lo que cualquier similitud en estas
    funciones a algun companero se debe a eso.
    """

    def __init__(self, PORT, HOST):
        self.host = HOST
        self.port = PORT
        self.clients = []
        self.users_name = []
        self.salas = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()
        self.usuarios_dic = {}
        self.canciones = {}
        self.canciones_actuales = {}
        self.canciones_archivos = {}
        self.lista_canciones()
        self.mandando = False

    def bind_and_listen(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def lista_canciones(self):
        lista = os.listdir('Canciones/')
        if 'Icon\r' in lista:
            lista.remove('Icon\r')
        for genero in lista[1:]:
            canciones = os.listdir('Canciones/' + genero)
            if 'Icon\r' in canciones:
                canciones.remove('Icon\r')
            self.canciones[genero] = canciones

            # Cargo las canciones a un diccionario para luego enviarlas al cliente.
            for cancion in self.canciones[genero]:
                with open('Canciones/' + genero + '/' + cancion, 'rb') as song:
                    song_arch = song.read()
                    self.canciones_archivos[cancion] = song_arch

            # Creo las distintas salas
            self.salas[genero] = sala.Sala(genero, self.canciones)

    def accept_connections(self):
        thread = Thread(target=self.accept_connections_thread)
        thread.start()
        # thread1 = Thread(target=self.actualizar_thread)
        # thread1.start()

    def accept_connections_thread(self):
        print("Servidor aceptando conexiones...")

        while True:
            client_socket, _ = self.server_socket.accept()
            listening_client_thread = Thread(target=self.listen_client_thread, args=(client_socket,),
                                             daemon=True)
            self.clients.append(client_socket)
            listening_client_thread.start()

    def listen_client_thread(self, client_socket):
        """
        El método listen_client_thread() sera ejecutado como thread que escuchará a un
        cliente en particular.

        """
        print("Servidor conectado a un nuevo cliente...")

        # Le mando el diccionario de los nombres de las canciones
        self.send(['lista canciones', self.canciones], client_socket)

        thread_actualiza = Thread(target=self.actualizar_thread, args=(client_socket,))
        thread_actualiza.start()

        run = True
        while run:
            if run:
                try:
                    response_bytes_length = client_socket.recv(4)
                    response_length = int.from_bytes(response_bytes_length, byteorder="big")
                    response = b""
                except:
                    pass

                while len(response) < response_length:
                    with Lock():

                        response += client_socket.recv(8388608)

                        resp = pickle.loads(response)

                        if resp[0] == 'loggin':
                            self.loggin(client_socket, resp[1])
                            self.users_name.append(resp[1])

                        if resp[0] == 'terminar':
                            self.users_name.remove(resp[1])
                            client_socket.close()
                            run = False

                        if resp[0] == 'puntajes':
                            # Mando los puntajes de todos los jugadores
                            buenas = []
                            malas = []
                            for sala in self.salas.keys():
                                buenas.append([self.salas[sala].genero, self.salas[sala].buenas])
                                malas.append([self.salas[sala].genero, self.salas[sala].malas])

                            self.send(['puntajes', self.usuarios_dic, buenas, malas], client_socket)

                        if resp[0] == 'listo':
                            self.mandando = False

                        if resp[0] == 'buena':
                            # Actualizo los puntos de ese usuario
                            self.usuarios_dic[resp[1]] = resp[2]
                            # A respuestas de la sala le agrego una lista con informacion del usuario
                            self.salas[resp[3]].respuestas.append(['buena', resp[1], resp[2], resp[3], resp[4]])
                            self.salas[resp[3]].buenas += 1
                            # le mando una lista con las respuestas a todos
                            for client in self.clients:
                                self.send(['actualizar respuestas', self.salas[resp[3]].respuestas], client)

                            # Actualizo el archivo que contiene todos los usuarios
                            self.escribir_usuario()

                        if resp[0] == 'mala':
                            # Si respondio mal la pregunta
                            # A respuestas de la sala le agrego una lista con informacion del usuario
                            self.salas[resp[3]].respuestas.append(['mala', resp[1], resp[2], resp[3], resp[4]])
                            self.salas[resp[3]].malas += 1

                            # le mando una lista con las respuestas a todos
                            for client in self.clients:
                                self.send(['actualizar respuestas', self.salas[resp[3]].respuestas], client)

                        if resp[0] == 'chat':
                            for client in self.clients:
                                self.send(resp, client)

                        elif resp[0] == 'pedir canciones':
                            self.mandando = True
                            """
                            Guardo las canciones que tengo en el directorio de ese genero y le mando las que le faltan.
                            """

                            # Guardo las canciones de ese genero
                            canciones = []
                            for song in self.canciones[resp[1]]:
                                canciones.append(song)

                            for cancion in resp[2]:
                                try:
                                    # Elimino la cancion de la lista auxiliar para no enviarsela de nuevo
                                    canciones.remove(cancion)
                                except:
                                    # Muchas veces va a pasar que elimina una cancion que no es de ese genero, por eso el try
                                    pass

                            mandar_canciones = []
                            for cancion in canciones:
                                # Agrego los archivos de canciones a una lista para enviarlos
                                mandar_canciones.append([cancion, self.canciones_archivos[cancion]])

                            # Le mando las canciones que le faltan al cliente.
                            self.send(['cancion', mandar_canciones], client_socket)

    def send(self, message, client):
        """
        El método send() enviará mensajes al cliente
        """
        try:

            with Lock():
                msg_bytes = pickle.dumps(message)
                msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
                client.send(msg_length)
                client.send(msg_bytes)
                time.sleep(0.1)

        except BrokenPipeError as err:
            pass
        except OSError as err:
            print(err)

    def actualizar_thread(self, client_socket):
        """

        Esta funcion le manda los datos al juego para que se vaya actualizando cada cierto tiempo. Esta actualizacion
        incluye que cancion se esta reproduciendo, los puntajes, el tiempo restante, etc...
        """
        run1 = True
        while run1:

            # No pasa nada si el socket esta cerrado
            if client_socket._closed:
                run1 = False
                pass

            try:
                # Para que no se mezcle con otro tipo de envio de datos
                if not self.mandando:
                    # actualizo las canciones actuales que se estan tocando, luego le envio un diccionario con las canciones
                    for genero in self.salas.keys():
                        sala = self.salas[genero]
                        self.canciones_actuales[sala.genero] = [sala.cancion_actual, sala.timer]
                    self.send(['canciones actuales', self.canciones_actuales], client_socket)

            except:
                run1 = False

    def loggin(self, client_socket, usuario):

        if os.path.isfile('usuarios.txt'):
            # Caso en que el archivo existe
            self.leer_usuarios()
            if usuario in self.users_name:
                # Si ya existe un usuario conectado con ese nombre
                self.send(['usuario ocupado', usuario])

            else:
                if usuario in self.usuarios_dic.keys():
                    # Le mando el usuario y los puntos si es que ya existe
                    self.send(['lista canciones', self.canciones], client_socket)
                    puntaje = int(self.usuarios_dic[usuario])
                    mandar = ['loggin', usuario, puntaje]
                    self.send(mandar, client_socket)
                else:
                    # Creo un usuario (el -1 indica que es nuevo)
                    self.send(['lista canciones', self.canciones], client_socket)
                    self.usuarios_dic[usuario] = '0'
                    self.escribir_usuario()
                    self.send(['loggin', usuario, -1], client_socket)

        else:
            # Caso en que no existe el archivo
            self.send(['lista canciones', self.canciones], client_socket)
            self.usuarios_dic[usuario] = '0'
            self.escribir_usuario()
            self.send(['loggin', usuario, -1], client_socket)

    def leer_usuarios(self):
        self.usuarios_dic = {}
        with open('usuarios.txt', 'r') as users:
            for linea in users:
                user = linea.strip().split(',')
                self.usuarios_dic[user[0]] = user[1]

    def escribir_usuario(self):
        with open('usuarios.txt', 'w') as file:
            for user in self.usuarios_dic.keys():
                file.write(str(user) + ',' + str(self.usuarios_dic[user]) + '\n')

    @staticmethod
    def get_path(path):
        abs_path = get_abs_path(path)
        if not os.path.exists(abs_path):
            return -1
        elif not os.path.isdir(abs_path):
            return 0
        else:
            return abs_path

    @staticmethod
    def get_abs_path(path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.abspath(os.sep.join(C_DIR.split(os.sep) + path.split(os.sep)))
