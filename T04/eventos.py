from random import randint

from numpy.random import choice


class Catedra:
    """Esta clase representa una catedra"""

    def __init__(self, simulacion, profesor, tiempo_inicio):
        """
        :param simulacion: Objeto de la simulacion
        :type simulacion: class Simulacion
        :param profesor: Profesor del curso
        :type profesor: class Profesor
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la catedra
        :type tiempo_inicio: int
        """
        self.simulacion = simulacion
        self.nombre = 'catedra'
        self.profesor = profesor
        self.seccion = self.profesor.seccion
        self.materia = self.simulacion.materia
        self.tiempo_inicio = tiempo_inicio
        self.alumnos = []
        self.preguntas = 0

        for alumno in self.simulacion.alumnos:
            if alumno.seccion == self.seccion:
                self.alumnos.append(alumno)

    @property
    def hay_control(self):
        """
        Este metodo revisa en el profesor de cada seccion cuantos controles han habido, y cuando fue el ultimo
            
        :return: Retorna True si es que hay control
        :rtype: bool
        """
        prob = randint(1, 2)
        if prob == 2:
            if self.profesor.controles['controles'] == 0:
                for profesor in self.simulacion.profesores:
                    profesor.controles['controles'] += 1
                    profesor.controles['fecha_ultimo_control'] = self.simulacion.semana
                return True
            else:
                if self.profesor.controles['controles'] < 5 and (
                            self.profesor.controles['fecha_ultimo_control'] + 1) < self.simulacion.semana:
                    for profesor in self.simulacion.profesores:
                        profesor.controles['controles'] += 1
                        profesor.controles['fecha_ultimo_control'] = self.simulacion.semana
                    return True


class ProfesorConsultas:
    """Esta clase representa recibir consultas del profesor"""

    def __init__(self, simulacion, profesor, tiempo_inicio):
        """
        
        :param simulacion: Objeto de la simulacion
        :type simulacion: class Simulacion
        :param profesor: Profesor que resuelve la duda
        :type profesor: class Profesor
        :param alumno: Alumno que efectua la consulta
        :type alumno: list
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la consulta
        :type tiempo_inicio: int
        """
        self.nombre = 'consultas'
        self.profesor = profesor
        self.materia = simulacion.materia
        self.tiempo_inicio = tiempo_inicio


class Ayudantia:
    """Esta clase representa una ayudantia"""

    def __init__(self, simulacion, tiempo_inicio):
        """
        
        :param simulacion: Objeto de la simulacion
        :type simulacion: class Simulacion
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la ayudantia
        :type tiempo_inicio: int
        """
        self.simulacion = simulacion
        self.nombre = 'ayudantia'
        ayudantes = choice(simulacion.ayudantes_d, 2, False)
        self.ayudante1 = ayudantes[0]
        self.ayudante2 = ayudantes[1]
        self.materia = self.simulacion.materia
        self.tiempo_inicio = tiempo_inicio

        mitad = int(len(simulacion.alumnos) / 2)
        self.alumnos1 = simulacion.alumnos[:mitad]
        self.alumnos2 = simulacion.alumnos[mitad + 1:]
        self.subir()

    def subir(self):
        if self.materia in self.ayudante1.materias:
            for alumno in self.alumnos1:
                alumno.habilidades[self.materia] *= 1.1
        if self.materia in self.ayudante2.materias:
            for alumno in self.alumnos2:
                alumno.habilidades[self.materia] *= 1.1


class Tarea:
    """Esta clase representa una tarea"""

    def __init__(self, tiempo_inicio, progreso_min, materia):
        """
        
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la Tarea
        :type tiempo_inicio: int
        
        :param progreso_min: Progreso necesario para obtener el 7
        :type progreso_min: int or float
        
        :param materia: materia de la tarea
        :type materia: str
        """
        self.nombre = 'tarea'
        self.materia = materia
        self.tiempo_inicio = tiempo_inicio
        self.progreso_min = progreso_min


class Actividad:
    """Esta clase representa una actividad"""

    def __init__(self, tiempo_inicio, progreso_min, materia):
        """

        :param tiempo_inicio: Tiempo de simulacion en que se efectua la actividad
        :type tiempo_inicio: int

        :param progreso_min: Progreso necesario para obtener el 7
        :type progreso_min: int
        
        :param materia: materia de la tarea
        :type materia: str
        """
        self.nombre = 'actividad'
        self.tiempo_inicio = tiempo_inicio
        self.progreso_min = progreso_min
        self.materia = materia


class SubirNotas:
    """Esta clase representa la accion subir notas"""

    def __init__(self, tiempo_inicio, tipo, materia):
        """

        :param tiempo_inicio: Tiempo de simulacion en que se suben las clases
        :type tiempo_inicio: int
        
        :param tipo: Tipo de evaluacion
        :type tipo: str
        
        :param materia: Materia de la evaluacion
        :type materia: str
        
        """
        self.tipo = tipo
        self.materia = materia
        self.nombre = 'subirnotas'
        self.tiempo_inicio = tiempo_inicio
        self.duracion = 0


class ReunionDocencia:
    """Esta clase representa una reunion de docencia"""

    def __init__(self, simulacion, tiempo_inicio):
        """

        :param simulacion: Objeto de la simulacion
        :type simulacion: class Simulacion
        
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la Tarea
        :type tiempo_inicio: int
        """
        self.simulacion = simulacion
        self.nombre = 'reuniondocencia'
        self.tiempo_inicio = tiempo_inicio
        self.materia = ''


class ReunionTarea:
    """Esta clase representa una reunion de docencia"""

    def __init__(self, simulacion, tiempo_inicio):
        """

        :param simulacion: Objeto de la simulacion
        :type simulacion: class Simulacion
        
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la Tarea
        :type tiempo_inicio: int
        """

        self.simulacion = simulacion
        self.nombre = 'reuniontarea'
        self.tiempo_inicio = tiempo_inicio
        self.materia = ''


class Examen:
    """Esta clase representa un examen"""

    def __init__(self, simulacion, tiempo_inicio, materias):
        """

        :param simulacion: Objeto simulacion
        :param tiempo_inicio: Tiempo de simulacion en que se efectua el Examen
        :type tiempo_inicio: int
        """

        self.materia = ''
        self.simulacion = simulacion
        self.nombre = 'examen'
        self.tiempo_inicio = tiempo_inicio
        self.duracion = 0
        self.materias = materias


class Fiesta:
    """Esta clase representa a una fiesta"""

    def __init__(self, tiempo_inicio):
        """
        
        :param tiempo_inicio: Tiempo de simulacion en que se efectua la Fiesta
        :type tiempo_inicio: int
        """
        self.nombre = 'fiesta'
        self.tiempo_inicio = tiempo_inicio
        self.duracion = 0
        self.materia = ''


class Partido:
    """Esta clase representa a una fiesta"""

    def __init__(self, tiempo_inicio):
        """

        :param tiempo_inicio: Tiempo de simulacion en que se efectua la Partido
        :type tiempo_inicio: int
        """
        self.nombre = 'partido'
        self.tiempo_inicio = tiempo_inicio
        self.duracion = 0
        self.materia = ''


class CorteAgua:
    """Esta clase representa a una fiesta"""

    def __init__(self, tiempo_inicio):
        """

        :param tiempo_inicio: Tiempo de simulacion en que se efectua el corte de agua
        :type tiempo_inicio: int
        """
        self.nombre = 'corte_agua'
        self.tiempo_inicio = tiempo_inicio
        self.duracion = 0
        self.materia = ''
