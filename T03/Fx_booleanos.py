import Fx_valor_numerico as fv

'''
COMANDOS QUE RETORNAN UN BOOLEANO
'''


def comparar_columna(columna_1, simbolo, comando, columna_2):
    if isinstance(columna_1, str):
        # Si me dan una variable guardada
        if '[' not in columna_1:
            columna_1 = (x for x in columna_1)

        # Si me entregan un string con datos, lo convierto a lista
        else:
            columna_1 = [int(x) for x in columna_1[1:-1].split(',')]

    if isinstance(columna_2, str):
        # Si me dan una variable guardada
        if '[' not in columna_2:
            columna_2 = (x for x in columna_2)

        # Si me entregan un string con datos, lo convierto a lista
        else:
            columna_2 = [int(x) for x in columna_2[1:-1].split(',')]

    if comando == 'LEN':
        columna_1 = fv.LEN(columna_1)
        columna_2 = fv.LEN(columna_2)
    elif comando == 'PROM':
        columna_1 = fv.PROM(columna_1)
        columna_2 = fv.PROM(columna_2)
    elif comando == 'DESV':
        columna_1 = fv.DESV(columna_1)
        columna_2 = fv.DESV(columna_2)
    elif comando == 'MEDIAN':
        columna_1 = fv.MEDIAN(columna_1)
        columna_2 = fv.MEDIAN(columna_2)
    elif comando == 'VAR':
        columna_1 = fv.VAR(columna_1)
        columna_2 = fv.VAR(columna_2)

    if simbolo == '==':
        return columna_1 == columna_2
    elif simbolo == '>':
        return columna_1 > columna_2
    elif simbolo == '<':
        return columna_1 < columna_2
    elif simbolo == '>=':
        return columna_1 >= columna_2
    elif simbolo == '<=':
        return columna_1 <= columna_2
    elif simbolo == '!=':
        return columna_1 != columna_2


def comparar(numero_1, simbolo, numero_2):
    if simbolo == '==':
        return numero_1 == numero_2
    elif simbolo == '>':
        return numero_1 > numero_2
    elif simbolo == '<':
        return numero_1 < numero_2
    elif simbolo == '>=':
        return numero_1 >= numero_2
    elif simbolo == '<=':
        return numero_1 <= numero_2
    elif simbolo == '!=':
        return numero_1 != numero_2
