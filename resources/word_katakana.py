from entity.WordJapanese import WordJapanese
from utility.japonais import transform_to_katakana

WORD_KATAKANA = [
    WordJapanese(transform_to_katakana("BE", "PAUSE", "DO"), "Beddo", "le lit"),
    WordJapanese(transform_to_katakana("SO", "FA", "ALLONGEMENT"), "Sofā", "le canapé"),
    WordJapanese(transform_to_katakana("PE", "N"), "Pen", "le stylo"),
    WordJapanese(transform_to_katakana("NO", "ALLONGEMENT", "TO"), "Nōto", "le cahier"),
    WordJapanese(transform_to_katakana("KA", "RE", "N", "DA", "ALLONGEMENT"), "Karendā", "le calendrier"),
    WordJapanese(transform_to_katakana("RA", "JI", "O"), "Rajio", "la radio"),
    WordJapanese(transform_to_katakana("SU", "TE", "RE", "O"), "Sutereo", "la chaîne hi-fi"),
    WordJapanese(transform_to_katakana("TE", "RE", "BI"), "Terebi", "la télévision"),
    WordJapanese(transform_to_katakana("KA", "ME", "RA"), "Kamera", "l'appareil photo"),
    WordJapanese(transform_to_katakana("KO", "N", "PYU", "ALLONGEMENT", "TA"), "Konpyūta", "l'ordinateur"),
    WordJapanese(transform_to_katakana("PA", "SO", "KO", "N"), "Pasokon", "le PC"),
    WordJapanese(transform_to_katakana("E", "A", "KO", "N"), "Eakon", "le climatiseur"),
    WordJapanese(transform_to_katakana("SO", "MO", "KO", "N"), "Somokon", "la télécommande"),
    WordJapanese(transform_to_katakana("KU", "RE", "JI", "PAUSE", "TO", "KA", "ALLONGEMENT", "DO"), "Kurejitokādo", "la carte de paiement"),
    WordJapanese(transform_to_katakana("DO", "A"), "Doa", "la porte"),
    WordJapanese(transform_to_katakana("RA", "N", "PU"), "Ranpu", "la lampe"),
    WordJapanese(transform_to_katakana("TE", "ALLONGEMENT", "BU", "RU"), "Tēburu", "la table"),
    WordJapanese(transform_to_katakana("FO", "ALLONGEMENT", "KU"), "Fōku", "la fourchette"),
    WordJapanese(transform_to_katakana("NA", "I", "FU"), "Naifu", "le couteau"),
    WordJapanese(transform_to_katakana("SU", "PU", "ALLONGEMENT", "N"), "Supūn", "la cuillère"),
    WordJapanese(transform_to_katakana("TO", "I", "RE"), "Toire", "les toilettes"),

    # nom des couleurs
    WordJapanese(transform_to_katakana("O", "RE", "N", "JI", "I", "RO"), "Orenjiiro", "le orange"),
    WordJapanese(transform_to_katakana("PI", "N", "KU"), "Pinku", "le rose"),
    WordJapanese(transform_to_katakana("CHA", "I", "RO"), "Chairo", "le marron"),
    WordJapanese(transform_to_katakana("BE", "ALLONGEMENT", "JU"), "Beju", "le beige"),
    WordJapanese(transform_to_katakana("MO", "ALLONGEMENT", "BU"), "Mobu", "le mauve"),
    WordJapanese(transform_to_katakana("MA", "ZE", "N", "TA"), "Mazenta", "le magenta"),
    WordJapanese(transform_to_katakana("SHI", "A", "N"), "Shian", "le cyan"),
    WordJapanese(transform_to_katakana("KI", "N", "I", "RO"), "Kiniro", "l'or"),
]