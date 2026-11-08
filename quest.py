MAIN_STEPS = [
    "Speak with Elder Rowan in Greenreach.",
    "Collect 3 Ember Shards from monsters.",
    "Speak with Captain Brann to open the Sunken Crypt.",
    "Defeat the Ember Warden in the Sunken Crypt."
]

class QuestManager:
    def __init__(self, player):
        self.player = player
        self.data = player.quest_data
        self.data.setdefault("main_step", 0)
        self.data.setdefault("herbs_done", False)
        self.data.setdefault("bandits_done", False)
        self.data.setdefault("goblins_defeated", 0)

    def main_step(self):
        return self.data["main_step"]

    def main_description(self):
        step = self.main_step()
        if step >= len(MAIN_STEPS):
            return "The Ember Warden has been defeated. The valley is safe!"
        return MAIN_STEPS[step]

    def talk_elder(self):
        if self.main_step() == 0:
            self.data["main_step"] = 1
            return "The seal is failing. Bring me 3 Ember Shards, then find Captain Brann."
        if self.main_step() == 1:
            return f"The seal needs 3 shards. You have {self.player.inventory.count('shard')}/3."
        if self.main_step() == 2:
            return "Captain Brann can guide you into the Sunken Crypt."
        return "The valley will remember your courage, hero."

    def collect_shard_progress(self):
        if self.main_step() == 1 and self.player.inventory.count("shard") >= 3:
            self.data["main_step"] = 2

    def talk_captain(self):
        self.collect_shard_progress()
        if self.main_step() == 2:
            self.data["main_step"] = 3
            return "The path is open. Enter the Sunken Crypt and end the Warden's reign!"
        if self.main_step() < 2:
            return "The crypt is sealed. Help the Elder gather 3 Ember Shards first."
        return "The crypt entrance is east. Do not underestimate the Warden."

    def boss_defeated(self):
        self.data["main_step"] = 4
        self.player.won = True

    def side_status(self):
        herbs = "Complete" if self.data["herbs_done"] else f"Collect 3 Moonleaf Herbs ({self.player.inventory.count('herb')}/3)"
        bandits = "Complete" if self.data["bandits_done"] else f"Defeat 2 Goblins ({self.data['goblins_defeated']}/2)"
        return herbs, bandits

    def to_dict(self):
        return dict(self.data)
