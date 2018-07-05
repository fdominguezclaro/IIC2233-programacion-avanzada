# Tarea 4
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___  

###**Librerías utilizadas** 
  
- csv 
- os
- random
- math
- numpy
- matplot


## Nota importante: 

Estimado corrector,  

Hoy en la ayudantía, el malvado ayudante me dijo que mi tarea tenia programación circular, cosa que está prohibido para esta tarea... Al programarla, traté de no usarla, pero en momentos de desesperación no me di cuenta que la usé. En la actividad de expeciones y testing, el profesor me dijo que mi expecion personalizada tenga como atributo el programa principal, para así tratarlo más fácil.


Mis eventos los traté como clases, y alguno de estos tienen como atributos la simulación. Para hacer esto me basé en lo que el profesor me dijo en la actividad antes mencionada, por lo que nunca pensé que estaba cometiendo un error... De echo, por las issues que leí, pensé que la programación circular solo se asociaba al llamado de funciones, y no al heredar o instanciar clases y objetos.

Las clases que tienen como atributo la simulación, no era estrictamente necesario que lo tuvieran, de echo no lo usan para ningun proceso clave de la simulación. De echo podría haberle pasado directamente el atributo que fuera a usar... Pero como no sabía que no podía usarlo, pensé que no estaba haciendo nada malo... De echo en parte lo hice porque pensé que podría facilitar la lectura del código.

No escribo para excusarme por este problema, pero consideré que era mejor aceptar mi error y hacercelos saber antes de que revisen mi tarea.

Prometo no volver a cometer dicho error. xD    

Muchas gracias, 


## Comentarios de la Tarea 

- No se que versión de mi tarea se alcanzó a subir... En la parte de ver las estadisticas, cada vez que pide un input para mostrar datos, se me olvido poner que el la comparacion debe ser de int - int o str - str... Por lo tanto, en las lineas 392, 397, 409, 414, 422, al numero que se le compara la respuesta debe ser str (if elegir == str(1) o etc...)


- En la carpeta hay un archivo parametros.csv... La simulación va a tomar todos los valores por defecto de este archivo, por lo tanto cualquier valor por defecto que se quiera modificar se puede hacer directamente desde este archivo.

- Para correr la simulacion, hay que correr el archivo main.py

- En las cátedras, para que un alumno escuche un tip, supuse de que la probabilidad de escucharlo o no es del 50%, ya que generalmente hay muchos alumnos leyendo el material a último minuto, por lo que no estás muy concentrados :P.
 
- Para las notas de cada alumno, tienen un atributo (diccionario) para tareas, actividades y controles, cada key es una lista de la forma [nota obtenida, nota esperada]. Las primeras dos (tareas y actividades), vienen predefinidos, en que están las evaluaciones enumeradas hasta 6 o 12, y nota obtenida = nota esperada = 1.

- Para las ayudantías consideré que hay dos ayudantías por semana, una por cada ayudante de docencia que salió elegido para dictar ayudantía. El total de los alumnos se dividen entre esas dos ayudantías, independiente que se mezclen secciones.

- En el módulo eventos.py, se encuentran las distintas clases que representan cada evento.

- Para estimar una nota esperada por el alumno, a las horas estudiadas * 0.3 le puse un round(), ya que habian numeros que quedaban sin un intervalo.

- Consideré que las clases son los jueves, las consultas los miércoles, ayudantias los martes, reunión docencia lunes. 

- La simulación comienza un día viernes, para simplificar el estudio de los alumnos. Entonces todos los viernes se define cuanto estudiará cada alumno esa semana.

- La mayoría de los eventos recibe como parámetro la clase simulación, para asi poder trabajar de manera mas fácil con los distintos elementos de la simulación.

- Para simplificar el código lo más posible, trate de hacer la mayor cantidad de funciones posibles fue de la funcion simular (Como por ejemplo los metodos de las clases de eventos, y la clase estudiante).

- Para los controles, aunque hayan 3 cátedras distintas, estimé que son coordinados (ya que a el malvado Dr. Mavrakis no le gusta estar haciendo controles todas las semanas).

- Para las tareas, como las tareas se reparten entre dos contenidos, considere mejor poner una tarea para cada contenido y repetir la nota

- Para las dudas en clases, los alumnos de esta dimensión son muy ansiosos, por lo tanto o preguntan todas las dudas que tengan, o no preguntan ninguna.
 
- Para el promedio del ramo, a ver si van a hacer consultas al profesor, la formula es: controles * 0.2 + actividades * 0.3 + tareas * 0.5. Para el promedio del ramo a fin de semestre consideré la misma fórmula que para nosotros en la vida real. 

- Si la confianza es menor a 0, estimé que va a ser 0.

- Al terminar la simulación y preguntar por el nombre de algun alumno, las notas del alumno vienen en el siguiente formato:
	- Actividades y controles [nota obtenida, nota esperada]
	- Tareas: [nota obtenida, nota esperada, horas dedicadas]
