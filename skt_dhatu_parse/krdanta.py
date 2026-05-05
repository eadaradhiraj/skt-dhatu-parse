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
    
    # 1. Map Upasargas & intercept ktvA to lyap
    if upasargas:
        for u in upasargas: prakriya.add_term(Term(u, 'upasarga'))
        if pratyaya_upadeza == 'ktvA':
            pratyaya_upadeza = 'lyap'
            prakriya.log("Rule 7.1.37: samāse'nañpūrve ktvo lyap (ktvA replaced by lyap)")
        
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 

    if any(t == 'gana_10' for t in dhatu.tags) and 'sanadi' not in dhatu.tags:
        from .sanadi import derive_secondary_root
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.upadeza)
        sanadi_prakriya = derive_secondary_root(clean_dhatu, 'Ric', gana=10, db_path=db_path)
        if sanadi_prakriya: dhatu = sanadi_prakriya.terms[0]

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
        rules.akrtsarvadhatukayor_dirghah(prakriya)
        rules.sarvadhatukam_apit(prakriya)
        rules.sna_sandhi(prakriya)
        rules.se_mucadinam(prakriya)
        rules.paghra_sthadi_adesha(prakriya) 
        rules.jna_janor_ja(prakriya)

        rules.vikarana_guna(prakriya)
        rules.kr_u_morphing(prakriya)
        rules.snasor_allopah(prakriya)

    # 2.5 Clean up ghost terms early
    prakriya.terms =[t for t in prakriya.terms if t.text]

    # 3. Augments & Internal Morphing
    rules.id_yati(prakriya)
    rules.ato_yuk(prakriya)
    rules.yuvor_anakau(prakriya)    
    rules.stha_adi_ita(prakriya)
    rules.it_agama(prakriya)
    rules.nisthayam_seti(prakriya)
    rules.sino_gunah(prakriya)
    rules.han_ghatva_tatva(prakriya)
    rules.aco_nniti(prakriya)
    rules.ata_upadhayah(prakriya)
    rules.rta_id_dhatoh(prakriya)
    rules.gam_hana_jana_lopa(prakriya)
    rules.sasa_id_anghaloh(prakriya)
    rules.vacisvapiyajadinam_kiti(prakriya)
    rules.srujidrusor_jhaly_amakiti(prakriya)  
    rules.che_ca(prakriya)                           
    rules.aane_muk(prakriya)
    rules.hrasvasya_piti_krti_tuk(prakriya)

    # 4. Phonetic Vowel Rules
    rules.sarvadhatuka_ardhadhatukayoh(prakriya)  
    rules.eco_yayavayah(prakriya)                 
    rules.usy_apadantat(prakriya)                 
    rules.ato_gune(prakriya)
    rules.atas_ca(prakriya)
    rules.ad_gunah(prakriya)
    rules.vrddhir_eci(prakriya)
    rules.akah_savarne_dirghah(prakriya)
    rules.iko_yanaci(prakriya)

    # 4.5 Clean up ghost terms AGAIN
    prakriya.terms =[t for t in prakriya.terms if t.text]
    
    # 5. Consonant Sandhi
    rules.hali_ca(prakriya)
    rules.anunasikalopo_jhali_kniti(prakriya)  
    rules.radabhyam_nishthato_nah(prakriya)
    rules.vrasca_bhrasja_sruja_mruja(prakriya) 
    rules.choh_kuh(prakriya)                
    rules.ho_dhah_dader_ghah(prakriya)      
    rules.jhasas_tathor_dho_dhah(prakriya)  
    
    rules.stuna_stuh(prakriya)    
    rules.dho_dhe_lopah(prakriya)                  
    rules.jhalam_jas_jhasi(prakriya)
    
    rules.khari_ca(prakriya)  
    rules.nascapadantasya_jhali(prakriya)          
    rules.anusvarasya_yayi_parasavarnah(prakriya)  
    rules.rashabhyam_no_nah(prakriya)       
    
    # 6. Upasarga Final Application
    rules.upasarga_satva(prakriya)
    rules.upasarga_sandhi(prakriya)
    
    return prakriya