# Estructura basica


class Nodo:
    # Creo la estructura del nodo
    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor

    def __repr__(self):
        return str(self.valor)


class ListaLigada:
    #  Creo la lista ligada
    def __init__(self, *valores):
        self.ultimo = None
        self.primero = None
        self.len = 0
        for valor in valores:
            if isinstance(valor, list):
                for elemento in valor:
                    self.append(elemento)
            else:
                self.append(valor)

    def append(self, *valores):
        for valor in valores:
            if valor == '':
                pass
            elif not self.primero:
                # Revisamos si el nodo primero tiene un nodo asignado.
                # Si no tiene nodo, creamos un nodo.
                self.primero = Nodo(valor)
                self.ultimo = self.primero
            else:
                # Si ya tiene un nodo
                self.ultimo.siguiente = Nodo(valor)
                self.ultimo = self.ultimo.siguiente

            self.len += 1

    def pop(self, i=None):

        #  Basado en material encontrado en http://librosweb.es/libro/algoritmos_python/capitulo_16/la_clase_
        #  listaenlazada.html

        if self.len == 0:
            # Si la lista está vacía, no hay nada que borrar.
            raise ValueError('Lista vacía')

        # Si se llama a pop(), se asume que i va a ser el ultimo elemento
        if i is None:
            i = self.len - 1

        if (i < 0) or (i >= self.len):
            raise IndexError('Indice fuera del rango permitido')

        # Si se borra el nodo primero, hay que tratarlo como un caso especial.
        if i == 0:
            eliminado = self.primero.valor
            self.primero = self.primero.siguiente

        # Caso general
        else:
            nodo_actual = self.primero
            for pos in range(0, i):
                nodo_anterior = nodo_actual
                nodo_actual = nodo_anterior.siguiente
            eliminado = nodo_actual.valor
            nodo_anterior.siguiente = nodo_actual.siguiente

        self.len -= 1
        return eliminado

    def remove(self, valor):

        #  Basado en material encontrado en http://librosweb.es/libro/algoritmos_python/capitulo_16/la_clase_
        #  listaenlazada.html
        if self.len == 0:
            raise ValueError('Lista vacía')

        elif self.primero.valor == valor:
            self.primero = self.primero.siguiente

        # Caso general
        else:
            nodo_anterior = self.primero
            nodo_actual = nodo_anterior.siguiente
            while (nodo_actual is not None) and nodo_actual.valor != valor:
                nodo_anterior = nodo_actual
                nodo_actual = nodo_anterior.prox

            # Si no encontro ese valor
            if nodo_actual is None:
                raise ValueError('Valor no encontrado')

            else:
                nodo_anterior.siguiente = nodo_actual.siguiente

        self.len -= 1

    def insert(self, i, valor):

        if (i > self.len) or (i < 0):
            # error
            raise IndexError("Posición inválida")

        nuevo = Nodo(valor)

        if i == 0:
            nuevo.siguiente = self.primero
            self.primero = nuevo

        # Caso general
        else:
            nodo_anterior = self.primero
            for pos in range(1, i):
                nodo_anterior = nodo_anterior.siguiente
            nuevo.siguiente = nodo_anterior.siguiente
            nodo_anterior.siguiente = nuevo

        self.len += 1

    def is_in(self, valor):
        nodo_actual = self.primero
        while nodo_actual:
            if nodo_actual.valor == valor:
                return True
            nodo_actual = nodo_actual.siguiente
        return False

    def index(self, valor):
        nodo = self.primero
        indice = 0
        for i in range(0, self.len):
            if nodo:
                if nodo.valor == valor:
                    return indice
                else:
                    nodo = nodo.siguiente
            indice += 1
            if not nodo:
                print('No existe el valor: ' + str(valor))

    def sort(self):
        # Metodo basado de la paguina en internet https://github.com/M2skills/Linked-List-in-Python
        actual = self.primero
        while True:
            sorteado = False
            while actual:
                # Hasta que actual sea None
                if actual.siguiente is not None:
                    if actual.valor > actual.siguiente.valor:
                        valor = actual.valor
                        actual.valor = actual.siguiente.valor
                        actual.siguiente.valor = valor
                        sorteado = True

                actual = actual.siguiente

            if not sorteado:
                #  Se va a repetir hasta que ya no quede nada que sortear
                break
            else:
                actual = self.primero
                # Vuelve el ciclo

    def __delitem__(self, key):

        if self.len == 0:
            raise ValueError('Lista vacía')

        if (key < 0) or (key >= self.len):
            raise IndexError('Indice fuera del rango permitido')

        elif key == 0:
            self.primero = self.primero.siguiente

        else:
            contador = 0
            nodo_anterior = self.primero
            nodo_actual = nodo_anterior.siguiente
            while (nodo_actual is not None) and contador != key:
                nodo_anterior = nodo_actual
                nodo_actual = nodo_anterior.prox
                contador += 1
            # Si no encontro ese valor
            if nodo_actual is None:
                raise ValueError('Valor no encontrado')

            else:
                nodo_anterior.siguiente = nodo_actual.siguiente

            self.len -= 1

    def __setitem__(self, key, valor):
        if self.len == 0:
            # Si la lista está vacía, no hay nada que borrar.
            raise ValueError('Lista vacía')

        if (key < 0) or (key >= self.len):
            raise IndexError('Indice fuera del rango permitido')

        nodo_anterior = self.primero
        nodo_actual = nodo_anterior.siguiente
        for pos in range(1, key):
            nodo_anterior = nodo_actual
            nodo_actual = nodo_anterior.siguiente
        nodo_actual.valor = valor

    def __getitem__(self, indice):
        if (indice < 0) or (indice >= self.len):
            raise IndexError('Indice fuera del rango permitido')
        nodo = self.primero
        for i in range(indice):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            print('no existe')
        else:
            return nodo.valor

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual
            actual = actual.siguiente

    def __len__(self):
        #  Para este metodo, lo unico que hice fue que cada vez que agrego/elimino un elemento a la lista modifico el
        #  atributo len.
        return self.len

    def __repr__(self):
        rep = ''
        nodo_actual = self.primero
        i = 0
        while nodo_actual:
            if i == 0:
                rep += '{0}'.format(nodo_actual.valor)
                nodo_actual = nodo_actual.siguiente
                i += 1
            else:
                rep += ', {0}'.format(nodo_actual.valor)
                nodo_actual = nodo_actual.siguiente

        return rep


