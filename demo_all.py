import sqlite3
import os
from engine import derive

# 1. Setup Mock Database with all Gaṇas
db_path = 'demo.db'
if os.path.exists(db_path): os.remove(db_path)
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('CREATE TABLE dhatu (dhatu_slp1 TEXT, gana INTEGER, pada TEXT, meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT)')

# We insert bhU (Gana 1), div (Gana 4), and tud (Gana 6)
mock_data =[
    ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
    ('div', 4, 'parasmaipada', 'krIqAyAm', '0001', 'divu~'),
    ('tud', 6, 'parasmaipada', 'vyathane', '0001', 'tuda~')
]
c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
conn.commit()

# 2. Run the Derivations!
print("\n🔥 PANINIAN ENGINE MASTER DEMO 🔥\n")

# A. Gaṇa 1: The Standard Present
p1 = derive('BU', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"1. Present Tense (laW): {p1.get_current_string()}") # Expected: Bavati

# B. The Past Tense
p2 = derive('BU', 'laN', purusha='prathama', vacana=0, db_path=db_path)
print(f"2. Past Tense (laN):    {p2.get_current_string()}") # Expected: aBavat

# C. The Future Tense
p3 = derive('BU', 'lfW', purusha='prathama', vacana=0, db_path=db_path)
print(f"3. Future Tense (lfW):  {p3.get_current_string()}") # Expected: Bavizyati

# D. Gaṇa 4 (divādi)
p4 = derive('div', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"4. Gaṇa 4 (div + ya):   {p4.get_current_string()}") # Expected: dIvyati

# E. Gaṇa 6 (tudādi) - Proving Guṇa Prevention!
p5 = derive('tud', 'laW', purusha='prathama', vacana=0, db_path=db_path)
print(f"5. Gaṇa 6 (tud + a):    {p5.get_current_string()}") # Expected: tudati

conn.close()