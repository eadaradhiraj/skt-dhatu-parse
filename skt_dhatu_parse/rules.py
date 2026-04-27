from .shivasutras import get_pratyahara, is_vowel, SLP1_VOWELS
from .models import Term, Prakriya

# --- Phonological Sets ---
IK_VOWELS = set(get_pratyahara('i', 'k') + ['I', 'U', 'F', 'X'])
EC_VOWELS = get_pratyahara('e', 'c')
YAY_CONSONANTS = set(get_pratyahara('y', 'Y'))
IN_VOWELS = set(get_pratyahara('i', 'R') + ['I', 'U', 'F', 'X'])
# ADD THIS LINE: Ask the Shivasutras for all consonants ('hal')
SLP1_CONSONANTS = set(get_pratyahara('h', 'l'))

# jhaṣ: J, B, G, Q, D (Voiced aspirates)
JHAS_CONSONANTS = set(get_pratyahara('J', 'z'))
# jhal: All obstruents
# jhaś: Voiced stops (Aspirated & Unaspirated)
JHAL_CONSONANTS = set(get_pratyahara('J', 'l'))
# jhaś: Voiced stops (Aspirated & Unaspirated)
JHAS_SOFT_CONSONANTS = set(get_pratyahara('J', 'S'))

# --- The 18 Tiṅ Affixes (Rule 3.4.78) ---
TIN_PARASMAIPADA = {
    'prathama': ['tip', 'tas', 'Ji'],
    'madhyama': ['sip', 'Tas', 'Ta'],
    'uttama':   ['mip', 'vas', 'mas']
}

TIN_ATMANEPADA = {
    'prathama': ['ta', 'AtAm', 'Ja'],
    'madhyama': ['TAs', 'ATAm', 'Dvam'],
    'uttama': ['iw', 'vahi', 'mahiN']
}

# ... your substitute_lakara function and the rest of the code remains below ...


def apply_guna(char: str) -> str:
    if char in ['i', 'I']:
        return 'e'
    if char in ['u', 'U']:
        return 'o'
    if char in ['f', 'F']:
        return 'ar'
    if char in ['x']:
        return 'al'
    return char


def substitute_lakara(
    prakriya: Prakriya,
    purusha: str = 'prathama',
    vacana: int = 0
) -> None:
    dhatu = prakriya.terms[0]
    lakara = prakriya.terms[-1]

    if 'parasmaipada' in dhatu.tags:
        new_suffix = TIN_PARASMAIPADA[purusha][vacana]
    elif 'atmanepada' in dhatu.tags:
        new_suffix = TIN_ATMANEPADA[purusha][vacana]
    else:
        new_suffix = TIN_PARASMAIPADA[purusha][vacana]

    lakara.text = new_suffix
    lakara.upadeza = new_suffix
    lakara.term_type = 'pratyaya'

    # RULE 1.1.56: sthānivadādeśo'nalvidhau (The substitute behaves like the substituted)
    # The new suffix inherits the tags of the Lakara (e.g., 'Wit' from 'laW')
    lakara.tags.add('tin')  # Mark it as a tin affix

    prakriya.log(
        f"Rule 3.4.78: Substituted lakara with '{new_suffix}'. Tags inherited: {lakara.tags}")

# --- VIKARANAS (Gana 4, Gana 6, and Future Tense) ---


def insert_vikarana(prakriya: Prakriya) -> None:
    dhatu = next(t for t in prakriya.terms if t.term_type == 'dhatu')
    suffix = prakriya.terms[-1]
    idx = prakriya.terms.index(dhatu) + 1  # Insert right after Dhatu

    # Future Tense (lṛṭ)
    if 'lfW' in suffix.tags:
        vik = Term('sya', 'vikaraRa')
        vik.tags.add('ardhadhatuka')  # 'sya' is an Ardhadhatuka affix!
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.33: Inserted 'sya' for Future Tense")
        return

    # Present/Past Tense (SArvadhatuka lakaras)
    if 'gana_1' in dhatu.tags:
        vik = Term('Sap', 'vikaraRa')
    elif 'gana_4' in dhatu.tags:
        vik = Term('Syan', 'vikaraRa')
    elif 'gana_6' in dhatu.tags:
        vik = Term('Sa', 'vikaraRa')
    else:
        return

    prakriya.terms.insert(idx, vik)
    prakriya.log(f"Inserted Vikarana '{vik.upadeza}'")


