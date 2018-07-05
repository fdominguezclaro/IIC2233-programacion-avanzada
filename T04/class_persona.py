class Persona:
    """Esta clase representa a una persona, que tiene nombre y un repr"""
    def __init__(self, nombre):
        """
        
        :param nombre: Nombre de la persona
        :type nombre: str
        """
        self.nombre = nombre

    def __repr__(self):
        return self.nombre
