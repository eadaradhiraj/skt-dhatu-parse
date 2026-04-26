from engine import derive

def print_conjugation(dhatu_slp1: str, lakara_name: str = 'laW'):
    print(f"\n======================================")
    print(f" Conjugation for: {dhatu_slp1} ({lakara_name})")
    print(f"======================================")
    
    purushas =['prathama', 'madhyama', 'uttama']
    
    # Header
    print(f"{'Person':<12} | {'Singular':<10} | {'Dual':<10} | {'Plural':<10}")
    print("-" * 50)
    
    for p in purushas:
        eka = derive(dhatu_slp1, lakara_name, purusha=p, vacana=0, gana=1)
        dvi = derive(dhatu_slp1, lakara_name, purusha=p, vacana=1, gana=1)
        bahu = derive(dhatu_slp1, lakara_name, purusha=p, vacana=2, gana=1)
        
        # Format the output beautifully
        if eka and dvi and bahu:
            print(f"{p.capitalize():<12} | {eka.get_current_string():<10} | {dvi.get_current_string():<10} | {bahu.get_current_string():<10}")
        else:
            print(f"Failed to derive forms for {p}")

if __name__ == "__main__":
    # Let's generate the tables for the verbs we've built!
    print_conjugation('BU')   # bhū (Parasmaipada)
    print_conjugation('aMh')  # aṃh (Ātmanepada)