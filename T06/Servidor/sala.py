import time
from random import shuffle
from threading import Thread


class Sala:
    """
    Esta clase va a ser una sala, cada una es un thread para que se puedan reproducir individualmente
    """

    def __init__(self, genero, canciones):
        self.genero = genero
        self.canciones = canciones
        self.timer = 20
        self.respuestas = []
        self.buenas = 0
        self.malas = 0
        # Pongo a sonar la primera cancion al principio
        self.cancion_actual = self.canciones[self.genero][0]
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):

        while True:
            time.sleep(1)
            self.timer -= 1

            if self.timer <= 0:
                self.timer = 20

                # Borro las respuestas
                self.respuestas = []
                shuffle(self.canciones[self.genero])
                self.cancion_actual = self.canciones[self.genero][0]
