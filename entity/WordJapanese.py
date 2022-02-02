class WordJapanese:
    def __init__(self, word, romanji, traduction, mode=1):
        self.word = word
        self.romanji = romanji
        self.traduction = traduction
        self.mode = mode

    def get_romanji(self):
        return self.romanji

    def get_word(self):
        return self.word