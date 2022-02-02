from resources.hiragana import HIRAGANA, HIRAGANA_PONCTUATION, HIRAGANA_COMBINAISONS
from resources.katakana import KATAKANA


def transform_to_katakana(*romanji):
    answer = ""

    for letter in romanji:
        letter = letter.upper()
        if letter not in KATAKANA:
            return None

        answer += KATAKANA[letter]

    return answer


def transform_to_hiragana(*romanji):
    answer = ""

    for letter in romanji:
        letter = letter.lower()
        if letter not in HIRAGANA:
            return None

        answer += HIRAGANA[letter]

    return answer