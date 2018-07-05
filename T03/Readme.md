# Tarea 3
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___  

###**Librerías utilizadas** 
  
- functools: Para usar reduce

- os: Para verificar si el archivo pedido con os.path.exists(file).

- Itertools: Usé la función tee para poder usar el mismo generador dos veces. 

## Comentarios de la Tarea 

  
- Todas las variables asignadas en el programa, se guardan dentro de RQL_dic.diccionario.
 
- Para graficar, la función normalizado, consideré que los valores negativos serán tomados como tal. 

- Consideré que para cuando hay factoriales, solo puedan usarse numeros enteros. 

- Para la funcion save_file del main, el parametro querry-array no lo usé, pero no quise borrarlo, para dejar lo más intacta posible la función original que nos entregaron.

- En la interfaz, al apretar realizar todas las consultas, no encontré la forma de hacer que se grafiquen los dos gráficos, sólo se grafica uno, y al cerrarlo no aparece el otro. Entonces le puse plt.ion(), que fue lo que encontré en google para que el programa siga ejecutándose.

- Para los errores, les cambié el formato al que pedían por uno mas legible, sin perder los datos importantes que debe tener.

- Para las excepciones, creé mis propias excepciones, porque me pareció mas entendible para leer el código.

- Para el testing de las excepciones, cada excepcion que creé tiene un self.nombre, por lo tanto lo que hago es que si la excepcion.nombre que se levantó es igual a la excepción probada, entonces es correcto. 


 