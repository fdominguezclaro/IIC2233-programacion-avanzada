import Exceptions as ex
import Funciones as f

'''
COMANDOS QUE RETORNAN UN CONJUNTO DE DATOS
'''


def extraer_columna(nombre_archivo, columna):  # nombre_archivo : arch.csv, columna : str -> generador
    # Extraigo las columnas desde la [1:], y los datos son int
    ind = f.orden_csv(nombre_archivo, columna)
    with open(nombre_archivo + '.csv', 'r') as file:
        columna = [pelicula.split(';')[ind].strip() for pelicula in file]
        lista = [float(i) for i in columna[1:]]
        return lista


def filtrar(columna, simbolo, valor):
    if not isinstance(valor, int) or not isinstance(valor, int):
        raise ex.ErrorDeTipo('filtrar')

    if simbolo == '==':
        filtrado = list(filter(lambda x: x == valor, columna))
    elif simbolo == '>':
        filtrado = list(filter(lambda x: x > valor, columna))
    elif simbolo == '<':
        filtrado = list(filter(lambda x: x < valor, columna))
    elif simbolo == '>=':
        filtrado = list(filter(lambda x: x >= valor, columna))
    elif simbolo == '<=':
        filtrado = list(filter(lambda x: x <= valor, columna))
    elif simbolo == '!=':
        filtrado = list(filter(lambda x: x != valor, columna))

    return filtrado


def operar(columna, simbolo, valor):
    if simbolo == '/' and valor == 0:
        raise ex.ErrorMatematico('Operar: ' + str(simbolo) + ' ' + str(valor))

    if not isinstance(valor, int) or not isinstance(valor, int):
        raise ex.ErrorDeTipo('operar')

    if simbolo == '+':
        operado = list(map(lambda x: x + valor, columna))
    elif simbolo == '-':
        operado = list(map(lambda x: x - valor, columna))
    elif simbolo == '<':
        operado = list(map(lambda x: x < valor, columna))
    elif simbolo == '*':
        operado = list(map(lambda x: x * valor, columna))
    elif simbolo == '/':
        operado = list(map(lambda x: x / valor, columna))
    elif simbolo == '!=':
        operado = list(map(lambda x: round(x, valor), columna))
    return operado


def evaluar(funcion, inicio, final, intervalo):
    # Primero creo una lista con los valores de inicio, los valores intermedios y despues el valor final. Luego uso esta
    # lista usando map.
    numeros = [x for x in f.frange(inicio, final, intervalo)]
    retornar = list(map(funcion, numeros))
    return retornar
