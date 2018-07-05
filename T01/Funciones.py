from os.path import isfile, join
import os

encoding = 'utf-8'


def unsigned_float():
    # Funcion para ver si un input es un int y mayor que 0, y try lo use para simplificar un ingreso correcto del input
    # de parte del usuario.
    while True:
        while True:
            try:
                dato = int(input())
                break
            except ValueError:
                print('Solo digite enteros positivos')
        if dato >= 0:
            break
        else:
            print('Solo digite enteros positivos')
    return dato


def signed_float():
    # Funcion para ver si un input es un int, y try lo use para simplificar un ingreso correcto del input de parte del
    # usuario.
    while True:
        try:
            dato = int(input())
            break
        except ValueError:
            print('Solo digite digitos')
    return dato


def orden(file):
    # Esta funcion la use para identificar en que orden estan las columnas
    with open(file, 'r', encoding='utf8') as data:
        order = data.readline()
        order = order.strip('\n')
        order = order.split(',')
        fila = []
        for i in order:
            fila.append(i.split(':')[0])
    return fila


def read_file(file):
    # Retorna una lista, con sublistas que corresponden a cada linea de un archivo
    lista = []
    with open(file, 'r') as fi:
        for line in fi:
            line = line.strip()
            line = line.split(',')
            lista.append(line)
    return lista


def date():
    print('\nIngrese la fecha y hora\n')
    while True:
        print('Ingrese ano: ')
        ano = unsigned_float()
        if ano < 2000 or ano > 9999:
            print('Ingrese un entero del 2000 al 9999')
            continue
        else:
            break

    while True:
        print('Ingrese mes: ')
        mes = unsigned_float()
        if mes > 12:
            print('Ingrese un entero del 1 al 12')
            continue
        else:
            break

    while True:
        print('Ingrese dia: ')
        dia = unsigned_float()
        if dia > 31 or dia == 0:
            print('\nIngrese un entero del 1 al 31, que sea acorde al mes.\n')
            continue
        for i in (4, 6, 9, 11):
            if mes == i and dia == 31:
                print('\nIngrese un entero del 1 al 31, que sea acorde al mes.\n')
                continue
        if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
            # Comprueba los anos biciestos, obtenido de:
            # https://francysystem.blogspot.cl/2015/04/anos-bisiestos-en-python.html
            if dia == 29:
                break
        if mes == 2 and dia > 28:
            print('\nIngrese un entero del 1 al 31, que sea acorde al mes.')
            continue
        else:
            break

    while True:
        print('\nAhora ingrese la hora, luego los minutos.\nIngrese hora: ')
        hora = unsigned_float()
        if hora > 23:
            print('Ingrese un entero del 0 al 23')
            continue
        else:
            break
    while True:
        print('Ingrese minutos: ')
        minuto = unsigned_float()
        if minuto > 59:
            print('Ingrese un entero del 0 al 59')
            continue
        else:
            break

    return ano, mes, dia, hora, minuto


def copiar_archivo_incendios():
    with open('Simulacion_incendios.txt', 'w', encoding='utf8') as sim_incendios:
        orden_datos = orden('incendios.csv')
        pos_id = orden_datos.index('id')
        pos_lat = orden_datos.index('lat')
        pos_lon = orden_datos.index('lon')
        pos_potencia = orden_datos.index('potencia')
        pos_fecha_i = orden_datos.index('fecha_inicio')
        incendios = read_file('incendios.csv')
        i = 0
        for linea in incendios:
            if i == 0:  # Evito copiar la primera linea
                i += 1
                continue
            escribir = [None, None, None, None, None, None]
            escribir[0] = linea[pos_id]
            escribir[1] = linea[pos_lat]
            escribir[2] = linea[pos_lon]
            escribir[3] = linea[pos_potencia]
            escribir[4] = linea[pos_fecha_i]
            escribir[5] = ''
            escribir_ordenado = ','.join(escribir)
            sim_incendios.write(escribir_ordenado + '\n')


