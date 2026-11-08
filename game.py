
import random
from colorama import Fore
from player import Player
from quest import QuestManager
from world_map import WorldMap, get_npc_at, HERB_LOCATIONS
from npc import NPCS
from monster import random_monster, EmberWarden, Goblin
from combat import fight
from shop import visit_shop
from ui import clear_screen, banner, say, pause, ask_choice, panel, bar


class Game:
    def __init__(self, db, username, new_game=False):
        self.db, self.username = db, username

        # Load saved game or create a new character
        data = None if new_game else db.load_save(username)

        self.player = Player(username, data)
        self.quests = QuestManager(self.player)
        self.new_game = new_game
        self.boss_spawned = False

    def save(self):
        self.player.quest_data = self.quests.to_dict()
        self.db.save_game(self.username, self.player.to_dict())

    def intro(self):
        clear_screen()
        banner("THE FALL OF EMBERFALL")

        print(Fore.YELLOW + """
  The valley of Emberfall was once protected by an ancient flame.
  Beneath the Sunken Crypt, the Ember Warden has awakened and the
  protective seal is breaking.

  You arrive in Greenreach as the last light fades. Elder Rowan
  believes the scattered Ember Shards can restore the seal—but
  the Warden must be defeated before the darkness spreads.
        """)

        say("Your story begins now, adventurer.", Fore.GREEN)
        pause()

    def status(self):
        p = self.player

        banner("CHARACTER")

        panel([
            f"{p.name}  |  Level {p.level}  |  XP {p.xp}/100",
            f"HP {p.hp}/{p.max_hp}  [{bar(p.hp, p.max_hp)}]",
            f"Attack {p.attack}  |  Gold {p.gold}",
            f"Map: {p.map_name}  |  Position: {p.position}",
            "Skills: " + ", ".join(p.skills),
        ])

        print("\n  INVENTORY")

        for row in p.inventory.describe():
            say(row)

        print("\n  MAIN QUEST")
        say(self.quests.main_description(), Fore.YELLOW)

        print("  SIDE QUESTS")

        for quest in self.quests.side_status():
            say(quest)

        pause()

    def talk(self):
        npc_name = get_npc_at(
            self.player.map_name,
            self.player.position
        )

        if not npc_name:
            say("There is nobody here to talk to.", Fore.YELLOW)
            return

        NPCS[npc_name].talk(self.player, self.quests)

        self.quests.collect_shard_progress()
        self.save()
        pause()

    def collect_herb(self, x, y):
        """Collect a Moonleaf Herb if the player enters its location."""

        if self.player.map_name != "Greenreach":
            return

        location = (x, y)

        # Get previously collected herb locations
        collected = self.quests.data.setdefault(
            "herb_locations_collected", []
        )

        # Convert saved coordinates to tuples for comparison
        collected_locations = {
            tuple(position) for position in collected
        }

        # Only collect herbs that have not already been collected
        if location in HERB_LOCATIONS and location not in collected_locations:

            self.player.inventory.add("herb")

            # Save location as a list for compatibility with existing saves
            collected.append([x, y])

            herb_count = self.player.inventory.count("herb")

            say(
                f"You collected a Moonleaf Herb! ({herb_count}/3)",
                Fore.GREEN
            )

            pause()

    def move(self):
        world = WorldMap(self.player.map_name)

        direction = ask_choice(
            "Move (W/A/S/D, Q cancel)",
            ["w", "a", "s", "d", "q"]
        )

        if direction == "q":
            return

        dx, dy = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }[direction]

        x, y = self.player.position

        nx = x + dx
        ny = y + dy

        if not world.can_move(nx, ny):
            say("A wall blocks your way.", Fore.RED)
            return

        self.player.position = [nx, ny]

        # Check for Moonleaf Herb collection
        self.collect_herb(nx, ny)

        # Final boss encounter
        if world.at_boss(self.player.position):

            if self.quests.main_step() < 3:
                say(
                    "The crypt seal rejects you. Complete the main quest steps first.",
                    Fore.RED
                )

                self.player.position = [6, 7]
                return

            result = fight(self.player, EmberWarden())

            if result == "won":
                self.quests.boss_defeated()

                banner("VICTORY")

                say(
                    "The Ember Warden falls. The ancient flame returns to Emberfall!",
                    Fore.GREEN
                )

                say(
                    "You completed the main quest. You are the valley's hero!",
                    Fore.YELLOW
                )

                pause()

        # Random monster encounters
        elif random.random() < (
            0.22 if self.player.map_name == "Greenreach" else 0.32
        ):

            monster = random_monster(self.player.map_name)
            result = fight(self.player, monster)

            if (
                result == "won"
                and isinstance(monster, Goblin)
                and not self.quests.data["bandits_done"]
            ):

                self.quests.data["goblins_defeated"] += 1

                say(
                    f"Tovin's Goblin quest: "
                    f"{self.quests.data['goblins_defeated']}/2 defeated.",
                    Fore.CYAN
                )

                pause()

        self.quests.collect_shard_progress()
        self.save()

    def travel(self):
        if self.player.map_name == "Greenreach":

            if self.quests.main_step() < 3:
                say(
                    "The road to the Sunken Crypt is locked until Captain Brann opens it.",
                    Fore.RED
                )
                return

            self.player.map_name = "Sunken Crypt"
            self.player.position = [1, 1]

        else:
            self.player.map_name = "Greenreach"
            self.player.position = [1, 1]

        say(f"You travel to {self.player.map_name}.", Fore.GREEN)
        self.save()

    def run(self):
        if self.new_game:
            self.intro()

        while not self.player.won:

            clear_screen()
            banner()

            p = self.player

            panel([
                f"{p.name}  LV {p.level}   HP {p.hp}/{p.max_hp}   Gold {p.gold}",
                f"XP {p.xp}/100  |  Main quest: {self.quests.main_step()+1}/4",
            ])

            # Display map and remaining herb locations
            WorldMap(p.map_name).render(
                p,
                self.quests.data.get("herb_locations_collected", [])
            )

            print(Fore.CYAN + """
  1) Move        2) Talk
  3) Character   4) Inventory
  5) Shop        6) Travel
  7) Save        8) Main menu
            """)

            choice = ask_choice(
                "Choose an action",
                [str(i) for i in range(1, 9)]
            )

            if choice == "1":
                self.move()

            elif choice == "2":
                self.talk()

            elif choice == "3":
                self.status()

            elif choice == "4":
                banner("INVENTORY")

                for line in p.inventory.describe():
                    say(line)

                pause()

            elif choice == "5":

                if p.map_name != "Greenreach":
                    say("Sera's shop is in Greenreach.", Fore.YELLOW)
                    pause()

                else:
                    visit_shop(p)
                    self.save()

            elif choice == "6":
                self.travel()
                pause()

            elif choice == "7":
                self.save()
                say("Game saved.", Fore.GREEN)
                pause()

            elif choice == "8":
                self.save()
                break

        if self.player.won:

            self.save()

            banner("EMBERFALL IS SAVED")

            say(
                "Your victory and character progress have been saved.",
                Fore.GREEN
            )

            pause()
