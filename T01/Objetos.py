import math
import os

import Funciones

encoding = 'utf-8'


def pronosticos_lista():
    cruzar = []

    # Esta funcion crea una lista con objetos los Meteorologia correspondiente del archivo

    pos_id, pos_fecha_i, pos_fecha_t, pos_tipo, pos_valor, pos_lat, pos_lon, pos_radio = Funciones.orden_pronosticos()
    pronosticos = Funciones.read_file('meteorologia.csv')
    i = 0
    with open('meteorologia.csv', 'r', encoding='utf8') as arch:
        ultimo_id = arch.readlines()[-1]
        ultimo_id = ultimo_id.strip('\n')
        ultimo_id = ultimo_id.split(',')

    for linea in pronosticos:  # creo una lista con los objetos Meteorologia del archivo Meteorologia.csv
        if i != 0:
            meteorologia = Metereologia(linea[pos_id], linea[pos_fecha_i], linea[pos_fecha_t], linea[pos_tipo],
                                        linea[pos_valor], linea[pos_lat], linea[pos_lon], linea[pos_radio])
            cruzar.append(meteorologia)

        if i == 0:
            i += 1
            continue

        if str(meteorologia.id) == str(ultimo_id[pos_id]):
            break

    return cruzar


def simular(fecha_actual):
    # Esta funcion simula el programa cruzando los incendios con la meteorologia y el avance del fuego.

    pos_inc_id, pos_lat, pos_lon, pos_pot, pos_fecha = Funciones.orden_incendios()
    incendios = Funciones.read_file('incendios.csv')
    i = 0
    print('Simulando...\n')
    list = pronosticos_lista()

    # Con este sorted, ordeno la lista de objetos Meteorologia, en base a su atributo fecha_i.

    lista = sorted(list, key=lambda objeto: objeto.minutos_inicio, reverse=True)
    incendios_listo = []
    informes = Funciones.ls(os.getcwd() + '/Reportes Estrategias de extincion')
    for linea in incendios:
        if i == 0:
            i += 1
            continue
        else:
            incendio = Incendio(linea[pos_inc_id], linea[pos_lat], linea[pos_lon], linea[pos_pot], linea[pos_fecha])
            min_actual = Funciones.contar_minutos(fecha_actual)

            # Analizo los archivos de estrategias para cada incendio correspondiente
            '''for archivo in informes:
                id = archivo.split('_')
                id = id[0]
                if incendio.id == id:
                    pass'''

            incendio.cruzar_metereo_y_recursos(min_actual, lista)
            incendios_listo.append(incendio)

    return incendios_listo


class Usuario:
    def __init__(self, id, recurso_id):
        self.id = id
        self.recurso_id = recurso_id
        self.estado = 'Standby'


class Incendio:
    def __init__(self, id, lat=0, lon=0, potencia=0, fecha=''):
        self.id = id
        self.lat = float(lat)
        self.lon = float(lon)
        self.potencia = potencia
        self.fecha = fecha
        self.ano, self.mes, self.dia, self.hora, self.minuto = Funciones.fecha_lista(fecha)
        self.radio = 1
        self.puntos_apagados = 0
        self.minutos = Funciones.contar_minutos(fecha)
        self.recursos_utilizados = []
        self.estado = 'Prendido'
        self.fecha_apagado = ''
        self.minutos_usar = Funciones.contar_minutos(fecha)

    def cruzar_metereo_y_recursos(self, minutos_actual, lista):
        if self.minutos < minutos_actual:
            self.radio = 0

            # Me cambio de directorio para abrir los reportes de estrategias

            dir_actual = os.getcwd()
            dir = (os.getcwd() + '/Reportes Estrategias de Extincion')
            os.chdir(dir)
            archivos = Funciones.ls(dir)
            os.chdir(dir_actual)

            while self.minutos_usar < minutos_actual:
                self.radio += 500 / 60
                for condicion in lista:
                    if condicion.fecha_i < self.fecha < condicion.fecha_t:

                        if Funciones.intersectan(condicion.lat, condicion.lon, condicion.radio, self.lat, self.lon,
                                                 self.radio):
                            if condicion.tipo == 'VIENTO':
                                self.radio += condicion.valor * 0.27783
                            if condicion.tipo == 'TEMPERATURA':
                                if condicion.valor <= 30:
                                    continue
                                if condicion.valor >= 30:
                                    self.radio += (condicion.valor - 30) / 60
                            if condicion.tipo == 'LLUVIA':
                                self.radio -= condicion.valor * (50 / 60)

                            # Como la lista que recibe esta funcion esta ordenada por el atributo Meteorologia.fecha_i,
                            # Cuando encuentre el primer pronostico que se cruce con ese incendio, con este break
                            # no va a usar ninguno que venga despues a ese.

                            break
                    self.minutos_usar += 1
        return

    def puntos_de_poder(self):
        return (self.radio ** 2) * math.pi


