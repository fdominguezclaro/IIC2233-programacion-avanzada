class Tower:
    def __init__(self, pos, team, constantes):
        self.pos = pos
        self.nombre = 'tower'
        self.constantes = constantes
        self.team = team
        self.att_range = self.constantes['att_range_tower']
        self.att_speed = self.constantes['att_speed_tower']
        self.strengh = self.constantes['strengh_tower']
        self.health_initial = self.constantes['health_tower']
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1


class Nexo:
    def __init__(self, team, constantes):
        self.team = team
        self.nombre = 'nexo'
        self.constantes = constantes
        self.health_initial = self.constantes['health_nexo']
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1


class Shop:
    def __init__(self, posicion, constantes):
        self.constantes = constantes
        self.nombre = 'shop'
        self.posicion = posicion
        self.froustmourne_cost = self.constantes['cost_froustmorne']
        self.froustmourne_upgrade = self.constantes['upgrade_froustmorne']
        self.ballesta_cost = self.constantes['cost_ballesta']
        self.ballesta_upgrade = self.constantes['upgrade_ballesta']
        self.boots_cost = self.constantes['cost_boots']
        self.boots_upgrade = self.constantes['upgrade_boots']
        self.objeto_magico_cost = self.constantes['cost_objeto_magico']
        self.objeto_magico_upgrade = self.constantes['upgrade_objeto_magico']
        self.armadura_cost = self.constantes['cost_armadura']
        self.armadura_upgrade = self.constantes['upgrade_armadura']
        self.carta_cost = self.constantes['cost_carta']
        self.carta_upgrade = self.constantes['upgrade_carta']


class Inhibidor:
    def __init__(self, team, constantes):
        self.team = team
        self.nombre = 'inhibidor'
        self.constantes = constantes
        self.health_initial = self.constantes['health_inhibidor']
        self.health = self.health_initial

    @property
    def health_bar(self):
        return int((self.health / self.health_initial) * 100) - 1
