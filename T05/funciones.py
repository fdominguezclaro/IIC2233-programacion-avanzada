from csv import reader


def leer_constantes():
    constantes_diccionario = {}
    with open('constantes.csv', 'r') as para:
        constantes = reader(para)
        next(constantes)
        for linea in constantes:
            i, j = linea
            constantes_diccionario[i] = int(j)
    return constantes_diccionario
