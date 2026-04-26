from models import Term, Prakriya
from shivasutras import is_vowel

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