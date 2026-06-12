import os
import random
import subprocess

from colorama import Fore, Style, init

# autoreset=True means after every print() the color resets by itself
init(autoreset=True)


def clear_screen():
    # Clears the terminal so the menu always re-draws fresh
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


def hp_bar(current, maximum, width=20):
    # Builds a text bar:  [********--------] 100/200
    ratio = current / maximum if maximum > 0 else 0
    filled = round(ratio * width)
    bar = "*" * filled + "-" * (width - filled)

    # Change bar color based on how much HP is left
    if ratio > 0.5:
        color = Fore.GREEN
    elif ratio > 0.2:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    return f"{color}[{bar}] {current}/{maximum}"


def print_menu(player):
    # Redraws the main menu with the player's current stats
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "==========================================")
    print(Fore.CYAN + Style.BRIGHT + "          ⚔   WARRIOR'S PATH   ⚔        ")
    print(Fore.CYAN + Style.BRIGHT + "==========================================")
    print(f"  Name:    {Style.BRIGHT}{player.name}")
    print(
        f"  Level:   {Fore.YELLOW}{player.level}    XP: {Fore.CYAN}{player.player_xp}"
    )
    print(f"  HP:      {hp_bar(player.hp, player.max_hp)}")
    print(
        f"  ATK:     {Style.BRIGHT}{player.attack_power}    DEF: {Style.BRIGHT}{player.defense}"
    )

    # Only show the equipped line if the player has something equipped
    if player.equipped:
        print(Fore.GREEN + f"  Equipped: {player.equipped['name']}")
    print(Fore.CYAN + "------------------------------------------")
    print(Fore.YELLOW + "  [1]  Fight")
    print(Fore.YELLOW + f"  [2]  Inventory ({len(player.inventory)} items)")
    print(Fore.YELLOW + "  [3]  Equip Item")
    print(Fore.YELLOW + "  [4]  Use Item")
    print(Fore.YELLOW + "  [5]  Exit")
    print(Fore.CYAN + "==========================================")
    print()


def print_inventory(inventory):
    # Prints inventory grouped by item type for easier reading
    print()
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------")
    print(Fore.CYAN + Style.BRIGHT + "               INVENTORY                  ")
    print(Fore.CYAN + Style.BRIGHT + "------------------------------------------")
    if not inventory:
        print(Style.DIM + "  (empty)")
    else:
        # Group all items by their type key before printing
        grouped = {}
        for item in inventory:
            grouped.setdefault(item["type"], []).append(item["name"])
        for item_type, names in grouped.items():
            print(Fore.YELLOW + Style.BRIGHT + f"  [{item_type.upper()}]")
            for name in names:
                print(f"    - {name}\n")
    print(Fore.CYAN + "------------------------------------------")
    print()


def pause():
    # Holds the screen so the player can read output before the menu redraws
    input(Style.DIM + "  Press Enter to continue..." + Style.RESET_ALL)


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
        self.rare_pity = 0  # counts kills toward guaranteed rare drop
        self.boss_pity = 0  # counts fights toward guaranteed boss drop
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
            print(Fore.MAGENTA + Style.BRIGHT + f"  ✦ Pity reward: {reward['name']} ✦")

    def check_boss_pity(self):
        if self.boss_pity >= 10:  # 10 boss skills required
            reward = random.choice(self.boss_items)
            self.inventory.append(reward)
            self.boss_pity = 0  # resets pity back to 0
            print(
                Fore.MAGENTA
                + Style.BRIGHT
                + f"  ✦ Boss pity reward: {reward['name']} ✦"
            )

    def level_up(self, exp):
        self.player_xp += exp  # accumulate xp first
        # Each level requires level * 250 total XP
        for cur_level in range(1, 26):  # max lvl 25
            if self.player_xp < cur_level * 250:
                self.level = cur_level - 1
                return
        self.level = 25

    def equip(self, item):
        if item is None:
            return

        if item["type"] != "weapon":
            print(Fore.RED + "  Cannot equip this item.")
            return

        if item not in self.inventory:
            print(Fore.RED + "  Item not in inventory.")
            return

        self.inventory.remove(item)

        # Swap: send currently equipped weapon back to inventory before equipping new one
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
            print(Fore.RED + "  This item cannot be used at this current time.")

    def upgrade_stats(self):
        self.attack_power += 10
        self.defense += 5
        print(
            Fore.CYAN
            + f"  Stats upgraded! ATK: {self.attack_power} | DEF: {self.defense}"
        )


