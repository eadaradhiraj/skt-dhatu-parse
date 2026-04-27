from .engine import derive
from .dhatu_loader import DEFAULT_DB_PATH

def print_conjugation(
    dhatu_slp1: str,
    lakara_name: str = 'laW',
    gana: int = None,
    db_path: str = DEFAULT_DB_PATH
) -> None:
    print(f"\n======================================")
    gana_text = f"Gaṇa {gana}" if gana else "Auto-Gaṇa"
    print(f" Conjugation: {dhatu_slp1} | {lakara_name} | {gana_text}")
    print(f"======================================")
    
    purushas =['prathama', 'madhyama', 'uttama']
    
    print(f"{'Person':<12} | {'Singular':<10} | {'Dual':<10} | {'Plural':<10}")
    print("-" * 50)
    
    for p in purushas:
        eka = derive(dhatu_slp1, lakara_name, purusha=p, vacana=0, gana=gana, db_path=db_path)
        dvi = derive(dhatu_slp1, lakara_name, purusha=p, vacana=1, gana=gana, db_path=db_path)
        bahu = derive(dhatu_slp1, lakara_name, purusha=p, vacana=2, gana=gana, db_path=db_path)
        
        if eka and dvi and bahu:
            print(f"{p.capitalize():<12} | {eka.get_current_string():<10} | {dvi.get_current_string():<10} | {bahu.get_current_string():<10}")
        else:
            print(f"Failed to derive forms for {p}")

if __name__ == "__main__":
    print_conjugation('BU', gana=1)