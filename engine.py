from dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from models import Term, Prakriya
from anubandha import resolve_it_markers
from rules import substitute_lakara, insert_vikarana, atmanepada_tere

def derive(dhatu_slp1: str, lakara_name: str = 'laW', db_path: str = DEFAULT_DB_PATH):
    prakriya = Prakriya()
    
    # 1. Fetch from Database
    dhatus = get_dhatu(dhatu_slp1, db_path=db_path)
    if not dhatus: return None
    dhatu = dhatus[0] 
    prakriya.add_term(dhatu)
    
    # 2. Resolve Dhatu Anubandhas
    resolve_it_markers(dhatu)
    
    # 3. Add Lakara
    lakara = Term(lakara_name, 'lakara')
    prakriya.add_term(lakara)
    
    # 4. Resolve LAKARA Anubandhas (e.g., laW -> la + 'Wit' tag) <--- NEW!
    resolve_it_markers(lakara)
    
    # 5. Substitute Lakara with Tin (inherits 'Wit' tag)
    substitute_lakara(prakriya, purusha='prathama', vacana=0)
    
    # 6. Resolve Suffix Anubandhas
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    
    # 7. Apply Atmanepada 'e' substitution (ta -> te) <--- NEW!
    atmanepada_tere(prakriya)
    
    # 8. Insert Vikarana
    insert_vikarana(prakriya)
    
    # 9. Resolve Vikarana Anubandhas
    vikarana = prakriya.terms[1]
    resolve_it_markers(vikarana)
    
    return prakriya