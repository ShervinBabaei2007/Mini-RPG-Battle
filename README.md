# Mini RPG Battle System (Python)

A turn-based RPG combat simulator featuring leveling, loot drops, boss fights, inventory management, and a test-driven core architecture built using Python OOP principles.

---

## Features

- Turn-based combat system (player vs enemies and bosses)
- XP-based leveling system (up to 25 levels)
- Weighted loot drop system with rarity tiers
- Boss fights with enraged phase at 50% HP
- Inventory system (equip + consumables)
- Pity system for rare and boss rewards
- Object-oriented architecture with inheritance
- Fully testable core mechanics using pytest

---

## Tech Stack

- Python 3.14
- pytest (unit testing)
- Object-Oriented Programming (OOP)
- CLI-based game loop

---

## Project Structure

```
main.py       # Core game logic (characters, combat, items, bosses)
test_game.py  # Unit tests using pytest
```

---

## How to Run

Run the game:

```bash
python main.py
```

Run tests:

```bash
python -m pytest
```

Expected output:

```
3 passed in 0.01s
```

---

## Core Systems

### Combat System

Turn-based combat between player and enemy.

- Damage formula:

  ```
  damage = attack_power - defense
  ```

- Battle ends when HP reaches 0
- Includes boss special attack behavior when enraged

### Leveling System

- XP is accumulated from battles
- Max level: 25
- Linear progression:

  ```
  level requirement = level × 250 XP
  ```

- Examples:
  - Level 1 → 250 XP
  - Level 2 → 500 XP
  - Level 10 → 2500 XP

### Loot System

Weighted probability-based drop system. Each item has a name, drop chance, and type:

```
("Iron Sword", 40.0, "weapon")
("Dragon Scale", 1.0, "material")
```

- Lower chance = rarer item
- System uses cumulative probability selection

### Boss System

Bosses replace normal enemies based on progression.

Boss types:

- White Tiger
- Shadow Dragon
- Ancient Golem

Mechanics:

- Enraged state triggers at 50% HP
- Attack power increases when enraged
- Special attack chance during enraged state

### Inventory System

Items are stored as dictionaries:

```python
{"name": "Iron Sword", "type": "weapon"}
```

Supported operations:

- Add item
- Remove item
- Equip weapons
- Use consumables

Validation rules:

- Only weapons can be equipped
- Only consumables can be used
- Items must exist in inventory before action

### Pity System

Prevents bad RNG streaks.

- **Rare pity:** triggers every 100 kills - rewards rare material
- **Boss pity:** triggers every 10 boss kills - guarantees boss-tier item

---

## Example Gameplay Output

```
Battle start: Hero vs White Tiger
You deal 14 damage
Enemy deals 9 damage
White Tiger is enraged!
Dropped: {"name": "Dragon Scale", "type": "material"}
Victory! Survived 6 rounds.
```

---

## Testing

All core systems are validated using automated unit tests.

Coverage includes:

- Player level progression
- Damage and HP boundary conditions
- Boss enraged state transitions
- Loot drop correctness
- Inventory add/remove logic

Run tests:

```bash
python -m pytest
```

Expected output:

```
3 passed in 0.01s
```

---

## Design Notes

- Fully object-oriented design: `Character → Player → Enemy → Boss`
- Clear separation of concerns:
  - Combat system
  - Inventory system
  - Progression system
- Extensible architecture for adding new bosses, items, and mechanics
- Designed for testability and simulation correctness
- CLI-based prototype (can be extended to GUI or web)

---

## Future Improvements

- Save/load system (JSON persistence)
- Skill and ability system
- Critical hit system
- Status effects (poison, burn, freeze)
- Procedural dungeon generation
- GUI version (Tkinter or web frontend)
- Equipment stat modifiers and set bonuses

---

## Author

Built as a learning project focused on:

- Python OOP design
- Game system architecture
- Unit testing with pytest
- Simulation-based gameplay logic
