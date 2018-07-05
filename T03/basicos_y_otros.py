import Exceptions as ex
import Funciones as f
import matplotlib.pyplot as plt
import numpy as np
from RQL_dic import diccionario

'''
COMANDOS BASICOS
'''


def asignar(variable, comando):
    if variable not in f.comandos:
        diccionario[variable] = comando
        return 'asignar'
    else:
        raise ex.ImposibleProcesar('Asignar')


def graficar(columna, opcion):
    columna = [x for x in columna]
    if isinstance(opcion, list):
        # Si es una lista, entonces uso eso como eje x
        opc = opcion
    elif opcion == 'numerico':
        opc = f.numerico(columna)
    elif opcion == 'normalizado':
        opc = f.normalizado(columna)
    elif ':' in opcion:
        opc = f.rango(opcion)

    if not len(columna) == len(opc):
        raise ex.ImposibleProcesar('Graficar')

    plt.close()
    plt.rcParams['agg.path.chunksize'] = 10000
    y = np.array(columna)
    x = np.array(opc)
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('grafica')
    plt.grid(True)
    plt.show()

    return 'Graficar'


'''
COMANDOS COMPUESTOS
'''


def do_if(consulta_a, consulta_b, consulta_c):
    if consulta_b:
        return consulta_a
    else:
        return consulta_c
