from colorama import Fore
from ui import say

class NPC:
    def __init__(self, name, role, dialogue):
        self.name, self.role, self.dialogue = name, role, dialogue

    def talk(self, player, quests):
        say(f"{self.name} — {self.role}", Fore.CYAN)
        say(self.dialogue)

class ElderRowan(NPC):
    def __init__(self):
        super().__init__("Elder Rowan", "Keeper of Greenreach", "The old seal beneath the crypt is breaking. The valley needs a hero.")

    def talk(self, player, quests):
        super().talk(player, quests)
        say(quests.talk_elder(), Fore.YELLOW)

class Mira(NPC):
    def __init__(self):
        super().__init__("Mira", "Herbalist", "The forest still grows moonleaf, if you know where to look.")
    def talk(self, player, quests):
        super().talk(player, quests)
        if quests.data["herbs_done"]:
            say("Thank you again. My remedies are stronger because of you.", Fore.GREEN)
        elif player.inventory.count("herb") >= 3:
            player.inventory.remove("herb", 3)
            player.gold += 35
            player.gain_xp(30)
            quests.data["herbs_done"] = True
            say("You brought the herbs! Here are 35 gold and 30 XP.", Fore.GREEN)
        else:
            say(f"Bring me 3 Moonleaf Herbs. You have {player.inventory.count('herb')}/3.", Fore.YELLOW)

class CaptainBrann(NPC):
    def __init__(self):
        super().__init__("Captain Brann", "Crypt Warden", "I've held the eastern gate for years. Something terrible stirs below.")
    def talk(self, player, quests):
        super().talk(player, quests)
        say(quests.talk_captain(), Fore.YELLOW)

class Tovin(NPC):
    def __init__(self):
        super().__init__("Tovin", "Retired Adventurer", "A quick strike is useful, but a well-timed skill can turn a battle.")
        say_text = "Train hard. New skills unlock as you gain levels."
    def talk(self, player, quests):
        super().talk(player, quests)
        if quests.data["bandits_done"]:
            say("Those goblins won't trouble the road again. Well done!", Fore.GREEN)
        elif quests.data["goblins_defeated"] >= 2:
            quests.data["bandits_done"] = True
            player.gold += 45
            for message in player.gain_xp(40):
                say(message, Fore.CYAN)
            say("You defeated two Goblins! Tovin rewards you with 45 gold and 40 XP.", Fore.GREEN)
        else:
            say(f"Two Goblins have been harassing travelers. Defeat them for me ({quests.data['goblins_defeated']}/2).", Fore.YELLOW)
        say("Train hard. Fireball unlocks at level 2, Mend at level 3, and Power Strike at level 4.", Fore.YELLOW)

class Sera(NPC):
    def __init__(self):
        super().__init__("Sera", "Traveling Merchant", "The road is dangerous, but a prepared traveler can survive anything.")
    def talk(self, player, quests):
        super().talk(player, quests)
        say("Visit the shop in Greenreach. Potions are worth their weight in gold.", Fore.YELLOW)

NPCS = {
    "Elder Rowan": ElderRowan(),
    "Mira": Mira(),
    "Captain Brann": CaptainBrann(),
    "Tovin": Tovin(),
    "Sera": Sera(),
}
