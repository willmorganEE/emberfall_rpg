class Skill:
    key = "skill"
    name = "Skill"
    description = "A basic skill."
    cooldown = 0
    energy_cost = 0

    def use(self, player, monster):
        raise NotImplementedError

class Strike(Skill):
    key, name, description, cooldown = "strike", "Quick Strike", "A reliable weapon attack.", 0
    def use(self, player, monster):
        damage = player.attack + 3
        monster.take_damage(damage)
        return f"You strike for {damage} damage."

class Fireball(Skill):
    key, name, description, cooldown = "fireball", "Fireball", "Hurl a blazing orb at one enemy.", 2
    def use(self, player, monster):
        damage = player.attack * 2 + 8
        monster.take_damage(damage)
        return f"Fireball erupts for {damage} damage!"

class Mend(Skill):
    key, name, description, cooldown = "mend", "Mend", "Restore 28 HP. Cannot exceed max HP.", 3
    def use(self, player, monster):
        restored = player.heal(28)
        return f"Warm light restores {restored} HP."

class PowerStrike(Skill):
    key, name, description, cooldown = "power_strike", "Power Strike", "A heavy blow with a short cooldown.", 2
    def use(self, player, monster):
        damage = player.attack * 3
        monster.take_damage(damage)
        return f"Power Strike deals {damage} damage!"

SKILL_TYPES = {c.key: c for c in (Strike, Fireball, Mend, PowerStrike)}

def get_skill(key):
    cls = SKILL_TYPES.get(key)
    return cls() if cls else None
