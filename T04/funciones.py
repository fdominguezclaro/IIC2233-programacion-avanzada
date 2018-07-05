import os
from csv import reader


def orden(file):
    """Esta funcion la use para identificar en que orden estan las columnas
    
    :param file: archivo .csv a leer
    :type file: str
    
    :return: lista con la primera fila
    :rtype: List
    """
    if not os.path.exists(file):
        raise AssertionError('No existe el archivo ' + str(file))

    with open(file, 'r', encoding='utf8') as data:
        order = data.readline()
        order = order.strip('\n')
        order = order.split(',')
        fila = []
        for i in order:
            fila.append(i.split(':')[0])
    return fila


def read_file(file):
    """Funcion que lee un archivo.csv
    :param file: archivo .csv a leer
    :type file: str
    
    :return: lista con todas las lineas
    :rtype: List
    """
    if not os.path.exists(file):
        raise AssertionError('No existe el archivo ' + str(file))
    lista = []
    with open(file, 'r') as fi:
        fi.readline()
        for line in fi:
            line = line.strip().split(',')
            lista.append(line)
    return lista


def leer_escenario(lista, n):
    """Funcion que lee un escenario determinado
    :param lista: Lista de todos los escenarios en escenario.csv
    :type lista: List
    
    :param n: numero de escenario
    :type n: integer
    
    :return: lista con los parametros de ese escenario
    :rtype: List
    """
    escenario = {}
    for linea in lista:
        if linea[n] != '-':
            value = float(linea[n])
        else:
            value = linea[n]
        escenario[linea[0]] = value

    return escenario


def leer_parametros():
    parametros_diccionario = {}
    with open('parametros.csv', 'r') as para:
        parametros = reader(para)
        next(parametros)
        for linea in parametros:
            i, j = linea
            parametros_diccionario[i] = j
    return parametros_diccionario


header = orden('integrantes.csv')
pos_nombre = header.index('Nombre')
pos_rol = header.index('Rol')
pos_seccion = header.index('Sección')
