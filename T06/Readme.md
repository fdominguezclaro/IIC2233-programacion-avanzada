# Tarea 6
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___  

## Librerías utilizadas
  
- Pyqt5 
- random
- functools
- threading

## Para correrla hacerla funcionar es necesario tener canciones .wavs en el server.

## Comentarios de la Tarea 

- Las clases Server y Client me base mucho en el material de clase y en la actividad echa en clases, por lo tanto cualquier parecido a otra tarea es mera coincidencia

- Para guardar los usuarios y que estos puedan ingresar al programa, use un archivo llamado usuarios.txt, que contiene en sus lineas: ***usuario,puntos del usuario***

- Me guie por el enunciado, y por lo tanto supuse que las canciones iban a estar como artista - nombre.wav... Por lo tanto las canciones como artista _ -_ (sin espacio antes y despues del guion) nombre cancion.wav no son validas. 

- En el menu de salas, no encontre como hacer para crear botones dentro de un layout a una pagina de un stacked widget, por lo tanto hice una funcion que me los crea, muestra y otra que me los esconde.

- El diccionario self.canciones_actuales de la clase Server, contiene las canciones actuales que se estan tocando en las distintas salas, para asi poder enviarselas al cliente y poder actualizar las salas en el frontend.

- Cuando el cliente se mete a una sala, le entrega al servidor una lista de las canciones que tiene en el directorio Songs, el servidor le manda de vuelta todas las canciones que necesita para poder funcionar en esa sala. 
	
	- Es por esto que la primera vez que se mete a cada sala se demora un poco el programa. Pero una vez tiene las canciones bajadas ya deja de existir ese lag al ingresar a dicha sala. *(En mi casa se demoraba como 40 segundos en descargar 200mb...)*
	
	- Para que esto funcione no se le puede cambiar de nombre a las canciones que ya fueron bajadas por el cliente, ni se le pueden quitar canciones del servidor desde la primera vez que se corrio.

- Al enviar canciones, para prevenir que hubieran error de que se cruce con otro envio de datos, hice un booleano que las actualizaciones me las envia solo si no se estan enviando canciones. Trate de hacerlo con threading.Lock() pero no me funciono. 

- Si un jugador entra a una sala que la cancion ya ha empezado, estime que su tiempo de respuesta parte desde 0.

- A veces pasa que no se muestra la opcion correcta, para estoy hay que salir de la sala y volver a ingresar... No alcanze a arreglar este error.

- Alcanze a implementar el chat pero no con los emojis...
