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

# Pāṇini Rule 1.4.58: prādayaḥ (The 22 Upasargas)
UPASARGAS =[
    'pra', 'parA', 'apa', 'sam', 'anu', 'ava', 'nis', 'nir', 
    'dus', 'dur', 'vi', 'A', 'ni', 'aDi', 'api', 'ati', 
    'su', 'ud', 'aBi', 'prati', 'pari', 'upa'
]

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
    parser.add_argument("dhatu", help="The SLP1 root to conjugate (e.g., BU, aMh, div, tud)")
    parser.add_argument("-g", "--gana", type=int, help="Specify the Gaṇa (1-10) for homonyms")
    parser.add_argument("-l", "--lakara", default="laW", help="Lakāra (Tense/Mood). Default: laW (Present)")
    parser.add_argument("-p", "--purusha", default="prathama", choices=["prathama", "madhyama", "uttama"], help="Person")
    parser.add_argument("-v", "--vacana", type=int, default=0, choices=[0, 1, 2], help="Number (0=Sing, 1=Dual, 2=Plur)")
    parser.add_argument("-t", "--table", action="store_true", help="Print the full 3x3 conjugation table")
    parser.add_argument("--krt", type=str, help="Generate a Primary Derivative (Kṛdanta) with given suffix (e.g., kta, GaY, lyuW)")
    parser.add_argument("--causative", action="store_true", help="Generate the Causative (Ṇic) secondary root")
    parser.add_argument("--history", action="store_true", help="Show the step-by-step Pāṇinian derivation history")
    parser.add_argument("--voice", choices=["parasmaipada", "atmanepada"], help="Force a specific voice (useful for Ubhayapada roots)")
    
    args = parser.parse_args()

    # Hyphen parsing logic for Upasargas
    raw_dhatu = args.dhatu
    upasarga = None
    if '-' in raw_dhatu:
        parts = raw_dhatu.split('-', 1)
        if parts[0] in UPASARGAS:
            upasarga = parts[0]
            raw_dhatu = parts[1]
        else:
            print(f"⚠️ Warning: '{parts[0]}' is not a recognized Pāṇinian Upasarga.")
            upasarga = parts[0]
            raw_dhatu = parts[1]

    gana = resolve_gana(raw_dhatu, args.gana)
    
    custom_root = None
    prakriya = None

    # 1. Check if we need to generate a Causative root first
    if args.causative:
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

    # 2. Route to the correct output pipeline
    if args.krt:
        prakriya = derive_krdanta(raw_dhatu, args.krt, gana=gana) 
        if prakriya:
            print(f"\n✨ Kṛdanta Result: {prakriya.get_current_string()}\n")

    elif args.table:
        # Pass custom_root (which will be None unless --causative was used)
        print_conjugation(raw_dhatu, lakara_name=args.lakara, gana=gana, upasarga=upasarga, custom_dhatu=custom_root, voice=args.voice) 

    else:
        # Single derivation (Pass custom_root if available)
        prakriya = derive(raw_dhatu, lakara_name=args.lakara, purusha=args.purusha, vacana=args.vacana, gana=gana, upasarga=upasarga, custom_dhatu=custom_root, voice=args.voice)
            
    # Print Tiṅanta History if requested
    if prakriya and args.history:
        prakriya.print_history()

if __name__ == "__main__":
    main()