class Enemy(Character):
    def get_damage(self, target):
        # Damage is floored at 0 so defense can never cause negative damage
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
    def __init__(self, name="WhiteTiger"):
        super().__init__(name)
        self.hp = 300
        self.max_hp = 300
        self.attack_power = 25
        self.defense = 10
        self.xp_reward = 200
        self.enraged = False  # tracks whether enrage has triggered yet (one-time event)

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
            print(
                Fore.RED
                + Style.BRIGHT
                + f"  !! {self.name} is enraged! Attack surges! !!"
            )

    def get_damage(self, target):
        # calculating base damage
        base_damage = max(0, self.attack_power - target.defense)

        # 30% chance of special attack when enraged
        chance = random.random()  # gives a number between 0.0 and 1.0
        special_attack = self.enraged and chance < 0.3

        if special_attack:
            print(
                Fore.RED + Style.BRIGHT + f"  !! {self.name} uses a special attack! !!"
            )
            return base_damage * 2

        return base_damage


class WhiteTiger(Boss):
    def __init__(self):
        super().__init__(name="White Tiger")
        self.hp = 300
        self.max_hp = 300
        self.attack_power = 25
        self.defense = 10
        self.xp_reward = 200


class ShadowDragon(Boss):
    def __init__(self):
        super().__init__(name="Shadow Dragon")
        self.hp = 500
        self.max_hp = 500
        self.attack_power = 40
        self.defense = 20
        self.xp_reward = 400


class AncientGolem(Boss):
    def __init__(self):
        super().__init__(name="Ancient Golem")
        self.hp = 800
        self.max_hp = 800
        self.attack_power = 30
        self.defense = 35
        self.xp_reward = 600


# Character vs Enemy
class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def player_turn(self):
        damage = max(0, self.player.attack_power - self.enemy.defense)
        self.enemy.take_damage(damage)
        self.player.Update_is_alive(self.player.hp)
        print(Fore.GREEN + f"  You deal {damage} damage.   Enemy HP: {self.enemy.hp}")

    def enemy_turn(self):
        damage = self.enemy.get_damage(self.player)
        self.player.take_damage(damage)
        print(Fore.RED + f"  Enemy deals {damage} damage.  Your HP: {self.player.hp}")

    def check_Battle_end(self):
        if not self.enemy.is_alive():
            self.player.level_up(self.enemy.xp_reward)
            if not isinstance(self.enemy, Boss):  # only upgrade on normal kills
                self.player.upgrade_stats()
            print(
                Fore.CYAN
                + f"  Level: {self.player.level} | XP: {self.player.player_xp}"
            )

            loot = self.enemy.drop_loots()
            if loot:
                self.player.inventory.append(loot)
                print(Fore.YELLOW + f"  Loot: {loot['name']}")
            print(
                Fore.GREEN
                + Style.BRIGHT
                + f"  *** Victory! Survived {self.player.aliveTime} rounds. ***"
            )
            return True

        if not self.player.is_alive():
            print(
                Fore.RED
                + Style.BRIGHT
                + f"  *** Defeated after {self.player.aliveTime} rounds. ***"
            )
            return True
        return False

    def start(self):
        self.player.aliveTime = 0
        self.player.hp = self.player.max_hp
        print(Fore.CYAN + Style.BRIGHT + "==========================================")
        print(
            Fore.CYAN
            + Style.BRIGHT
            + f"  Battle: {self.player.name} vs {self.enemy.name}"
        )
        print(Fore.CYAN + Style.BRIGHT + "==========================================")
        print()

        # Alternate player and enemy turns until one side is dead
        while True:
            self.player_turn()
            if self.check_Battle_end():
                break
            self.enemy_turn()
            if self.check_Battle_end():
                break


if __name__ == "__main__":
    player1 = Player("Hero")

    while True:
        print_menu(player1)
        choice = input("  Choose: ").strip()

        if choice == "1":
            player1.rare_pity += 1
            player1.boss_pity += 1

            boss_roster = [WhiteTiger, ShadowDragon, AncientGolem]

            if player1.boss_pity >= 10:
                index = min(
                    player1.level // 5, len(boss_roster) - 1
                )  # pick a boss based on level, but never go past the last boss in the list.
                enemy1 = boss_roster[index]()
                print(Fore.RED + Style.BRIGHT + f"\n  *** A {enemy1.name} appears! ***")
            else:
                enemy1 = Enemy()

            Battle(player1, enemy1).start()

            player1.check_rare_pity()
            player1.check_boss_pity()
            pause()

        elif choice == "2":
            print_inventory(player1.inventory)
            pause()

        elif choice == "3":
            print_inventory(player1.inventory)
            name = input("  Item name to equip: ").strip()
            item = next((i for i in player1.inventory if i["name"] == name), None)
            if item is None:
                print(Fore.RED + "  Item not found.")
            else:
                player1.equip(item)
            pause()

        elif choice == "4":
            print_inventory(player1.inventory)
            name = input("  Item name to use: ").strip()
            item = next((i for i in player1.inventory if i["name"] == name), None)
            if item is None:
                print(Fore.RED + "  Item not found.")
            else:
                player1.use_item(item)
            pause()

        elif choice == "5":
            print(Fore.CYAN + f"\n  Farewell, {player1.name}.\n")
            break

        else:
            print(Fore.RED + "  Invalid choice.")
            pause()
