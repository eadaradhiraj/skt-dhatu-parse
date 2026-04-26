from dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from models import Term, Prakriya
from anubandha import resolve_it_markers
from rules import (
    substitute_lakara, insert_vikarana, atmanepada_tere, 
    idito_num_dhatoh, sarvadhatuka_ardhadhatukayoh, eco_yayavayah,
    ato_dirgho_yayi, rutva_visarga # <-- Import new rules
)

def derive(dhatu_slp1: str, lakara_name: str = 'laW', 
           purusha: str = 'prathama', vacana: int = 0, # <-- Add these params!
           db_path: str = DEFAULT_DB_PATH):
           
    prakriya = Prakriya()
    
    # 1-4. Fetch, It-Lopa, Add Lakara, Resolve Lakara Anubandhas
    dhatus = get_dhatu(dhatu_slp1, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)
    lakara = Term(lakara_name, 'lakara')
    prakriya.add_term(lakara)
    resolve_it_markers(lakara)
    
    # 5. Substitute Lakara with Tin (Pass Purusha and Vacana!)
    substitute_lakara(prakriya, purusha=purusha, vacana=vacana)
    
    # 6-11. Resolve Suffix, Atmanepada 'e', Vikarana, It-Lopa, Guna, Sandhi
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    atmanepada_tere(prakriya)
    insert_vikarana(prakriya)
    if len(prakriya.terms) > 2: # Ensure vikarana exists
        vikarana = prakriya.terms[1]
        resolve_it_markers(vikarana)
    sarvadhatuka_ardhadhatukayoh(prakriya)
    eco_yayavayah(prakriya)
    
    # --- NEW: Lengthening and Word-Final rules ---
    
    # 12. Lengthen 'a' to 'A' before 'm' or 'v' (yaY)
    ato_dirgho_yayi(prakriya)
    
    # 13. Convert terminal 's' to 'H'
    rutva_visarga(prakriya)
    
    return prakriya