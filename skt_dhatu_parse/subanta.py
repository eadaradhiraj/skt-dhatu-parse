"""
subanta.py
Pipeline for Nominal Declensions (Subanta).
"""
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from . import rules

def derive_subanta(pratipadika: str, vibhakti: int, vacana: int, gender: str = 'm') -> Prakriya:
    prakriya = Prakriya()
    
    stem = Term(pratipadika, 'pratipadika')
    if gender == 'n': stem.tags.add('napumsaka')
    elif gender == 'f': stem.tags.add('stri')
    prakriya.add_term(stem)
    
    sup = Term('sup', 'pratyaya')
    prakriya.add_term(sup)
    
    # 1. Substitute the specific 7x3 affix
    rules.substitute_sup(prakriya, vibhakti, vacana)
    resolve_it_markers(sup)
    
    # 2. Advanced Nominal Replacements
    rules.napumsaka_nom_acc(prakriya)
    rules.stri_ap_nom_acc(prakriya)
    rules.stri_nadi_ngit_yA(prakriya)
    
    # 2. Advanced Nominal Replacements
    rules.ta_nasi_nasam_ina_at_syah(prakriya)
    rules.aani_capah(prakriya)
    rules.jasi_ca(prakriya)
    rules.aango_na_astriyam(prakriya)
    rules.aut_ni(prakriya)
    rules.gher_ngiti(prakriya)
    rules.ngasi_ngasosh_ca(prakriya)
    rules.neryah(prakriya)
    rules.ato_bhisa_ais(prakriya)
    rules.hrasvanadyapo_nut_and_nami(prakriya)
    
    # 3. Stem Vowel Modifiers
    rules.suti_ca_yanyi(prakriya)
    rules.bahuvacane_jhalyet(prakriya)
    rules.osi_ca(prakriya)
    
    # 4. Vowel Sandhi
    rules.ami_purvah(prakriya)
    rules.prathamayoh_purvasavarnah(prakriya)
    rules.tasmac_chasah_nah_pumsi(prakriya)
    rules.vrddhir_eci(prakriya)
    rules.ad_gunah(prakriya)
    rules.eco_yayavayah(prakriya)
    rules.akah_savarne_dirghah(prakriya)
    rules.iko_yanaci(prakriya)
    
    # 5. Consonant Sandhi & Cleanup
    rules.adesa_pratyayayoh(prakriya) # ṣatva for rāmeṣu
    rules.natva_sandhi(prakriya)      # ṇatva for rāmeṇa, rāmāṇām
    rules.rutva_visarga(prakriya)     # s -> H
    
    return prakriya
