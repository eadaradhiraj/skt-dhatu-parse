"""
engine.py
"""
from dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from models import Term, Prakriya
from anubandha import resolve_it_markers
from rules import (
    substitute_lakara, insert_vikarana, atmanepada_tere, 
    idito_num_dhatoh, sarvadhatuka_ardhadhatukayoh, eco_yayavayah,
    ato_dirgho_yayi, rutva_visarga, jhonta, ato_gune, thasah_se, ato_nitah
)

def derive(dhatu_slp1: str, lakara_name: str = 'laW', 
           purusha: str = 'prathama', vacana: int = 0,
           gana: int = None,
           db_path: str = DEFAULT_DB_PATH):
           
    prakriya = Prakriya()
    
    # 1-4. Fetch, It-Lopa, Lakara setup
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)
    
    lakara = Term(lakara_name, 'lakara')
    prakriya.add_term(lakara)
    resolve_it_markers(lakara)
    
    # 5. Substitute Lakara with Tin
    substitute_lakara(prakriya, purusha=purusha, vacana=vacana)
    suffix = prakriya.terms[-1]
    
    # 6. Apply Jhonta (Jh -> ant) IMMEDIATELY after substitution
    jhonta(prakriya)
    thasah_se(prakriya)    # <-- Changes TAs to se BEFORE 'tere' can ruin it!
    
    # 7. Suffix It-Lopa & Atmanepada Morphing
    resolve_it_markers(suffix)
    atmanepada_tere(prakriya)
    
    # 8. Vikarana Insertion & It-Lopa
    insert_vikarana(prakriya)
    if len(prakriya.terms) > 2:
        vikarana = prakriya.terms[1]
        resolve_it_markers(vikarana)
        
    # 9. Phonetic Morphing (Guna & Sandhi)
    sarvadhatuka_ardhadhatukayoh(prakriya)
    eco_yayavayah(prakriya)
    
    # 10. Lengthening (a -> A before y, v, m)
    ato_dirgho_yayi(prakriya)
    
    # 11. Final Vowel Merges (a + anti -> anti)
    ato_nitah(prakriya)    # <-- NEW: Resolves a + Ate -> ete
    ato_gune(prakriya)     # Resolves a + anti -> anti
    
    # 12. Word-Final Rules (s -> H)
    rutva_visarga(prakriya)
    
    return prakriya