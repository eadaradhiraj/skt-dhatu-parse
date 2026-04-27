"""
sanadi.py
Pipeline for Secondary Roots (Causative, Desiderative, etc.)
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    idito_num_dhatoh,
    ata_upadhayah,
    aco_nniti,
    eco_yayavayah,
    sanadyanta_dhatavah,
    dhatvadeh_sah_sah_no_nah,
    pug_nau
)

def derive_secondary_root(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
    """Derives a new secondary Dhatu (like a Causative) from a base Dhatu."""
    prakriya = Prakriya()
    
    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: 
        return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    # 2. Resolve Root Markers & Preprocessing
    resolve_it_markers(dhatu)
    dhatvadeh_sah_sah_no_nah(prakriya)  # <--- NEW: Fixes zWA -> sTA
    idito_num_dhatoh(prakriya)
    
    # 3. Add Secondary Affix (e.g., 'Ric')
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    prakriya.add_term(pratyaya)
    
    # 4. Resolve Affix Markers ('Ric' loses 'R' and 'c' -> 'i')
    resolve_it_markers(pratyaya)
    
    # 5. Apply Vrddhi & Augment Rules
    pug_nau(prakriya)        # <--- NEW: Adds 'puk' augment (sTA + Ric -> sTAp + i)
    ata_upadhayah(prakriya)  # Vṛddhi for penultimate 'a' (e.g., ram + i -> rAmi)
    aco_nniti(prakriya)      # Vṛddhi for terminal vowels (e.g., BU + i -> BO + i)
    
    # 6. Apply Sandhi
    eco_yayavayah(prakriya)  # BO + i -> BAv + i
    
    # 7. Merge into a new Dhatu!
    sanadyanta_dhatavah(prakriya)
    
    return prakriya