"""
decline.py
Generates a full 7x3 nominal declension table.
"""
from .subanta import derive_subanta

def print_declension(pratipadika: str, gender: str = 'm') -> None:
    if gender == 'f' and pratipadika.endswith('a'):
        pratipadika = pratipadika[:-1] + 'A'
        print(f"\n✨ Auto-applied feminine ṭāp (ā) suffix: {pratipadika}")
    stem_type = f"{pratipadika[-1]}-stem" if pratipadika[-1] in "aAiIuUfFxX" else "Consonant-stem"
    g_str = "Masculine" if gender == 'm' else "Feminine" if gender == 'f' else "Neuter"
    
    print(f"\n=======================================================")
    print(f" Declension (Subanta): {pratipadika} | {g_str} {stem_type}")
    print(f"=======================================================")
    
    vibhaktis =['1st (Nom)', '2nd (Acc)', '3rd (Inst)', '4th (Dat)', '5th (Abl)', '6th (Gen)', '7th (Loc)']
    print(f"{'Case':<12} | {'Singular':<15} | {'Dual':<15} | {'Plural':<15}")
    print("-" * 65)
    
    for i, v_name in enumerate(vibhaktis):
        v = i + 1
        eka = derive_subanta(pratipadika, v, 0, gender)
        dvi = derive_subanta(pratipadika, v, 1, gender)
        bahu = derive_subanta(pratipadika, v, 2, gender)
        
        eka_str = eka.get_current_string() if eka else "Failed"
        dvi_str = dvi.get_current_string() if dvi else "Failed"
        bahu_str = bahu.get_current_string() if bahu else "Failed"
        
        print(f"{v_name:<12} | {eka_str:<15} | {dvi_str:<15} | {bahu_str:<15}")
    print()
