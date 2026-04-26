"""
anubandha.py
Rules for identifying and removing 'It' (meta-markers)
"""
from models import Term

SLP1_CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")

def resolve_it_markers(term: Term):
    # Rule 1.3.2: Nasalized Vowels (!)
    if '!' in term.text:
        idx = term.text.find('!')
        vowel = term.text[idx-1]
        term.tags.add(f"{vowel}dit")
        term.text = term.text[:idx-1] + term.text[idx+1:]

    if term.term_type in ['pratyaya', 'vikaraRa', 'lakara']:
        
        # Rule 1.3.8: laśakvataddhite (INITIAL CONSONANT)
        if len(term.text) > 0:
            initial_char = term.text[0]
            if initial_char in['l', 'S', 'k', 'K', 'g', 'G', 'N']:
                term.tags.add(f"{initial_char}it")
                term.text = term.text[1:]
                
        # Rule 1.3.3: hal antyam (FINAL CONSONANT)
        if len(term.text) > 0 and term.text[-1] in SLP1_CONSONANTS:
            final_char = term.text[-1]
            
            # Rule 1.3.4: na vibhaktau tusmAH (Protect inflectional suffixes)
            is_vibhakti = 'tin' in term.tags
            is_tusmah = final_char in['t', 'T', 'd', 'D', 'n', 's', 'm']
            
            if not (is_vibhakti and is_tusmah):
                term.tags.add(f"{final_char}it")
                term.text = term.text[:-1]