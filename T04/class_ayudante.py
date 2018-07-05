from random import sample

import class_persona as cp


class AyudanteDocencia(cp.Persona):
    """Esta clase representa a un ayudante de docencia"""

    def __init__(self, nombre):
        """
        
        :param nombre: nombre del ayudante
        :type nombre: str
        """
        super().__init__(nombre)
        self.materias = sample(
            ['oop', 'herencia', 'listas', 'arbol', 'funcinal', 'metaclases', 'simulacion', 'threading', 'gui',
             'serializacion', 'networking', 'webservices'], 3)
        self.dudas_respondidas = 0


class AyudanteTareo(cp.Persona):
    """Esta clase representa a un ayudante de tareas"""

    def __init__(self, nombre):
        """

        :param nombre: nombre del ayudante
        :type nombre: str
        """
        super().__init__(nombre)


class AyudanteCoordinador(cp.Persona):
    """Esta clase representa al ayudante coordinador (Mavrakis en este caso)"""

    def __init__(self, nombre):
        """

        :param nombre: nombre del ayudante
        :type nombre: str
        """
        super().__init__(nombre)