class Metereologia:
    def __init__(self, id, fecha_i, fecha_t, tipo, valor, lat, lon, radio):
        self.id = id
        self.fecha_i = fecha_i
        self.fecha_t = fecha_t
        self.lat = float(lat)
        self.lon = float(lon)
        self.tipo = tipo
        self.valor = float(valor)
        self.radio = float(radio)
        self.minutos_inicio = Funciones.contar_minutos(self.fecha_i)
        self.minutos_termino = Funciones.contar_minutos(self.fecha_t)


class Recurso:
    def __init__(self, id, tipo, lat, lon, velocidad, autonomia, delay, tasa, costo):
        self.id = id
        self.tipo = tipo
        self.lat = lat
        self.lon = lon
        self.velocidad = velocidad
        self.autonomia = autonomia
        self.delay = delay
        self.tasa = tasa
        self.costo = costo
        self.tiempo_trabajado = 1
        self.tiempo_standby = 1
        self.puntos_extintos = 0

class Anaf(Usuario):
    def __init__(self, id, recurso_id):
        self.id = id
        self.recurso_id = recurso_id
        super().__init__(id, recurso_id)

    def leer_incendios(self, fecha_actual):
        lista_incendios = simular(fecha_actual)

        # Veo que recursos estan en la posicion del incendio

        pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos = Funciones.orden_recursos()
        recursos_lista = Funciones.read_file('recursos.csv')
        for incendio in lista_incendios:
            recursos_trabajando = []
            for recurso in recursos_lista:
                if incendio.lat == recurso[pos_lat] and incendio.lon == recurso[pos_lon]:
                    recursos_trabajando.append((recurso[pos_rec_id]))
            print('ID: ' + str(incendio.id), 'Lat: ' + str(incendio.lat), 'Lon: ' + str(incendio.lon),
                  'Potencia: ' + str(incendio.potencia),
                  'Fecha inicio: ' + str(incendio.fecha),
                  'Porcentaje de extincion: ' + str(
                      (round(incendio.puntos_apagados, 4) / round(incendio.puntos_de_poder(), 4))),
                  'ID Recursos trabajando en el incendio: ' + str(recursos_trabajando), sep=', ')

    def leer_recursos(self):
        pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos = Funciones.orden_recursos()
        recursos_lista = Funciones.read_file('recursos.csv')
        for linea in recursos_lista:
            print('\n ID: ' + linea[pos_rec_id], 'Tipo: ' + linea[pos_tipo], 'Velocidad: ' + linea[pos_vel],
                  'Lat: ' + linea[pos_lat], 'Lon: ' + linea[pos_lon], 'Autonomia: ' + linea[pos_aut], 'Delay: ' +
                  linea[pos_del], 'Tasa extincion: ' + linea[pos_tas], 'Costo: ' + linea[pos_cos], sep=',  ')

    def leer_usuarios(self):
        orden_datos = Funciones.orden('usuarios.csv')
        pos_id = orden_datos.index('id')
        pos_nombre = orden_datos.index('nombre')
        pos_contrasena = orden_datos.index('contraseña')
        pos_recurso_id = orden_datos.index('recurso_id')
        usuarios = Funciones.read_file('usuarios.csv')
        for linea in usuarios:
            print('ID: ' + linea[pos_id], 'Nombre usuario: ' + linea[pos_nombre],
                  'Contrasena: ' + linea[pos_contrasena],
                  'ID recurso asociado: ' + linea[pos_recurso_id], sep=',  ')

    def crear_usuarios(self):

        orden_datos = Funciones.orden('usuarios.csv')
        pos_id = orden_datos.index('id')
        pos_nombre = orden_datos.index('nombre')
        pos_contrasena = orden_datos.index('contraseña')
        pos_recurso_id = orden_datos.index('recurso_id')
        recursos = Funciones.read_file('recursos.csv')
        nombre = str(input('Ingrese nombre de nuevo usuario: '))
        contrasena = str(input('Ingrese nueva contrasena: '))
        while True:
            recurso_id = str(input('\nSi no quiere asociarlo a ningun recurso, ingrese espacio.\nEscriba el recurso_ID '
                                   'al que quiere asociarlo: '))

            if recurso_id == ' ':
                recurso_id = ''
                break

            # Esta parte comprueba si existe dicho recurso_id.

            ids = []
            for linea in recursos:
                if linea[pos_recurso_id] == 'id:string':
                    pass
                else:
                    ids.append(str(linea[pos_recurso_id]))

            if recurso_id in ids or recurso_id == ' ':
                break

            else:
                print('\nIngrese un id correcto\n')

        with open('usuarios.csv', 'a', encoding='utf8') as archivo:
            with open('usuarios.csv', 'r', encoding='utf8') as arch:
                ultimo_id = arch.readlines()[-1]
            ultimo_id = ultimo_id.strip('\n')
            ultimo_id = ultimo_id.split(',')
            nuevo_id = str(int(ultimo_id[pos_id]) + 1)
            escribir = [None, None, None, None]
            escribir[pos_id] = nuevo_id
            escribir[pos_nombre] = nombre
            escribir[pos_contrasena] = contrasena
            escribir[pos_recurso_id] = recurso_id
            escribir_ordenado = ','.join(escribir)
            archivo.write(escribir_ordenado + '\n')
            print('\nUsuario creado')

    def agregar_pronosticos(self):

        pos_id, pos_fecha_i, pos_fecha_t, pos_tipo, pos_valor, pos_lat, pos_lon, pos_radio = \
            Funciones.orden_pronosticos()

        print('\nIngresar fecha de inicio')
        ano, mes, dia, hora, min = Funciones.date()
        fecha_in = str('{0}-{1}-{2} {3}:{4}:00'.format(ano, mes, dia, hora, min))
        print('\nIngresar fecha de termino')
        ano1, mes1, dia1, hora1, min1 = Funciones.date()
        fecha_ter = str('{0}-{1}-{2} {3}:{4}:00'.format(ano1, mes1, dia1, hora1, min1))

        while True:
            tipos = ['VIENTO', 'TEMPERATURA', 'NUBES', 'LLUVIA']
            tipo = str(input('tipo: '))
            if tipo in tipos:
                break
            else:
                print('\nIngresa VIENTO, TEMPERATURA, NUBES, LLUVIA')
                continue

        print('\nIngrese valor: ')
        valor = Funciones.unsigned_float()
        valor = valor
        print('\nIngrese lat: ')
        lat = Funciones.signed_float()
        lat = lat
        print('\nIngrese lon: ')
        lon = Funciones.signed_float()
        lon = lon
        print('\nIngrese radio: ')
        radio = Funciones.unsigned_float()

        with open('meteorologia.csv', 'a', encoding='utf8') as archivo:
            with open('meteorologia.csv', 'r', encoding='utf8') as arch:
                ultimo_id = arch.readlines()[-1]
            ultimo_id = ultimo_id.strip('\n')
            ultimo_id = ultimo_id.split(',')
            nuevo_id = str(int(ultimo_id[pos_id]) + 1)
            escribir = [None, None, None, None, None, None, None, None]
            escribir[pos_id] = nuevo_id
            escribir[pos_fecha_i] = fecha_in
            escribir[pos_fecha_t] = fecha_ter
            escribir[pos_tipo] = tipo
            escribir[pos_valor] = str(valor)
            escribir[pos_lat] = str(lat)
            escribir[pos_lon] = str(lon)
            escribir[pos_radio] = str(radio)
            escribir_ordenado = ','.join(escribir)
            print(escribir_ordenado)
            archivo.write(escribir_ordenado + '\n')
            print('Pronostico agregado')

    def agregar_incendio(self):
        orden = Funciones.orden('incendios.csv')
        pos_id = orden.index('id')
        pos_lat = orden.index('lat')
        pos_lon = orden.index('lon')
        pos_potencia = orden.index('potencia')
        pos_fecha_i = orden.index('fecha_inicio')

        print('\nIngrese lat: ')
        lat = Funciones.signed_float()
        lat = str(lat)
        print('\nIngrese lon: ')
        lon = Funciones.signed_float()
        lon = str(lon)
        print('\nIngrese potencia: ')
        potencia = Funciones.unsigned_float()
        potencia = str(potencia)
        print('\nIngresar fecha de inicio')
        dia, mes, ano, hora, mes = Funciones.date()
        fecha_in = str('{0}-{1}-{2} {3}:{4}:00'.format(dia, mes, ano, hora, mes))

        with open('incendios.csv', 'a', encoding='utf8') as archivo:
            with open('incendios.csv', 'r', encoding='utf8') as arch:
                ultimo_id = arch.readlines()[-1]
            ultimo_id = ultimo_id.strip('\n')
            ultimo_id = ultimo_id.split(',')
            nuevo_id = str(int(ultimo_id[pos_id]) + 1)
            escribir = [None, None, None, None, None]
            escribir[pos_id] = nuevo_id
            escribir[pos_lat] = lat
            escribir[pos_lon] = lon
            escribir[pos_potencia] = potencia
            escribir[pos_fecha_i] = fecha_in
            escribir_ordenado = ','.join(escribir)
            archivo.write(escribir_ordenado + '\n')
            print('Incendio agregado')

    def incendios_activos(self, fecha_actual):
        incendios = Funciones.read_file('incendios.csv')
        orden_datos = Funciones.orden('incendios.csv')
        pos_inc_id = orden_datos.index('id')
        pos_fecha = orden_datos.index('fecha_inicio')
        print('Los incendios activos actualmente son:\n')
        incendios = simular(fecha_actual)
        for incendio in incendios:
            if incendio.estado == 'Prendido' and incendio.minutos <= Funciones.contar_minutos(fecha_actual):
                print('ID: ' + incendio.id + ' - Fecha inicio: ' + incendio.fecha, ' - IDs recursos utilizados: ')

    def incendios_apagados(self, fecha_actual):
        print('Los incendios apagados son:\n')
        incendios = simular(fecha_actual)
        for incendio in incendios:
            if incendio.estado == 'Apagado' and incendio.minutos <= fecha_actual:
                print('ID: ' + incendio.id + ' - Fecha inicio: ' + incendio.fecha,
                      ' - Fecha termino: ' + incendio.fecha_apagado, ' - IDs recursos utilizados: ')

    def recursos_mas_utilizados(self):
        pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos = Funciones.orden_recursos()
        recursos_lista = Funciones.read_file('recursos.csv')
        recursos_datos = Funciones.read_file('recursos_datos.txt')

        recursos = []  # Lista de todos los recursos
        i = 0
        for recurso in recursos_lista:
            if i == 0:
                i += 1
                continue
            else:
                recurso = Recurso(recurso[pos_rec_id], recurso[pos_tipo], recurso[pos_lat], recurso[pos_lon],
                                  recurso[pos_vel], recurso[pos_aut], recurso[pos_del], recurso[pos_tas],
                                  recurso[pos_cos])
                for dato in recursos_datos:
                    if dato[0] == recurso.id:
                        recurso.tiempo_trabajado = dato[2]
                        recurso.tiempo_standby = dato[3]
                recursos.append(recurso)
        lista = sorted(recursos, key=lambda objeto: (objeto.tiempo_trabajado/objeto.tiempo_standby))
        for recurso in lista:
            print(recurso.id)

    def recursos_mas_efectivos(self):
        pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos = Funciones.orden_recursos()
        recursos_lista = Funciones.read_file('recursos.csv')
        recursos_datos = Funciones.read_file('recursos_datos.txt')

        recursos = []  # Lista de todos los recursos
        i = 0
        for recurso in recursos_lista:
            if i == 0:
                i += 1
                continue
            else:
                recurso = Recurso(recurso[pos_rec_id], recurso[pos_tipo], recurso[pos_lat], recurso[pos_lon],
                                  recurso[pos_vel], recurso[pos_aut], recurso[pos_del], recurso[pos_tas],
                                  recurso[pos_cos])
                for dato in recursos_datos:
                    if dato[0] == recurso.id:
                        recurso.tiempo_trabajado = dato[2]
                        recurso.tiempo_standby = dato[3]
                recursos.append(recurso)
        lista = sorted(recursos, key=lambda objeto: (objeto.puntos_extintos/objeto.tiempo_trabajado)/objeto.potencia)
        for recurso in lista:
            print(recurso.id)

    def planificar_estrategia(self, fecha_actual):
        minutos_actual = Funciones.contar_minutos(fecha_actual)
        exit_loop = True
        options = ['1', '2', '3']

        while exit_loop:

            print(''' \nBienvenido.

    Que estrategia quiere usar:\n
        1. Cantidad de recursos
        2. Tiempo de extincion
        3. Costo economico

    Respuesta: ''')
            user_entry = input()

            if user_entry in options:
                exit_loop = False

            else:
                print('Ingrese una opcion valida')

            while True:
                incendio_id = str(input('\nEscriba el ID del incendio: '))

                # Esta parte comprueba si existe dicho id.

                ids = []
                with open('incendios.csv', 'r', encoding='utf8') as arch:
                    archivo = arch.readlines()
                    orden = Funciones.orden('incendios.csv')
                    pos_id = orden.index('id')
                    for linea in archivo:
                        if linea[pos_id] == 'id:string':
                            pass
                        else:
                            ids.append(str(linea[pos_id]))

                    if incendio_id in ids:
                        break

                    else:
                        print('\nIngrese un id correcto\n')  # Pido id

        pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos = Funciones.orden_recursos()
        ipos_inc_id, ipos_lat, ipos_lon, ipos_pot, ipos_fecha = Funciones.orden_incendios()
        recursos_lista = Funciones.read_file('recursos.csv')
        recursos = []  # Lista de todos los recursos
        meteorologia = pronosticos_lista()  # Lista con los reportes meteorologicos
        dir = os.getcwd()
        i = 0
        for recurso in recursos_lista:
            if i == 0:
                i += 1
                continue
            else:
                recurso = Recurso(recurso[pos_rec_id], recurso[pos_tipo], recurso[pos_lat], recurso[pos_lon],
                                  recurso[pos_vel], recurso[pos_aut], recurso[pos_del], recurso[pos_tas],
                                  recurso[pos_cos])
                recursos.append(recurso)

        if user_entry == 1:
            lista = sorted(recursos, key=lambda objeto: objeto.potencia)
            tipo = 'Cantidad_de_recursos'
        if user_entry == 2:
            lista = sorted(recursos, key=lambda objeto: objeto.tasa)
            tipo = 'Tiempo_extincion'
        if user_entry == 3:
            lista = sorted(recursos, key=lambda objeto: objeto.costo)
            tipo = 'Costo_economico'

        incendios = Funciones.read_file('incendios.csv')
        i = 0
        for linea in incendios:
            if i == 0:
                i += 1
                continue
            else:
                if linea[ipos_inc_id] == incendio_id:
                    incendio = Incendio(linea[ipos_inc_id], linea[ipos_lat], linea[ipos_lon], linea[ipos_pot],
                                        linea[ipos_fecha])

        if incendio.minutos < minutos_actual:
            incendio.radio = 0
            while incendio.minutos < minutos_actual:
                incendio.radio += 500 / 60
                for condicion in meteorologia:
                    if condicion.fecha_i < incendio.fecha < condicion.fecha_t:

                        if Funciones.intersectan(condicion.lat, condicion.lon, condicion.radio, incendio.lat,
                                                 incendio.lon, incendio.radio):
                            if condicion.tipo == 'VIENTO':
                                incendio.radio += condicion.valor * 0.27783
                            if condicion.tipo == 'TEMPERATURA':
                                if condicion.valor <= 30:
                                    continue
                                if condicion.valor >= 30:
                                    incendio.radio += (condicion.valor - 30) / 60
                            if condicion.tipo == 'LLUVIA':
                                incendio.radio -= condicion.valor * 50 / 60

                            # Como la lista que recibe esta funcion esta ordenada por el atributo Meteorologia.fecha_i,
                            # Cuando encuentre el primer pronostico que se cruce con ese incendio, con este break
                            # no va a usar ninguno que venga despues a ese.

                            break

                    # Mando los primeros 30 recursos de la lista ordenada a apagar el incendio
                    for r in range(30):
                        recurso = lista[r]
                        with open('/{0}_{1}.txt'.format(incendio_id, tipo), 'a') as informe:
                            informe.write(
                                'Recurso: {0}, Hora de salida: {1}, Hora llegada al incenido: {2}, hora de retirada: {3}, '
                                'Hora de regreso a la base: {4}')
                        distancia = Funciones.distancia(incendio.lat, incendio.lon, recurso.lat, recurso.lon) ** 110000
                        distancia -= recurso.velocidad * 60
                        if distancia <= 0:
                            incendio.puntos_apagados += (recurso.tasa / 60)

                    incendio.minutos += 1


