import math
import random

import edd


class Infeccion:
    def __init__(self, tipo):
        self.tipo = str(tipo)
        self.contagiosidad = 0
        self.mortalidad = 0
        self.resistencia = 0
        self.visibilidad = 0
        Infeccion.identificar_tipo(self)

    def identificar_tipo(self):
        if self.tipo == 'Virus':
            self.contagiosidad = 1.5
            self.mortalidad = 1.2
            self.resistencia = 1.5
            self.visibilidad = 0.5

        if self.tipo == 'Bacteria':
            self.contagiosidad = 1.0
            self.mortalidad = 1.0
            self.resistencia = 0.5
            self.visibilidad = 0.7

        if self.tipo == 'Parasito':
            self.contagiosidad = 0.5
            self.mortalidad = 1.5
            self.resistencia = 1.0
            self.visibilidad = 0.45


class Pais:
    def __init__(self, nombre, poblacion_i):
        self.nombre = str(nombre)
        self.poblacion = int(poblacion_i)
        self.poblacion_inicial = int(poblacion_i)
        self.aeropuertos = edd.ListaLigada()
        self.vecinos = edd.ListaLigada()
        self.estado_aeropuertos = True
        self.estado_fronteras = True
        self.gente_infectada = 0
        self.gente_muerta = 0
        self.estado = 'limpio'
        self.mascarillas = False
        self.cura = False
        self.infeccion = False

    def __repr__(self):
        return self.nombre

    def estado_pais(self):
        if self.gente_infectada == 0:
            self.estado = 'limpio'
        if self.gente_infectada != 0:
            self.estado = 'infectado'
        if self.poblacion <= 0:
            self.estado = 'muerto'

    def cerrar_fronteras(self):
        self.estado_fronteras = False

    def cerrar_aeropuertos(self):
        self.estado_aeropuertos = False

    def abrir_fronteras(self):
        self.estado_aeropuertos = True

    def abrir_aeropuertos(self):
        self.estado_aeropuertos = True

    def entregar_mascarillas(self):
        self.mascarillas = True


