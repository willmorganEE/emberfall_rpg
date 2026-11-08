import hashlib
import os
import re
from colorama import Fore
from ui import say, ask_choice

def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000).hex()

def register(db):
    print(Fore.CYAN + "\n  === CREATE ACCOUNT ===")
    while True:
        username = input("  Username (3-16 letters/numbers/_): ").strip()
        if re.fullmatch(r"[A-Za-z0-9_]{3,16}", username):
            break
        say("Use 3-16 letters, numbers, or underscores.", Fore.RED)
    if db.account_exists(username):
        say("That username already exists.", Fore.RED)
        return None
    while True:
        password = input("  Password (at least 6 characters): ")
        if len(password) >= 6:
            confirm = input("  Confirm password: ")
            if password == confirm:
                break
            say("Passwords do not match.", Fore.RED)
        else:
            say("Password must be at least 6 characters.", Fore.RED)
    salt = os.urandom(16).hex()
    db.create_account(username, salt, _hash_password(password, salt))
    say("Account created. Your adventure begins!", Fore.GREEN)
    return username.lower()

def login(db):
    print(Fore.CYAN + "\n  === LOGIN ===")
    username = input("  Username: ").strip()
    salt = db.get_salt(username)
    if not salt:
        say("Account not found.", Fore.RED)
        return None
    password = input("  Password: ")
    if not db.verify_account(username, _hash_password(password, salt)):
        say("Incorrect password.", Fore.RED)
        return None
    say(f"Welcome back, {username}!", Fore.GREEN)
    return username.lower()
