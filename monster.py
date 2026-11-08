import random

class Monster:
    name = "Monster"
    max_hp = 20
    attack = 5
    xp_reward = 12
    gold_range = (4, 10)
    drops = [("potion", 0.10)]

    def __init__(self):
        self.hp = self.max_hp

    def take_damage(self, amount):
        self.hp = max(0, self.hp - max(0, amount))
        return self.hp

    def choose_attack(self):
        return random.randint(max(1, self.attack - 2), self.attack + 2)

    def loot(self):
        gold = random.randint(*self.gold_range)
        drops = []
        for item, chance in self.drops:
            if random.random() < chance:
                drops.append(item)
        return gold, drops

class CaveBat(Monster):
    name, max_hp, attack, xp_reward = "Cave Bat", 22, 6, 14
    gold_range = (4, 9)
    drops = [("potion", 0.12)]

class Goblin(Monster):
    name, max_hp, attack, xp_reward = "Goblin", 32, 8, 20
    gold_range = (7, 14)
    drops = [("herb", 0.20), ("potion", 0.12), ("shard", 0.42)]

class Wolf(Monster):
    name, max_hp, attack, xp_reward = "Ash Wolf", 38, 10, 24
    gold_range = (9, 16)
    drops = [("herb", 0.18), ("potion", 0.15), ("shard", 0.35)]

class Skeleton(Monster):
    name, max_hp, attack, xp_reward = "Crypt Skeleton", 48, 12, 30
    gold_range = (12, 20)
    drops = [("ether", 0.20), ("potion", 0.20), ("shard", 0.55)]

class EmberWarden(Monster):
    name, max_hp, attack, xp_reward = "EMBER WARDEN", 145, 16, 160
    gold_range = (100, 130)
    drops = [("ward_charm", 1.0), ("shard", 1.0)]

MONSTER_TYPES = {
    "Greenreach": [CaveBat, Goblin, Wolf],
    "Sunken Crypt": [Goblin, Skeleton, Wolf],
}

def random_monster(map_name):
    choices = MONSTER_TYPES.get(map_name, [CaveBat, Goblin])
    return random.choice(choices)()
