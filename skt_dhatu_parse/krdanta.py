"""
krdanta.py
Pipeline for Primary Derivatives (Participles/Krdantas).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from .rules import (
    idito_num_dhatoh,
    jhasas_tathor_dho_dhah,
    jhalam_jas_jhasi
)


def derive_krdanta(
    dhatu_slp1: str,
    pratyaya_upadeza: str,
    gana: int = None,
    db_path: str = DEFAULT_DB_PATH
) -> list[Term]:
    prakriya = Prakriya()

    # 1. Fetch Dhatu
    dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
    if not dhatus:
        return None
    dhatu = dhatus[0]
    prakriya.add_term(dhatu)

    # 2. Resolve Dhatu Meta-Markers
    resolve_it_markers(dhatu)
    idito_num_dhatoh(prakriya)

    # 3. Add Krt Pratyaya (e.g., 'kta')
    pratyaya = Term(pratyaya_upadeza, 'pratyaya')
    prakriya.add_term(pratyaya)

    # 4. Resolve Pratyaya Markers (e.g., 'kta' loses 'k' -> 'ta', tagged 'kit')
    resolve_it_markers(pratyaya)

    # 5. Apply Consonant Sandhi
    jhasas_tathor_dho_dhah(prakriya)  # t -> dh
    jhalam_jas_jhasi(prakriya)        # dh -> d

    return prakriya
