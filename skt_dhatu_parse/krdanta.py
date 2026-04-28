"""
krdanta.py
Pipeline for Primary Derivatives (Participles/Krdantas).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    idito_num_dhatoh,
    jhasas_tathor_dho_dhah,
    jhalam_jas_jhasi,
    yuvor_anakau,        
    ata_upadhayah,       
    rashabhyam_no_nah,
    anunasikalopo_jhali_kniti,
    vacisvapiyajadinam_kiti,   
    choh_kuh,                  
    radabhyam_nishthato_nah,
    it_agama,
    ho_dhah_dader_ghah
)

def derive_krdanta(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
    prakriya = Prakriya()
    
    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Meta-Markers
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)
    
    # 3. Add Krt Pratyaya 
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    pratyaya.tags.add('ardhadhatuka') # Rule 3.4.114
    prakriya.add_term(pratyaya)
    
    # 4. Resolve Pratyaya Markers 
    resolve_it_markers(pratyaya)

    # 5. Apply iW Augment (SeT/AniW logic)
    it_agama(prakriya)                # paW + ta -> paW + ita
    
    # 6. Suffix Text Replacements && Internal Root Vowel Morphing
    yuvor_anakau(prakriya) 
    ata_upadhayah(prakriya)
    vacisvapiyajadinam_kiti(prakriya) # vac -> uc
    
    # 7. Consonant Sandhi & Deletions
    anunasikalopo_jhali_kniti(prakriya)  
    radabhyam_nishthato_nah(prakriya) # Cid + ta -> Cin + na
    choh_kuh(prakriya)                # uc + ta -> uk + ta
    ho_dhah_dader_ghah(prakriya)      # duh + ta -> duG + ta
    jhasas_tathor_dho_dhah(prakriya)  # duG + ta -> duG + Da
    jhalam_jas_jhasi(prakriya)        # duG + Da -> dug + Da  
    rashabhyam_no_nah(prakriya)       
    
    return prakriya