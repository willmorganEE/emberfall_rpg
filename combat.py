from colorama import Fore
from skill import get_skill
from ui import banner, say, ask_choice, panel

def fight(player, monster):
    banner(f"BATTLE: {monster.name.upper()}")
    say(f"A {monster.name} blocks your path!", Fore.RED)
    while monster.hp > 0 and player.hp > 0:
        panel([
            f"{player.name}  HP {player.hp}/{player.max_hp}   LV {player.level}",
            f"{monster.name}  HP {monster.hp}/{monster.max_hp}",
            "Skills: " + ", ".join(get_skill(k).name for k in player.skills if get_skill(k))
        ])
        available = []
        for key in player.skills:
            skill = get_skill(key)
            if skill and player.cooldowns.get(key, 0) == 0:
                available.append(key)
        print(Fore.CYAN + "  1) Use skill")
        print(Fore.CYAN + "  2) Use healing potion")
        print(Fore.CYAN + "  3) Try to flee")
        choice = ask_choice("Action", ["1", "2", "3"])
        if choice == "3" and monster.name != "EMBER WARDEN":
            say("You retreat from the fight.", Fore.YELLOW)
            return "fled"
        if choice == "2":
            if player.inventory.remove("potion"):
                healed = player.heal(35)
                say(f"You use a potion and restore {healed} HP.", Fore.GREEN)
            else:
                say("You do not have a healing potion.", Fore.RED)
                continue
        else:
            if not available:
                say("All skills are cooling down. You lose your turn!", Fore.YELLOW)
            else:
                print("  Available skills:")
                for i, key in enumerate(available, 1):
                    skill = get_skill(key)
                    print(f"  {i}) {skill.name} — {skill.description}")
                index = int(ask_choice("Skill number", [str(i) for i in range(1, len(available)+1)])) - 1
                key = available[index]
                skill = get_skill(key)
                say(skill.use(player, monster), Fore.GREEN)
                player.cooldowns[key] = skill.cooldown
        if monster.hp <= 0:
            break
        damage = monster.choose_attack()
        player.hp = max(0, player.hp - damage)
        say(f"{monster.name} hits you for {damage} damage.", Fore.RED)
        for key in list(player.cooldowns):
            player.cooldowns[key] = max(0, player.cooldowns[key] - 1)
    if player.hp <= 0:
        say("You have fallen. The healers bring you back to Greenreach.", Fore.RED)
        player.hp = max(1, player.max_hp // 2)
        player.map_name, player.position = "Greenreach", [1, 1]
        player.gold = max(0, player.gold - 10)
        return "lost"
    say(f"{monster.name} is defeated!", Fore.GREEN)
    gold, drops = monster.loot()
    player.gold += gold
    say(f"You collect {gold} gold.", Fore.YELLOW)
    for item in drops:
        player.inventory.add(item)
        say(f"Monster drop: {item.replace('_', ' ').title()}!", Fore.MAGENTA)
    for message in player.gain_xp(monster.xp_reward):
        say(message, Fore.CYAN)
    return "won"