class Normal(Usuario):
    def __init__(self, id, recurso_id):
        self.id = id
        self.recurso_id = recurso_id
        super().__init__(id, recurso_id)

    def leer_incendios(self):
        recursos_datos = Funciones.read_file('recursos_datos.txt')
        incendio_id = str(input('\nEscriba el incendio_ID que quieres ver: '))

        # Esta parte comprueba si existe dicho incendio_id asociado al recurso.
        permiso = False
        for linea in recursos_datos:
            if linea[0] == self.recurso_id:
                if incendio_id == linea[1]:
                    permiso = True
        if permiso:
            orden_datos = Funciones.orden('incendios.csv')
            pos_inc_id = orden_datos.index('id')
            pos_lat = orden_datos.index('lat')
            pos_lon = orden_datos.index('lon')
            pos_pot = orden_datos.index('potencia')
            pos_fecha = orden_datos.index('fecha_inicio')
            incendios = Funciones.read_file('incendios.csv')
            for linea in incendios:
                if incendio_id == linea[pos_inc_id]:
                    print(linea[pos_inc_id], linea[pos_lat], linea[pos_lon], linea[pos_pot], linea[pos_fecha],
                          sep=',  ')
        else:
            print('\nIngrese un id de incendio al que se te haya asignado\n')

    def leer_recursos(self):
        orden_datos = Funciones.orden('recursos.csv')
        pos_rec_id = orden_datos.index('id')
        pos_tipo = orden_datos.index('tipo')
        pos_lat = orden_datos.index('lat')
        pos_lon = orden_datos.index('lon')
        pos_vel = orden_datos.index('velocidad')
        pos_aut = orden_datos.index('autonomia')
        pos_del = orden_datos.index('delay')
        pos_tas = orden_datos.index('tasa_extincion')
        pos_cos = orden_datos.index('costo')
        recursos = Funciones.read_file('recursos.csv')
        while True:
            id = str(input('\nIngresa el ID del recurso al cual estas asociado: '))
            if self.recurso_id == id:
                for linea in recursos:
                    if linea[pos_rec_id] == id:
                        print('\n ID: ' + linea[pos_rec_id], 'Tipo: ' + linea[pos_tipo], 'Velocidad: ' + linea[pos_vel],
                              'Lat: ' + linea[pos_lat], 'Lon: ' + linea[pos_lon], 'Autonomia: ' + linea[pos_aut],
                              'Delay: ' +
                              linea[pos_del], 'Tasa extincion: ' + linea[pos_tas], 'Costo: ' + linea[pos_cos],
                              sep=',  ')
                        break
                break
            else:
                continue
