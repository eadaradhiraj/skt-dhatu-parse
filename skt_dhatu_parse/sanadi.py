"""
sanadi.py
Pipeline for Secondary Roots (Causative, Desiderative, etc.)
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    idito_num_dhatoh, ata_upadhayah, aco_nniti, eco_yayavayah,
    sanadyanta_dhatavah, dhatvadeh_sah_sah_no_nah, pug_nau,
    sarvadhatuka_ardhadhatukayoh
)

def derive_secondary_root(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
    """Derives a new secondary Dhatu (like a Causative) from a base Dhatu."""
    prakriya = Prakriya()
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    resolve_it_markers(dhatu)
    dhatvadeh_sah_sah_no_nah(prakriya)  
    idito_num_dhatoh(prakriya)
    
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    prakriya.add_term(pratyaya)
    resolve_it_markers(pratyaya)

    # 5. Apply Vrddhi & Augment Rules
    pug_nau(prakriya)        
    ata_upadhayah(prakriya)  
    aco_nniti(prakriya)
    sarvadhatuka_ardhadhatukayoh(prakriya)   
    
    eco_yayavayah(prakriya)  
    sanadyanta_dhatavah(prakriya)
    
    return prakriya