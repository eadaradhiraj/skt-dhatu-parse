"""
anubandha.py
Rules for identifying and removing 'It' (meta-markers) defined in the first chapter of the Ashtadhyayi.
"""
from .models import Term

SLP1_CONSONANTS = set("kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")

def resolve_it_markers(term: Term) -> None:
    """
    Strips instructional markers (anubandhas) from terms and saves their grammatical implications as tags.
    """
    
    # ==========================================
    # 1. INITIAL & FINAL MARKERS FOR DHATUS
    # ==========================================
    if term.term_type == 'dhatu':
        if 'i!r' in term.text:
            term.tags.add('irit')
            term.text = term.text.replace('i!r', '')
            
        for prefix in ['Yi', 'wu', 'qu']:
            if term.text.startswith(prefix):
                term.tags.add(f"{prefix}it")
                term.text = term.text[len(prefix):]
                
        if len(term.text) > 0 and term.upadeza[-1] in SLP1_CONSONANTS:
            if 'irit' not in term.tags: 
                final_char = term.text[-1]
                term.tags.add(f"{final_char}it")
                term.text = term.text[:-1]

    # ==========================================
    # 2. NASALIZED VOWELS (All terms)
    # ==========================================
    for marker in['!', '~']:
        while marker in term.text:
            idx = term.text.find(marker)
            if idx > 0:
                vowel = term.text[idx-1]
                term.tags.add(f"{vowel}dit")
                term.text = term.text[:idx-1] + term.text[idx+1:]
            else:
                term.text = term.text.replace(marker, "", 1)

    # ==========================================
    # 3. MARKERS FOR AFFIXES
    # ==========================================
    if term.term_type in['pratyaya', 'vikaraRa', 'lakara', 'Agama']:
        
        # Preprocessors for tricky pedagogical affixes
        if term.upadeza == 'Satf':
            term.tags.add('fdit')
            term.tags.add('Sit')
            term.text = 'at'
            return
        elif term.upadeza == 'ktavatu':
            term.tags.add('udit')
            term.tags.add('kit')
            term.text = 'tavat'
            return
        elif term.upadeza == 'tumun':
            term.tags.add('udit')
            term.tags.add('nit')
            term.text = 'tum'
            return
        elif term.upadeza == 'lyap':
            term.tags.add('pit')
            term.tags.add('lit') 
            term.tags.add('kit')
            term.text = 'ya'
            return
        elif term.upadeza == 'SAnac':
            term.tags.add('Sit')
            term.tags.add('cit')
            term.text = 'Ana'
            return
        elif term.upadeza == 'ktin':
            term.tags.add('kit')
            term.tags.add('nit')
            term.text = 'ti'
            return
        elif term.upadeza == 'kyap':
            term.tags.add('kit')
            term.tags.add('pit')
            term.text = 'ya'
            return
        elif term.upadeza == 'Ramul':
            term.tags.add('Rit')
            term.tags.add('lit') 
            term.text = 'am'
            return
        elif term.upadeza == 'Nasi':
            term.tags.add('Nit')
            term.text = 'as'
            return
            
        if len(term.text) > 0:
            initial_char = term.text[0]
            if initial_char in['c', 'C', 'j', 'J', 'Y', 'w', 'W', 'q', 'Q', 'R']:
                term.tags.add(f"{initial_char}it")
                term.text = term.text[1:]
                
        if len(term.text) > 0:
            initial_char = term.text[0]
            if initial_char in['l', 'S', 'k', 'K', 'g', 'G', 'N']:
                term.tags.add(f"{initial_char}it")
                term.text = term.text[1:]
                
        if len(term.text) > 0 and term.upadeza and term.upadeza[-1] in SLP1_CONSONANTS:
            final_char = term.text[-1]
            is_vibhakti = 'tin' in term.tags or any(tag.startswith('vibhakti_') for tag in term.tags)
            is_tusmah = final_char in['t', 'T', 'd', 'D', 'n', 's', 'm']
            
            if not (is_vibhakti and is_tusmah):
                term.tags.add(f"{final_char}it")
                term.text = term.text[:-1]