def atmanepada_tere(prakriya: Prakriya) -> None:
    """
    Rule 3.4.79: wita AtmanepadAnAM were
    If the lakara was 'Wit' (ṭit) and the suffix is Atmanepada, 
    replace its 'wi' (ṭi) portion with 'e'.
    """
    dhatu = prakriya.terms[0]
    suffix = prakriya.terms[-1]

    # Only apply if it's Atmanepada AND the Lakara had a 'W' (ṭ) marker
    if 'atmanepada' in dhatu.tags and 'Wit' in suffix.tags:

        # Rule 1.1.64: aco'ntyAdi wi (The portion beginning with the last vowel is 'wi')
        # We must find the last vowel in the suffix's text and replace it + everything after with 'e'
        text = suffix.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                # Found the last vowel! Replace from here to the end with 'e'
                original_ti = text[i:]
                suffix.text = text[:i] + 'e'
                prakriya.log(
                    f"Rule 3.4.79: Replaced 'wi' ({original_ti}) with 'e' -> {suffix.text}")
                break


def idito_num_dhatoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'idit' in dhatu.tags:
        text = dhatu.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                dhatu.text = text[:i+1] + 'M' + text[i+1:]
                prakriya.log(
                    f"Rule 7.1.58: Applied 'num' augment -> {dhatu.text}")
                break

# --- GUNA WITH GANA 6 PREVENTION ---


def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu:
        return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms):
        return
    next_term = prakriya.terms[idx + 1]

    is_sarva = 'tin' in next_term.tags or 'Sit' in next_term.tags
    is_ardha = 'ardhadhatuka' in next_term.tags

    # Rule 1.2.4: sArvadhAtukam apit (An apit Sarvadhatuka behaves as Nit!)
    is_apit = 'pit' not in next_term.tags
    if is_sarva and is_apit:
        next_term.tags.add('Nit')

    # Rule 1.1.5: kNiti ca (Prevents Guna for Nit/kit affixes - This perfectly handles Gana 6!)
    if 'Nit' in next_term.tags or 'kit' in next_term.tags:
        prakriya.log("Rule 1.1.5 (kNiti ca): Guna prevented")
        return

    if is_sarva or is_ardha:
        text = dhatu.text
        # Simplified: Check if ending in ik, or if short penultimate (like 'div')
        if text and text[-1] in IK_VOWELS:
            dhatu.text = text[:-1] + apply_guna(text[-1])
            prakriya.log(f"Rule 7.3.84: Guna applied to terminal vowel")


def eco_yayavayah(prakriya: Prakriya) -> None:
    # Dynamically find the dhatu!
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu:
        return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms):
        return
    next_term = prakriya.terms[idx + 1]

    text = dhatu.text
    if text and text[-1] in EC_VOWELS and next_term.text and is_vowel(next_term.text[0]):
        last_char = text[-1]
        if last_char == 'e':
            rep = 'ay'
        elif last_char == 'o':
            rep = 'av'
        elif last_char == 'E':
            rep = 'Ay'
        elif last_char == 'O':
            rep = 'Av'
        dhatu.text = text[:-1] + rep
        prakriya.log(
            f"Rule 6.1.78 (Sandhi): eco'yavAyAvaH applied '{last_char}' -> '{rep}'")


