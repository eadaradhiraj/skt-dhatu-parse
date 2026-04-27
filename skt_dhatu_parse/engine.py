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
    tasthasthamipam, samyogantasya_lopah,
    thasah_se, ato_nitah,
    liti_dhator_anabhyasasya, hrasvah, bhavater_ah, abhyase_car_ca, bhuvo_vug_lunlitoh
)

def derive(dhatu_slp1: str = None, lakara_name: str = 'laW', 
           purusha: str = 'prathama', vacana: int = 0,
           gana: int = None,
           db_path: str = DEFAULT_DB_PATH,
           custom_dhatu: Term = None) -> Prakriya:
           
    prakriya = Prakriya()
    
    # ==========================================
    # PHASE 1: INITIALIZATION & DATA FETCHING
    # ==========================================
    
    # 1. Fetch or Receive Dhatu
    if custom_dhatu:
        dhatu = custom_dhatu
        # Secondary roots act like Gana 1 (taking 'Sap' infix)
        if not any(tag.startswith('gana_') for tag in dhatu.tags):
            dhatu.tags.add('gana_1')
        # Default to Parasmaipada for standard causative active voice
        if 'parasmaipada' not in dhatu.tags and 'atmanepada' not in dhatu.tags:
            dhatu.tags.add('parasmaipada')
    else:
        dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
        if not dhatus: 
            return None
        dhatu = dhatus[0] 
        
    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Anubandhas and Apply Root Augments
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)  # idit -> num augment (e.g., ah -> aMh)
    
    # 3. Add Lakara (Tense/Mood) and Past Tense Prefix (aW)
    lakara = Term(lakara_name, 'lakara')
    lakara.tags.add(lakara_name) # Ensure tags like 'laN' or 'lfW' are passed down
    prakriya.add_term(lakara)
    at_agama(prakriya)           # 6.4.71: Adds 'aW' prefix for laN
    
    # 4. Resolve Initial Meta-Markers for Prefix/Lakara
    for term in prakriya.terms:
        resolve_it_markers(term)
    
    # ==========================================
    # PHASE 2: SUFFIX SUBSTITUTIONS
    # ==========================================
    
    # 5. Substitute Lakara with 18 Tiṅ Suffixes (ti/tas/Ji etc.)
    substitute_lakara(prakriya, purusha=purusha, vacana=vacana)
    
    # 6. Early Suffix Replacements
    jhonta(prakriya)            # 7.1.3: Jh -> ant
    thasah_se(prakriya)         # 3.4.80: ThAs -> se
    tasthasthamipam(prakriya)   # 3.4.101: tas/Thas/Tha/mip -> tAm/tam/ta/am (Past Tense)
    
    # 7. Resolve Suffix Markers and apply Voice Morphing
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    atmanepada_tere(prakriya)   # 3.4.79: ta -> te
    itasca(prakriya)            # 3.4.100: Drops terminal 'i' for Past Tense
    
    # ==========================================
    # PHASE 3: VIKARANA (CLASS INFIXES) & AUGMENTS
    # ==========================================
    
    # 8. Insert Vikarana (Sap, Syan, Sa, or sya)
    insert_vikarana(prakriya)
    
    # 9. Resolve Vikarana Markers and add Future Tense Augment
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if vikarana:
        resolve_it_markers(vikarana)
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
    
    # ==========================================
    # PHASE 6: WORD-FINAL OPERATIONS
    # ==========================================
    
    # 12. Terminal Consonant Rules
    samyogantasya_lopah(prakriya)           # 8.2.23: Drops 't' from 'nt'
    rutva_visarga(prakriya)                 # 8.3.15: Terminal 's' -> 'H'
    
    return prakriya