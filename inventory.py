from item import get_item

class Inventory:
    def __init__(self, data=None):
        self.items = dict(data or {})

    def add(self, key, amount=1):
        if amount > 0:
            self.items[key] = self.items.get(key, 0) + amount

    def remove(self, key, amount=1):
        if self.items.get(key, 0) < amount:
            return False
        self.items[key] -= amount
        if self.items[key] <= 0:
            del self.items[key]
        return True

    def count(self, key):
        return self.items.get(key, 0)

    def has(self, key, amount=1):
        return self.count(key) >= amount

    def to_dict(self):
        return dict(self.items)

    def describe(self):
        if not self.items:
            return ["Your pack is empty."]
        rows = []
        for key, amount in sorted(self.items.items()):
            item = get_item(key)
            name = item.name if item else key.replace("_", " ").title()
            rows.append(f"{name} x{amount}")
        return rows
