"""
engine.py
The main orchestrator for the Paninian derivation pipeline (Prakriya).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    substitute_lakara, insert_vikarana, atmanepada_tere, 
    idito_num_dhatoh, sarvadhatuka_ardhadhatukayoh, eco_yayavayah,
    ato_dirgho_yayi, rutva_visarga, jhonta, ato_gune, 
    at_agama, itasca, it_agama, adesa_pratyayayoh, hali_ca,
    tasthasthamipam, samyogantasya_lopah, rashabhyam_no_nah,
    thasah_se, ato_nitah, upasarga_satva, sna_sandhi,
    liti_dhator_anabhyasasya, hrasvah, bhavater_ah, abhyase_car_ca, bhuvo_vug_lunlitoh,
    upasarga_sandhi, dhatvadeh_sah_sah_no_nah, paghra_sthadi_adesha
)

def derive(
    dhatu_slp1: str = None, lakara_name: str = 'laW', 
    purusha: str = 'prathama', vacana: int = 0,
    gana: int = None,
    db_path: str = DEFAULT_DB_PATH,
    custom_dhatu: Term = None,
    upasarga: str = None,
    voice: str = None
) -> Prakriya:
           
    prakriya = Prakriya()

    # Add Upasarga FIRST ---
    if upasarga:
        up_term = Term(upasarga, 'upasarga')
        prakriya.add_term(up_term)
    
    # ==========================================
    # PHASE 1: INITIALIZATION & DATA FETCHING
    # ==========================================
    if custom_dhatu:
        dhatu = custom_dhatu
        if not any(tag.startswith('gana_') for tag in dhatu.tags):
            dhatu.tags.add('gana_1')
        if 'parasmaipada' not in dhatu.tags and 'atmanepada' not in dhatu.tags:
            dhatu.tags.add('parasmaipada')
    else:
        dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
        if not dhatus: return None
        dhatu = dhatus[0] 
        
        # --- NEW: Manual Voice Override from CLI ---
        if voice:
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('atmanepada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add(voice)
            
        # Upasarga Voice Overrides (Runs after manual voice!)
        if dhatu_slp1 == 'krI' and upasarga in ['vi', 'parA']:
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.add('atmanepada')
            prakriya.log(f"Rule 1.3.44: 'krI' becomes Atmanepada after '{upasarga}'")
            
    prakriya.add_term(dhatu)
    # ...[Keep Phase 1 and 2 the same] ...

    # ==========================================
    # PHASE 3: VIKARANA (CLASS INFIXES) & AUGMENTS
    # ==========================================
    insert_vikarana(prakriya)
    
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if vikarana:
        resolve_it_markers(vikarana)
        
    sna_sandhi(prakriya)            # <--- DROP THIS IN HERE!
    paghra_sthadi_adesha(prakriya)
    it_agama(prakriya)          # 7.2.35: Adds 'i' to 'sya'
    
    # ==========================================
    # PHASE 4: REDUPLICATION (ABHYASA)
    # ==========================================
    
    liti_dhator_anabhyasasya(prakriya) # 6.1.8: Clones root (BU -> BU + BU)
    hrasvah(prakriya)                  # 7.4.59: Shortens clone (BU -> Bu)
    bhavater_ah(prakriya)              # 7.4.73: Bu -> Ba (Exception for bhū)
    abhyase_car_ca(prakriya)           # 8.4.54: De-aspirates (Ba -> ba)
    bhuvo_vug_lunlitoh(prakriya)       # 6.4.88: Appends 'v' augment before vowels
    
    # ==========================================
    # PHASE 5: PHONETICS, GUNA, AND SANDHI
    # ==========================================
    
    # 10. Core Phonetic Morphing
    hali_ca(prakriya)                       # 8.2.77: div -> dIv
    sarvadhatuka_ardhadhatukayoh(prakriya)  # 7.3.84: Guna (with built-in Gana 6 blocking)
    eco_yayavayah(prakriya)                 # 6.1.78: o + a -> av
    
    # 11. Vowel Sandhi and Consonant Shifts
    ato_dirgho_yayi(prakriya)               # 7.3.101: a -> A (before y, v, m)
    ato_nitah(prakriya)                     # 7.2.81: a + Ate -> ete
    ato_gune(prakriya)                      # 6.1.97: a + anti -> anti
    adesa_pratyayayoh(prakriya)             # 8.3.59: isya -> izya
    rashabhyam_no_nah(prakriya)             # krI + nI -> krIRI
    
    # ==========================================
    # PHASE 6: WORD-FINAL OPERATIONS
    # ==========================================
    
    # 12. Terminal Consonant Rules
    samyogantasya_lopah(prakriya)           # 8.2.23: Drops 't' from 'nt'
    upasarga_satva(prakriya)                # prati + sTA -> pratizWA
    upasarga_sandhi(prakriya)               # 6.1.101: Merge the prefix vowels

    rutva_visarga(prakriya)                 # 8.3.15: Terminal 's' -> 'H'
    
    return prakriya