from entity.blindtest.Music import Music
from utility.build import build_id


class BlindTest:
    def __init__(self, name, win_per_round=3):
        self.id = build_id()
        self.name = name
        self.win_per_round = win_per_round
        self.music_list = []

    def add_music(self, music: Music):
        """
        Add a music in the blind test
        BlindTest, Music -> None
        """
        self.music_list.append(music)

    def get_id(self):
        return self.id
