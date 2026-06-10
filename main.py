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
        return self.hp > 0

    def Update_is_alive(self, health):
        if health > 0:
            self.aliveTime += 1
            return True
        else:
            self.aliveTime = 0
            return False


class player(character):
    player_xp = 0
    gold = 0
    inventory = []  # TODO: store collected items

    def level_up(self, xp):
        # TODO: Define XP progression for 25 levels (linear scaling)
        # TODO: Use cumulative XP system to determine level (250xp needed for lvl 1, 500xp for lvl 2, etc...)
        # TODO: Cap at max level (25) and handle extra XP overflow
        pass

    def equip(self, item):
        # TODO: Move item from inventory into equipped slot
        # TODO: Validate item type before equipping
        # TODO: Replace currently equipped item if needed
        pass

    def use_item(self, item):
        # TODO: Determine if item is consumable or equip-based or both...
        # TODO: Apply item effect (heal, buff, etc.)
        # TODO: Remove item if consumed
        pass


class enemy(character):
    xp_reward = 0
    loot_tools = []  # TODO: Define 25-item loot table with rarity distribution

    def drop_loots(self):
        # TODO: Roll chance (e.g., 30% drop rate)
        # TODO: If success, pick one random item from loot_tools
        # TODO: Return item
        # TODO: If fail, return None
        pass