def fecha_lista(fecha):
    # Me retorna una lista, con 5 datos: ['ano', 'mes', 'dia', 'hora', 'minuto']
    fcha = fecha.split(' ')
    hr = fcha[1]
    hra = hr.split(':')
    hora = hra[0]
    minutos = hra[1]
    date = fcha[0]
    fecha = date.split('-')
    ano = fecha[0]
    mes = fecha[1]
    dia = fecha[2]
    return ano, mes, dia, hora, minutos


def contar_minutos(fecha):
    # Esta funcion le asigna 'puntos' a cada fecha, siendo cada minuto del ano equivalente a 1 punto.

    an, me, dia, hora, minutos = fecha_lista(fecha)
    cuenta = 0
    cuenta += (int(dia) * 1440)
    cuenta += (int(hora) * 60)
    cuenta += int(minutos)
    ano = int(an)
    mes = int(me)

    for y in range(1, ano + 1):
        biciesto = False
        if y % 4 == 0 and y % 100 != 0 or y % 400 == 0:
            biciesto = True
        for m in range(1, 13):
            if m in [4, 6, 9, 11]:
                cuenta += 43200

            if m in [1, 3, 5, 7, 8, 10, 12]:
                cuenta += 44640

            else:
                if biciesto:
                    cuenta += 41760
                else:
                    cuenta += 40320

    for ms in range(1, mes + 1):
        biciesto = False
        if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
            biciesto = True
        if ms in [4, 6, 9, 11]:
            cuenta += 43200

        if ms in [1, 3, 5, 7, 8, 10, 12]:
            cuenta += 44640

        else:
            if biciesto:
                cuenta += 41760
            else:
                cuenta += 40320
    return cuenta


def orden_incendios():
    orden_datos = orden('incendios.csv')
    pos_inc_id = orden_datos.index('id')
    pos_lat = orden_datos.index('lat')
    pos_lon = orden_datos.index('lon')
    pos_pot = orden_datos.index('potencia')
    pos_fecha = orden_datos.index('fecha_inicio')
    return pos_inc_id, pos_lat, pos_lon, pos_pot, pos_fecha


def orden_recursos():
    orden_datos = orden('recursos.csv')
    pos_rec_id = orden_datos.index('id')
    pos_tipo = orden_datos.index('tipo')
    pos_lat = orden_datos.index('lat')
    pos_lon = orden_datos.index('lon')
    pos_vel = orden_datos.index('velocidad')
    pos_aut = orden_datos.index('autonomia')
    pos_del = orden_datos.index('delay')
    pos_tas = orden_datos.index('tasa_extincion')
    pos_cos = orden_datos.index('costo')
    return pos_rec_id, pos_tipo, pos_lat, pos_lon, pos_vel, pos_aut, pos_del, pos_tas, pos_cos


def orden_pronosticos():
    orden_datos = orden('meteorologia.csv')
    pos_id = orden_datos.index('id')
    pos_fecha_i = orden_datos.index('fecha_inicio')
    pos_fecha_t = orden_datos.index('fecha_termino')
    pos_tipo = orden_datos.index('tipo')
    pos_valor = orden_datos.index('valor')
    pos_lat = orden_datos.index('lat')
    pos_lon = orden_datos.index('lon')
    pos_radio = orden_datos.index('radio')
    return pos_id, pos_fecha_i, pos_fecha_t, pos_tipo, pos_valor, pos_lat, pos_lon, pos_radio


def intersectan(x1, y1, r1, x2, y2, r2):
    distancia = (float(x1) - float(x2)) ** 2 + (float(y1) - float(y2)) ** 2
    if distancia <= (int(r1) + int(r2)):
        return True
    else:
        return False


def distancia(x1, y1, x2, y2):
    distancia = (float(x1) - float(x2)) ** 2 + (float(y1) - float(y2)) ** 2
    return distancia


def ls(ruta='.'):

    # Devuelve una lista de los archivos en ese directorio
    # Fuente: http://es.stackoverflow.com/questions/24278/cómo-listar-todos-los-archivos-de-una-carpeta-usando-
    # python/24279

    return [arch for arch in os.listdir(ruta) if isfile(join(ruta, arch))]