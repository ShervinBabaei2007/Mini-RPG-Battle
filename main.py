import random


# Character
class Character:
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


class Player(Character):
    def __init__(self, name):
        super().__init__(name)
        self.player_xp = 0
        self.gold = 0
        self.inventory = []
        self.rare_pity = 0
        self.boss_pity = 0
        self.equipped = None

    # Dictonary list
    rare_items = [
        {"name": "Dragon Scale", "type": "material"},
        {"name": "Mythic Core", "type": "material"},
        {"name": "Ancient Relic", "type": "material"},
        {"name": "Cursed Ring", "type": "accessory"},
        {"name": "Void Fragment", "type": "material"},
    ]

    boss_items = [
        {"name": "Celestial Shard", "type": "material"},
        {"name": "Godstone", "type": "material"},
        {"name": "Time Crystal", "type": "material"},
        {"name": "World Core", "type": "material"},
        {"name": "Reality Seed", "type": "material"},
    ]

    def check_rare_pity(self):
        if self.rare_pity >= 100:  # 100 kills required
            reward = random.choice(self.rare_items)
            self.inventory.append(reward)
            self.rare_pity = 0
            print(f"Pity reward: {reward}")

    def check_boss_pity(self):
        if self.boss_pity >= 10:  # 10 boss skills required
            reward = random.choice(self.boss_items)
            self.inventory.append(reward)
            self.boss_pity = 0
            print(f"Boss pity reward: {reward}")

    def level_up(self, exp):
        self.player_xp += exp  # accumulate xp first
        for cur_level in range(1, 26):  # max lvl 25
            if self.player_xp < cur_level * 250:
                self.level = cur_level - 1
                return
        self.level = 25

    def equip(self, item):
        if item is None:
            return

        if item["type"] != "weapon":
            print("Cannot equip this item.")
            return

        if item not in self.inventory:
            print("Item not in inventory.")
            return

        self.inventory.remove(item)

        if self.equipped is not None:
            self.inventory.append(self.equipped)

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


class Enemy(Character):
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
    ]

    def __init__(
        self, name="Enemy"
    ):  # a constructor that is going to hold this inventory
        super().__init__(name)
        self.inventory = []

    def drop_loots(self):
        total = sum(chance for _, chance, _ in self.loot_table)
        roll = random.uniform(0, total)
        cumulative = 0

        for name, chance, item_type in self.loot_table:
            cumulative += chance
            if roll <= cumulative:
                return {"name": name, "type": item_type}
        return None


# runs directly as a script
if __name__ == "__main__":
    player1 = Player("Hero")
    enemy1 = Enemy()

    while True:
        print("\n--- MENU ---")
        print("1. Fight enemy (drop loot)")
        print("2. View inventory")
        print("3. Equip item (by name)")
        print("4. Use item (by name)")
        print("5. Exit")

        choice = input("Choose action: ")

        if choice == "1":
            loot = enemy1.drop_loots()
            print("Dropped:", loot)

            if loot is not None:
                player1.inventory.append(loot)

            # pity system hook
            player1.rare_pity += 1
            player1.check_rare_pity()

        elif choice == "2":
            print("Inventory:", player1.inventory)

        elif choice == "3":
            name = input("Item name to equip: ")

            item = next(
                (item for item in player1.inventory if item["name"] == name), None
            )

            if item is None:
                print("Item not found.")
            else:
                player1.equip(item)

        elif choice == "4":
            name = input("Item name to use: ")

            item = next((i for i in player1.inventory if i["name"] == name), None)

            if item is None:
                print("Item not found.")
            else:
                player1.use_item(item)

        elif choice == "5":
            break

        else:
            print("Invalid choice")
