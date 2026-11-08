
from colorama import Fore
from ui import say

MAPS = {
    "Greenreach": [
        "#############",
        "#...N.......#",
        "#..###..#...#",
        "#..#....#...#",
        "#..#.....N..#",
        "#.....##....#",
        "#...........#",
        "#..N....N...#",
        "#.....N.....#",
        "#############",
    ],
    "Sunken Crypt": [
        "#############",
        "#.....#.....#",
        "#.##..#..##.#",
        "#....N......#",
        "###.####.####",
        "#...........#",
        "#.####.##...#",
        "#.....#....B#",
        "#############",
    ],
}

NPC_LOCATIONS = {
    "Greenreach": {
        (4, 1): "Elder Rowan",
        (3, 7): "Mira",
        (8, 7): "Tovin",
        (6, 8): "Sera",
        (9, 4): "Captain Brann",
    },
    "Sunken Crypt": {
        (5, 3): "Captain Brann",
    },
}

HERB_LOCATIONS = {
    (2, 1),
    (10, 4),
    (6, 6),
}


class WorldMap:
    def __init__(self, name):
        self.name = name

    def render(self, player, collected_herbs=None):
        layout = MAPS[self.name]
        collected_herbs = collected_herbs or []

        collected = {
            tuple(position) for position in collected_herbs
        }

        print(Fore.CYAN + f"\n  {self.name}")
        print("  Legend: @ You  # Wall  N NPC  H Herb  B Boss")

        for y, row in enumerate(layout):
            output = "  "

            for x, tile in enumerate(row):

                if [x, y] == player.position:
                    output += Fore.YELLOW + "@"

                elif tile == "#":
                    output += Fore.BLUE + "█"

                elif tile == "N":
                    output += Fore.GREEN + "◆"

                elif (x, y) in HERB_LOCATIONS and (x, y) not in collected:
                    output += Fore.GREEN + "H"

                elif tile == "B":
                    output += Fore.RED + "♛"

                else:
                    output += Fore.WHITE + "·"

            print(output + Fore.RESET)

    def can_move(self, x, y):
        layout = MAPS[self.name]

        return (
            0 <= y < len(layout)
            and 0 <= x < len(layout[y])
            and layout[y][x] != "#"
        )

    def at_boss(self, position):
        x, y = position
        return MAPS[self.name][y][x] == "B"


def get_npc_at(map_name, position):
    x, y = position
    return NPC_LOCATIONS.get(map_name, {}).get((x, y))