# Creo la clase Queue, que hereda de la clase ListaLigada, y le agrego los dos metodos caracteristicos de las colas
class Queue(ListaLigada):
    def enqueue(self, valor):
        self.append(valor)

    def dequeue(self):
        out = self.primero
        self.primero = self.primero.siguiente
        self.len -= 1
        return out


def orden(file):
    #  Esta funcion la use como base para las funciones que identifican en que orden estan las columnas
    with open(file, 'r', encoding='utf8') as data:
        order = data.readline()
        order = order.strip('\n')
        if ',' in order:
            linkedlist = ListaLigada(order.split(','))
        if ';' in order:
            linkedlist = ListaLigada(order.split(';'))
        fila = ListaLigada()
        for i in linkedlist:
            i = i.valor.strip()
            fila.append(i)
    return fila


def orden_poblacion():
    #  Me retorna una lista ligada, con dos elementos, el primero el indice de la columna Pais, el segundo es el
    #  indice de la columna Poblacion
    orden_datos = orden('population.csv')
    pos_pais = orden_datos.index('Pais')
    pos_pob = orden_datos.index('Poblacion')
    return ListaLigada(pos_pais, pos_pob)


def orden_borders():
    #  Me retorna una lista ligada, con dos elementos, el primero el indice de la columna Pais 1, el segundo es el
    #  indice de la columna Pais 2
    orden_datos = orden('borders.csv')
    pos_pais1 = orden_datos.index('Pais 1')
    pos_pais2 = orden_datos.index('Pais 2')
    return ListaLigada(pos_pais1, pos_pais2)


def orden_random_airports():
    #  Me retorna una lista ligada, con dos elementos, el primero el indice de la columna Pais 1, el segundo es el
    #  indice de la columna Pais 2
    orden_datos = orden('random_airports.csv')
    pos_pais1 = orden_datos.index('Pais 1')
    pos_pais2 = orden_datos.index('Pais 2')
    return ListaLigada(pos_pais1, pos_pais2)
