"""
krdanta.py
Pipeline for Primary Derivatives (Participles/Krdantas).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from . import rules

def derive_krdanta(dhatu_slp1: str, pratyaya_upadeza: str, gana: int = None, db_path: str = DEFAULT_DB_PATH, upasargas: list[str] = None) -> Prakriya:
    prakriya = Prakriya()
    
    # 1. Map Upasargas
    if upasargas:
        for u in upasargas: prakriya.add_term(Term(u, 'upasarga'))
        
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    resolve_it_markers(dhatu)
    rules.dhatvadeh_sah_sah_no_nah(prakriya)  
    rules.idito_num_dhatoh(prakriya)
    
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    prakriya.add_term(pratyaya)
    resolve_it_markers(pratyaya)

    if 'Sit' in pratyaya.tags: pratyaya.tags.add('sarvadhatuka')
    else: pratyaya.tags.add('ardhadhatuka')
        
    # 2. Vikarana & Sārvadhātuka Morphing
    if 'sarvadhatuka' in pratyaya.tags:
        rules.insert_vikarana(prakriya)
        vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
        if vikarana: resolve_it_markers(vikarana)
        rules.sarvadhatukam_apit(prakriya)
        rules.sna_sandhi(prakriya)
        rules.se_mucadinam(prakriya)
        rules.paghra_sthadi_adesha(prakriya) 

        rules.vikarana_guna(prakriya)
        rules.kr_u_morphing(prakriya)
        rules.snasor_allopah(prakriya)

    # 3. Augments & Internal Morphing
    rules.id_yati(prakriya)
    rules.ato_yuk(prakriya)
    rules.yuvor_anakau(prakriya)    
    rules.stha_adi_ita(prakriya)
    rules.it_agama(prakriya)                
    rules.aco_nniti(prakriya)
    rules.ata_upadhayah(prakriya)
    rules.gam_hana_jana_lopa(prakriya)
    rules.vacisvapiyajadinam_kiti(prakriya)
    rules.srujidrusor_jhaly_amakiti(prakriya)  
    rules.che_ca(prakriya)                           
    
    # 3.5 Remove empty terms
    prakriya.terms =[t for t in prakriya.terms if t.text]
    
    # 4. Phonetic Vowel Rules
    rules.sarvadhatuka_ardhadhatukayoh(prakriya)  
    rules.eco_yayavayah(prakriya)                 
    rules.iko_yanaci(prakriya)
    rules.ato_gune(prakriya)                 
    rules.akah_savarne_dirghah(prakriya)
    
    # 5. Consonant Sandhi
    rules.anunasikalopo_jhali_kniti(prakriya)  
    rules.radabhyam_nishthato_nah(prakriya)
    rules.vrasca_bhrasja_sruja_mruja(prakriya) 
    rules.choh_kuh(prakriya)                
    rules.ho_dhah_dader_ghah(prakriya)      
    rules.jhasas_tathor_dho_dhah(prakriya)  
    rules.jhalam_jas_jhasi(prakriya)
    rules.khari_ca(prakriya)  
    rules.stuna_stuh(prakriya)    
    rules.nascapadantasya_jhali(prakriya)          
    rules.anusvarasya_yayi_parasavarnah(prakriya)  
    rules.anusvarasya_yayi_parasavarnah(prakriya)
    rules.rashabhyam_no_nah(prakriya)       
    
    # 6. Upasarga Final Application
    rules.upasarga_satva(prakriya)
    rules.upasarga_sandhi(prakriya)
    
    return prakriya