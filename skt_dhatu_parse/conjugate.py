"""
conjugate.py
Generates a full 3x3 verbal paradigm table.
"""
import copy
from .engine import derive
from .dhatu_loader import DEFAULT_DB_PATH
from .models import Term

def print_conjugation(
    dhatu_slp1: str,
    lakara_name: str = 'laW',
    gana: int = None,
    db_path: str = DEFAULT_DB_PATH,
    upasarga: str = None,
    custom_dhatu: Term = None  # <--- NEW PARAMETER
) -> None:
    
    print(f"\n======================================")
    gana_text = f"Gaṇa {gana}" if gana else "Auto-Gaṇa"
    prefix_text = f"{upasarga}-" if upasarga else ""
    
    # If a custom root (like Causative) was passed, display that instead!
    root_text = custom_dhatu.text if custom_dhatu else dhatu_slp1
    
    print(f" Conjugation: {prefix_text}{root_text} | {lakara_name} | {gana_text}")
    print(f"======================================")
    
    purushas = ['prathama', 'madhyama', 'uttama']
    print(f"{'Person':<12} | {'Singular':<10} | {'Dual':<10} | {'Plural':<10}")
    print("-" * 50)
    
    for p in purushas:
        # We MUST deepcopy the custom root so the state machine 
        # doesn't destroy it for the next loop iteration!
        d_eka = copy.deepcopy(custom_dhatu) if custom_dhatu else None
        d_dvi = copy.deepcopy(custom_dhatu) if custom_dhatu else None
        d_bahu = copy.deepcopy(custom_dhatu) if custom_dhatu else None
        
        eka = derive(dhatu_slp1, lakara_name, purusha=p, vacana=0, gana=gana, db_path=db_path, upasarga=upasarga, custom_dhatu=d_eka)
        dvi = derive(dhatu_slp1, lakara_name, purusha=p, vacana=1, gana=gana, db_path=db_path, upasarga=upasarga, custom_dhatu=d_dvi)
        bahu = derive(dhatu_slp1, lakara_name, purusha=p, vacana=2, gana=gana, db_path=db_path, upasarga=upasarga, custom_dhatu=d_bahu)
        
        if eka and dvi and bahu:
            print(f"{p.capitalize():<12} | {eka.get_current_string():<10} | {dvi.get_current_string():<10} | {bahu.get_current_string():<10}")
        else:
            print(f"Failed to derive forms for {p}")