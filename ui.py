import os
from colorama import Fore, Style

WIDTH = 66

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner(title="EMBERFALL"):
    title = f" {title} "
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * WIDTH + "╗")
    print("║" + title.center(WIDTH) + "║")
    print("╚" + "═" * WIDTH + "╝" + Style.RESET_ALL)

def panel(lines, color=Fore.WHITE):
    print(Fore.BLUE + "┌" + "─" * WIDTH + "┐")
    for line in lines:
        clean = str(line)
        print(Fore.BLUE + "│" + color + " " + clean[:WIDTH-2].ljust(WIDTH-2) + Fore.BLUE + "│")
    print(Fore.BLUE + "└" + "─" * WIDTH + "┘" + Style.RESET_ALL)

def say(message, color=Fore.WHITE):
    print(color + "  " + str(message) + Style.RESET_ALL)

def pause():
    input(Fore.BLACK + Style.BRIGHT + "\n  Press Enter to continue..." + Style.RESET_ALL)

def ask_choice(prompt, choices):
    allowed = {str(x).lower() for x in choices}
    while True:
        answer = input(Fore.YELLOW + f"{prompt} > " + Style.RESET_ALL).strip().lower()
        if answer in allowed:
            return answer
        say("That choice is not available. Try again.", Fore.RED)

def ask_int(prompt, low, high):
    while True:
        raw = input(Fore.YELLOW + f"{prompt} > " + Style.RESET_ALL).strip()
        try:
            value = int(raw)
            if low <= value <= high:
                return value
        except ValueError:
            pass
        say(f"Enter a whole number from {low} to {high}.", Fore.RED)

def bar(value, maximum, width=18):
    maximum = max(1, maximum)
    filled = max(0, min(width, round(width * value / maximum)))
    return "█" * filled + "░" * (width - filled)
