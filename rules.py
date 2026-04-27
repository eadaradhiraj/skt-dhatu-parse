from models import Term, Prakriya
from shivasutras import get_pratyahara, is_vowel, SLP1_VOWELS

TIN_PARASMAIPADA = {
    'prathama': ['tip', 'tas', 'Ji'],
    'madhyama':['sip', 'Tas', 'Ta'],
    'uttama':   ['mip', 'vas', 'mas']
}

TIN_ATMANEPADA = {
    'prathama': ['ta', 'AtAm', 'Ja'],
    'madhyama': ['TAs', 'ATAm', 'Dvam'],
    'uttama':   ['iw', 'vahi', 'mahiN']
}
# Phonological sets for quick lookup
IK_VOWELS = set(get_pratyahara('i', 'k') +['I', 'U', 'F', 'X'])
EC_VOWELS = get_pratyahara('e', 'c')
YAY_CONSONANTS = set(get_pratyahara('y', 'Y')) # 'yaY' pratyahara for 7.3.101

def apply_guna(char: str) -> str:
    if char in ['i', 'I']: return 'e'
    if char in ['u', 'U']: return 'o'
    if char in ['f', 'F']: return 'ar'
    if char in['x']: return 'al'
    return char

def substitute_lakara(prakriya: Prakriya, purusha: str = 'prathama', vacana: int = 0):
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
    lakara.tags.add('tin') # Mark it as a tin affix
    
    prakriya.log(f"Rule 3.4.78: Substituted lakara with '{new_suffix}'. Tags inherited: {lakara.tags}")

# --- VIKARANAS (Gana 4, Gana 6, and Future Tense) ---
def insert_vikarana(prakriya: Prakriya):
    dhatu = next(t for t in prakriya.terms if t.term_type == 'dhatu')
    suffix = prakriya.terms[-1]
    idx = prakriya.terms.index(dhatu) + 1 # Insert right after Dhatu
    
    # Future Tense (lṛṭ)
    if 'lfW' in suffix.tags:
        vik = Term('sya', 'vikaraRa')
        vik.tags.add('ardhadhatuka') # 'sya' is an Ardhadhatuka affix!
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

def atmanepada_tere(prakriya: Prakriya):
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
                prakriya.log(f"Rule 3.4.79: Replaced 'wi' ({original_ti}) with 'e' -> {suffix.text}")
                break

def idito_num_dhatoh(prakriya: Prakriya):
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'idit' in dhatu.tags:
        text = dhatu.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                dhatu.text = text[:i+1] + 'M' + text[i+1:]
                prakriya.log(f"Rule 7.1.58: Applied 'num' augment -> {dhatu.text}")
                break

# --- GUNA WITH GANA 6 PREVENTION ---
def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya):
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
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


def eco_yayavayah(prakriya: Prakriya):
    # Dynamically find the dhatu!
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    text = dhatu.text
    if text and text[-1] in EC_VOWELS and next_term.text and is_vowel(next_term.text[0]):
        last_char = text[-1]
        if last_char == 'e': rep = 'ay'
        elif last_char == 'o': rep = 'av'
        elif last_char == 'E': rep = 'Ay'
        elif last_char == 'O': rep = 'Av'
        dhatu.text = text[:-1] + rep
        prakriya.log(f"Rule 6.1.78 (Sandhi): eco'yavAyAvaH applied '{last_char}' -> '{rep}'")

def ato_dirgho_yayi(prakriya: Prakriya):
    # Dynamically find the vikarana!
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in YAY_CONSONANTS:
        vikarana.text = vikarana.text[:-1] + 'A'
        prakriya.log(f"Rule 7.3.101: Lengthened 'a' to 'A'")

def rutva_visarga(prakriya: Prakriya):
    """
    Rule 8.2.66 / 8.3.15 (Simplified): sasajuSo ruH -> kharavasAnayor visarjanIyaH
    Changes a word-final 's' into a Visarga ('H').
    """
    suffix = prakriya.terms[-1] # The final term
    
    if suffix.text.endswith('s'):
        suffix.text = suffix.text[:-1] + 'H'
        prakriya.log("Rule 8.3.15: Terminal 's' converted to Visarga 'H'")

def jhonta(prakriya: Prakriya):
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
            suffix.text = suffix.text[1:] # Delete the second 'a' to merge them
            prakriya.log("Rule 6.1.97: Pararupa Sandhi applied ('a' + 'a' -> 'a')")

