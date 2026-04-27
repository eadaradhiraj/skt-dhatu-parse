from dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from models import Term, Prakriya
from anubandha import resolve_it_markers
from rules import *

def derive(dhatu_slp1: str, lakara_name: str = 'laW', purusha: str = 'prathama', vacana: int = 0, gana: int = None, db_path: str = DEFAULT_DB_PATH):
    prakriya = Prakriya()
    
    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)
    
    # 2. Add Lakara and Past Tense Prefix (aW)
    lakara = Term(lakara_name, 'lakara')
    lakara.tags.add(lakara_name) # Ensure tags like 'laN' or 'lfW' are passed down
    prakriya.add_term(lakara)
    at_agama(prakriya)           # <-- NEW: Past tense prefix
    for term in prakriya.terms:
        resolve_it_markers(term)
    
    # 3. Lakara Substitutions
    substitute_lakara(prakriya, purusha=purusha, vacana=vacana)
    jhonta(prakriya)
    thasah_se(prakriya)
    
    # 4. Suffix Anubandhas & Past Tense drops
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    atmanepada_tere(prakriya)
    itasca(prakriya)             # <-- NEW: Drops 'i' for Past Tense
    
    # 5. Insert Vikarana & Future Tense Augment
    insert_vikarana(prakriya)
    vikarana = prakriya.terms[-2]
    resolve_it_markers(vikarana)
    it_agama(prakriya)           # <-- NEW: Adds 'i' to 'sya'
    
    # 6. Guna and Sandhi
    hali_ca(prakriya)            # <-- NEW: div -> dIv
    sarvadhatuka_ardhadhatukayoh(prakriya) # Has built-in Gana 6 prevention!
    eco_yayavayah(prakriya)
    ato_dirgho_yayi(prakriya)
    ato_nitah(prakriya)
    ato_gune(prakriya)
    adesa_pratyayayoh(prakriya)  # <-- NEW: 'isya' -> 'izya'
    rutva_visarga(prakriya)
    
    return prakriya