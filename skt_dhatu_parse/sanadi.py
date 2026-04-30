"""
sanadi.py
Pipeline for Secondary Roots (Causative, Desiderative, etc.)
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from . import rules

def derive_secondary_root(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
    """Derives a new secondary Dhatu (like a Causative) from a base Dhatu."""
    prakriya = Prakriya()
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    resolve_it_markers(dhatu)
    rules.dhatvadeh_sah_sah_no_nah(prakriya)  
    rules.idito_num_dhatoh(prakriya)
    
    # 3. Add Secondary Affix (e.g., 'Ric')
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    pratyaya.tags.add('ardhadhatuka') # Crucial tag so Guna can fire!
    prakriya.add_term(pratyaya)

    # 4. Resolve Affix Markers
    resolve_it_markers(pratyaya)       # Strips 'Ric' to 'i' + Rit

    # 5. Apply Vrddhi & Augment Rules
    rules.pug_nau(prakriya)        
    rules.ata_upadhayah(prakriya)  
    rules.aco_nniti(prakriya)
    rules.sarvadhatuka_ardhadhatukayoh(prakriya)   
    
    rules.eco_yayavayah(prakriya)  
    rules.sanadyanta_dhatavah(prakriya)
    
    return prakriya