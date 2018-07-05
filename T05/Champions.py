from Unit import Unit


class Arthas(Unit):
    def __init__(self, team, constantes):
        self.constantes = constantes
        super().__init__(team, self.constantes['speed_arthas'],
                         self.constantes['strengh_arthas'], self.constantes['att_speed_arthas'],
                         self.constantes['att_range_arthas'])
        self.name = 'Arthas'
        self.vivo = True

        self.health_initial = self.constantes['health_arthas']
        self.puntos = 0
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1


class Chau(Unit):
    def __init__(self, team, constantes):
        self.constantes = constantes
        super().__init__(team, self.constantes['speed_chau'],
                         self.constantes['strengh_chau'], self.constantes['att_speed_chau'],
                         self.constantes['att_range_chau'])
        self.name = 'Chau'
        self.vivo = True
        self.health_initial = self.constantes['health_chau']
        self.puntos = 0
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1


class Hernan(Unit):
    def __init__(self, team, constantes):
        self.constantes = constantes
        super().__init__(team, self.constantes['speed_hernan'],
                         self.constantes['strengh_hernan'], self.constantes['att_speed_hernan'],
                         self.constantes['att_range_hernan'])
        self.name = 'Hernan'
        self.vivo = True
        self.health_initial = self.constantes['health_hernan']
        self.puntos = 0
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1
