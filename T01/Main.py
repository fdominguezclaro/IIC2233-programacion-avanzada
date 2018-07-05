import Menu
import os

encoding = 'utf-8'

# Creo un nuevo archivo para guardar informacion de los recursos
txt = open('recursos_datos.txt', 'a')
txt.close()

txt1 = open('incendios_datos.txt', 'a')
txt1.close()

# Creo directorio para meter los reportes
dir = (os.getcwd() + '/Reportes Estrategias de Extincion')
if not os.path.exists(dir):
    os.mkdir('Reportes Estrategias de Extincion')

# Inicio el programa
enter = Menu.Menu
enter()

