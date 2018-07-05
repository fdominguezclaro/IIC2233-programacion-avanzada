class ArgumentoInvalido(Exception):
    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Argumento Invalido'
        super().__init__()


class ReferenciaInvalida(Exception):
    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Referencia Invalida'
        super().__init__()


class ErrorDeTipo(Exception):
    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Error de tipo'
        super().__init__()


class ErrorMatematico(Exception):
    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Error Matematico'
        super().__init__()


class ImposibleProcesar(Exception):
    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Imposible procesar'
        super().__init__()
