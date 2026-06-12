# ⚔ Warrior’s Path

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)
![Style](https://img.shields.io/badge/Type-CLI%20RPG-orange)
![OOP](https://img.shields.io/badge/Architecture-OOP-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A terminal-based RPG combat system built in Python featuring turn-based battles, boss scaling, weighted loot drops, inventory management, and progression systems.

---

## 🎮 Gameplay Preview

```
==========================================
          ⚔   WARRIOR'S PATH   ⚔
==========================================

Name:    Hero
Level:   3    XP: 620
HP:      [********--------] 150/200
ATK:     25    DEF: 10
------------------------------------------
[1] Fight
[2] Inventory (6 items)
[3] Equip Item
[4] Use Item
[5] Exit
==========================================
```

---

## ⚔ Combat Example

```
Battle: Hero vs White Tiger

You deal 14 damage. Enemy HP: 186
Enemy deals 9 damage. Your HP: 191

!! White Tiger is enraged! Attack surges! !!
Enemy uses a special attack!

Loot: Dragon Scale
*** Victory! Survived 6 rounds. ***
```

---

## 📌 Core Features

### ⚔ Combat System

- Turn-based player vs enemy battles
- Damage formula:
  damage = max(0, attack_power - defense)
- Bosses:
  - White Tiger
  - Shadow Dragon
  - Ancient Golem
- Enrage mechanic at 50% HP
- Special attack chance (30% when enraged)

---

### 📈 Progression System

- Max level: 25
- XP formula:
  level threshold = level × 250 XP
- Stat growth:
  - +10 ATK
  - +5 DEF per normal kill

---

### 🎁 Loot System (Weighted RNG)

("Iron Sword", 40.0, "weapon")
("Dragon Scale", 1.0, "material")

Supports:

- weapons
- armor
- consumables
- materials
- accessories

---

### 🍀 Pity System

- Rare pity: 100 kills → guaranteed rare item
- Boss pity: 10 boss fights → guaranteed boss reward

---

### 🎒 Inventory System

{"name": "Iron Sword", "type": "weapon"}

- Equip weapons (1 slot)
- Use consumables
- Auto-swap equipment

---

### 🧠 Boss System

- Level 0–4 → White Tiger
- Level 5–9 → Shadow Dragon
- Level 10+ → Ancient Golem

Boss mechanics:

- HP scaling
- Enrage at 50% HP
- XP scaling

---

### 🖥️ UI System

- colorama-based terminal UI
- HP bar:
  🟢 High / 🟡 Mid / 🔴 Low
- Menu-driven gameplay

---

## 🧱 Architecture

Character → Player / Enemy → Boss

Battle controller handles combat loop.

Separation of:

- Combat logic
- Inventory system
- Progression system
- UI rendering

---

## 🛠 Tech Stack

- Python 3.10+
- OOP
- colorama
- random
- os + subprocess

---

## 🚀 Run

pip install colorama
python main.py

---

## 🎮 Controls

1 Fight
2 Inventory
3 Equip
4 Use
5 Exit

---

## 🔮 Future Roadmap

- Save/Load system
- Skills system
- Crit/dodge
- Status effects
- Equipment modifiers
- Procedural dungeons
- GUI version

---

## 👤 Author

Systems-focused Python RPG project:

- OOP architecture
- RNG systems
- CLI UI design
- Game loop engineering
