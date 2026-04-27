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
    yuvor_anakau,        # <--- NEW
    ata_upadhayah,       # <--- NEW
    rashabhyam_no_nah    # <--- NEW
)

def derive_krdanta(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH):
    prakriya = Prakriya()
    
    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: 
        return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Meta-Markers
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)
    
    # 3. Add Krt Pratyaya
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    prakriya.add_term(pratyaya)
    
    # 4. Resolve Pratyaya Markers (e.g., GhaY -> a + Yit)
    resolve_it_markers(pratyaya)
    
    # 5. Suffix Text Replacements
    yuvor_anakau(prakriya)    # lyuW -> yu -> ana
    
    # 6. Internal Root Vowel Morphing
    ata_upadhayah(prakriya)   # Yit/Rit causes penultimate 'a' -> 'A'
    
    # 7. Consonant Sandhi
    jhasas_tathor_dho_dhah(prakriya)  
    jhalam_jas_jhasi(prakriya)        
    rashabhyam_no_nah(prakriya)       # n -> R
    
    return prakriya