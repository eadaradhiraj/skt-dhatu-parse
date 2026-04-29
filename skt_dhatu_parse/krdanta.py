"""
krdanta.py
Pipeline for Primary Derivatives (Participles/Krdantas).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    idito_num_dhatoh, jhasas_tathor_dho_dhah, jhalam_jas_jhasi, yuvor_anakau,        
    ata_upadhayah, rashabhyam_no_nah, anunasikalopo_jhali_kniti, vacisvapiyajadinam_kiti,   
    choh_kuh, radabhyam_nishthato_nah, it_agama, ho_dhah_dader_ghah, dhatvadeh_sah_sah_no_nah, 
    sarvadhatuka_ardhadhatukayoh, eco_yayavayah, vrasca_bhrasja_sruja_mruja, stuna_stuh,
    khari_ca, insert_vikarana, sna_sandhi, se_mucadinam, anusvarasya_yayi_parasavarnah, ato_gune
)

def derive_krdanta(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> Prakriya:
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

    if 'Sit' in pratyaya.tags: pratyaya.tags.add('sarvadhatuka')
    else: pratyaya.tags.add('ardhadhatuka')
        
    if 'sarvadhatuka' in pratyaya.tags:
        insert_vikarana(prakriya)
        vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
        if vikarana: resolve_it_markers(vikarana)
        sna_sandhi(prakriya)
        se_mucadinam(prakriya)

    it_agama(prakriya)                
    yuvor_anakau(prakriya)    
    ata_upadhayah(prakriya)
    vacisvapiyajadinam_kiti(prakriya)
    
    sarvadhatuka_ardhadhatukayoh(prakriya)  
    eco_yayavayah(prakriya)                 
    ato_gune(prakriya)
    
    anunasikalopo_jhali_kniti(prakriya)  
    radabhyam_nishthato_nah(prakriya) 
    vrasca_bhrasja_sruja_mruja(prakriya) 
    choh_kuh(prakriya)                
    ho_dhah_dader_ghah(prakriya)      
    jhasas_tathor_dho_dhah(prakriya)  
    jhalam_jas_jhasi(prakriya)
    khari_ca(prakriya)  
    stuna_stuh(prakriya)                 
    anusvarasya_yayi_parasavarnah(prakriya)
    rashabhyam_no_nah(prakriya)       
    
    return prakriya