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
        
        # Insert our test root: buD (to know/awaken)
        mock_data =[
            ('buD', 1, 'parasmaipada', 'avagamane', '0994', 'buDa~')
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

if __name__ == '__main__':
    unittest.main()