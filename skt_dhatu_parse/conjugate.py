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
    upasargas: list[str] = None,
    custom_dhatu: Term = None,
    voice: str = None
) -> None:
    
    print(f"\n======================================")
    gana_text = f"Gaṇa {gana}" if gana else "Auto-Gaṇa"
    prefix_text = "-".join(upasargas) + "-" if upasargas else ""
    root_text = custom_dhatu.text if custom_dhatu else dhatu_slp1
    
    print(f" Conjugation: {prefix_text}{root_text} | {lakara_name} | {gana_text}")
    print(f"======================================")
    
    purushas = ['prathama', 'madhyama', 'uttama']
    print(f"{'Person':<12} | {'Singular':<18} | {'Dual':<18} | {'Plural':<18}")
    print("-" * 74)
    
    for p in purushas:
        def get_dual_forms(vacana: int) -> str:
            d_norm = copy.deepcopy(custom_dhatu) if custom_dhatu else None
            d_vik = copy.deepcopy(custom_dhatu) if custom_dhatu else None
            
            # Run the primary timeline
            res_norm = derive(dhatu_slp1, lakara_name, purusha=p, vacana=vacana, gana=gana, 
                              db_path=db_path, upasargas=upasargas, custom_dhatu=d_norm, voice=voice, vikalpa=False)
            # Run the alternate timeline
            res_vik = derive(dhatu_slp1, lakara_name, purusha=p, vacana=vacana, gana=gana, 
                             db_path=db_path, upasargas=upasargas, custom_dhatu=d_vik, voice=voice, vikalpa=True)
            
            if not res_norm: return "Failed"
            
            str_norm = res_norm.get_current_string()
            str_vik = res_vik.get_current_string() if res_vik else str_norm
            
            # If the vikalpa timeline diverged, display both!
            if str_norm != str_vik:
                return f"{str_norm}/{str_vik}"
            return str_norm

        eka_str = get_dual_forms(0)
        dvi_str = get_dual_forms(1)
        bahu_str = get_dual_forms(2)
        
        if "Failed" not in[eka_str, dvi_str, bahu_str]:
            print(f"{p.capitalize():<12} | {eka_str:<18} | {dvi_str:<18} | {bahu_str:<18}")
        else:
            print(f"Failed to derive forms for {p}")