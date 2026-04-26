"""
anubandha.py
Rules for identifying and removing 'It' (meta-markers) - Sūtras 1.3.2 to 1.3.9
Encoding: SLP1
"""
from models import Term

# A quick set of SLP1 consonants for Rule 1.3.3 (hal antyam)
# Eventually, you can import 'hal' from shivasutras.py!
SLP1_CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")

def resolve_it_markers(term: Term):
    """
    Examines a Term's upadeza, identifies 'it' markers, applies lopa (deletion),
    and assigns tags (e.g., 'pit', 'idit') to the Term.
    """
    # -----------------------------------------------------------------------
    # Rule 1.3.2: upadeśe'janunāsik it 
    # "In an upadeza, a nasalized vowel is an 'it'."
    # In computational datasets, this is often marked by '!' after the vowel.
    # -----------------------------------------------------------------------
    if '!' in term.text:
        idx = term.text.find('!')
        vowel = term.text[idx-1]  # The vowel preceding '!'
        
        # Tag it. E.g., 'u' -> 'udit', 'i' -> 'idit', 'f' -> 'fdit'
        term.tags.add(f"{vowel}dit")
        
        # Tasya lopaH (1.3.9) - Remove the vowel and the '!'
        term.text = term.text[:idx-1] + term.text[idx+1:]


    # -----------------------------------------------------------------------
    # Rules specific to Pratyayas (Suffixes/Infixes)
    # -----------------------------------------------------------------------
    if term.term_type in['pratyaya', 'vikaraRa', 'lakara']:
        
        # Rule 1.3.3: hal antyam 
        # "A final consonant in an upadeza is an 'it'."
        if term.text and term.text[-1] in SLP1_CONSONANTS:
            final_char = term.text[-1]
            
            # --- NEW: Rule 1.3.4 ---
            # 'na vibhaktau tusmAH': Protects dentals, s, and m in Tin/Sup affixes
            is_vibhakti = 'tin' in term.tags
            is_tusmah = final_char in['t', 'T', 'd', 'D', 'n', 's', 'm']
            
            if not (is_vibhakti and is_tusmah):
                term.tags.add(f"{final_char}it")
                term.text = term.text[:-1] # Remove the final consonant