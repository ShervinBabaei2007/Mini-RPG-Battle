import random


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
    def __init__(self, name):
        super().__init__(name)
        self.player_xp = 0
        self.gold = 0
        self.inventory = []
        self.equipped = None

    def level_up(self, exp):
        level = 0  # setting base level
        for cur_level in range(1, 26):  # max lvl of 25
            xp_required = (
                cur_level * 250
            )  # XP required = level × 250 (linear progression, max level 25)

            if exp >= xp_required:
                level = cur_level
            else:
                break
        return level

    def inv(self, item):
        # Adding the item into inv
        if item is not None:
            self.inventory.append(item)

    def equip(self, item):
        if item is None:
            return

        # Item must exist in inv
        if item["type"] != "weapon":
            print("Cannot equip this item.")
            return

        # remove from inv
        self.inventory.remove(item)

        # replacing current equip item (if any)
        if self.equipped is not None:
            self.inventory.append(self.equipped)

        # equiping new item
        self.equipped = item

    def use_item(self, item):
        if item not in self.inventory:
            return

        # consumable for now
        if item["type"] == "consumable":
            # adding minor effect
            if item["name"] == "Healing Herb":
                self.heal(25)
            elif item["name"] == "Posion Vial":
                self.take_damage(10)
            # removing effect after usage
            self.inventory.remove(item)
        else:
            print("This item cannot be used at this current time.")


class enemy(character):
    xp_reward = 0
    loot_table = [
        ("Shards", 75.0, "material"),
        ("Healing Herb", 60.0, "consumable"),
        ("Wolf Pelt", 55.0, "material"),
        ("Rusty Dagger", 50.0, "weapon"),
        ("Iron Sword", 40.0, "weapon"),
        ("Leather Armor", 35.0, "armor"),
        ("Hunter Bow", 30.0, "weapon"),
        ("Steel Sword", 25.0, "weapon"),
        ("Fire Crystal", 15.0, "material"),
        ("Ice Crystal", 12.0, "material"),
        ("Thunder Fragment", 10.0, "material"),
        ("Poison Vial", 8.0, "consumable"),
        ("Knight's Emblem", 6.0, "accessory"),
        ("Dark Amulet", 5.0, "accessory"),
        ("Sunstone", 3.0, "material"),
        ("Dragon Scale", 1.0, "material"),
        ("Mythic Core", 0.75, "material"),
        ("Ancient Relic", 0.3, "material"),
        ("Cursed Ring", 0.2, "accessory"),
        ("Void Fragment", 0.125, "material"),
        ("Celestial Shard", 0.05, "material"),
        ("Godstone", 0.025, "material"),
        ("Time Crystal", 0.01, "material"),
        ("World Core", 0.005, "material"),
        ("Reality Seed", 0.00133, "material"),
    ]

    def __init__(self):  # a constructor that is going to hold this inventory
        self.inventory = []

    def drop_loots(self):
        roll = random.uniform(0, 100)  # 0% to 100%

        for (
            name,
            chance,
            item_type,
        ) in (
            self.loot_table
        ):  # loops through the item and the chance (%), returns an item
            if roll <= chance:
                return {"name": name, "type": item_type}
        return None
