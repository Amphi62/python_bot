class Music:
    def __init__(self, title, url, other_title):
        self.title = title
        self.url = url
        self.other_title = other_title

    def check_music_correct(self, proposition):
        # TODO : enlever les accents + tout mettre en lowercase
        return proposition == self.title or proposition in self.other_title
