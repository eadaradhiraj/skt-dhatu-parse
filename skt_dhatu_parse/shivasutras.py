"""
shivasutras.py
Defines the 14 Shiva Sutras using SLP1 encoding.
"""

SHIVA_SUTRAS = [
    (['a', 'i', 'u'], 'R'),                         # 1. a i u ṇ
    (['f', 'x'], 'k'),                              # 2. ṛ ḷ k
    (['e', 'o'], 'N'),                              # 3. e o ṅ
    (['E', 'O'], 'c'),                              # 4. ai au c
    (['h', 'y', 'v', 'r'], 'w'),                    # 5. h y v r ṭ
    (['l'], 'R'),                                   # 6. l ṇ (Note: R is here again)
    (['Y', 'm', 'N', 'R', 'n'], 'm'),               # 7. ñ m ṅ ṇ n m
    (['J', 'B'], 'Y'),                              # 8. jh bh ñ
    (['G', 'Q', 'D'], 'z'),                         # 9. gh ḍh dh ṣ
    (['j', 'b', 'g', 'q', 'd'], 'S'),               # 10. j b g ḍ d ś
    (['K', 'P', 'C', 'W', 'T', 'c', 'w', 't'], 'v'),# 11. kh ph ch ṭh th c ṭ t v
    (['k', 'p'], 'y'),                              # 12. k p y
    (['S', 'z', 's'], 'r'),                         # 13. ś ṣ s r
    (['h'], 'l')                                    # 14. h l
]

def get_pratyahara(start_letter: str, it_marker: str) -> list[str]:
    collecting = False
    phonemes =[]
    
    # In SLP1, 'ṇ' is 'R'. 'aR' is Sutra 1, 'iR'/'yaR' is Sutra 6.
    target_n_occurrences = 1 if (start_letter == 'a' and it_marker == 'R') else 2
    n_seen = 0

    for phoneme_list, marker in SHIVA_SUTRAS:
        if marker == 'R':
            n_seen += 1

        for p in phoneme_list:
            if p == start_letter:
                collecting = True
            if collecting:
                phonemes.append(p)
                
        if collecting and marker == it_marker:
            if marker == 'R' and n_seen < target_n_occurrences:
                continue
            return phonemes
            
    raise ValueError(f"Invalid Pratyahara: {start_letter}{it_marker}")

# Create a global set of vowels (ac) for fast lookup in other files
# Note: we add long vowels manually because Shiva Sutras only list short ones!
AC_PRATYAHARA = get_pratyahara('a', 'c')
SLP1_VOWELS = set(AC_PRATYAHARA +['A', 'I', 'U', 'F', 'X'])

def is_vowel(char: str) -> bool:
    return char in SLP1_VOWELS