from colorama import Fore, Style, init
from auth import register, login
from database import GameDatabase
from game import Game
from ui import clear_screen, banner, pause, ask_choice, say

init(autoreset=True)

def main():
    db = GameDatabase()
    while True:
        clear_screen()
        banner()
        print(Fore.CYAN + "  1) Login")
        print(Fore.CYAN + "  2) Create account")
        print(Fore.CYAN + "  3) How to play")
        print(Fore.CYAN + "  4) Exit")
        choice = ask_choice("  Choose", ["1", "2", "3", "4"])
        if choice == "1":
            username = login(db)
            if username:
                Game(db, username).run()
        elif choice == "2":
            username = register(db)
            if username:
                Game(db, username, new_game=True).run()
        elif choice == "3":
            clear_screen()
            banner("HOW TO PLAY")
            say("Move around the maps, talk to the five characters, complete quests,")
            say("fight monsters, buy supplies, learn skills, and defeat the Warden.")
            say("Your progress saves automatically after important actions.")
            say("Controls: W/A/S/D move | menu choices use numbers | Q returns to menu.")
            pause()
        else:
            print(Fore.YELLOW + "\n  Thanks for playing Emberfall. See you next time!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n  Game closed. Your last autosave is safe.")
