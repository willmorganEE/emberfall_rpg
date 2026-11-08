from colorama import Fore
from item import ITEMS
from ui import say, ask_choice

SHOP_STOCK = ["potion", "ether", "iron_sword", "ward_charm"]

def visit_shop(player):
    while True:
        print(Fore.CYAN + "\n  === SERA'S SUPPLY SHOP ===")
        print(f"  Your gold: {player.gold}")
        for i, key in enumerate(SHOP_STOCK, 1):
            item = ITEMS[key]
            print(f"  {i}) {item.name:<20} {item.price:>3}g  — {item.description}")
        print("  0) Leave shop")
        choice = ask_choice("Buy item", [str(i) for i in range(len(SHOP_STOCK)+1)])
        if choice == "0":
            return
        item = ITEMS[SHOP_STOCK[int(choice)-1]]
        if player.gold < item.price:
            say("You do not have enough gold.", Fore.RED)
        elif item.kind == "weapon" and player.flags.get("iron_sword"):
            say("You already own this upgrade.", Fore.YELLOW)
        elif item.kind == "armor" and player.flags.get("ward_charm"):
            say("You already own this upgrade.", Fore.YELLOW)
        else:
            player.gold -= item.price
            if item.kind == "weapon":
                player.attack += item.power
                player.flags["iron_sword"] = True
            elif item.kind == "armor":
                player.max_hp += item.power
                player.hp += item.power
                player.flags["ward_charm"] = True
            else:
                player.inventory.add(item.key)
            say(f"Purchased {item.name}!", Fore.GREEN)
