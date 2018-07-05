import clases
import connections_generator as cg
import edd


def inicio():
    while True:
        print('\nBienvenid@ a un nuevo juego de Pandemic\n')

        while True:
            print('1. Cargar una partida')
            print('2. Empezar una nueva partida')
            print('3. Salir')
            opcion = str(input('\nQue deseas hacer: '))
            opciones = edd.ListaLigada('1', '2', '3')
            if opciones.is_in(opcion):
                break
            else:
                print('\nIngresa una opcion correcta\n')

        if opcion == '3':
            raise SystemExit()
        elif opcion == '1':
            mundo = clases.Mundo('cargar')
        elif opcion == '2':
            mundo = clases.Mundo('nueva')


if __name__ == '__main__':
    cg.generate_connections()
    inicio()
