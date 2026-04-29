"""
engine.py
The main orchestrator for the Paninian derivation pipeline (Prakriya).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    substitute_lakara, insert_vikarana, atmanepada_tere, idito_num_dhatoh, sarvadhatuka_ardhadhatukayoh, 
    eco_yayavayah, ato_dirgho_yayi, rutva_visarga, jhonta, ato_gune, at_agama, itasca, it_agama, 
    adesa_pratyayayoh, hali_ca, tasthasthamipam, samyogantasya_lopah, ur_at, thasah_se, ato_nitah, 
    khari_ca, kuhos_cuh, aco_nniti, liti_dhator_anabhyasasya, hrasvah, bhavater_ah, abhyase_car_ca, 
    bhuvo_vug_lunlitoh, upasarga_sandhi, upasarga_satva, dhatvadeh_sah_sah_no_nah, paghra_sthadi_adesha,
    sna_sandhi, rashabhyam_no_nah, iko_yanaci, se_mucadinam, anusvarasya_yayi_parasavarnah,
    vikarana_guna, kr_u_morphing
)

def derive(dhatu_slp1: str = None, lakara_name: str = 'laW', purusha: str = 'prathama', vacana: int = 0,
           gana: int = None, db_path: str = DEFAULT_DB_PATH, custom_dhatu: Term = None,
           upasargas: list[str] = None, voice: str = None) -> Prakriya:
           
    prakriya = Prakriya()
    if upasargas:
        for u in upasargas: prakriya.add_term(Term(u, 'upasarga'))
        
    if custom_dhatu:
        dhatu = custom_dhatu
        if not any(tag.startswith('gana_') for tag in dhatu.tags): dhatu.tags.add('gana_1')
        if 'parasmaipada' not in dhatu.tags and 'atmanepada' not in dhatu.tags: dhatu.tags.add('parasmaipada')
    else:
        dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
        if not dhatus: return None
        dhatu = dhatus[0] 
        
        if voice:
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('atmanepada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add(voice)
            
        if dhatu_slp1 == 'krI' and upasargas and upasargas[-1] in['vi', 'parA']:
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add('atmanepada')
            prakriya.log(f"Rule 1.3.44: 'krI' becomes Atmanepada after '{upasargas[-1]}'")

    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Anubandhas and Preprocessing
    resolve_it_markers(dhatu)
    dhatvadeh_sah_sah_no_nah(prakriya)  
    idito_num_dhatoh(prakriya)  
    
    # 3. Add Lakara and Past Tense Prefix (aW)
    lakara = Term(lakara_name, 'lakara')
    lakara.tags.add(lakara_name) 
    prakriya.add_term(lakara)
    at_agama(prakriya)           
    
    # 4. Resolve Meta-Markers for Prefix/Lakara
    for term in prakriya.terms:
        if term.term_type != 'dhatu': resolve_it_markers(term)
    
    # 5. Substitute Lakara
    substitute_lakara(prakriya, purusha=purusha, vacana=vacana)
    
    # 6. Early Suffix Replacements
    jhonta(prakriya)            
    thasah_se(prakriya)         
    tasthasthamipam(prakriya)   
    
    # 7. Resolve Suffix Markers and Morphing
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    atmanepada_tere(prakriya)   
    itasca(prakriya)            
    
    # 8. Insert Vikarana
    insert_vikarana(prakriya)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if vikarana: resolve_it_markers(vikarana)
        
    # 9. Gana 9 and Root Substitutions
    sna_sandhi(prakriya)
    se_mucadinam(prakriya)
    paghra_sthadi_adesha(prakriya)
    vikarana_guna(prakriya)
    kr_u_morphing(prakriya)
    it_agama(prakriya)          
    
    # 10. Abhyasa (Reduplication)
    liti_dhator_anabhyasasya(prakriya) 
    hrasvah(prakriya)
    ur_at(prakriya)                    
    bhavater_ah(prakriya)              
    abhyase_car_ca(prakriya)
    kuhos_cuh(prakriya)                
    bhuvo_vug_lunlitoh(prakriya)       
    
    # 11. Core Phonetics
    hali_ca(prakriya)
    aco_nniti(prakriya)                              
    sarvadhatuka_ardhadhatukayoh(prakriya)  
    eco_yayavayah(prakriya)                 
    iko_yanaci(prakriya)
    
    # 12. Sandhi and Final Consonants
    ato_dirgho_yayi(prakriya)               
    ato_nitah(prakriya)                     
    ato_gune(prakriya)                      
    adesa_pratyayayoh(prakriya)             
    rashabhyam_no_nah(prakriya)
    
    khari_ca(prakriya)                      
    samyogantasya_lopah(prakriya)           
    anusvarasya_yayi_parasavarnah(prakriya)
    upasarga_satva(prakriya)                
    upasarga_sandhi(prakriya)               
    rutva_visarga(prakriya)                 
    
    return prakriya