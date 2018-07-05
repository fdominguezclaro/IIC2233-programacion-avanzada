import Exceptions as ex
import Funciones as f
import Fx_booleanos as fb
import Fx_conjunto_datos as fc
import Fx_valor_numerico as fv
import basicos_y_otros as bo
import crear_funciones as cf
from RQL_dic import diccionario


def interprete(consulta):  # lista : list -> tipo de consulta
    if consulta[0] not in f.comandos:
        return consulta
    lista = [comando if not isinstance(comando, list) else interprete(comando) for comando in consulta]

    # Voy a separar segun el numero de parametros que cada funcion acepta, para asi identificar errores
    no_entro = False

    try:
        if len(consulta) == 2:

            # Veo, al igual que en las siguientes, si la variable entregada esta previamente guardada

            if isinstance(lista[1], str):
                if lista[1] in diccionario:
                    lista[1] = diccionario[lista[1]]

            if lista[0] == 'LEN':
                return fv.LEN(lista[1])
            elif lista[0] == 'PROM':
                return fv.PROM(lista[1])
            elif lista[0] == 'DESV':
                return fv.DESV(lista[1])
            elif lista[0] == 'MEDIAN':
                return fv.MEDIAN(lista[1])
            elif lista[0] == 'VAR':
                return fv.VAR(lista[1])

        if len(consulta) == 3:

            if lista[1] != 'normal' and lista[1] != 'exponencial' and lista[1] != 'gamma':
                if isinstance(lista[1], str):
                    if lista[1] in diccionario:
                        lista[1] = diccionario[lista[1]]

                if isinstance(lista[2], str) and ':' in lista[1]:
                    if lista[2] in diccionario:
                        lista[2] = diccionario[lista[2]]

            if lista[0] == 'asignar':
                return bo.asignar(lista[1], lista[2])
            elif lista[0] == 'graficar':
                return bo.graficar(lista[1], lista[2])
            elif lista[0] == 'extraer_columna':
                return fc.extraer_columna(lista[1], lista[2])
            elif lista[0] == 'crear_funcion':
                return cf.crear_funcion(lista[1], lista[2])

        if len(consulta) == 4:
            if lista[1] != 'normal' and lista[1] != 'exponencial' and lista[1] != 'gamma':
                if isinstance(lista[1], str):
                    if lista[1] in diccionario:
                        lista[1] = diccionario[lista[1]]

                if isinstance(lista[2], str):
                    if lista[2] in diccionario:
                        lista[2] = diccionario[lista[2]]

                if isinstance(lista[3], str):
                    if lista[3] in diccionario:
                        lista[3] = diccionario[lista[3]]

            if lista[0] == 'crear_funcion':
                return cf.crear_funcion(lista[1], lista[2], lista[3])
            elif lista[0] == 'filtrar':
                return fc.filtrar(lista[1], lista[2], lista[3])
            elif lista[0] == 'operar':
                return fc.operar(lista[1], lista[2], lista[3])
            elif lista[0] == 'comparar':
                return fb.comparar(lista[1], lista[2], lista[3])
            elif lista[0] == 'do_if':
                return bo.do_if(lista[1], lista[2], lista[3])

        if len(consulta) == 5:

            if isinstance(lista[1], str):
                if lista[1] in diccionario:
                    lista[1] = diccionario[lista[1]]

            if isinstance(lista[2], str):
                if lista[2] in diccionario:
                    lista[2] = diccionario[lista[2]]

            if isinstance(lista[3], str):
                if lista[3] in diccionario:
                    lista[3] = diccionario[lista[3]]

            if isinstance(lista[4], str):
                if lista[4] in diccionario:
                    lista[4] = diccionario[lista[4]]

            if lista[0] == 'evaluar':
                return fc.evaluar(lista[1], lista[2], lista[3], lista[4])
            elif lista[0] == 'comparar_columna':
                return fb.comparar_columna(lista[1], lista[2], lista[3], lista[4])

    except TypeError:
        raise ex.ReferenciaInvalida(consulta[0])


    except ValueError:
        raise ex.ErrorDeTipo(consulta[0])

    else:
        no_entro = True

    if no_entro:
        raise ex.ArgumentoInvalido(consulta)
