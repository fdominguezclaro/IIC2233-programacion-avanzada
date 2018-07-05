from random import choice, random, uniform, randint

import class_persona as cp
import numpy


class Estudiante(cp.Persona):
    """Esta clase define a un estudiante"""

    def __init__(self, nombre, seccion, escenario):
        """
        :param nombre: nombre del profesor
        :type nombre: str
        
        :param seccion: seccion a la que pertenece
        :type seccion: int
        
        :param escenario: diccionario con toda la informacion del escenario
        :type escenario: dict
        
        """
        super().__init__(nombre)
        self.seccion = seccion
        self.escenario = escenario
        self.personalidad = choice(['eficiente', 'artistico', 'teorico'])
        self.creditos = None
        self.confianza = uniform(int(self.escenario['nivel_inicial_confianza_inferior']),
                                 int(self.escenario['nivel_inicial_confianza_superior']))
        self.tareas = {'oop': [0, 0, 0], 'herencia': [0, 0, 0], 'listas': [0, 0, 0], 'arbol': [0, 0, 0],
                       'funcional': [0, 0, 0],
                       'metaclases': [0, 0, 0], 'simulacion': [0, 0, 0], 'threading': [0, 0, 0], 'gui': [0, 0, 0],
                       'serializacion': [0, 0, 0], 'networking': [0, 0, 0], 'webservices': [0, 0, 0]}
        self.actividades = {'oop': [0, 0], 'herencia': [0, 0], 'listas': [0, 0], 'arbol': [0, 0], 'funcional': [0, 0],
                            'metaclases': [0, 0], 'simulacion': [0, 0], 'threading': [0, 0], 'gui': [0, 0],
                            'serializacion': [0, 0], 'networking': [0, 0], 'webservices': [0, 0]}
        self.controles = {'oop': [0, 0], 'herencia': [0, 0], 'listas': [0, 0], 'arbol': [0, 0], 'funcional': [0, 0],
                          'metaclases': [0, 0], 'simulacion': [0, 0], 'threading': [0, 0], 'gui': [0, 0],
                          'serializacion': [0, 0], 'networking': [0, 0], 'webservices': [0, 0]}
        self.examen = 0
        self.nivel_programacion = 0
        self.horas_dedicadas_semana = 0
        self.habilidades = {'oop': 0, 'herencia': 0, 'listas': 0, 'arbol': 0, 'funcional': 0, 'metaclases': 0,
                            'simulacion': 0, 'threading': 0, 'gui': 0, 'serializacion': 0, 'networking': 0,
                            'webservices': 0}
        self.definir_creditos()
        self.horas_dedicadas_semana = 0
        self.notas = []

    def definir_creditos(self):
        """Esta funcion me define los creditos que tendra el alumno"""
        lista = [40, 50, 55, 60]
        elegido = numpy.random.choice(lista, 1,
                                      p=[self.escenario['prob_40_creditos'], self.escenario['prob_50_creditos'],
                                         self.escenario['prob_55_creditos'], self.escenario['prob_60_creditos']])

        self.creditos = elegido[0]

    def estudiar_ayudantia(self, materia):
        """Mejora el nivel de manejo de contenidos para esa materia
        
        :param materia: materia a estudiar
        :type materia: str
        """

        self.habilidades[materia] += ((5 / 7) * self.horas_dedicadas_semana) * (1 / int(self.escenario[materia]))
        self.tareas[materia][2] += (5 / 7) * self.horas_dedicadas_semana

    def estudiar_catedra(self, materia):
        """Mejora el nivel de manejo de contenidos para una materia
        
        :param materia: materia a estudiar
        :type materia: str
        
        """

        self.habilidades[materia] += ((2 / 7) * self.horas_dedicadas_semana) * (1 / int(self.escenario[materia]))
        self.tareas[materia][2] += (5 / 7) * self.horas_dedicadas_semana

    def tip(self, materia):
        """Mejora el nivel de manejo de contenidos para una materia cuando escucha un tip

        :param materia: materia a estudiar
        :type materia: str

        """

        prob = choice([0, 1])
        if prob == 1:
            self.habilidades[materia] *= 1.1

    @staticmethod
    def preguntar():
        """Dice si es que va a preguntar en clases

        :return: cantidad de dudas
        :rtype: int
        """

        dudas = int(numpy.random.triangular(1, 3, 10))
        return dudas

    @property
    def promedio_1(self):
        """
        
        :return: promedio de las notas a medio semestre, sin examen
        :rtype: int or float
        """
        # nota_controles
        controles = 0
        contador = 0
        for control in self.controles.values():
            if control[0] == 0:
                break
            else:
                contador += 1
                controles += control[0]
        if contador == 0:
            controles = 1
        else:
            controles = controles / contador

        # Nota actividades
        actividades = 0
        contador = 0
        for actividad in self.actividades.values():
            if actividad[0] == 0:
                break
            else:
                contador += 1
                actividades += actividad[0]
        if contador == 0:
            actividades = 1
        else:
            actividades = actividades / contador

        # Notas Tareas
        tareas = 0
        contador = 0
        for tarea in self.tareas.values():
            if tarea[0] == 0:
                break
            else:
                contador += 1
                tareas += tarea[0]
        if contador == 0:
            tareas = 1
        else:
            tareas = tareas / contador

        return controles * 0.2 + actividades * 0.3 + tareas * 0.5

    @property
    def promedio(self):
        """

        :return: promedio del alumno a fin de semestre
        :rtype: int of float
        """
        # nota_controles
        controles = 0
        contador = 0
        for control in self.controles.values():
            if control[0] == 0:
                break
            else:
                contador += 1
                controles += control[0]
        if contador == 0:
            controles = 1
        else:
            controles = controles / contador

        # Nota actividades
        actividades = 0
        contador = 0
        for actividad in self.actividades.values():
            if actividad[0] == 0:
                break
            else:
                contador += 1
                actividades += actividad[0]
        if contador == 0:
            actividades = 1
        else:
            actividades = actividades / contador

        # Notas Tareas
        tareas = 0
        contador = 0
        for tarea in self.tareas.values():
            if tarea[0] == 0:
                break
            else:
                contador += 1
                tareas += tarea[0]
        if contador == 0:
            tareas = 1
        else:
            tareas = tareas / contador

        return controles * 0.2 + actividades * 0.25 + tareas * 0.4 + self.examen * 0.15

    @property
    def consulta(self):
        if self.promedio_1 <= 5:
            self.nivel_programacion *= 1.08
            return True
        else:
            respuesta = numpy.random.choice([True, False], 1, p=[self.escenario['prob_visitar_profesor'], 0.8])
            if respuesta:
                self.nivel_programacion *= 1.08
                return True
            else:
                return False

    def definir_confianza(self, x, y, z, nota_final, nota_esperada):
        """Redefine self.confianza segun los eventos ocurridos
        :param x: 1 si hay actividad, 0 otro caso 
        :type x: integer
        
        :param y: 1 si hay tarea, 0 otro caso 
        :type y: integer
        
        :param z: 1 si hay control, 0 otro caso 
        :type z: integer
        
        :param nota_final: nota_obtenida en evaluacion 
        :type nota_final: integer
        
        :param nota_esperada: nota esperada por el alumno en la evaluacion
        :type nota_esperada: integer
        """

        self.confianza += (3 * x * (nota_final - nota_esperada)) + (5 * y * (nota_final - nota_esperada)) + (
            z * (nota_final - nota_esperada))
        if self.confianza < 0:
            self.confianza = 0

    def nivel_progra(self, n, reunion_profesor, fiesta):
        """Cambia el nivel de programacion del alumno segun los eventos que ocurrieron
        :param n: numero de semanas de la simulacion
        :type n: integer
        
        :param reunion_profesor: True si el alumno se reunio con el profesor esa semana
        :type reunion_profesor: boolean
        
        :param fiesta: True si el alumno fue a una fiesta esa semana
        :type fiesta: boolean"""

        if reunion_profesor:
            v = 0.08
        else:
            v = 0
        if fiesta:
            w = 0.15
        else:
            w = 0

        if n == 1:
            self.nivel_programacion = random(2, 10)
        else:
            self.nivel_programacion = 1.05 * (1 + v - w) * self.nivel_programacion

    def nota_esperada(self, contenido):
        """Me calcula la nota esperada por el alumno segun el contenido correspondiente
        :param contenido: contenido evaluado
        :type contenido: string
        
        :return: nota esperada
        :rtype: integer o float
        """
        if contenido in ['oop']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 2:
                return uniform(11, 39) / 10
            if 3 <= round(self.horas_dedicadas_semana * 0.3) <= 4:
                return uniform(40, 59) / 10
            if 5 <= round(self.horas_dedicadas_semana * 0.3) <= 6:
                return uniform(60, 69) / 10
            if 7 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['herencia']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 3:
                return uniform(11, 39) / 10
            if 4 <= round(self.horas_dedicadas_semana * 0.3) <= 6:
                return uniform(40, 59) / 10
            if 7 == round(self.horas_dedicadas_semana * 0.3):
                return uniform(60, 69) / 10
            if 8 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['listas', 'gui']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 1:
                return uniform(11, 39) / 10
            if 2 <= round(self.horas_dedicadas_semana * 0.3) <= 4:
                return uniform(40, 59) / 10
            if 5 <= round(self.horas_dedicadas_semana * 0.3) <= 6:
                return uniform(60, 69) / 10
            if 7 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['arbol', 'threading', 'networking']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 2:
                return uniform(11, 39) / 10
            if 3 <= round(self.horas_dedicadas_semana * 0.3) <= 5:
                return uniform(40, 59) / 10
            if 6 <= round(self.horas_dedicadas_semana * 0.3) <= 7:
                return uniform(60, 69) / 10
            if 8 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['funcional']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 3:
                return uniform(11, 39) / 10
            if 4 <= round(self.horas_dedicadas_semana * 0.3) <= 7:
                return uniform(40, 59) / 10
            if 8 == round(self.horas_dedicadas_semana * 0.3):
                return uniform(60, 69) / 10
            if 9 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['metaclases', 'serializacion']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 4:
                return uniform(11, 39) / 10
            if 5 <= round(self.horas_dedicadas_semana * 0.3) <= 7:
                return uniform(40, 59) / 10
            if 8 <= round(self.horas_dedicadas_semana * 0.3) <= 9:
                return uniform(60, 69) / 10
            if 10 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['simulacion']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 3:
                return uniform(11, 39) / 10
            if 4 <= round(self.horas_dedicadas_semana * 0.3) <= 6:
                return uniform(40, 59) / 10
            if 7 <= round(self.horas_dedicadas_semana * 0.3) <= 8:
                return uniform(60, 69) / 10
            if 9 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

        elif contenido in ['webservices']:
            if 0 <= round(self.horas_dedicadas_semana * 0.3) <= 2:
                return uniform(11, 39) / 10
            if 3 <= round(self.horas_dedicadas_semana * 0.3) <= 7:
                return uniform(40, 59) / 10
            if 8 == round(self.horas_dedicadas_semana * 0.3):
                return uniform(60, 69) / 10
            if 9 <= round(self.horas_dedicadas_semana * 0.3):
                return 7

    def horas_semanales(self):
        """
        Estima cuantas horas va a estudiar esa semana
        """
        if self.creditos == 40:
            self.horas_dedicadas_semana = randint(10, 25)
        elif self.creditos == 50:
            self.horas_dedicadas_semana = randint(10, 15)
        elif self.creditos == 55:
            self.horas_dedicadas_semana = randint(5, 15)
        elif self.creditos == 50:
            self.horas_dedicadas_semana = randint(5, 10)

    def progreso_pep8_actividad(self, materia):
        """
        
        :param materia: materia de la evaluacion
        :type materia: str
        
        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.7 * self.habilidades[materia] + 0.2 * self.nivel_programacion + 0.1 * self.confianza
        return progreso

    def progreso_funcionalidad_actividad(self, materia):
        """

        :param materia: materia de la evaluacion
        :type materia: str

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.3 * self.habilidades[materia] + 0.6 * self.nivel_programacion + 0.1 * self.confianza
        return progreso

    def progreso_contenido_actividad(self, materia):
        """

        :param materia: materia de la evaluacion
        :type materia: str

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.7 * self.habilidades[materia] + 0.2 * self.nivel_programacion + 0.1 * self.confianza
        return progreso

    def progreso_pep8_tarea(self, materia):
        """

        :param materia: materia de la evaluacion
        :type materia: str

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.5 * self.tareas[materia][2] + 0.5 * self.nivel_programacion
        return progreso

    def progreso_contenido_tarea(self, materia, promedio_hab):
        """

        :param materia: materia de la evaluacion
        :type materia: str
        
        :param promedio_hab: habilidad materia de la evaluacion
        :type promedio_hab: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.7 * promedio_hab + 0.2 * self.tareas[materia][2] + 0.1 * self.nivel_programacion
        return progreso

    def progreso_funcionalidad_tarea(self, materia, promedio_hab):
        """
        :param materia: materia de la evaluacion
        :type materia: str
        
        :param promedio_hab: habilidad materia de la evaluacion
        :type promedio_hab: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.5 * promedio_hab + 0.4 * self.tareas[materia][2] + 0.1 * self.nivel_programacion
        return progreso

    def progreso_contenido_control(self, materia):
        """

        :param materia: habilidad materia de la evaluacion
        :type materia: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.7 * self.habilidades[materia] + 0.25 * self.confianza + 0.05 * self.nivel_programacion
        return progreso

    def progreso_funcionalidad_control(self, materia):
        """

        :param materia: habilidad materia de la evaluacion
        :type materia: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.3 * self.habilidades[materia] + 0.5 * self.confianza + 0.2 * self.nivel_programacion
        return progreso

    def progreso_contenido_examen(self, materia):
        """

        :param materia: habilidad materia de la evaluacion
        :type materia: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.5 * self.habilidades[materia] + 0.4 * self.confianza + 0.1 * self.nivel_programacion
        return progreso

    def progreso_funcionalidad_examen(self, materia):
        """

        :param materia: habilidad materia de la evaluacion
        :type materia: int

        :return: progreso pep8 para esa evaluacion
        :rtype: int
        """
        progreso = 0.3 * self.habilidades[materia] + 0.5 * self.confianza + 0.2 * self.nivel_programacion
        return progreso
