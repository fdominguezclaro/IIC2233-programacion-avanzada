from math import e
from math import pi

import Exceptions as ex
import Funciones as fu


def crear_funcion(nombre_modelo, *parametros):
    if isinstance(parametros, tuple):
        parametros = [x for x in parametros]

    if nombre_modelo == 'normal':
        if len(parametros) != 2:
            raise ex.ArgumentoInvalido('Crear funcion normal')
        else:
            funcion = normal(*parametros)
    elif nombre_modelo == 'exponencial':
        if len(parametros) != 1:
            raise ex.ArgumentoInvalido('Crear funcion exponencial')
        else:
            funcion = exponencial(*parametros)
    elif nombre_modelo == 'gamma':
        if len(parametros) != 2:
            raise ex.ArgumentoInvalido('Crear funcion gamma')
        else:
            funcion = gamma(*parametros)
    else:
        raise ex.ArgumentoInvalido('Crear Funcion')
    return funcion


'''
DISTRIBUICIONES DE PROBABILIDAD
'''


def normal(u, o):
    def normal1(x):
        f = (1 / ((2 * pi * (o ** 2)) ** (1 / 2))) * (e ** (-(1 / 2) * (((x - u) / o) ** 2)))
        return f

    return normal1


def exponencial(v):
    if v <= 0:
        raise ex.ImposibleProcesar('')

    def exponencial1(x):
        f = v * (e ** (-v * x))
        return f

    return exponencial1


def gamma(v, k):
    # K tiene que se un entero, si no levanto un error
    if not isinstance(k, int):
        raise ex.ErrorMatematico('Gamma')

    def gamm1(x):
        f = ((v ** k) / (fu.factorial(k - 1))) * (x ** (k - 1)) * (e ** (-v * x))
        return f

    return gamm1
