import sqlite3
import os
from engine import derive

# 1. Setup Mock Database
db_path = 'demo.db'
if os.path.exists(db_path): os.remove(db_path)
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('CREATE TABLE dhatu (dhatu_slp1 TEXT, gana INTEGER, pada TEXT, meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT)')

mock_data =[
    ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
    ('div', 4, 'parasmaipada', 'krIqAyAm', '0001', 'divu~'),
    ('tud', 6, 'parasmaipada', 'vyathane', '0001', 'tuda~'),
    ('ji', 1, 'parasmaipada', 'jaye', '0593', 'ji') # <--- ADDED JI
]
c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
conn.commit()

# 2. Run the Derivations!
print("\n🔥 PANINIAN ENGINE MASTER DEMO 🔥\n")

p1 = derive('BU', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"1. Present Tense (BU -> Bavati): {p1.get_current_string()}") 

p2 = derive('BU', 'laN', purusha='prathama', vacana=0, db_path=db_path)
print(f"2. Past Tense (BU -> aBavat):    {p2.get_current_string()}") 

p3 = derive('BU', 'lfW', purusha='prathama', vacana=0, db_path=db_path)
print(f"3. Future SeW (BU -> Bavizyati): {p3.get_current_string()}") 

p4 = derive('div', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"4. Gaṇa 4 (div -> dIvyati):      {p4.get_current_string()}") 

p5 = derive('tud', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"5. Gaṇa 6 (tud -> tudati):       {p5.get_current_string()}") 

# --- NEW TEST ---
p6 = derive('ji', 'lfW', purusha='prathama', vacana=0, db_path=db_path)
print(f"6. Future AniW (ji -> jezyati):  {p6.get_current_string()}") 

conn.close()