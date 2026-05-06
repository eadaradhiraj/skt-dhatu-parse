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
    if pratyaya_upadeza == 'Ric':
        rules.pug_nau(prakriya)
        rules.labh_rabh_num(prakriya)
        rules.han_ghatva_tatva(prakriya)
        rules.ata_upadhayah(prakriya)  
        rules.aco_nniti(prakriya)
        rules.sarvadhatuka_ardhadhatukayoh(prakriya)   
        rules.eco_yayavayah(prakriya)  
    elif pratyaya_upadeza == 'san':
        rules.iko_jhal(prakriya)      # MUST run first to apply 'kit' tag
        rules.it_agama(prakriya)      # Can now accurately block iṭ due to 'kit'
        rules.ajjhanagamam_sani(prakriya)
        
        rules.sanyan_rta_id_dhatoh(prakriya)
        rules.hali_ca(prakriya)
        rules.sarvadhatuka_ardhadhatukayoh(prakriya)
        
        rules.sanyan_reduplication(prakriya)
        rules.jes_ca(prakriya)
        rules.haladi_seshah(prakriya)
        rules.hrasvah(prakriya)
        rules.ur_at(prakriya)
        rules.abhyase_car_ca(prakriya)
        rules.kuhos_cuh(prakriya)
        rules.sany_atah(prakriya)
        
        rules.jhasas_tathor_dho_dhah(prakriya)
        rules.jhalam_jas_jhasi(prakriya)
        rules.ekaco_baso_bhas(prakriya)
        rules.sadhoh_kas_si(prakriya)
        rules.khari_ca(prakriya)
        rules.adesa_pratyayayoh(prakriya)
    rules.sanadyanta_dhatavah(prakriya)
    
    return prakriya