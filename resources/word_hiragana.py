from entity.WordJapanese import WordJapanese
from utility.japonais import transform_to_hiragana

WORD_HIRAGANA = [
    WordJapanese(transform_to_hiragana("ha", "i"), "Hai", "Oui"),
    WordJapanese(transform_to_hiragana("i", "i", "e"), "Īe", "Non"),
    WordJapanese(transform_to_hiragana("o", "ne", "ga", "i", "shi", "ma", "su"), "onegaishimasu", "S'il vous plaît"),
    WordJapanese(transform_to_hiragana("a", "ri", "ga", "to"), "arigato", "Merci"),
    WordJapanese(transform_to_hiragana("do", "allongement", "i", "ta", "shi", "ma", "shi", "te"), "Dōitashimashite", "il n'y a pas de quoi"),
    WordJapanese(transform_to_hiragana("o", "ha", "yo", "allongement"), "ohayō", "Bonjour (matin)"),
    WordJapanese(transform_to_hiragana("ko", "n", "ni", "chi", "ha"), "konichiwa", "Bonjour (journée)"),
    WordJapanese(transform_to_hiragana("ko", "n", "ba", "n", "ha"), "konbanwa", "Bonsoir"),
    WordJapanese(transform_to_hiragana("sa", "yo", "allongement", "na", "ra"), "sayōnara", "Au revoir"),
    WordJapanese(transform_to_hiragana("o", "ya", "su", "mi"), "oyasumi", "Bonne nuit"),
    WordJapanese(transform_to_hiragana("do", "allongement", "zo"), "dōzo", "Je vous en prie"),
    WordJapanese(transform_to_hiragana("i", "ta", "da", "ki", "ma", "su"), "itadakimasu", "Bon appétit"),
    WordJapanese(transform_to_hiragana("su", "mi", "ma", "se", "n"), "sumimasen", "Excusez-moi"),
    WordJapanese(transform_to_hiragana("go", "me", "n"), "gomen", "Pardonne(z)-moi"),
    WordJapanese(transform_to_hiragana("i", "pause", "te", "ki", "ma", "su"), "itekimasu", "J'y vais"),
    WordJapanese(transform_to_hiragana("ta", "da", "i", "ma"), "tadaima", "Je suis rentré"),
    WordJapanese(transform_to_hiragana("i", "ra", "pause", "shi", "ya", "i", "ma", "se"), "irashiyaimase", "Bienvenue"),
    WordJapanese(transform_to_hiragana("yo", "u", "ko", "so"), "yōkoso", "Bienvenue")
]