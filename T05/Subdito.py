import Unit


class WeakSubdito(Unit.Unit):
    def __init__(self, team, constantes):
        self.constantes = constantes
        super().__init__(team, self.constantes['speed_weak_subdito'],
                         self.constantes['strengh_weak_subdito'], self.constantes['att_speed_weak_subdito'],
                         self.constantes['att_range_weak_subdito'])

        self.health_initial = self.constantes['health_weak_subdito']
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1


class StrongSubdito(Unit.Unit):
    def __init__(self, team, constantes):
        self.constantes = constantes
        super().__init__(team, self.constantes['speed_strong_subdito'],
                         self.constantes['strengh_stong_subdito'], self.constantes['att_speed_strong_subdito'],
                         self.constantes['att_range_strong_subdito'])
        self.health_initial = self.constantes['health_strong_subdito']
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1

    def hulk(self):
        self.healh = self.constantes['health_hulk_subdito']
        self.speed = self.constantes['speed_hulk_subdito']

    def nothulk(self):
        self.healths = self.constantes['health_strong_subdito']
        self.speed = self.constantes['speed_strong_subdito']
