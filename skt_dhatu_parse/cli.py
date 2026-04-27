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

def resolve_gana(dhatu_slp1: str, user_gana: int = None) -> int:
    """Fetches the root and safely resolves homonyms (multiple ganas)."""
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
    
    # Core Positional Argument
    parser.add_argument("dhatu", help="The SLP1 root to conjugate (e.g., BU, aMh, div, tud)")
    parser.add_argument("-g", "--gana", type=int, help="Specify the Gaṇa (1-10) for homonyms")
    
    # Verb (Tiṅanta) Arguments
    parser.add_argument("-l", "--lakara", default="laW", help="Lakāra (Tense/Mood). Default: laW (Present)")
    parser.add_argument("-p", "--purusha", default="prathama", choices=["prathama", "madhyama", "uttama"], help="Person")
    parser.add_argument("-v", "--vacana", type=int, default=0, choices=[0, 1, 2], help="Number (0=Sing, 1=Dual, 2=Plur)")
    parser.add_argument("-t", "--table", action="store_true", help="Print the full 3x3 conjugation table")
    
    # NEW: Participle & Secondary Root Arguments
    parser.add_argument("--krt", type=str, help="Generate a Primary Derivative (Kṛdanta) with given suffix (e.g., kta, GaY, lyuW)")
    parser.add_argument("--causative", action="store_true", help="Generate the Causative (Ṇic) secondary root")
    
    parser.add_argument("--history", action="store_true", help="Show the step-by-step Pāṇinian derivation history")

    args = parser.parse_args()
    gana = resolve_gana(args.dhatu, args.gana)

    prakriya = None

    # Route the computation to the correct pipeline
    if args.krt:
        prakriya = derive_krdanta(args.dhatu, args.krt, gana=gana)
        if prakriya:
            print(f"\n✨ Kṛdanta Result: {prakriya.get_current_string()}\n")
            
    elif args.causative:
        prakriya = derive_secondary_root(args.dhatu, 'Ric', gana=gana)
        if prakriya:
            print(f"\n✨ Causative Root (Ṇic): {prakriya.get_current_string()}\n")
            
    elif args.table:
        print_conjugation(args.dhatu, lakara_name=args.lakara, gana=gana)
        
    else:
        prakriya = derive(args.dhatu, lakara_name=args.lakara, purusha=args.purusha, vacana=args.vacana, gana=gana)
        if prakriya:
            print(f"\n✨ Tiṅanta Result: {prakriya.get_current_string()}\n")
            
    # Print the math if requested
    if prakriya and args.history:
        prakriya.print_history()

if __name__ == "__main__":
    main()