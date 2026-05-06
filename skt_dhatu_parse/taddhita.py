"""
taddhita.py
Pipeline for Secondary Nominal Derivatives.
"""
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from . import rules

def derive_taddhita(pratipadika: str, pratyaya_upadeza: str) -> Prakriya:
    prakriya = Prakriya()
    stem = Term(pratipadika, 'pratipadika')
    prakriya.add_term(stem)
    
    suf = Term(pratyaya_upadeza, 'pratyaya')
    suf.tags.add('taddhita')
    prakriya.add_term(suf)
    
    resolve_it_markers(suf)
    rules.taddhita_adivrddhi(prakriya)
    rules.or_gunah(prakriya)
    rules.bhasya_ter_lopah(prakriya)
    rules.eco_yayavayah(prakriya) 
    
    return prakriya
