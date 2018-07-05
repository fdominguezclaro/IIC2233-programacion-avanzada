import os
from functools import reduce

import Exceptions as ex
import Fx_valor_numerico as fv
import matplotlib.pyplot as plt

plt.ion()
comandos = ['numerico', 'normalizado', 'asignar', 'crear_funcion', 'graficar', 'extraer_columna', 'filtrar',
            'operar', 'evaluar', 'LEN', 'PROM', 'DESV', 'MEDIAN', 'VAR', 'comparar_columna', 'comparar',
            'do_if', 'normal', 'exponencial', 'gamma']


def orden_csv(file, buscado):  # file : archivo csv, *args : lista de strings con nombres de columna buscados  ->
    # retorna lista con las posiciones de las columnas buscadas en orden respecto al archivo que nos entregaron
    # Esta funcion la use para identificar en que orden estan las columnas. Aqui no abro el archivo entero, por lo tanto
    # esta funcion no me interesa hacerla optima

    if not os.path.exists(file + '.csv'):
        raise ex.ImposibleProcesar('Extraer columna, no existe el archivo ' + str(file))

    with open(file + '.csv', 'r', encoding='utf8') as data:
        fila = data.readline()
        fila = fila.strip('\n')
        fila = fila.split(';')
        fila = [item.split(':')[0].strip() for item in fila]
        if buscado not in fila:
            raise ex.ImposibleProcesar('Extraer columna, no existe la columna ' + str(buscado))
    return fila.index(buscado)


def factorial(n):
    # Funcion que resuelve factoriales recursivamente
    if not isinstance(n, int):
        raise ex.ErrorDeTipo('Factorial, tiene que ser un numero entero, no: ' + str(n))
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def numerico(valores):
    val = [x for x in range(fv.LEN(valores))]
    return val


def normalizado(valores):
    # Creo una lista con valores del 0 a len(valores), para luego dividirla por la suma total, y luego hacerle un zip
    # con valores
    suma = reduce(lambda x, y: x + y, valores)
    enumerados = numerico(valores)
    divididos = list(map(lambda x: x / suma, enumerados))
    return divididos


def rango(string):
    sep = string.split(':')
    lista = sep[1].split(',')
    lista = [float(x) for x in lista]
    a = lista[0]
    b = lista[1]
    c = lista[2]
    retornar = list(x for x in frange(a, b, c))
    return retornar


def frange(inicio, final, intervalo):
    # Cree una funcion que me deja crear un for i in range() con intervalo decimal
    x = inicio
    while x <= final:
        yield x
        x += intervalo
