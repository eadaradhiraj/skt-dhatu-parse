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


def insert_vikarana(prakriya: Prakriya):
    dhatu = prakriya.terms[0]
    if 'gana_1' in dhatu.tags:
        vikarana = Term('Sap', 'vikaraRa')
        prakriya.terms.insert(1, vikarana)
        prakriya.log("Rule 3.1.68: Inserted Vikarana 'Sap'")


# --- NEW RULE ---
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
    """
    Rule 7.1.58: idito num dhAtoH
    Adds the 'num' augment to roots tagged with 'idit'.
    The 'm' is inserted immediately after the last vowel of the root (Rule 1.1.47: midaco'ntyātparaḥ).
    """
    dhatu = prakriya.terms[0]
    
    if 'idit' in dhatu.tags:
        text = dhatu.text
        
        # Find the last vowel in the dhatu
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                # Insert 'M' (anusvara) right after the vowel
                # Note: Technically 'num' is 'n', which becomes 'M' via Sandhi (8.3.24), 
                # but we'll insert 'M' directly here for simplicity at this stage.
                dhatu.text = text[:i+1] + 'M' + text[i+1:]
                prakriya.log(f"Rule 7.1.58: Applied 'num' augment -> {dhatu.text}")
                break

def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya):
    """
    Rule 7.3.84: sArvadhAtukArdhadhAtukayoH
    If a Sarvadhatuka suffix follows, the 'ik' vowel of the stem gets Guna.
    """
    dhatu = prakriya.terms[0]
    
    if len(prakriya.terms) > 1:
        next_term = prakriya.terms[1] # This is usually the Vikarana (e.g., 'a' from 'Sap')
        
        # Rule 3.4.113: tiN-Sit sArvadhAtukam (Affixes with 'Sit' or 'tiN' are Sarvadhatuka)
        is_sarvadhatuka = 'tin' in next_term.tags or 'Sit' in next_term.tags
        
        if is_sarvadhatuka:
            text = dhatu.text
            if text and text[-1] in IK_VOWELS:
                old_vowel = text[-1]
                new_vowel = apply_guna(old_vowel)
                # Replace the last vowel with its Guna equivalent
                dhatu.text = text[:-1] + new_vowel
                prakriya.log(f"Rule 7.3.84 (Guna): '{old_vowel}' -> '{new_vowel}' before Sarvadhatuka")


def eco_yayavayah(prakriya: Prakriya):
    """
    Rule 6.1.78: eco'yavAyAvaH
    'ec' vowels (e, o, E, O) followed by a vowel ('ac') become ay, av, Ay, Av.
    """
    dhatu = prakriya.terms[0]
    
    if len(prakriya.terms) > 1:
        next_term = prakriya.terms[1]
        
        text = dhatu.text
        # If Dhatu ends in ec, and the next term starts with a vowel
        if text and text[-1] in EC_VOWELS and next_term.text and is_vowel(next_term.text[0]):
            last_char = text[-1]
            if last_char == 'e': rep = 'ay'
            elif last_char == 'o': rep = 'av'
            elif last_char == 'E': rep = 'Ay'
            elif last_char == 'O': rep = 'Av'
            
            dhatu.text = text[:-1] + rep
            prakriya.log(f"Rule 6.1.78 (Sandhi): eco'yavAyAvaH applied '{last_char}' -> '{rep}'")

def ato_dirgho_yayi(prakriya: Prakriya):
    """
    Rule 7.3.101: ato dIrgho yaYi
    Lengthens the short 'a' of an anga (stem) before a Sarvadhatuka affix beginning with 'yaY'.
    """
    # In our engine, the 'a' currently sits in the Vikarana term (e.g., 'a' from 'Sap')
    if len(prakriya.terms) >= 3:
        vikarana = prakriya.terms[1]
        suffix = prakriya.terms[2]
        
        # Check if Vikarana ends in 'a' AND Suffix starts with a 'yaY' letter
        if vikarana.text.endswith('a') and suffix.text and suffix.text[0] in YAY_CONSONANTS:
            # Lengthen 'a' to 'A'
            vikarana.text = vikarana.text[:-1] + 'A'
            prakriya.log(f"Rule 7.3.101: Lengthened 'a' to 'A' before 'yaY' letter '{suffix.text[0]}'")


def rutva_visarga(prakriya: Prakriya):
    """
    Rule 8.2.66 / 8.3.15 (Simplified): sasajuSo ruH -> kharavasAnayor visarjanIyaH
    Changes a word-final 's' into a Visarga ('H').
    """
    suffix = prakriya.terms[-1] # The final term
    
    if suffix.text.endswith('s'):
        suffix.text = suffix.text[:-1] + 'H'
        prakriya.log("Rule 8.3.15: Terminal 's' converted to Visarga 'H'")