def ato_dirgho_yayi(prakriya: Prakriya) -> None:
    # Dynamically find the vikarana!
    vikarana = next(
        (t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]

    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in YAY_CONSONANTS:
        vikarana.text = vikarana.text[:-1] + 'A'
        prakriya.log(f"Rule 7.3.101: Lengthened 'a' to 'A'")


def rutva_visarga(prakriya: Prakriya) -> None:
    """
    Rule 8.2.66 / 8.3.15 (Simplified): sasajuSo ruH -> kharavasAnayor visarjanIyaH
    Changes a word-final 's' into a Visarga ('H').
    """
    suffix = prakriya.terms[-1]  # The final term

    if suffix.text.endswith('s'):
        suffix.text = suffix.text[:-1] + 'H'
        prakriya.log("Rule 8.3.15: Terminal 's' converted to Visarga 'H'")


def jhonta(prakriya: Prakriya) -> None:
    """Rule 7.1.3: jho'ntaH - Replaces 'Jh' in a suffix with 'ant'"""
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        suffix.text = 'ant' + suffix.text[1:]
        prakriya.log("Rule 7.1.3: Replaced 'Jh' with 'ant'")

    """Rule 6.1.97: ato guNe - a + a = a (Pararupa Sandhi)"""
    if len(prakriya.terms) >= 3:
        vikarana = prakriya.terms[1]
        suffix = prakriya.terms[2]
        if vikarana.text.endswith('a') and suffix.text.startswith('a'):
            # Delete the second 'a' to merge them
            suffix.text = suffix.text[1:]
            prakriya.log(
                "Rule 6.1.97: Pararupa Sandhi applied ('a' + 'a' -> 'a')")


def jhonta(prakriya: Prakriya) -> None:
    """Rule 7.1.3: jho'ntaH - Replaces 'Jh' in a suffix with 'ant'"""
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        # E.g., Ji -> anti, Jha -> antha (which becomes anta via another rule, but we simplify here)
        # Note: If it's Atmanepada 'Ja' that became 'Je', 'J' becomes 'ant' so 'Je' -> 'ante'
        suffix.text = 'ant' + suffix.text[1:]
        prakriya.log(f"Rule 7.1.3: Replaced 'Jh' with 'ant' -> {suffix.text}")


def thasah_se(prakriya: Prakriya) -> None:
    """Rule 3.4.80: thAsaH se - Replaces Atmanepada 'TAs' with 'se' in a Wit lakara."""
    suffix = prakriya.terms[-1]
    if suffix.text == 'TAs' and 'Wit' in suffix.tags:
        suffix.text = 'se'
        prakriya.log("Rule 3.4.80: Replaced 'TAs' with 'se'")


def ato_gune(prakriya: Prakriya) -> None:
    """Rule 6.1.97: ato guNe"""
    vikarana = next(
        (t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]

    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in ['a', 'e', 'o']:
        # If 'a' meets 'a', 'e', or 'o', they merge into the second vowel.
        # We simply delete the 'a' from the Vikarana!
        vikarana.text = vikarana.text[:-1]
        prakriya.log(
            f"Rule 6.1.97 (Ato Gune): Merged 'a' + '{suffix.text[0]}' -> '{suffix.text[0]}'")


def ato_nitah(prakriya: Prakriya) -> None:
    """
    Rules 1.2.4 & 7.2.81: Ato NitaH 
    An 'A' of an apit Sarvadhatuka following an 'a' becomes 'iy'.
    Combined with Sandhi (6.1.66, 6.1.87), 'a' + 'Ate'/'ATe' becomes 'ete'/'eTe'.
    """
    if len(prakriya.terms) >= 3:
        vikarana = prakriya.terms[1]
        suffix = prakriya.terms[-1]

        # If Vikarana ends in 'a', Suffix starts with 'A', and Suffix is 'apit' (no 'pit' tag)
        if vikarana.text.endswith('a') and suffix.text.startswith('A') and 'pit' not in suffix.tags:
            # We execute the final phonetic result of the chain: a + A -> e
            vikarana.text = vikarana.text[:-1]      # Remove 'a'
            suffix.text = 'e' + suffix.text[1:]     # Replace 'A' with 'e'
            prakriya.log(
                "Rule 7.2.81 (Ato NitaH + Sandhi): Merged 'a' + 'A' -> 'e'")

# --- PAST TENSE AUGMENT ---


def at_agama(prakriya: Prakriya) -> None:
    """Rule 6.4.71: luNlaNlfNkzvaq udAttaH - Adds 'aw' before the root for laN (Past Tense)."""
    lakara = prakriya.terms[-1]
    if 'laN' in lakara.tags:
        agama = Term('aw', 'Agama')
        prakriya.terms.insert(0, agama)
        prakriya.log("Rule 6.4.71: Inserted 'aw' augment for Past Tense")

# --- TERMINAL DELETION FOR PAST TENSE ---


def itasca(prakriya: Prakriya) -> None:
    """Rule 3.4.100: itaSca - Drops terminal 'i' of Parasmaipada affixes in Nit lakaras (like laN)."""
    suffix = prakriya.terms[-1]
    if 'laN' in suffix.tags and suffix.text.endswith('i'):
        suffix.text = suffix.text[:-1]
        prakriya.log("Rule 3.4.100 (itaSca): Dropped terminal 'i'")


def hali_ca(prakriya: Prakriya) -> None:
    """Rule 8.2.77: hali ca - Lengthens i/u of div before consonant (div + ya -> dIvya)"""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text == 'div':
        dhatu.text = 'dIv'
        prakriya.log("Rule 8.2.77: Lengthened 'div' to 'dIv'")


def tasthasthamipam(prakriya: Prakriya) -> None:
    """
    Rule 3.4.101: tasthasthamipAM tAMtaMtAmaH
    In a Nit lakara (like laN), the suffixes tas, Thas, Tha, and mip 
    are replaced by tAm, tam, ta, and am.
    """
    lakara = next((t for t in prakriya.terms if t.term_type ==
                  'lakara' or 'laN' in t.tags), None)
    suffix = prakriya.terms[-1]

    # Check if we are dealing with a past tense (laN) suffix
    if lakara and 'laN' in lakara.tags:
        if suffix.text == 'tas':
            suffix.text = 'tAm'
            prakriya.log("Rule 3.4.101: Replaced 'tas' with 'tAm'")
        elif suffix.text == 'Tas':
            suffix.text = 'tam'
            prakriya.log("Rule 3.4.101: Replaced 'Tas' with 'tam'")
        elif suffix.text == 'Ta':
            suffix.text = 'ta'
            prakriya.log("Rule 3.4.101: Replaced 'Ta' with 'ta'")
        elif suffix.text == 'mip':
            suffix.text = 'am'
            prakriya.log("Rule 3.4.101: Replaced 'mip' with 'am'")


def samyogantasya_lopah(prakriya: Prakriya) -> None:
    """
    Rule 8.2.23: saMyogAntasya lopaH
    If a word ends in a conjunct consonant (like 'nt'), the final consonant drops.
    Example: aBavant -> aBavan
    """
    suffix = prakriya.terms[-1]
    text = suffix.text
    # Check if the last two characters are both consonants
    if len(text) >= 2 and text[-1] in SLP1_CONSONANTS and text[-2] in SLP1_CONSONANTS:
        suffix.text = text[:-1]
        prakriya.log(
            f"Rule 8.2.23: Dropped final consonant of cluster '{text[-2:]}'")

# --- FUTURE TENSE AUGMENT ---


def it_agama(prakriya: Prakriya) -> None:
    """
    Rules 7.2.35 & 7.2.10: Applies 'iw' augment, blocked for anudatta (AniW) roots.
    """
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)

    # We emulate the anudatta accent data with a known AniW set
    # (In a production app, you would add an 'anit' boolean column to your SQLite DB)
    ANIT_ROOTS = ['ji', 'dA', 'Sru', 'pA', 'han', 'dfS']

    is_anit = dhatu and (dhatu.text in ANIT_ROOTS)

    for term in prakriya.terms:
        if term.upadeza == 'sya':
            if not is_anit:
                term.text = 'i' + term.text
                prakriya.log("Rule 7.2.35: Added 'iw' augment to 'sya'")
            else:
                prakriya.log(
                    "Rule 7.2.10 (AniW): 'iw' augment blocked for anudatta root")

# --- SANDHI FOR FUTURE TENSE ---


def adesa_pratyayayoh(prakriya: Prakriya) -> None:
    """
    Rule 8.3.59: AdeSapratyayayoH 
    An 's' belonging to an affix becomes 'z' if preceded by an iR vowel or a velar.
    Handles both cross-term (je + sya) and intra-term (Bav + isya) boundaries.
    """
    for i, curr_term in enumerate(prakriya.terms):
        text = curr_term.text
        if 's' in text:
            # Find the index of the 's'
            idx = text.find('s')

            # Check what character comes immediately before the 's'
            if idx > 0:
                # The 's' is inside the term (e.g., 'isya'). Look at the letter before it.
                prev_char = text[idx-1]
            else:
                # The 's' is at the very beginning (e.g., 'sya'). Look at the end of the previous term.
                if i > 0 and prakriya.terms[i-1].text:
                    prev_char = prakriya.terms[i-1].text[-1]
                else:
                    continue  # Nothing precedes this 's'

            # If the preceding character is an iR vowel or a velar (ku)
            if prev_char in IN_VOWELS or prev_char in ['k', 'K', 'g', 'G', 'N']:
                curr_term.text = text[:idx] + 'z' + text[idx+1:]
                prakriya.log(
                    f"Rule 8.3.59 (Satva): Changed 's' to 'z' after '{prev_char}'")

# ==========================================
# CONSONANT SANDHI
# ==========================================

def jhasas_tathor_dho_dhah(prakriya: Prakriya) -> None:
    """
    Rule 8.2.40: jhaSastathor dho'dhaH
    If an affix begins with 't' or 'th' and follows a 'jhaz' consonant (voiced aspirates), 
    the 't'/'th' is replaced by 'dh' ('D').
    """
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        
        if dhatu.text and dhatu.text[-1] in JHAS_CONSONANTS:
            if suffix.text.startswith('t'):
                suffix.text = 'D' + suffix.text[1:]
                prakriya.log("Rule 8.2.40: Changed 't' to 'dh' ('D') after jhaz")
            elif suffix.text.startswith('T'):
                suffix.text = 'D' + suffix.text[1:]
                prakriya.log("Rule 8.2.40: Changed 'th' to 'dh' ('D') after jhaz")

def jhalam_jas_jhasi(prakriya: Prakriya) -> None:
    """
    Rule 8.4.53: jhalAM jaS jhaSi
    A 'jhal' consonant followed by a 'jhaS' consonant becomes a 'jaS' (unaspirated voiced stop).
    """
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        
        if dhatu.text and dhatu.text[-1] in JHAL_CONSONANTS and suffix.text and suffix.text[0] in JHAS_SOFT_CONSONANTS:
            last_char = dhatu.text[-1]
            jas_char = last_char
            
            # Map the character to its unaspirated, voiced equivalent (jaS) based on mouth position
            if last_char in['k', 'K', 'g', 'G', 'h']: jas_char = 'g'
            elif last_char in['c', 'C', 'j', 'J', 'S']: jas_char = 'j'
            elif last_char in ['w', 'W', 'q', 'Q', 'z']: jas_char = 'q'
            elif last_char in ['t', 'T', 'd', 'D', 's']: jas_char = 'd'
            elif last_char in ['p', 'P', 'b', 'B']: jas_char = 'b'
            
            if jas_char != last_char:
                dhatu.text = dhatu.text[:-1] + jas_char
                prakriya.log(f"Rule 8.4.53: Changed '{last_char}' to '{jas_char}' (jaS Sandhi)")

def yuvor_anakau(prakriya: Prakriya):
    """
    Rule 7.1.1: yuvor anAkau
    The affixes 'yu' and 'vu' are replaced by 'ana' and 'aka'.
    (This happens after the 'l' and 'w' of 'lyuW' are stripped, leaving 'yu')
    """
    for term in prakriya.terms:
        if term.term_type == 'pratyaya':
            if term.text == 'yu':
                term.text = 'ana'
                prakriya.log("Rule 7.1.1: Replaced 'yu' with 'ana'")
            elif term.text == 'vu':
                term.text = 'aka'
                prakriya.log("Rule 7.1.1: Replaced 'vu' with 'aka'")

def ata_upadhayah(prakriya: Prakriya) -> None:
    """
    Rule 7.2.116: ata upadhAyAH
    A penultimate short 'a' (upadhA) gets Vrddhi ('A') before a Yit (ñ) or Rit (ṇ) affix.
    """
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1] 
    
    if dhatu and ('Yit' in suffix.tags or 'Rit' in suffix.tags):
        text = dhatu.text
        # Find the penultimate letter (Rule 1.1.65: alo'ntyAt pUrva upadhA)
        if len(text) >= 2 and text[-2] == 'a':
            dhatu.text = text[:-2] + 'A' + text[-1]
            prakriya.log(f"Rule 7.2.116: Vrddhi of penultimate 'a' -> 'A' (Yit/Rit affix). Result: {dhatu.text}")

