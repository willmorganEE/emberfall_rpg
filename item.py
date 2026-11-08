from dataclasses import dataclass

@dataclass(frozen=True)
class Item:
    key: str
    name: str
    description: str
    price: int
    kind: str
    power: int = 0

ITEMS = {
    "potion": Item("potion", "Healing Potion", "Restores 35 HP.", 18, "heal", 35),
    "ether": Item("ether", "Focus Tonic", "Restores 2 skill energy (combat cooldowns).", 22, "tonic", 2),
    "herb": Item("herb", "Moonleaf Herb", "A fragrant herb wanted by Mira.", 0, "quest", 0),
    "shard": Item("shard", "Ember Shard", "A warm fragment of the ancient seal.", 0, "quest", 0),
    "iron_sword": Item("iron_sword", "Ironblade", "A sturdy blade. Adds 4 attack damage.", 65, "weapon", 4),
    "ward_charm": Item("ward_charm", "Warden's Charm", "A protective charm. Adds 12 maximum HP.", 55, "armor", 12),
}

def get_item(key):
    return ITEMS.get(key)
