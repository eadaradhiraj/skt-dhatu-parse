"""
dhatu_loader.py
Queries the SQLite database and retrieves roots as Term objects.
"""
import os
import sqlite3
from .models import Term

# 1. Get the absolute path of the directory containing THIS file (dhatu_loader.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default to production DB
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'data', 'dhatupatha.db')

def get_dhatu(dhatu_slp1: str, gana: int = None, db_path: str = DEFAULT_DB_PATH) -> list[Term]:
    """
    Looks up a dhatu by its SLP1 string using SQLite.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name
    c = conn.cursor()

    query = "SELECT * FROM dhatu WHERE dhatu_slp1 = ?"
    params = [dhatu_slp1]

    if gana is not None:
        query += " AND gana = ?"
        params.append(gana)

    c.execute(query, params)
    rows = c.fetchall()
    
    results =[]
    for row in rows:
        t = Term(upadeza=row['dhatu_with_anubandha'], term_type='dhatu')
        t.tags.add(f"gana_{row['gana']}")
        t.tags.add(row['pada'])
        t.tags.add(f"clean_{row['dhatu_slp1']}")
        results.append(t)
        
    conn.close()
    return results