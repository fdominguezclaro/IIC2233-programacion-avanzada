from functools import reduce
from itertools import tee

import Exceptions as ex

'''
COMANDOS QUE RETORNAN UN VALOR NUMERICO
'''


def LEN(datos):
    len = reduce(lambda x, y: x + 1, datos, 0)
    return len


def PROM(datos):
    if isinstance(datos, str):
        # Si me dan una variable guardada, reviso que no sea lista (que no tenga '[')
        if '[' not in datos:
            datos = (x for x in datos)
            datos, datos1 = tee(datos)
            suma = reduce(lambda x, y: x + y, datos1)
            largo = LEN(datos)
        # Si me entregan un string con datos, lo convierto a lista
        else:
            datos = [int(x) for x in datos[1:-1].split(',')]
            suma = reduce(lambda x, y: x + y, datos)
            largo = len(datos)

    # Si me dan un generador
    else:
        datos, datos1 = tee(datos)
        suma = reduce(lambda x, y: x + y, datos)
        largo = LEN(datos1)

    if largo <= 0:
        raise ex.ErrorMatematico('PROM: no hay datos ingresados, division por cero')
    else:
        promedio = suma / largo
    return promedio


def DESV(datos):
    if isinstance(datos, str):
        # Si me dan una variable guardada, reviso que no sea lista (que no tenga '[')
        if '[' not in datos:
            datos, datos1 = tee(datos)
            datos, datos2 = tee(datos)
            largo = LEN(datos)
        # Si me entregan un string con datos, lo convierto a lista
        else:
            datos = [int(x) for x in datos[1:-1].split(',')]
            largo = len(datos)

    # Si me llega una lista
    elif isinstance(datos, list):
        datos = (x for x in datos)
        datos, datos1 = tee(datos)
        datos, datos2 = tee(datos)
        largo = LEN(datos)

    else:
        datos, datos1 = tee(datos)
        datos, datos2 = tee(datos)
        largo = LEN(datos)

    if largo <= 1:
        raise ex.ErrorMatematico('')
    else:
        promedio = PROM(datos1)
        des = ((reduce(lambda x, y: x + y, (list(map(lambda x: ((x - promedio) ** 2), (x for x in datos2)))))) / (
            largo - 1)) ** (1 / 2)

    return des


def MEDIAN(datos):
    datos = (x for x in datos)
    datos, datos1 = tee(datos)
    lista = list(datos)

    largo = LEN(datos1)
    if largo == 0:
        return None
    elif largo % 2 == 0:
        return (lista[int((largo / 2) - 1)] + lista[int((largo / 2))]) / 2
    else:
        return lista[(int(largo / 2))]


def VAR(datos):
    datos = (x for x in datos)
    datos, datos1 = tee(datos)
    datos, datos2 = tee(datos)
    len = LEN(datos)
    if len <= 1:
        raise ex.ErrorMatematico('')
    else:
        promedio = PROM(datos1)
        des = (reduce(lambda x, y: x + y, (list(map(lambda x: ((x - promedio) ** 2), (x for x in datos2)))))) / (
            len - 1)
    return des
