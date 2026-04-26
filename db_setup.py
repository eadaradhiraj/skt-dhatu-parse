"""
db_setup.py
Converts dhatupatha.tsv into an indexed SQLite database.
"""
import sqlite3
import csv
import os

def setup_database():
    db_path = 'data/dhatupatha.db'
    tsv_path = 'data/dhatupatha.tsv'
    
    # Remove old DB if it exists so we start fresh
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create the table
    c.execute('''
        CREATE TABLE dhatu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dhatu_slp1 TEXT NOT NULL,
            gana INTEGER NOT NULL,
            pada TEXT NOT NULL,
            meaning_en TEXT,
            number TEXT,
            dhatu_with_anubandha TEXT NOT NULL
        )
    ''')

    # Create an index on the SLP1 root for blazing fast lookups
    c.execute('CREATE INDEX idx_dhatu_slp1 ON dhatu(dhatu_slp1)')

    # Load TSV and insert data
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        records =[]
        for row in reader:
            records.append((
                row['dhatu_slp1'],
                int(row['gana']),
                row['pada'],
                row['meaning_en'],
                row['number'],
                row['dhatu_with_anubandha']
            ))

    c.executemany('''
        INSERT INTO dhatu (dhatu_slp1, gana, pada, meaning_en, number, dhatu_with_anubandha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', records)

    conn.commit()
    conn.close()
    print("Successfully created dhatupatha.db with indexes!")

if __name__ == '__main__':
    setup_database()