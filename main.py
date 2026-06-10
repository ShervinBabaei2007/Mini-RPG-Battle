# Character
class character:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 200
        self.attack_power = 1
        self.defense = 10
        self.level = 0
        self.aliveTime = 0

    # Character takes hits from an enemy
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:  # if character hp <= 0 it will reset and start over
            self.hp = 0

    # Character heals itself, if hp < maxhp
    def heal(self, amount_healthReg):
        if self.hp < self.max_hp:
            self.hp += amount_healthReg

        if self.hp >= self.max_hp:
            self.hp = self.max_hp

    # Character alive
    def is_alive(self):
        # TODO: Iterate the aliveTime counter when health is > 0
        # TODO: Reset aliveTime when hp <= 0
        return self.hp > 0
