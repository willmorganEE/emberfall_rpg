from inventory import Inventory
from config import XP_PER_LEVEL, MAX_LEVEL

class Player:
    def __init__(self, username, data=None):
        data = data or {}
        self.username = username
        self.name = data.get("name", username.title())
        self.level = int(data.get("level", 1))
        self.xp = int(data.get("xp", 0))
        self.gold = int(data.get("gold", 35))
        self.max_hp = int(data.get("max_hp", 85))
        self.hp = int(data.get("hp", self.max_hp))
        self.attack = int(data.get("attack", 12))
        self.inventory = Inventory(data.get("inventory", {"potion": 2}))
        self.skills = list(data.get("skills", ["strike"]))
        self.cooldowns = dict(data.get("cooldowns", {}))
        self.map_name = data.get("map_name", "Greenreach")
        self.position = list(data.get("position", [1, 1]))
        self.quest_data = data.get("quest_data", {})
        self.flags = data.get("flags", {})
        self.won = bool(data.get("won", False))

    def gain_xp(self, amount):
        self.xp += amount
        messages = []
        while self.xp >= XP_PER_LEVEL and self.level < MAX_LEVEL:
            self.xp -= XP_PER_LEVEL
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.attack += 2
            messages.append(f"LEVEL UP! You are now level {self.level}. HP and attack increased.")
            if self.level == 2 and "fireball" not in self.skills:
                self.skills.append("fireball")
                messages.append("You learned Fireball!")
            if self.level == 3 and "mend" not in self.skills:
                self.skills.append("mend")
                messages.append("You learned Mend!")
            if self.level == 4 and "power_strike" not in self.skills:
                self.skills.append("power_strike")
                messages.append("You learned Power Strike!")
        return messages

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old

    def to_dict(self):
        return {
            "name": self.name, "level": self.level, "xp": self.xp,
            "gold": self.gold, "max_hp": self.max_hp, "hp": self.hp,
            "attack": self.attack, "inventory": self.inventory.to_dict(),
            "skills": self.skills, "cooldowns": self.cooldowns,
            "map_name": self.map_name, "position": self.position,
            "quest_data": self.quest_data, "flags": self.flags, "won": self.won
        }
