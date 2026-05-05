"""
subanta.py
The derivation pipeline for Nominal Declensions (Subanta).
"""
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .sup_affixes import SUP_AFFIXES
from . import rules

def derive_subanta(pratipAdika: str, linga: str, vibhakti: str, vacana: int) -> Prakriya:
    prakriya = Prakriya()
    
    stem = Term(pratipAdika, 'prAtipadika')
    stem.tags.add(linga)
    
    last_char = stem.text[-1]
    if last_char in['a', 'i', 'u', 'f', 'x', 'e', 'o', 'E', 'O', 'A', 'I', 'U', 'F']:
        stem.tags.add('ajanta')
        stem.tags.add(f"ends_with_{last_char}")
    else:
        stem.tags.add('halanta')
        
    prakriya.add_term(stem)
    
    sup_upadeza = SUP_AFFIXES[vibhakti][vacana]
    affix = Term(sup_upadeza, 'pratyaya')
    affix.tags.add('sup')
    affix.tags.add(vibhakti)
    if vacana == 0: affix.tags.add('ekavacana')
    elif vacana == 1: affix.tags.add('dvivacana')
    else: affix.tags.add('bahuvacana')
    
    if vibhakti == 'sambodhana' and vacana == 0:
        affix.tags.add('sambuddhi')
    
    prakriya.add_term(affix)
    resolve_it_markers(affix)
    
    rules.rutva_visarga(prakriya)
    return prakriya
