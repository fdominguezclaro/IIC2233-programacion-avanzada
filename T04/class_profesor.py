import class_persona as cp


class Profesor(cp.Persona):
    """Esta clase representa a un profesor"""

    def __init__(self, nombre, seccion):
        """

        :param nombre: nombre del profesor
        :type nombre: str
        :param seccion: seccion a la que pertenece
        :type seccion: int
        """
        super().__init__(nombre)
        self.seccion = seccion
        self.consultas = 0
        self.controles = {'controles': 0, 'fecha_ultimo_control': None}
