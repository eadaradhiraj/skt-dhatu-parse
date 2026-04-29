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
    ho_dhah_dader_ghah,
    dhatvadeh_sah_sah_no_nah, 
    sarvadhatuka_ardhadhatukayoh, 
    eco_yayavayah, 
    vrasca_bhrasja_sruja_mruja, 
    stuna_stuh 
)

def derive_krdanta(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
    prakriya = Prakriya()
    
    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Meta-Markers & PREPROCESS
    resolve_it_markers(dhatu)
    dhatvadeh_sah_sah_no_nah(prakriya)  # Fixes Yizvapa -> svap
    idito_num_dhatoh(prakriya)
    
    # 3. Add Krt Pratyaya 
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    pratyaya.tags.add('ardhadhatuka') 
    prakriya.add_term(pratyaya)
    
    # 4. Resolve Pratyaya Markers 
    resolve_it_markers(pratyaya)
    
    # 5. Apply iW Augment (SeT/AniW logic)
    it_agama(prakriya)                
    
    # 6. Suffix Text Replacements & Vowel Morphing
    yuvor_anakau(prakriya)    
    ata_upadhayah(prakriya)
    vacisvapiyajadinam_kiti(prakriya)
    sarvadhatuka_ardhadhatukayoh(prakriya)  # BU -> Bo
    eco_yayavayah(prakriya)                 # Bo + i -> Bavi
    
    # 7. Consonant Sandhi & Deletions
    anunasikalopo_jhali_kniti(prakriya)  
    radabhyam_nishthato_nah(prakriya) 
    vrasca_bhrasja_sruja_mruja(prakriya) # sfj -> sfz
    choh_kuh(prakriya)                
    ho_dhah_dader_ghah(prakriya)      
    jhasas_tathor_dho_dhah(prakriya)  
    jhalam_jas_jhasi(prakriya)        
    stuna_stuh(prakriya)                 # ta -> wa
    rashabhyam_no_nah(prakriya)       
    
    return prakriya