from tinydb import TinyDB, Query
from pathlib import Path

class GameDatabase:
    def __init__(self, path="emberfall_data.json"):
        self.db = TinyDB(path)
        self.accounts = self.db.table("accounts")
        self.saves = self.db.table("saves")

    def account_exists(self, username):
        U = Query()
        return self.accounts.contains(U.username == username.lower())

    def create_account(self, username, salt, password_hash):
        self.accounts.insert({
            "username": username.lower(),
            "salt": salt,
            "password_hash": password_hash
        })

    def verify_account(self, username, password_hash):
        U = Query()
        record = self.accounts.get(U.username == username.lower())
        return record is not None and record["password_hash"] == password_hash

    def get_salt(self, username):
        U = Query()
        record = self.accounts.get(U.username == username.lower())
        return record["salt"] if record else None

    def load_save(self, username):
        U = Query()
        record = self.saves.get(U.username == username.lower())
        return record.get("data") if record else None

    def save_game(self, username, data):
        U = Query()
        self.saves.upsert({"username": username.lower(), "data": data}, U.username == username.lower())

    def close(self):
        self.db.close()
