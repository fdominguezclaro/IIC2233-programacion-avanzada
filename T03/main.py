import sys

import Exceptions as ex
import interprete as i
from PyQt5 import QtWidgets
from gui.Gui import MyWindow


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        # Para generar el archivo uso estas dos variables
        self.contador = 1
        self.guardar = ''
        with open('resultados.txt', 'w') as arc:
            # Creo mi archivo
            pass

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!

        for consulta in querry_array:
            try:
                procesado = str(i.interprete(consulta))

                # Con este if vemos si existe la funcion pedida. Para esto verificamos que la entrada y salia sean distintas
                if procesado == str(consulta):
                    raise ex.ImposibleProcesar('No existe esa funcion')

                self.guardar += '\n\n---- Consulta {} ----\n'.format(self.contador)
                self.contador += 1
                self.add_answer(procesado + '\n\n')
                self.guardar += procesado

            except (ex.ErrorDeTipo, ex.ErrorMatematico, ex.ImposibleProcesar, ex.ArgumentoInvalido,
                    ex.ReferenciaInvalida, NameError) as err:
                self.add_answer('\nError de consulta: ' + str(err.comando) + '\nCausa: ' + str(err.nombre) + '\n\n')
                self.guardar += '\n\n---- Consulta {} ----\n'.format(self.contador)
                self.contador += 1
                self.guardar += '\nError de consulta: ' + str(err.comando) + '\nCausa: ' + str(err.nombre) + '\n'

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        with open('resultados.txt', 'a') as arc:
            arc.write(self.guardar)
        self.guardar = ''


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
