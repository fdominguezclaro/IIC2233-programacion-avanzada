#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from math import floor
from random import randint, shuffle, expovariate

import class_ayudante as ca
import class_estudiante as ce
import class_profesor as cpro
import eventos as ev
import funciones as f
import matplotlib.pyplot as plt


class Simulacion:
    """Esta es la clase para la simulacion"""

    def __init__(self):
        self.tiempo = 0
        self.dia_semana = 0
        self.examen = False
        self.alumnos = []
        self.alumnos_iniciales = 0
        self.botaron_ramo = []
        self.ayudantes_d = []
        self.ayudantes_t = []
        self.ayudantes_c = []
        self.profesores = []
        self.controles = []
        self.tareas = 0
        self.master_list = None
        self.evento_no_programado = False
        self.parametros_defecto = f.leer_parametros()
        self.escenario = {}
        self.lista_materias = ['', 'oop', 'herencia', 'listas', 'arbol', 'funcional', 'metaclases', 'simulacion',
                               'threading', 'gui', 'serializacion', 'networking', 'webservices']
        self.promedio_semestral = {'oop': [], 'herencia': [], 'listas': [], 'arbol': [], 'funcional': [],
                                   'metaclases': [],
                                   'simulacion': [], 'threading': [], 'gui': [], 'serializacion': [], 'networking': [],
                                   'webservices': []}

        self.estadisticas_aprobaron = []
        self.promedio_confianza_iniciales = 0
        self.catedra = False
        self.consultas = False

    @property
    def semana(self):
        """
        
        :return: numero de semana actual
        :rtype: int
        """
        semana = floor(self.tiempo / 7) + 1
        return int(semana)

    @property
    def materia(self):
        """
        :return: materia de la semana
        :rtype: str
        """
        if self.semana > 12:
            return 'webservices'
        else:
            return self.lista_materias[self.semana]

    @property
    def materia_siguiente(self):
        """
        :return: materia de la semana siguiente
        :rtype: str
        """
        if self.semana > 12:
            return 'webservices'
        else:
            return self.lista_materias[self.semana + 1]

    @property
    def materia_anterior(self):
        """
        :return: materia de la semana anterio
        :rtype: str
        """
        if self.semana > 13:
            return 'webservices'
        else:
            return self.lista_materias[self.semana - 1]

    @staticmethod
    def progreso_act_tarea(funcionalidad, contenido, pep8):
        """
        
        :param funcionalidad: progreso de funcionalidad
        :type funcionalidad: int or float
        :param contenido: progreso de contenido
        :type contenido: int or float
        :param pep8: progreso pep8
        :type pep8: int or float
        
        :return: progreso total tarea
        :rtype: int or float
        """
        progreso = 0.4 * funcionalidad + 0.4 * contenido + 0.2 * pep8
        return progreso

    @staticmethod
    def progreso_control_examen(funcionalidad, contenido):
        """

        :param funcionalidad: progreso de funcionalidad
        :type funcionalidad: int or float
        :param contenido: progreso de contenido
        :type contenido: int or float

        :return: progreso total evaluacion
        :rtype: int or float
        """
        progreso = 0.3 * funcionalidad + 0.7 * contenido
        return progreso

    def progreso_min_actividad(self):
        """
        
        :return: progreso minimo establecido para esa evaluacion 
        :rtype: int
        """
        progreso = 7 + (randint(1, 5) / int(self.escenario[self.materia]))
        return progreso

    def progreso_min_tarea(self):
        """

        :return: progreso minimo establecido para esa evaluacion 
        :rtype: float
        """

        promedio = (int(self.escenario[self.materia]) + int(self.escenario[self.materia_siguiente])) / 2
        progreso = (7 + (randint(1, 5)) / promedio)
        return progreso

    def elegir(self):
        """Elige que se quiere hacer en el programa"""
        while True:
            opciones = [1, 2]
            while True:
                respuesta = input(
                    'Elige una opcion:\n1. Correr una simulacion con valores por defecto?\n2. Comparar los resultados '
                    'de los distintos escenarios?\n')
                if respuesta.isdigit():
                    respuesta = int(respuesta)
                if respuesta not in opciones:
                    print('ingresa una opcion correcta')
                else:
                    break
            if respuesta == 1:
                self.run('defecto')

            else:
                self.run('.')
            seguir = input('\n\n\n1. Hacer otra consulta\n2. Salir del programa')
            if seguir.isdigit():
                if int(seguir) == 2:
                    sys.exit()

    def poblar(self, escenario):
        """Metodo que me pobla la simulacion. Ademas, guardo la cantidad de alumnos para usarla para las estadisticas
        
        :param escenario: escenario para poblar la simulacion
        :type escenario: dict
        """
        self.escenario = escenario
        header = f.orden('integrantes.csv')
        pos_nombre = header.index('Nombre')
        pos_rol = header.index('Rol')
        pos_seccion = header.index('Sección')

        """Creo las personas con el archivo integrantes.csv"""
        integrantes = f.read_file('integrantes.csv')
        for integrante in integrantes:
            if integrante[pos_rol] == 'Profesor':
                self.profesores.append(cpro.Profesor(integrante[pos_nombre], integrante[pos_seccion]))
            elif integrante[pos_rol] == 'Docencia':
                self.ayudantes_d.append(ca.AyudanteDocencia(integrante[pos_nombre]))
            elif integrante[pos_rol] == 'Tareas':
                self.ayudantes_t.append(ca.AyudanteTareo(integrante[pos_nombre]))
            elif integrante[pos_rol] == 'Coordinación':
                self.ayudantes_c.append(ca.AyudanteCoordinador(integrante[pos_nombre]))
            elif integrante[pos_rol] == 'Alumno':
                self.alumnos.append(
                    ce.Estudiante(integrante[pos_nombre], integrante[pos_seccion], escenario))

        self.alumnos_iniciales = len(self.alumnos)

        # Veo los promedios de confianza iniciales
        self.promedio_confianza_iniciales = [alumno.confianza for alumno in self.alumnos]
        self.promedio_confianza_iniciales = sum(self.promedio_confianza_iniciales) / len(
            self.promedio_confianza_iniciales)

    def elegir_escenario(self, n):
        """Metodo que recorre todos los escenarios
        
        :param n: numero de escenario
        :type n: int
        
        :return: escenario del archivo escenarios.csv
        :rtype: dict
        """
        escenario = f.leer_escenario(f.read_file('escenarios.csv'), n)
        for parametro in escenario:
            if parametro != '-':
                escenario[parametro] = self.parametros_defecto[parametro]

        return escenario

    def run(self, tipo):
        """Esta funcion corre mi funcion simular con los distintos escenarios

        :param tipo: 'nada' si se corre por defecto.
        :type tipo: list or str
        """

        if tipo == '.':
            for n in range(1, len(f.read_file('escenarios.csv')[0])):
                escenario = self.elegir_escenario(n)

                # Si no viene un parametro lo agrego
                for key in self.parametros_defecto.keys():
                    if key not in escenario.keys():
                        escenario[key] = self.parametros_defecto[key]

                self.simular(escenario, '.')
                if self.alumnos != 0:
                    self.estadisticas_aprobaron.append(self.alumnos_iniciales / len(self.alumnos))
                else:
                    self.estadisticas_aprobaron.append(10000)
            max_valor = min(self.estadisticas_aprobaron)
            max_index = self.estadisticas_aprobaron.index(max_valor)
            print('\n\nEl escenario que mas maximizo la aprobacion fue el escenario {}'.format(max_index))

        else:
            escenario = self.parametros_defecto
            self.simular(escenario, 'defecto')
            self.estadisticas()

    def definir_preguntas(self):
        """
        Funcion que define las 8 preguntas del examen, ademas de calcular los promedios para cada materia
        
        :return: lista de materias para preguntas del examen
        :rtype: list
        """
        self.promedio_actividades = {'oop': [], 'herencia': [], 'listas': [], 'arbol': [], 'funcional': [],
                                     'metaclases': [],
                                     'simulacion': [], 'threading': [], 'gui': [], 'serializacion': [],
                                     'networking': [],
                                     'webservices': []}
        self.promedio_controles = {'oop': [], 'herencia': [], 'listas': [], 'arbol': [], 'funcional': [],
                                   'metaclases': [],
                                   'simulacion': [], 'threading': [], 'gui': [], 'serializacion': [], 'networking': [],
                                   'webservices': []}
        self.promedio_tareas = {'oop': [], 'herencia': [], 'listas': [], 'arbol': [], 'funcional': [], 'metaclases': [],
                                'simulacion': [], 'threading': [], 'gui': [], 'serializacion': [], 'networking': [],
                                'webservices': []}

        for alumno in self.alumnos:
            for materia in alumno.actividades.keys():
                self.promedio_actividades[materia].append(alumno.actividades[materia][0])

        for alumno in self.alumnos:
            for materia in alumno.controles.keys():
                if alumno.controles[materia][0] != 0:
                    self.promedio_controles[materia].append(alumno.controles[materia][0])

        for alumno in self.alumnos:
            for materia in alumno.tareas.keys():
                self.promedio_tareas[materia].append(alumno.tareas[materia][0])

        for materia in self.promedio_semestral.keys():
            if len(self.promedio_controles[materia]) > 0:
                promedio = [sum(self.promedio_actividades[materia]) / len(self.promedio_actividades[materia]),
                            sum(self.promedio_controles[materia]) / len(self.promedio_controles[materia]),
                            sum(self.promedio_tareas[materia]) / len(self.promedio_tareas[materia])]
            else:
                promedio = [sum(self.promedio_actividades[materia]) / len(self.promedio_actividades[materia]),
                            sum(self.promedio_tareas[materia]) / len(self.promedio_tareas[materia])]

            self.promedio_semestral[materia] = sum(promedio) / 3

        lista_promedios = [[k, v] for k, v in self.promedio_semestral.items()]
        lista_promedios = sorted(lista_promedios, key=lambda x: x[1], reverse=True)

        lista_materias = []
        lista_materias.append(lista_promedios[0][0])
        lista_materias.append(lista_promedios[1][0])
        lista_materias.append(lista_promedios[-1][0])
        lista_materias.append(lista_promedios[-2][0])
        lista_materias.append(lista_promedios[-3][0])
        lista_materias.append(lista_promedios[-4][0])
        lista_materias.append(lista_promedios[-5][0])
        lista_materias.append(lista_promedios[-6][0])

        return lista_materias

    def estadisticas(self):
        """
        Muestra las estadisticas de la simulacion
        """
        semanas = [dia for dia in range(12)]
        actividades = []
        for materias in self.lista_materias[1:]:
            actividades.append(sum(self.promedio_actividades[materias]) / len(self.promedio_actividades[materias]))

        self.actividades = actividades

        controles = []
        for materias in self.lista_materias[1:]:
            if len(self.promedio_controles[materias]) > 0:
                controles.append(sum(self.promedio_controles[materias]) / len(self.promedio_controles[materias]))
            else:
                controles.append(0)
        self.controles = controles

        tareas = []
        for materias in self.lista_materias[1:]:
            tareas.append(sum(self.promedio_tareas[materias]) / len(self.promedio_tareas[materias]))
        self.tareas = tareas

        self.prom_examen = [alumno.examen for alumno in self.alumnos]
        self.prom_examen = sum(self.prom_examen) / len(self.prom_examen)

        plt.plot(semanas, self.actividades, label='Actividades')
        plt.plot(semanas, self.tareas, label='Tareas')
        plt.plot(semanas, self.controles, label='Controles')
        plt.plot(self.semana, self.examen, label='Examen', markersize=30, color="brown")
        plt.legend()
        plt.ylabel('Notas Promedio')
        plt.xlabel('Semana')
        plt.title('Notas promedio vs semanas')
        plt.show()

        stats = True

        promedio_confianza = [alumno.confianza for alumno in self.alumnos]
        promedio_confianza = sum(promedio_confianza) / len(promedio_confianza)

        print('\n***** Estadisticas *****\n')
        print('\n{} Alumnos botaron el ramo'.format(len(self.botaron_ramo)))
        print('\nConfianza promedio inicial: ', self.promedio_confianza_iniciales)
        print('Confianza promedio final: ', promedio_confianza)

        for key in self.lista_materias[1:]:
            aprobacion_control = 0
            reprobacion_control = 0
            for value in self.promedio_controles[key]:
                if value < 4:
                    reprobacion_control += 1
                else:
                    aprobacion_control += 1
            print('Control de {}, aprobados: %{}  -  reprobados: %{}'.format(key, 100 * aprobacion_control / len(
                self.alumnos), 100 * reprobacion_control / len(self.alumnos)))

        for key in self.lista_materias[1:]:
            aprobacion_actividades = 0
            reprobacion_actividades = 0
            for value in self.promedio_actividades[key]:
                if value < 4:
                    reprobacion_actividades += 1
                else:
                    aprobacion_actividades += 1
            print('Actividad de {}, aprobados: %{}  -  reprobados: %{}'.format(key, 100 * aprobacion_actividades / len(
                self.alumnos), 100 * aprobacion_actividades / len(self.alumnos)))

        for key in self.lista_materias[1:]:
            aprobacion_tareas = 0
            reprobacion_tareas = 0
            for value in self.promedio_actividades[key]:
                if value < 4:
                    reprobacion_tareas += 1
                else:
                    aprobacion_tareas += 1
            print('Tarea de {}, aprobados: %{}  -  reprobados: %{}'.format(key, 100 * aprobacion_tareas / len(
                self.alumnos), 100 * aprobacion_tareas / len(self.alumnos)))

        while stats:
            nombre = input('Ingresa un nombre de alumno para ver estadisticas: ')
            for alumno in self.alumnos:
                if alumno.nombre == nombre:
                    while True:
                        elegir = input('\nQue quieres ver: \n1. Cualidades\n2. Notas')
                        if elegir == '1':
                            print('\nNivel de programacion: {}'.format(alumno.nivel_programacion))
                            print('Confianza: {}'.format(alumno.confianza))
                            print('Contenidos: {}'.format(alumno.habilidades))
                            break
                        elif elegir == '2':
                            print('Notas actividades: ', alumno.actividades)
                            print('Notas controles: ', alumno.controles)
                            print('Notas tareas: ', alumno.tareas)
                            print('Promedio final: ', alumno.promedio)
                            break

            for alumno in self.botaron_ramo:
                if alumno.nombre == nombre:
                    print('\nEste alumno boto el ramo...\n')
                    while True:
                        elegir = input('\nQue quieres ver: \n1. Cualidades\n2. Notas')
                        if elegir == '1':
                            print('\nNivel de programacion: {}'.format(alumno.nivel_programacion))
                            print('Confianza: {}'.format(alumno.confianza))
                            print('Contenidos: {}'.format(alumno.habilidades))
                            break
                        elif elegir == '2':
                            print('Notas actividades: ', alumno.actividades)
                            print('Notas controles: ', alumno.controles)
                            print('Notas tareas: ', alumno.tareas)
                            print('Promedio final: ', alumno.promedio)
                            break

            seguir = input('\n1. Preguntar por otro alumno\n2. Seguir con el programa')
            if seguir == '2':
                stats = False

    def simular(self, escenario, tipo):
        """Esta funcion simula el semestre

        :param escenario: 'nada' si se corre por defecto.
        :type escenario: dict
        :param tipo: tipo de simulacion
        :type tipo: str
        """
        # Reestablesco todos los parametros
        self.tiempo = 0
        self.dia_semana = 0
        self.examen = False
        self.alumnos = []
        self.botaron_ramo = []
        self.ayudantes_d = []
        self.ayudantes_t = []
        self.ayudantes_c = []
        self.profesores = []
        self.controles = []
        self.tareas = 0
        self.master_list = None
        self.master_list = []

        self.poblar(escenario)

        for alumno in self.alumnos:
            alumno.horas_semanales()

        """La simulacion parte un dia viernes"""

        for i in range(len(self.profesores)):
            self.master_list.append(ev.Catedra(self, self.profesores[i], 6))
            self.master_list.append(ev.ProfesorConsultas(self, self.profesores[i], 5))

        self.master_list.append(ev.ReunionDocencia(self, 3))
        self.master_list.append(ev.ReunionTarea(self, 3))
        self.master_list.append(ev.Ayudantia(self, 4))

        self.master_list.append(ev.Fiesta((expovariate(float(self.escenario['fiesta_mes'])))))
        self.master_list.append(ev.Partido((expovariate(float(self.escenario['partido_futbol_mes'])))))
        self.master_list.append(ev.CorteAgua((expovariate(float(self.escenario['corte_agua'])))))

        while not self.examen and len(self.master_list) != 0:
            self.master_list = sorted(self.master_list, key=lambda x: x.tiempo_inicio, reverse=True)
            evento = self.master_list.pop()
            self.tiempo = evento.tiempo_inicio

            if evento.nombre == 'catedra':
                self.evento_no_programado = False
                # Este if es para que se imprima solo una vez la catedra
                if not self.catedra:
                    print('\nHubo catedra de {}'.format(self.materia))
                    print('{} alumnos rindieron una actividad de {}'.format(len(self.alumnos), self.materia))
                    self.catedra = True

                    # Hago el control si es que lo hay
                    if evento.hay_control:
                        print('Hubo un control sorpresa')
                        for alumno in evento.alumnos:
                            progreso = self.progreso_control_examen(alumno.progreso_funcionalidad_control(self.materia),
                                                                    alumno.progreso_contenido_control(self.materia))
                            nota = max((progreso / self.progreso_min_actividad()) * 7, 1)
                            if nota > 7:
                                nota = 7
                            # Se le asigna la nota que tuvo
                            alumno.controles[self.materia][0] = nota
                            # Se espera una nota
                            alumno.controles[self.materia][1] = alumno.nota_esperada(self.materia)
                        self.master_list.append(ev.SubirNotas(self.tiempo + 14, 'control', self.materia))

                # Antes de entrar a la catedra estudian
                for alumno in evento.alumnos:
                    alumno.estudiar_catedra(self.materia)

                if not self.materia == 'webservices' and self.semana < 12:
                    self.master_list.append(ev.Catedra(self, evento.profesor, self.tiempo + 7))

                # Tip del profesor
                for alumno in self.alumnos:
                    alumno.tip(self.materia)

                # Ahora responden dudas
                alumnos_desorden = [alumno for alumno in self.alumnos]
                shuffle(alumnos_desorden)
                for alumno in alumnos_desorden:
                    dudas = alumno.preguntar()
                    if self.consultas + dudas >= 200:
                        break
                    else:
                        alumno.habilidades[self.materia] += (dudas / 10) * alumno.habilidades[self.materia]
                        self.consultas += dudas
                print('Se respondieron: {} dudas'.format(self.consultas))
                self.consultas = 0

                # Ahora hacen la actividad
                for alumno in evento.alumnos:
                    progreso = self.progreso_act_tarea(alumno.progreso_funcionalidad_actividad(self.materia),
                                                       alumno.progreso_contenido_actividad(self.materia),
                                                       alumno.progreso_pep8_actividad(self.materia))
                    nota = max((progreso / self.progreso_min_actividad()) * 7, 1)
                    if nota > 7:
                        nota = 7
                    # Se le asigna la nota que tuvo
                    alumno.actividades[self.materia][0] = nota
                    # Se espera una nota
                    alumno.actividades[self.materia][1] = alumno.nota_esperada(self.materia)
                self.master_list.append(ev.SubirNotas(self.tiempo + 14, 'actividad', self.materia))

                # Calculo las horas que estudiara la semana que viene
                for alumno in self.alumnos:
                    alumno.horas_semanales()

            if evento.nombre == 'ayudantia':
                print('\nSe realizo una ayudantia de {}'.format(self.materia))
                # Antes de entrar a la ayudantia estudian
                for alumno in self.alumnos:
                    alumno.estudiar_catedra(self.materia)
                self.catedra = False
                self.consultas = False
                if not self.materia == 'webservices' and self.semana < 12:
                    self.master_list.append(ev.Ayudantia(self, self.tiempo + 7))

            if evento.nombre == 'reuniondocencia':
                print('\nSe juntaron los ayudantes de docencia')
                if not self.materia == 'webservices' and self.semana < 12:
                    self.master_list.append(ev.ReunionDocencia(self, self.tiempo + 7))

            if evento.nombre == 'reuniontarea':
                # Solo si es en semana impar
                self.tareas += 1
                print('\nSe juntaron los ayudantes de tarea')
                if self.semana < 14:
                    self.master_list.append(
                        ev.Tarea(self.tiempo + 14, self.progreso_min_tarea(), self.materia_siguiente))
                    print('Salio la tarea {}: de {} y {}\n'.format(self.tareas, self.materia, self.materia_siguiente))
                    self.master_list.append(ev.ReunionTarea(self, self.tiempo + 14))

            if evento.nombre == 'tarea':
                print('\n{} alumnos entregan tarea {}'.format(len(self.alumnos), self.tareas - 1))

                for alumno in self.alumnos:
                    promedio = (alumno.habilidades[self.materia] + alumno.habilidades[self.materia_anterior]) / 2
                    progreso = self.progreso_act_tarea(alumno.progreso_funcionalidad_tarea(evento.materia, promedio),
                                                       alumno.progreso_contenido_tarea(evento.materia, promedio),
                                                       alumno.progreso_pep8_tarea(evento.materia))
                    nota = max(progreso / evento.progreso_min * 7, 1)

                    if nota > 7:
                        nota = 7
                    # Se le asigna la nota que tuvo
                    alumno.tareas[evento.materia][0] = nota
                    # Se espera una nota
                    alumno.tareas[evento.materia][1] = alumno.nota_esperada(evento.materia)

                    # Copio esa nota para que las dos materias tengan una nota de tareas
                    alumno.tareas[self.lista_materias[self.lista_materias.index(evento.materia) - 1]][0] = nota
                    alumno.tareas[self.lista_materias[self.lista_materias.index(evento.materia) - 1]][1] = \
                        alumno.tareas[evento.materia][1]
                self.master_list.append(ev.SubirNotas(self.tiempo + 14, evento.nombre, self.materia_anterior))

            if evento.nombre == 'consultas':
                # Ahora hago una consulta
                seccion = [alumno for alumno in self.alumnos if alumno.seccion == evento.profesor.seccion]
                shuffle(seccion)
                consultas_realizadas = 0
                for alumno in seccion:
                    # Ahora hago una consulta
                    if alumno.consulta:
                        consultas_realizadas += 1
                    if consultas_realizadas >= 10:
                        break

                print('\nProfesor {} recibio {} consultas'.format(evento.profesor, consultas_realizadas))
                if not self.materia == 'webservices':
                    self.master_list.append(ev.ProfesorConsultas(self, evento.profesor, self.tiempo + 7))

            if evento.nombre == 'examen':
                print('\nExamen final!!')
                self.examen = True
                self.master_list.append(ev.SubirNotas(self.tiempo + 14, evento.nombre, 'examen'))
                for alumno in self.alumnos:
                    p1 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[0]),
                                                      alumno.progreso_contenido_examen(evento.materias[0]))
                    p2 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[1]),
                                                      alumno.progreso_contenido_examen(evento.materias[1]))
                    p3 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[2]),
                                                      alumno.progreso_contenido_examen(evento.materias[2]))
                    p4 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[3]),
                                                      alumno.progreso_contenido_examen(evento.materias[3]))
                    p5 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[4]),
                                                      alumno.progreso_contenido_examen(evento.materias[4]))
                    p6 = self.progreso_control_examen(alumno.progreso_funcionalidad_examen(evento.materias[5]),
                                                      alumno.progreso_contenido_examen(evento.materias[5]))

                    p1 = max(p1 / int(self.escenario[evento.materias[0]]) * 7, 1)
                    p2 = max(p2 / int(self.escenario[evento.materias[1]]) * 7, 1)
                    p3 = max(p3 / int(self.escenario[evento.materias[2]]) * 7, 1)
                    p4 = max(p4 / int(self.escenario[evento.materias[3]]) * 7, 1)
                    p5 = max(p5 / int(self.escenario[evento.materias[4]]) * 7, 1)
                    p6 = max(p6 / int(self.escenario[evento.materias[5]]) * 7, 1)

                    alumno.examen = (p1 + p2 + p3 + p4 + p5 + p6) / 6

            if evento.nombre == 'subirnotas':
                print('Entregaron notas de: {}'.format(evento.tipo))
                for alumno in self.alumnos:
                    if evento.tipo == 'actividad':
                        nota_esperada = alumno.actividades[evento.materia][1]
                        nota = alumno.actividades[evento.materia][0]
                        alumno.definir_confianza(1, 0, 0, nota, nota_esperada)
                        alumno.notas.append(nota)

                    if evento.tipo == 'tarea':
                        nota_esperada = alumno.tareas[evento.materia][1]
                        nota = alumno.tareas[evento.materia][0]
                        alumno.definir_confianza(0, 1, 0, nota, nota_esperada)
                        alumno.notas.append(nota)

                    if evento.tipo == 'control':
                        nota_esperada = alumno.controles[evento.materia][1]
                        nota = alumno.controles[evento.materia][0]
                        alumno.definir_confianza(0, 0, 1, nota, nota_esperada)
                        alumno.notas.append(nota)

                ex = True
                for evento in self.master_list:
                    if evento.nombre == 'subirnotas':
                        ex = False
                if ex:
                    materias = self.definir_preguntas()
                    self.master_list.append(ev.Examen(self, self.tiempo + 5, materias))

                if evento.materia == 'arbol' and len(self.botaron_ramo) == 0:
                    # Alumnos botan el ramo
                    for alumno in self.alumnos:
                        promedio = sum(alumno.notas) / len(alumno.notas)
                        bota = alumno.confianza * 0.8 + promedio * 0.2
                        if bota < 20:
                            self.botaron_ramo.append(alumno)
                            self.alumnos.remove(alumno)
                    print('{} Botaron el ramo'.format(len(self.botaron_ramo)))

            if evento.nombre == 'fiesta':
                if not self.evento_no_programado:
                    print('\nLos alumnos tuvieron fiesta!!\n')
                    alumnos = [alumno for alumno in self.alumnos]
                    shuffle(alumnos)
                    for alumno in alumnos:
                        alumno.horas_dedicadas_semana *= 0.8
                        alumno.nivel_programacion *= 0.85

                    self.evento_no_programado = True
                self.master_list.append(ev.Fiesta((expovariate(float(self.escenario['fiesta_mes'])))))

            if evento.nombre == 'partido':
                if not self.evento_no_programado:
                    print('\nLos alumnos tuvieron partido!!\n')
                    alumnos = [alumno for alumno in self.alumnos]
                    shuffle(alumnos)
                    partir = floor(len(alumnos) * 0.8)
                    alumnos = alumnos[:partir]
                    for alumno in alumnos:
                        alumno.horas_dedicadas_semana *= 0.9

                    self.evento_no_programado = True
                self.master_list.append(ev.Partido((expovariate(float(self.escenario['fiesta_mes'])))))

            if evento.nombre == 'corte_agua':
                if not self.evento_no_programado:
                    print('\nHubo un corte de agua!!\n')
                    for profesor in self.profesores:
                        profesor.consultas = 4

                    self.evento_no_programado = True
                self.master_list.append(ev.Partido((expovariate(float(self.escenario['fiesta_mes'])))))

        if tipo == 'defecto':
            self.estadisticas()
