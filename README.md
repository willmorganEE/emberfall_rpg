# EMBERFALL — Terminal RPG

A modular, terminal-based Python RPG built for the ET2100 project. It includes account registration/login, TinyDB saves, inheritance, combat, skills, quests, NPCs, a shop, inventory, and two tile maps.

## Run in VS Code

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   ```

   Activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`

5. Install the packages:

   ```bash
   uv add colorama tinydb
   ```

   If you do not have `uv`, install it first, or use `pip install -r requirements.txt`.

6. Start the game:

   ```bash
   python main.py
   ```

The first run creates `emberfall_data.json` in the project folder. **Do not delete this file** if you want to keep accounts and saved games.

## Controls

- Use `W`, `A`, `S`, `D` to move one tile.
- Talk when standing on a green landmark (`◆`).
- Use numbered menu options for actions.
- Combat lets you use learned skills, healing potions, or flee (the final boss cannot be fled).
- The game autosaves after movement, NPC interactions, shop purchases, travel, and explicit saves.

## Story / objective

1. Speak with Elder Rowan in Greenreach.
2. Collect 3 Ember Shards from monsters.
3. Speak with Captain Brann to unlock the Sunken Crypt.
4. Enter the Crypt and defeat the Ember Warden.

Side quests:
- Mira: bring 3 Moonleaf Herbs for gold and XP.
- Tovin: defeat 2 Goblins for 45 gold and 40 XP; he also explains skill progression.

## Project map

| File | Responsibility |
|---|---|
| `main.py` | Main menu and application entry point |
| `game.py` | Main game loop, story, movement, menus, autosaving |
| `player.py` | Player state, leveling, XP, stats, serialization |
| `monster.py` | Monster base class and five monster types |
| `skill.py` | Skill base class and skill subclasses |
| `combat.py` | Turn-based battle logic |
| `inventory.py` | Item counts and inventory operations |
| `item.py` | Item definitions and item lookup |
| `quest.py` | Main and side quest state/progression |
| `npc.py` | Five NPCs and dialogue/interactions |
| `shop.py` | Gold purchases and permanent upgrades |
| `world_map.py` | Map layouts, walls, movement collision, NPC positions |
| `database.py` | TinyDB account/save persistence |
| `auth.py` | Registration, password hashing, login |
| `ui.py` | Terminal colors, panels, prompts, validation |
| `config.py` | Shared game settings |

## How TinyDB saving works

TinyDB stores JSON-compatible Python data. This project uses two tables:
- `accounts`: username, random salt, and PBKDF2 password hash.
- `saves`: username and a nested `data` dictionary.

Before saving, `Player.to_dict()` converts the player's state into ordinary strings, numbers, lists, dictionaries, and booleans. `GameDatabase.save_game()` uses `upsert`, so it inserts a save for a new player or replaces that player's existing save. On login, `load_save()` retrieves the dictionary and `Player(username, data)` rebuilds the objects, including the `Inventory`.

The database file is local to this project. It is not encrypted; the password is hashed, but game-save data is plain JSON.

## Inheritance

- `Goblin`, `Wolf`, `CaveBat`, `Skeleton`, and `EmberWarden` inherit from `Monster`. They reuse `take_damage()`, `choose_attack()`, and `loot()`, while overriding class attributes such as health, attack, XP, and drops.
- `Fireball`, `Mend`, `Strike`, and `PowerStrike` inherit from `Skill`. Each subclass implements its own `use()` behavior and cooldown.

## Midterm 2 study guide: understand these ideas

1. **Object creation:** `Player(...)` creates the player object. `self` refers to that specific object.
2. **Inheritance:** a subclass receives methods/attributes from its parent. `class Goblin(Monster)` means Goblin is a Monster.
3. **Polymorphism:** combat can call `monster.choose_attack()` or `monster.loot()` without needing to know which monster subclass it received.
4. **Serialization:** `to_dict()` turns an object into JSON-compatible data. Methods and class instances are not stored directly.
5. **Restore:** TinyDB returns a dictionary; constructors use that dictionary to restore object attributes.
6. **Authentication:** registration creates a random salt and PBKDF2 hash. Login hashes the entered password using the saved salt and compares hashes.
7. **Quest state:** `quest_data["main_step"]` is an integer state. Talking to NPCs and collecting items advance it; saving the player dictionary preserves it.
8. **Cooldowns:** the dictionary maps skill keys to remaining turns. A skill is selectable only when its cooldown is zero.
9. **Input validation:** `ask_choice()` only accepts allowed values; registration validates username/password; `ask_int()` validates number ranges.
10. **Modular design:** each file owns one responsibility, and `game.py` coordinates the modules.

## Important project note

This is a student starter project, not a commercial game. Read every module and test the full quest yourself before recording your gameplay video. You should be able to explain the code in your own words.
