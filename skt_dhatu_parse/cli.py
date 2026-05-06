"""
cli.py
Command Line Interface for the Paninian Sanskrit Engine.
"""
import argparse
import sys
from .dhatu_loader import get_dhatu
from .engine import derive
from .conjugate import print_conjugation
from .krdanta import derive_krdanta
from .sanadi import derive_secondary_root
from .rules import UPASARGAS

def resolve_gana(dhatu_slp1: str, user_gana: int = None) -> int:
    dhatus = get_dhatu(dhatu_slp1)
    if not dhatus:
        print(f"❌ Error: Root '{dhatu_slp1}' not found in the database.")
        sys.exit(1)

    available_ganas =[]
    for d in dhatus:
        for tag in d.tags:
            if tag.startswith('gana_'):
                available_ganas.append(int(tag.split('_')[1]))
    
    if user_gana:
        if user_gana not in available_ganas:
            print(f"❌ Error: '{dhatu_slp1}' does not exist in Gaṇa {user_gana}. Available: {available_ganas}")
            sys.exit(1)
        return user_gana
        
    if len(available_ganas) > 1:
        print(f"⚠️  Warning: '{dhatu_slp1}' belongs to multiple classes: {available_ganas}")
        if 1 in available_ganas:
            print("👉 Defaulting to Gaṇa 1. Use -g to specify otherwise.\n")
            return 1
        else:
            default = available_ganas[0]
            print(f"👉 Defaulting to Gaṇa {default}. Use -g to specify otherwise.\n")
            return default
            
    return available_ganas[0]

