import unittest
import sqlite3
import os
from skt_dhatu_parse.krdanta import derive_krdanta

class TestKrdanta(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = 'test_krdanta.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # Insert buD and ram
        mock_data =[
            ('buD', 1, 'parasmaipada', 'avagamane', '0994', 'buDa~'),
            ('ram', 1, 'atmanepada', 'krIDAyAm', '0989', 'ramu~')  # <--- NEW
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_buddha_derivation(self):
        """
        Tests buD + kta -> budDa (buddha).
        Verifies:
        1. 'kta' loses 'k' (Rule 1.3.8)
        2. 't' becomes 'D' (Rule 8.2.40)
        3. 'D' becomes 'd' (Rule 8.4.53)
        """
        prakriya = derive_krdanta('buD', 'kta', gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'budDa')
        
        # Verify internal states
        dhatu = prakriya.terms[0]
        suffix = prakriya.terms[1]
        
        self.assertEqual(dhatu.text, 'bud')
        self.assertEqual(suffix.text, 'Da')
        self.assertIn('kit', suffix.tags)

    def test_rama_ghany(self) -> None:
        """
        Tests ram + GaY -> rAma.
        Verifies:
        1. 'GaY' loses 'G' (Rule 1.3.8) and 'Y' (Rule 1.3.3) -> 'a', tagged 'Yit'
        2. Penultimate 'a' gets Vrddhi because of 'Yit' (Rule 7.2.116) -> rAm + a
        """
        # Fixed: 'GaY' is the strict SLP1 encoding for 'ghañ'
        prakriya = derive_krdanta('ram', 'GaY', gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'rAma')
        self.assertIn('Yit', prakriya.terms[1].tags)

    def test_ramana_lyut(self):
        """
        Tests ram + lyuW -> ramaRa.
        Verifies:
        1. 'lyuW' loses 'l' and 'W' -> 'yu'
        2. 'yu' becomes 'ana' (Rule 7.1.1)
        3. 'n' becomes 'R' due to Natva Sandhi (Rule 8.4.1)
        """
        prakriya = derive_krdanta('ram', 'lyuW', gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'ramaRa')

if __name__ == '__main__':
    unittest.main()