class Mundo:
    def __init__(self, tipo):
        self.fecha = 0
        self.paises = edd.ListaLigada()
        self.poblacion = 0
        self.poblacion_inicial = 0
        self.prioridades = edd.Queue()
        self.cura = False
        self.progreso_cura = 0
        self.tipo = tipo
        self.infeccion = None
        self.gente_infectada = 0
        self.gente_muerta = 0
        self.gente_sana = 0
        self.diario = edd.ListaLigada()
        #  Para las estadisticas
        self.murio = 0
        self.infecto = 0
        self.llego_infeccion = edd.ListaLigada()
        self.cerro_fronteras = edd.ListaLigada()
        self.cerro_aeropuertos = edd.ListaLigada()
        self.entrego_mascarillas = edd.ListaLigada()

        Mundo.poblar(self)

    def poblar(self):
        #  Veo si se abrio una partida nueva o se eligio cargar una antigua.
        if self.tipo == 'cargar':
            self.cargar_partida()

        else:
            orden = edd.orden_poblacion()
            with open('population.csv', 'r') as f:
                i = 0
                for info in f:
                    if i == 0:
                        i += 1
                        pass
                    else:
                        info = info.strip()
                        pais = edd.ListaLigada(info.split(','))
                        self.paises.append(Pais(pais[orden[0]], pais[orden[1]]))

            orden = edd.orden_random_airports()
            with open('random_airports.csv', 'r') as file:
                i = 0
                for info in file:
                    if i == 0:
                        i += 1
                        pass
                    else:
                        paises = edd.ListaLigada()
                        info = info.strip()
                        pais_separado = edd.ListaLigada(info.split(','))
                        paises.append(pais_separado[int(orden[0])])
                        paises.append(pais_separado[int(orden[1])])
                        for pais in self.paises:
                            if pais.valor.nombre == paises[0]:
                                if not pais.valor.aeropuertos.is_in(paises[1]):
                                    pais.valor.aeropuertos.append(paises[1])
                                for pais_destino in self.paises:
                                    if pais_destino.valor.nombre == paises[1]:
                                        if not pais_destino.valor.aeropuertos.is_in(paises[0]):
                                            pais_destino.valor.aeropuertos.append(paises[0])

            with open('borders.csv', 'r') as file:
                i = 0
                for info in file:
                    if i == 0:
                        i += 1
                        pass
                    else:
                        paises = edd.ListaLigada()
                        info = info.strip()
                        pais_separado = edd.ListaLigada(info.split(';'))
                        paises.append(pais_separado[0])
                        paises.append(pais_separado[1])
                        for pais in self.paises:
                            if pais.valor.nombre == paises[0]:
                                if not pais.valor.vecinos.is_in(paises[1]):
                                    pais.valor.vecinos.append(paises[1])
                                for pais_destino in self.paises:
                                    if pais_destino.valor.nombre == paises[1]:
                                        if not pais_destino.valor.vecinos.is_in(paises[0]):
                                            pais_destino.valor.vecinos.append(paises[0])
            for pais in self.paises:
                self.poblacion += pais.valor.poblacion
            self.poblacion_inicial = self.poblacion

            #  Elige una enfermedad
            while True:
                opcion = str(input('\nElige un tipo de enfermedad para propagar:'
                                   '\n1. Virus\n2. Bacteria\n3. Parasito'))

                opciones = edd.ListaLigada('1', '2', '3')
                if opciones.is_in(opcion):
                    if opcion == '1':
                        self.infeccion = Infeccion('Virus')
                    elif opcion == '2':
                        self.infeccion = Infeccion('Bacteria')
                    elif opcion == '3':
                        self.infeccion = Infeccion('Parasito')
                    break
                else:
                    print('\nIngresa una opcion correcta\n')

            encontrado = True
            while encontrado:
                #  Pone la enfermedad en un pais
                print('\nAhora debes ingresar un pais para partir progagando la enfermedad, aqui '
                      'se muestra la lista de paises posibles:\n')

                for pais in self.paises:
                    print(pais)

                paciente0 = str(input('\nIngresa un pais:'))
                for pais in self.paises:
                    if pais.valor.nombre == paciente0:
                        pais.valor.infeccion = True
                        pais.valor.gente_infectada = 1
                        encontrado = False
                        break
                if encontrado:
                    print('\nIngresa un pais valido')
        Mundo.menu(self)

    def menu(self):
        while True:
            print('\nQue deseas hacer?')
            print('\n1. Pasar de dia')
            print('2. Estadisticas')
            print('3. Guardar estado')
            print('4. Salir al menu')
            opcion = str(input('\nQue deseas hacer: '))
            opciones = edd.ListaLigada('1', '2', '3', '4')
            if opciones.is_in(opcion):
                break
            else:
                print('Ingresa una opcion correcta')

        if opcion == '4':
            Mundo.salir(self)
        elif opcion == '1':
            Mundo.pasar_dia(self)
        elif opcion == '2':
            Mundo.estadisticas(self)
        elif opcion == '3':
            Mundo.guardar_partida(self)

    def pasar_dia(self):
        # Reseteo las estadisticas
        self.murio = 0
        self.infecto = 0
        self.llego_infeccion = edd.ListaLigada()
        self.cerro_fronteras = edd.ListaLigada()
        self.cerro_aeropuertos = edd.ListaLigada()
        self.entrego_mascarillas = edd.ListaLigada()
        self.prioridades = edd.Queue()

        Mundo.descubrir_cura(self)

        for pais in self.paises:
            if pais.valor.poblacion > 0:

                # Propagacion de enfermedad
                #  Veo si tiene las fronteras abiertas
                if pais.valor.estado_fronteras:
                    #  Reviso las fronteras del pais 1
                    for frontera in pais.valor.vecinos:
                        conecciones = 0
                        #  Busco cada frontera en la lista de paises
                        for buscado in self.paises:
                            if str(frontera) == str(buscado.valor.nombre):
                                if buscado.valor.estado_fronteras:
                                    conecciones += 1
                                if (self.gente_infectada / self.poblacion) >= 0.04:
                                    for aeropuerto in pais.valor.aeropuertos:
                                        if str(aeropuerto) == str(buscado.valor.nombre):
                                            if buscado.valor.estado_aeropuertos:
                                                conecciones += 1

                                if conecciones != 0:
                                    if buscado.valor.estado == 'limpio' and buscado.valor.gente_infectada == 0:
                                        contagio = min((7 * self.gente_infectada) / (self.poblacion * conecciones), 1)
                                        #  Metodo para ver aplicar la probabilidad de ocurrencia del suceso
                                        a = random.randint(1, 100)
                                        if a <= (contagio * 100):
                                            buscado.valor.gente_infectada = 1
                                            buscado.valor.estado = 'infectado'
                                            self.llego_infeccion.append(buscado.valor.nombre)

                # Hago lo mismo pero parto desde los aeropuertos
                # Aplico que solo se puede propagar con un 4% de poblacion mundial infectada
                if (self.gente_infectada / self.poblacion) >= 0.04:
                    if pais.valor.estado_aeropuertos:
                        for aeropuerto in pais.valor.aeropuertos:
                            conecciones = 0
                            for buscado in self.paises:
                                if str(aeropuerto) == str(buscado.valor.nombre):
                                    if buscado.valor.estado_aeropuertos:
                                        conecciones += 1
                                    for frontera in pais.valor.vecinos:
                                        if str(frontera) == str(buscado.valor.nombre):
                                            if buscado.valor.estado_fronteras:
                                                conecciones += 1

                                    if conecciones != 0:
                                        if buscado.valor.estado == 'limpio' and buscado.valor.gente_infectada == 0:
                                            contagio = min(
                                                (7 * self.gente_infectada) / (
                                                    self.poblacion * conecciones), 1)
                                            #  Metodo para ver aplicar la probabilidad de ocurrencia del suceso
                                            a = random.randint(1, 100)
                                            if a <= (contagio * 100):
                                                buscado.valor.gente_infectada = 1
                                                buscado.valor.estado = 'infectado'
                                                self.llego_infeccion.append(
                                                    buscado.valor.nombre)

                # Infecto gente
                if pais.valor.mascarillas:
                    infectados = int(math.floor(
                        pais.valor.gente_infectada * random.randint(0, 6) * 0.3 * self.infeccion.contagiosidad))
                    if pais.valor.poblacion >= infectados:
                        pais.valor.gente_infectada += infectados
                        self.infecto += infectados

                    elif infectados >= int(pais.valor.poblacion):
                        pais.valor.gente_infectada = pais.valor.poblacion
                        self.infecto += pais.valor.poblacion

                if not pais.valor.mascarillas:
                    infectados = int(
                        math.floor(pais.valor.gente_infectada * (random.randint(0, 6)) * self.infeccion.contagiosidad))
                    if int(pais.valor.poblacion) >= infectados:
                        pais.valor.gente_infectada += infectados
                        self.infecto += infectados
                    elif infectados > int(pais.valor.poblacion):
                        pais.valor.gente_infectada = pais.valor.poblacion
                        self.infecto += pais.valor.poblacion

                # Muere gente
                muertos = int(math.floor(
                    pais.valor.gente_infectada * min(max(0.2, ((self.fecha ** 2) / 1000)) * self.infeccion.mortalidad,
                                                     1)))
                if int(pais.valor.poblacion) >= muertos:
                    pais.valor.gente_muerta += muertos
                    pais.valor.gente_infectada -= muertos
                    pais.valor.poblacion -= muertos
                    self.poblacion -= muertos
                    self.murio += muertos

                elif muertos > int(pais.valor.poblacion):
                    pais.valor.poblacion = 0
                    pais.valor.gente_infectada = 0
                    self.poblacion -= pais.valor.poblacion
                    self.murio += pais.valor.poblacion

                # Obtengo los datos de gente infectada y muerta
                Mundo.obtener_datos(self)

                #  Entrego la cura
                if self.progreso_cura >= 100:
                    #  Si tiene la cura que la entregue a los aeropuertos
                    if pais.valor.cura:
                        for destino in pais.valor.aeropuertos:
                            #  Veo si el pais de destino tiene la cura
                            for pais_analizar in self.paises:
                                if str(pais_analizar.valor.nombre) == str(destino):
                                    #  Le doy la cura al pais
                                    if not pais_analizar.valor.cura:
                                        pais_analizar.valor.cura = True

                if pais.valor.cura:
                    sanados = int(math.floor(pais.valor.gente_infectada * (0.25 * self.infeccion.resistencia)))
                    pais.valor.gente_infectada -= sanados

                # Obtengo los datos de gente sanada despues de aplicar la cura
                Mundo.obtener_datos(self)

                # Agrego las decisiones a la cola de prioridades
                if pais.valor.poblacion > 0:

                    # Cierro fronteras
                    if pais.valor.estado_fronteras:
                        if ((pais.valor.gente_infectada / pais.valor.poblacion) >= 0.5) or (
                                    pais.valor.gente_muerta / pais.valor.poblacion) >= 0.25:
                            des = edd.ListaLigada()
                            print(des)
                            accion = 0
                            contador = 0
                            for pais1 in pais.valor.vecinos:
                                for buscado in self.paises:
                                    if buscado.valor.poblacion > 0:
                                        if str(buscado.valor.nombre) == str(pais1):
                                            accion += buscado.valor.gente_infectada / buscado.valor.poblacion
                                            contador += 1
                            if contador != 0:
                                prioridad = ((accion / contador) * pais.valor.gente_infectada) / pais.valor.poblacion
                                des.append(pais.valor.nombre, 'cerrar fronteras', prioridad)
                                self.prioridades.enqueue(des)

                    # Cierro aeropuertos
                    if pais.valor.estado_aeropuertos:
                        if ((pais.valor.gente_infectada / pais.valor.poblacion) >= 0.8) or (
                                    pais.valor.gente_muerta / pais.valor.poblacion) >= 0.20:
                            des = edd.ListaLigada()
                            prioridad = (0.8 * pais.valor.gente_infectada) / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'cerrar aeropuertos', prioridad)
                            self.prioridades.enqueue(des)

                    # Abro aeropuertos  y fronteras por la cura
                    if pais.valor.cura:
                        if not pais.valor.estado_aeropuertos:
                            prioridad = pais.valor.gente_infectada / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'abrir aeropuertos', prioridad)
                            self.prioridades.enqueue(des)

                        if not pais.valor.estado_fronteras:
                            prioridad = pais.valor.gente_infectada / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'abrir frontera', prioridad)
                            self.prioridades.enqueue(des)

                    # Abro aeropuertos
                    if not pais.valor.estado_aeropuertos:
                        if ((pais.valor.gente_infectada / pais.valor.poblacion) < 0.8) and (
                                    pais.valor.gente_muerta / pais.valor.poblacion) < 0.20:
                            des = edd.ListaLigada()
                            prioridad = (0.7 * pais.valor.gente_infectada) / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'abrir aeropuertos', prioridad)
                            self.prioridades.enqueue(des)

                    # Abro fronteras
                    if not pais.valor.estado_fronteras:
                        if ((pais.valor.gente_infectada / pais.valor.poblacion) < 0.5) or (
                                    pais.valor.gente_muerta / pais.valor.poblacion) < 0.25:
                            des = edd.ListaLigada()
                            prioridad = (0.7 * pais.valor.gente_infectada) / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'abrir fronteras', prioridad)
                            self.prioridades.enqueue(des)

                    # Entrego macascarillas
                    if not pais.valor.mascarillas:
                        if pais.valor.gente_infectada > (pais.valor.poblacion // 3):
                            des = edd.ListaLigada()
                            prioridad = (1 * pais.valor.gente_infectada) / pais.valor.poblacion
                            des.append(pais.valor.nombre, 'entrego mascarillas', prioridad)
                            self.prioridades.enqueue(des)

            pais.valor.estado_pais()

        # Ordeno las cola de prioridades y ejecuto 3
        # Prioridades es una cola del tipo [pais, accion, prioridad]
        if len(self.prioridades) > 0:
            # No use el metodo sort porque requeria meterse a una sublista, entonces es mas facil con sorted.
            prioridades = edd.Queue(sorted(self.prioridades, key=lambda p: p.valor[2], reverse=True))
            contador = 0
            while contador < 3:
                # Tuve que hacer esto para que no tire error, porque el nodo.siguiente era None
                if len(prioridades) == 1:
                    accion = prioridades[0]
                    nombre_pais = accion.valor[0]
                    ejecutar = accion.valor[1]
                    for pais1 in self.paises:
                        if pais1.valor.nombre == str(nombre_pais):
                            if ejecutar == 'cerrar fronteras':
                                self.cerro_fronteras.append(str(pais1.valor.nombre))
                                pais1.valor.cerrar_fronteras()
                            if ejecutar == 'cerrar aeropuertos':
                                pais1.valor.cerrar_aeropuertos()
                                self.cerro_aeropuertos.append(str(pais1.valor.nombre))
                            if ejecutar == 'abrir fronteras':
                                pais1.valor.abrir_fronteras()
                            if ejecutar == 'abrir aeropuertos':
                                pais1.valor.abrir_aeropuertos()
                            if ejecutar == 'entrego mascarillas':
                                self.entrego_mascarillas.append(str(pais1.valor.nombre))
                                pais1.valor.entregar_mascarillas()
                    self.prioridades = edd.Queue()
                    break

                if len(prioridades) > 1:
                    accion = prioridades.dequeue()
                    nombre_pais = accion.valor.valor[0]
                    ejecutar = accion.valor.valor[1]
                    for pais1 in self.paises:
                        if pais1.valor.nombre == str(nombre_pais):
                            if str(ejecutar) == 'cerrar fronteras':
                                self.cerro_fronteras.append(str(pais1.valor.nombre))
                                pais1.valor.cerrar_fronteras()
                            if str(ejecutar) == 'cerrar aeropuertos':
                                pais1.valor.cerrar_aeropuertos()
                                self.cerro_aeropuertos.append(str(pais1.valor.nombre))
                            if str(ejecutar) == 'abrir fronteras':
                                pais1.valor.abrir_fronteras()
                            if str(ejecutar) == 'abrir aeropuertos':
                                pais1.valor.abrir_aeropuertos()
                            if str(ejecutar) == 'entrego mascarillas':
                                self.entrego_mascarillas.append(str(pais1.valor.nombre))
                                pais1.valor.entregar_mascarillas()
                contador += 1
                # Para usarla despues en las estadisticas
            self.prioridades = prioridades

        # Agrego el resumen del dia a self.diario
        self.diario.append(edd.ListaLigada(self.fecha, self.infecto, self.murio))
        self.fecha += 1

        if self.poblacion == 0:
            print('Has ganado, todos han muerto')
        elif self.gente_infectada <= 0:
            print('Has perdido, no queda ningun infectado')
        else:
            Mundo.menu(self)

    def estadisticas(self):

        while True:
            print('\nQue deseas hacer?')
            print('\n1. Resumen del dia')
            print('2. Por pais')
            print('3. Global')
            print('4. Muertes e infecciones por dia')
            print('5. Promedio muertes e infecciones')

            opcion = str(input('\nQue deseas hacer: '))
            opciones = edd.ListaLigada('1', '2', '3', '4', '5')
            if opciones.is_in(opcion):
                break
            else:
                print('Ingresa una opcion correcta')

        if opcion == '1':
            print('\nResumen del dia: ')
            print('\nSe infecto: {} personas'.format(str(self.infecto)))
            print('Murio: {0} personas'.format(str(self.murio)))
            print('La infeccion llego a: ', self.llego_infeccion)
            print('Cerraron aeropuertos: ', self.cerro_aeropuertos)
            print('Cerraron frontera: ', self.cerro_fronteras)
            print('Entrego mascarillas: ', self.entrego_mascarillas)

        elif opcion == '2':
            print('\nResumen por pais: ')
            encontrado = True
            while encontrado:
                #  Pone la enfermedad en un pais
                print('\nAhora debes ingresar un pais:\n')

                for pais in self.paises:
                    print(pais)

                buscado = str(input('\nIngresa un pais:'))
                for pais in self.paises:
                    if pais.valor.nombre == buscado:
                        print('\n' + str(pais.valor.nombre))
                        print('Gente viva: ' + str(pais.valor.poblacion))
                        print('Gente infectada: ' + str(pais.valor.gente_infectada))
                        print('Gente muerta: ' + str(pais.valor.gente_muerta))
                        print('Propuestas: ')
                        for propuesta in self.prioridades:
                            if propuesta.valor.valor[0] == pais.valor.nombre:
                                print(propuesta)

                        encontrado = False
                        break
                if encontrado:
                    print('\nIngresa un pais valido')

        elif opcion == '3':
            print('\nResumen global: \n')
            print('Poblacion mundial: ', self.poblacion)
            print('Poblacion muerta: ', self.gente_muerta)
            print('Poblacion total infectada: ', self.gente_infectada)
            print('Poblacion total sana: ', int(self.poblacion) - int(self.gente_infectada))
            print('')
            for pais in self.paises:
                print('{0} -> {1}'.format(pais.valor.nombre, pais.valor.estado))

        elif opcion == '4':
            for dia in self.diario:
                print('Dia: {0} -> Infectados: {1}, muertos: {2}'.format(str(dia.valor[0]), str(dia.valor[1]),
                                                                         str(dia.valor[2])))

        elif opcion == '5':
            print('Tasa de vida: ', self.poblacion / self.poblacion_inicial)
            print('Tasa de muerte: ', self.gente_muerta / self.poblacion_inicial)

        Mundo.menu(self)

    def guardar_partida(self):
        pass

    def cargar_partida(self):
        print('Que partida quieres cargar?')
        print('Lo siento, esta parte aun esta en proceso... ')

    def salir(self):
        pass

    def descubrir_cura(self):
        descubrir = (self.infeccion.visibilidad * self.gente_infectada * (self.gente_muerta ** 2)) / \
                    (self.poblacion_inicial ** 2)
        #  La probabilidad a comparar le puse dos decimales para hacerla mas exacta
        a = random.randrange(10000) / 100
        if not self.cura:
            #  Aplica la probabilidad de ocurrencia
            if a <= (descubrir * 100):
                #  Se descubrio la cura
                self.cura = True
                #  Le doy la cura al azar a un pais
                index = random.randint(0, len(self.paises) - 1)
                self.paises[index].cura = True

        if self.progreso_cura <= 100:
            if self.cura:
                self.progreso_cura += self.gente_sana / (2 * self.poblacion_inicial)

    def obtener_datos(self):
        #  Por cada dia, me cuenta los infectados y la gente muerta que hay.
        self.gente_infectada = 0
        self.gente_muerta = 0
        for pais in self.paises:
            self.gente_infectada += pais.valor.gente_infectada
            self.gente_muerta += pais.valor.gente_muerta
            self.gente_sana = self.poblacion - self.gente_infectada

    # La use para probar, pero  la deje de todas formas
    def __repr__(self):
        rep = ''
        i = 0
        for pais in self.paises:
            if i == 0:
                rep += '\nPais: {0} - Estado: {1}'.format(pais.valor.nombre, pais.valor.estado)
                i += 1
            else:
                rep += '\nPais: {0} - Estado: {1}'.format(pais.valor.nombre, pais.valor.estado)
        return rep
