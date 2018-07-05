# Tarea 2
___

Felipe Domínguez C  
*fdominguezc@uc.cl*  
1562188J  
___  

###**Librerías utilizadas** 
  
- random: Para elegir un número al azar entre 0 y 6, para la gente que muere cada día. 

- math: Para redondear numeros para abajo con la funcion floor   

## Comentarios de la Tarea 

  
- El cuerpo del programa tuvo algunos cambios leves con respecto al diagrama de clases. Estos fueron para hacer arreglos menores, o para simplificar el código. Pero la estructura general del programa sigue igual. 

- El "gobierno" consideré que era mejor hacerlo dentro de la función pasar de día, de la clase mundo. Ahí se toman las decisiones, se agregan a la cola y después se ejecutan las 3 con mayor prioridad.

- Para la progagación de la enfermedad, consideré que un país ya infectado, no admite que se contagien mas personas por medio de la propagación de otros países.

- Al propagar la enferdad entre países, un país que recibió la enferdad un día, la puede propagar ese mismo dia a otro país (Los tiempos de viaje los consideré como infinitesimales).

- Para las estadísticas, mi método era que al comienzo de cada día reseteo algunos atributos de la clase mundo, y las modifico durante ese día, para asi poder usarlas en las estadísticas. 

- La fecha del juego, consideré que se parte del día 0 (día en que se implanta la infección).

- Si bien implementé el método sort, este no lo usé, si no que usé sorted, ya que en ese caso era más útil.

- Las fórmulas en general no son muy correctas, ya que algunas cosas no están bien calculadas y el juego tiende a no ser muy "correcto".


- La fórmula de contagio entre países, decidí modificarla, y en vez de ser **0.07** x ..., la cambié por **7** x ...

- La fórmula de descubrir cura, decidí modificarla, y en vez de ser **poblacion mundial ^3**..., la cambié por **poblacion mundial ^2** ... 
 
- La fórmula de muertes de personas, esta muy alta yo creo, no quise modificarla, pero las personas mueren demasiado rapido para poder desarrollar bien el juego.

 