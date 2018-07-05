# Tarea 1
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___
  
     
## Comentarios de la Tarea 
  
- En primer lugar destacar que se omitieron todos los tíldes y ñ's para evitar posibles errores en al ejecución del programa (excepto al ingresar usuario y contraseña. 

- Alguna de las funciones avanzadas no estan terminadas, por lo que podrian tener inconsistencias. 

###**Librerías utilizadas** 
  
  - Os: Para crear el nuevo directorio en que se agregarán los reportes de extinción.
  - Math: Para usar funciones relacionadas con areas y pitágoras.
  
  
###**Menú principal**
 Al ingresar la contraseña, consideré que:  

- No era necesario dar la opción de salir del inicio, ya que no estaba especificado en la rúbrica.  

- El programa lo creé en PyCharm, por lo tanto el uso de tíldes o ñ's no interrumpía la ejecución del programa, por lo tanto para lograr un ingreso correcto hay que escribir el nombre de usuario con los tíldes y ñ's correspondientes.  
  
- Cada vez que se ingrese la contraseña, será necesario ingresar la fecha y hora. Estime conveniente no ingresar los segundos, por lo tanto el tiempo "pasa en minutos".
      - La fecha está en formato yyyy/m/d
      - La hora está en formato h/mm    
  
En el **menu Anaf**:   

- Al consultar por leer una base de datos, se imprime la base completa. 
- Al crear un usuario, se le va a pedir un recurso ID al que asociarlo. 
  
###**Usuarios**:  

- Inicialmente todos se encuentran con estado actual Standby. Esto cambia cuando las estrategias creadas lo requieran.  

###**Archivos creados**:  

- El archivo **recursos_datos.txt**, lo uso para almacenar información extra de los recursos. las filas del archivos son (id-recurso, [ids-incendios-ayudados], horas-trabajadas, horas-standby)  
  
- El archivo **incendios_datos.txt**, lo uso para almacenar información extra de los recursos. las filas del archivos son (id-incendio, [ids-recursos-usados])  


###**Otros**:  

- Asumí que las fechas en los archivos serán tal cuál vienen en las bases de datos que nos entregaron (yyyy-mm-dd hh:mm:ss)  

- El algoritmo para ver que eventos ocurren antes o después, está basado en la función contar_minutos, que a cada fecha, la transforma en una cantidad de minutos. Por lo tanto comparo la cantidad de minutos de las dos fechas, y con esto, según si la resta es positiva o negativa puedo identificar que fecha es más antigua.   

- Para comparar si un reporte meteorológico se cruza con un incendio, usa una fórmula que compara la distancia entre dos puntos. Si esa distancia es menor o igual a la suma de los dos radios, entonces estos se intersectan.  

- Siempre que aparezca un i = 0, lo use para evitar leer la primera línea del archivo.
  