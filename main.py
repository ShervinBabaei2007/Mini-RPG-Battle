import random


# Character
class Character:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 200
        self.attack_power = 15
        self.defense = 5
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
            self.rare_pity = 0  # resets pity back to 0
            print(f"Pity reward: {reward}")

    def check_boss_pity(self):
        if self.boss_pity >= 10:  # 10 boss skills required
            reward = random.choice(self.boss_items)
            self.inventory.append(reward)
            self.boss_pity = 0  # resets pity back to 0
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

    def upgrade_stats(self):
        self.attack_power += 10
        self.defense += 5
        print(f"Stats upgraded! Attack: {self.attack_power} | Defense: {self.defense}")


class Enemy(Character):
    def get_damage(self, target):
        return max(0, self.attack_power - target.defense)

    # All enemy loots and chances
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
        self.xp_reward = 50
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


class Boss(Enemy):
    def __init__(self, name="White Tiger"):
        super().__init__(name)
        self.hp = 300
        self.max_hp = 300
        self.attack_power = 25
        self.defense = 10
        self.xp_reward = 200
        self.enraged = False

    # Boss takes damage from character
    def take_damage(self, amount):
        super().take_damage(amount)

        # checks if boss should enrage (only once, at half HP)
        half_hp = self.max_hp // 2
        already_enraged = self.enraged
        at_half_hp = self.hp <= half_hp

        if not already_enraged and at_half_hp:
            self.enraged = True
            self.attack_power += 15
            print(f"{self.name} is enraged! Attack surges!")

    def get_damage(self, target):
        # calculating base damage
        base_damage = max(0, self.attack_power - target.defense)

        # 30% chance of special attack when enraged
        chance = random.random()  # gives a number between 0.0 and 1.0
        special_attack = self.enraged and chance < 0.3

        if special_attack:
            print(f"{self.name} uses a special attack!")
            return base_damage * 2

        return base_damage


# Character vs Enemy
class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def player_turn(self):
        damage = max(0, self.player.attack_power - self.enemy.defense)
        self.enemy.take_damage(damage)
        self.player.Update_is_alive(self.player.hp)
        print(f"You deal {damage} damage. Enemy HP: {self.enemy.hp}\n")

    def enemy_turn(self):
        damage = self.enemy.get_damage(self.player)
        self.player.take_damage(damage)
        print(f"Enemy deals {damage} damage. Your HP: {self.player.hp}")

    def check_Battle_end(self):
        if not self.enemy.is_alive():
            self.player.level_up(self.enemy.xp_reward)
            if not isinstance(self.enemy, Boss):  # only upgrade on normal kills
                self.player.upgrade_stats()
            print(f"Level: {self.player.level} | XP: {self.player.player_xp}")

            loot = self.enemy.drop_loots()
            if loot:
                self.player.inventory.append(loot)
                print(f"Dropped: {loot['name']}")
            print(f"Victory! Survived {self.player.aliveTime} rounds.")
            return True

        if not self.player.is_alive():
            print(f"Defeated after {self.player.aliveTime} rounds.")
            return True
        return False

    def start(self):
        self.player.aliveTime = 0
        self.player.hp = self.player.max_hp
        print(f"\nBattle start: {self.player.name} vs {self.enemy.name}")
        while True:
            self.player_turn()
            if self.check_Battle_end():
                break
            self.enemy_turn()
            if self.check_Battle_end():
                break


if __name__ == "__main__":
    player1 = Player("Hero")
    enemy1 = Enemy()

    while True:
        print("\n--- MENU ---")
        print(f"Hero | Level {player1.level} | XP: {player1.player_xp}")
        print("1. Fight enemy (drop loot)")
        print("2. View inventory")
        print("3. Equip item (by name)")
        print("4. Use item (by name)")
        print("5. Exit")

        choice = input("Choose action: ")

        if choice == "1":
            player1.rare_pity += 1
            player1.boss_pity += 1

            if player1.boss_pity >= 10:
                enemy1 = Boss()
                print("A boss appears!")
            else:
                enemy1 = Enemy()

            battle = Battle(player1, enemy1)
            battle.start()

            player1.check_rare_pity()
            player1.check_boss_pity()

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