def main() -> None:
    parser = argparse.ArgumentParser(description="🕉️  Paninian Sanskrit Derivation Engine")
    parser.add_argument("dhatu", nargs="?", default="dummy", help="The SLP1 root/stem to process")
    parser.add_argument("-g", "--gana", type=int, help="Specify the Gaṇa (1-10) for homonyms")
    parser.add_argument("-l", "--lakara", default="laW", help="Lakāra (Tense/Mood)")
    parser.add_argument("-p", "--purusha", default="prathama", choices=["prathama", "madhyama", "uttama"], help="Person")
    parser.add_argument("-v", "--vacana", type=int, default=0, choices=[0, 1, 2], help="Number")
    parser.add_argument("-t", "--table", action="store_true", help="Print the full 3x3 conjugation table")
    parser.add_argument("--krt", type=str, help="Generate a Primary Derivative (Kṛdanta)")
    parser.add_argument("--all-krt", action="store_true", help="Generate all common Kṛdanta forms")
    parser.add_argument("--causative", action="store_true", help="Generate the Causative (Ṇic) secondary root")
    parser.add_argument("--desiderative", action="store_true", help="Generate the Desiderative (san) secondary root")
    parser.add_argument("--voice", choices=["parasmaipada", "atmanepada", "karmani", "bhave"], help="Force a specific voice")
    parser.add_argument("--history", action="store_true", help="Show derivation history")
    parser.add_argument("--decline", action="store_true", help="Decline a nominal stem (Subanta)")
    parser.add_argument("--taddhita", type=str, help="Generate a Secondary Derivative (Taddhita)")
    parser.add_argument("--analyze", type=str, help="Analyze a form (Reverse Lookup MVP)")
    parser.add_argument("--gender", choices=['m', 'f', 'n', 'p'], default='m', help="Gender for declension (m/f/n)")

    args = parser.parse_args()

    raw_dhatu = args.dhatu
    upasargas = None
    if '-' in raw_dhatu:
        parts = raw_dhatu.split('-')
        raw_dhatu = parts[-1]  # The last element is the dhatu
        upasargas =[]
        for p in parts[:-1]:   # Everything before is an upasarga
            if p in UPASARGAS:
                upasargas.append(p)
            else:
                print(f"⚠️ Warning: '{p}' is not a recognized Pāṇinian Upasarga. Attempting to process anyway.")
                upasargas.append(p)

    if (getattr(args, 'decline', False) or getattr(args, 'taddhita', False) or getattr(args, 'analyze', False)) and not getattr(args, 'krt', False):
        gana = None
    else:
        gana = resolve_gana(raw_dhatu, args.gana)
    
    custom_root = None
    prakriya = None

    # 1. Secondary Root Generation
    if args.desiderative:
        sanadi_prakriya = derive_secondary_root(raw_dhatu, 'san', gana=gana)
        if sanadi_prakriya:
            custom_root = sanadi_prakriya.terms[0]
            print(f"\n✨ Forged Secondary Root (San): {custom_root.text}\n")
            if args.history:
                print("[San Derivation History]")
                sanadi_prakriya.print_history()
                print("-" * 40)
        else:
            print("❌ Failed to generate desiderative root.")
            sys.exit(1)
            
    elif args.causative:
        causative_prakriya = derive_secondary_root(raw_dhatu, 'Ric', gana=gana)
        if causative_prakriya:
            custom_root = causative_prakriya.terms[0]
            print(f"\n✨ Forged Secondary Root (Ṇic): {custom_root.text}\n")
            if args.history:
                print("[Ṇic Derivation History]")
                causative_prakriya.print_history()
                print("-" * 40)
        else:
            print("❌ Failed to generate causative root.")
            sys.exit(1)

    # 2. Main Output Routing
    if args.all_krt:
        pratyayas =[
            "kta", "ktavatu", "ktvA", "tumun", "tavya", "anIyar", 
            "yat", "Ryat", "Satf", "lyuW", "Rvul", "tfc", "GaY"
        ]
        
        print(f"\n✨ All Common Kṛdanta Forms for: {raw_dhatu} (Gaṇa {gana})\n")
        print(f"{'Affix (Upadeśa)':<20} | {'Derived Form'}")
        print("-" * 40)
        
        for p in pratyayas:
            p_prakriya = derive_krdanta(raw_dhatu, p, gana=gana, upasargas=upasargas)
            if p_prakriya:
                print(f"{p:<20} | {p_prakriya.get_current_string()}")
            else:
                print(f"{p:<20} | Failed")
        print()
        
    if args.analyze:
        from .analyzer import analyze_word
        res = analyze_word(args.analyze)
        print(f"\n🔬 Analysis for '{args.analyze}':")
        for r in res['analysis']:
            print(f"  - {r}")
        sys.exit(0)
        
    elif args.taddhita:
        from .taddhita import derive_taddhita
        prakriya = derive_taddhita(raw_dhatu, args.taddhita)
        if prakriya:
            print(f"\n✨ Taddhita Result: {prakriya.get_current_string()}\n")
            if args.history:
                prakriya.print_history()
                
    elif args.krt:
        prakriya = derive_krdanta(raw_dhatu, args.krt, gana=gana, upasargas=upasargas) 
        if prakriya:
            krt_stem = prakriya.get_current_string()
            print(f"\n✨ Kṛdanta Result: {krt_stem}\n")
            if args.decline:
                from .decline import print_declension
                print_declension(krt_stem, args.gender)
            
    elif args.table:
        print_conjugation(raw_dhatu, lakara_name=args.lakara, gana=gana, upasargas=upasargas, custom_dhatu=custom_root, voice=args.voice) 
        
    elif args.decline and not args.krt:
        from .decline import print_declension
        print_declension(raw_dhatu, args.gender)
        
    else:
        prakriya = derive(raw_dhatu, lakara_name=args.lakara, purusha=args.purusha, vacana=args.vacana, gana=gana, upasargas=upasargas, custom_dhatu=custom_root, voice=args.voice)
        if prakriya:
            print(f"\n✨ Tiṅanta Result: {prakriya.get_current_string()}\n")
            
    # 3. Print History
    if prakriya and args.history:
        prakriya.print_history()

if __name__ == "__main__":
    main()