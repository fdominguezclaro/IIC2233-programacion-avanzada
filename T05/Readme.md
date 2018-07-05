# Tarea 5
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___  

###Librerías utilizadas
  
- Pyqt5 
- Math
- Sys
- Random


## Comentarios de la Tarea 

- En primer lugar disculparme por la calidad de mi tarea, la partí haciendo el viernes 2 de junio (tres días antes de la entrega) por que habia tenido dos semanas llenas de pruebas y tenía que salvar 2 ramos :( ... Asi que traté de hacer lo más que pude en estos días (dormí como 4  horas por día haciéndola jaja), pero valió la pena, es la más entretenida que hemos echo por ahora. Por esto mismo la presentación y el formato no es el mas bonito ni llamativo, pero no tuve tiempo para dedicarle a la parte estética.

- En archivo Backend.py se encuentran todos los QObjects que interactuan con el Frontend. Cada uno de estos objetos tiene instanciado dentro una clase segun corresponda (en el QObject respectivo a Character se encuentra self.champion = Champions.Champion)

- No pude encontrar un sprite para chau, por lo que la dejé como una persona con pistola. Con respecto a los subditos, deje que fueran un sprite para los dos tipos, solo que uno mide 30x30 y el otro 40x40.

- En la tienda, cambié los nombres de los objetos por nombres equivalentes pero un poco más originales (frostmourne es la espada de Artas en warfcraft 3 :D).

- En el archivo constante.csv se encuentran las constantes del juego. Este archivo es leido por funciones.leer_constantes, que las guarda en un diccionario que es usado para crear las distintas clases. 

- Para partir, hay que hacer click en alguna parte del mapa, ahi el personaje va a empezar a mirar a la posicion del mouse.

- Los botones de menu, tienda y pausa los dejé en el menu bar, así no molestaban en la pantalla.

- Para lograr identicar cuando el mouse estaba por sobre un label, descubrí los metodos EnterEvent y leaveEvent, por lo tanto cree una clase FLabel, que redefine estos eventos.

- Me costó mucho evitar la referencia circular al momento de identificar cuando el mouse pasaba por sobre un label, pero al final logre arreglarlo emitiendo una señal hasta el QObject correspondiente, y que luego este mandara una señal hasta el Frontend.

- No se si hay algo mal con mi función de atacar o que pero Hernan, que tiene muy poco rango le resulta casi imposible atacar en la mayoria de las veces. Y además los subditos los agregué a ultimo momemnto por lo que no me quedaron atacables, pero los edificios si.

- Con respecto a que el jugador siga el mouse, trate de hacerlo que no logré que funcione perfecto... Antes había echo otro tipo de movimiento, que se mueva independiente de la posición del mouse, así que si quieren dejarlo de esta manera (Para poder mover al jugador y evaluar los otros aspectos) en el modulo Backend, clase Character, pueden cambiarle las funciones move_right, move_left, move_front y move_back por las funciones con el mismo nombre de la clase Champion Enemigo.

- Se crea el campeon enemigo, y tambien los subditos (elegi solo que se creen 1 subdito weak y uno strong) para no estorbar tanto la pantalla), pero estos solo caminan en direccion hacia el enemigo... No alcance a automatizarlos.

- La metodología que usé para la tarea fue que al crear el juego, el frontend instancia QObjects del backend... Estos a su vez crean los QLabels respectivos y instancian a sus respectivas unidades... Por lo tanto lo QObjects son los intermediarios entre las dos partes del programa... Usé threads en vez de QTimers, y me pareció mas ordenado hacer que dentro de los QObjects, se creen Qtimers que esten dirigos a alguna función en específica.