def rashabhyam_no_nah(prakriya: Prakriya) -> None:
    """
    Rule 8.4.1 & 8.4.2: raSAbhyAM no NaH samAnapade (Natva Sandhi)
    An 'n' becomes 'R' (ṇ) if it follows 'r' or 'S' (ṣ), even if separated by vowels/velars/labials.
    (This turns ram + ana into ramaRa).
    """
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    
    # If the root contains 'r' or 'z' (ṣ) and the suffix has 'n'
    if dhatu and ('r' in dhatu.text or 'z' in dhatu.text) and 'n' in suffix.text:
        suffix.text = suffix.text.replace('n', 'R')
        prakriya.log("Rule 8.4.1 (Natva Sandhi): Changed 'n' to 'R'")

def apply_vrddhi(char: str) -> str:
    """Returns the Vrddhi equivalent of a vowel."""
    if char in ['a']: return 'A'
    if char in ['i', 'I', 'e']: return 'E'
    if char in['u', 'U', 'o']: return 'O'
    if char in ['f', 'F']: return 'Ar'
    if char in ['x']: return 'Al'
    return char

# ==========================================
# SANADI (SECONDARY ROOTS)
# ==========================================

def aco_nniti(prakriya: Prakriya) -> None:
    """
    Rule 7.2.115: aco YRiti
    A root ending in a vowel gets vrddhi when followed by a Yit or Rit affix.
    """
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    # Check if the suffix has the Rit or Yit tag
    if 'Rit' in suffix.tags or 'Yit' in suffix.tags:
        text = dhatu.text
        # If the root ends in a vowel
        if text and text[-1] in SLP1_VOWELS:
            old_vowel = text[-1]
            new_vowel = apply_vrddhi(old_vowel)
            dhatu.text = text[:-1] + new_vowel
            prakriya.log(f"Rule 7.2.115 (aco YRiti): Vrddhi applied '{old_vowel}' -> '{new_vowel}'")


def sanadyanta_dhatavah(prakriya: Prakriya) -> None:
    """
    Rule 3.1.32: sanAdyantA dhAtavaH
    Roots formed with san, Ric, etc., are classified as a new 'dhatu'.
    This merges the Dhatu and Suffix into a single term.
    """
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[0]
        suffix = prakriya.terms[1]
        
        # Merge the strings
        merged_text = dhatu.text + suffix.text
        dhatu.text = merged_text
        
        # Collapse the Prakriya state to just the new Dhatu
        prakriya.terms = [dhatu]
        prakriya.log(f"Rule 3.1.32: Merged into new secondary dhatu -> '{dhatu.text}'")