def jhonta(prakriya: Prakriya):
    """Rule 7.1.3: jho'ntaH - Replaces 'Jh' in a suffix with 'ant'"""
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        # E.g., Ji -> anti, Jha -> antha (which becomes anta via another rule, but we simplify here)
        # Note: If it's Atmanepada 'Ja' that became 'Je', 'J' becomes 'ant' so 'Je' -> 'ante'
        suffix.text = 'ant' + suffix.text[1:]
        prakriya.log(f"Rule 7.1.3: Replaced 'Jh' with 'ant' -> {suffix.text}")

def thasah_se(prakriya: Prakriya):
    """Rule 3.4.80: thAsaH se - Replaces Atmanepada 'TAs' with 'se' in a Wit lakara."""
    suffix = prakriya.terms[-1]
    if suffix.text == 'TAs' and 'Wit' in suffix.tags:
        suffix.text = 'se'
        prakriya.log("Rule 3.4.80: Replaced 'TAs' with 'se'")

def ato_gune(prakriya: Prakriya):
    """Rule 6.1.97: ato guNe"""
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in ['a', 'e', 'o']:
        # If 'a' meets 'a', 'e', or 'o', they merge into the second vowel.
        # We simply delete the 'a' from the Vikarana!
        vikarana.text = vikarana.text[:-1] 
        prakriya.log(f"Rule 6.1.97 (Ato Gune): Merged 'a' + '{suffix.text[0]}' -> '{suffix.text[0]}'")

def ato_nitah(prakriya: Prakriya):
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
            prakriya.log("Rule 7.2.81 (Ato NitaH + Sandhi): Merged 'a' + 'A' -> 'e'")

# --- PAST TENSE AUGMENT ---
def at_agama(prakriya: Prakriya):
    """Rule 6.4.71: luNlaNlfNkzvaq udAttaH - Adds 'aw' before the root for laN (Past Tense)."""
    lakara = prakriya.terms[-1]
    if 'laN' in lakara.tags:
        agama = Term('aw', 'Agama')
        prakriya.terms.insert(0, agama)
        prakriya.log("Rule 6.4.71: Inserted 'aw' augment for Past Tense")

# --- TERMINAL DELETION FOR PAST TENSE ---
def itasca(prakriya: Prakriya):
    """Rule 3.4.100: itaSca - Drops terminal 'i' of Parasmaipada affixes in Nit lakaras (like laN)."""
    suffix = prakriya.terms[-1]
    if 'laN' in suffix.tags and suffix.text.endswith('i'):
        suffix.text = suffix.text[:-1]
        prakriya.log("Rule 3.4.100 (itaSca): Dropped terminal 'i'")

# --- FUTURE TENSE AUGMENT ---
def it_agama(prakriya: Prakriya):
    """Rule 7.2.35: ArdhadhAtukasya iq valAdeH - Adds 'i' before 'sya'."""
    for term in prakriya.terms:
        if term.upadeza == 'sya':
            term.text = 'i' + term.text
            prakriya.log("Rule 7.2.35: Added 'iw' augment to 'sya'")

# --- SANDHI FOR FUTURE TENSE ---
def adesa_pratyayayoh(prakriya: Prakriya):
    """Rule 8.3.59: AdeSapratyayayoH - 's' becomes 'z' after 'ik' vowels (e.g. isya -> izya)"""
    for term in prakriya.terms:
        if 'is' in term.text:
            term.text = term.text.replace('is', 'iz')
            prakriya.log("Rule 8.3.59 (Satva): Changed 's' to 'z'")

def hali_ca(prakriya: Prakriya):
    """Rule 8.2.77: hali ca - Lengthens i/u of div before consonant (div + ya -> dIvya)"""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text == 'div':
        dhatu.text = 'dIv'
        prakriya.log("Rule 8.2.77: Lengthened 'div' to 'dIv'")

def tasthasthamipam(prakriya: Prakriya):
    """
    Rule 3.4.101: tasthasthamipAM tAMtaMtAmaH
    In a Nit lakara (like laN), the suffixes tas, Thas, Tha, and mip 
    are replaced by tAm, tam, ta, and am.
    """
    lakara = next((t for t in prakriya.terms if t.term_type == 'lakara' or 'laN' in t.tags), None)
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

def samyogantasya_lopah(prakriya: Prakriya):
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
        prakriya.log(f"Rule 8.2.23: Dropped final consonant of cluster '{text[-2:]}'")