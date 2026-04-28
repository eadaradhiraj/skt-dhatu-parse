"""
anubandha.py
Rules for identifying and removing 'It' (meta-markers)
"""
from .models import Term

SLP1_CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")

def resolve_it_markers(term: Term) -> None:
    
    # 1. INITIAL & FINAL MARKERS FOR DHATUS
    if term.term_type == 'dhatu':
        # Rule 1.3.5: Adir YiWuqavaH
        for prefix in['Yi', 'wu', 'qu']:
            if term.text.startswith(prefix):
                term.tags.add(f"{prefix}it")
                term.text = term.text[len(prefix):]
                
        # Rule 1.3.3: hal antyam (Strips final consonant of the upadesa)
        if len(term.text) > 0 and term.upadeza[-1] in SLP1_CONSONANTS:
            final_char = term.text[-1]
            term.tags.add(f"{final_char}it")
            term.text = term.text[:-1]

    # 2. NASALIZED VOWELS (All terms)
    for marker in['!', '~']:
        if marker in term.text:
            idx = term.text.find(marker)
            if idx > 0:
                vowel = term.text[idx-1]
                term.tags.add(f"{vowel}dit")
                term.text = term.text[:idx-1] + term.text[idx+1:]

    # 3. MARKERS FOR AFFIXES (Pratyayas, Vikaranas, Lakaras, Agamas)
    if term.term_type in['pratyaya', 'vikaraRa', 'lakara', 'Agama']:
        
        # Rule 1.3.7: cuwU (Initial Palatals and Retroflexes)
        if len(term.text) > 0:
            initial_char = term.text[0]
            if initial_char in['c', 'C', 'j', 'J', 'Y', 'w', 'W', 'q', 'Q', 'R']:
                term.tags.add(f"{initial_char}it")
                term.text = term.text[1:]
                
        # Rule 1.3.8: lazakvataddhite (Initial l, S, velars)
        if len(term.text) > 0:
            initial_char = term.text[0]
            if initial_char in['l', 'S', 'k', 'K', 'g', 'G', 'N']:
                term.tags.add(f"{initial_char}it")
                term.text = term.text[1:]
                
        # Rule 1.3.3 & 1.3.4: hal antyam / na vibhaktau tusmAH
        if len(term.text) > 0 and term.text[-1] in SLP1_CONSONANTS:
            final_char = term.text[-1]
            is_vibhakti = 'tin' in term.tags
            is_tusmah = final_char in['t', 'T', 'd', 'D', 'n', 's', 'm']
            
            if not (is_vibhakti and is_tusmah):
                term.tags.add(f"{final_char}it")
                term.text = term.text[:-1]