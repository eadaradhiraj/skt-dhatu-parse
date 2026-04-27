import unittest
import sqlite3
import os
from skt_dhatu_parse.sanadi import derive_secondary_root

class TestSanadi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = 'test_sanadi.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # We test BU (Terminal vowel) and ram (Penultimate 'a')
        mock_data =[
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
            ('ram', 1, 'atmanepada', 'krIDAyAm', '0989', 'ramu~')
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_causative_bhu(self) -> None:
        """
        Tests Causative: BU + Ric -> BAvi.
        1. 'Ric' loses 'R' and 'c' -> 'i' (tagged 'Rit')
        2. Terminal 'U' gets Vrddhi because of 'Rit' -> 'O'
        3. Sandhi: 'O' + 'i' -> 'Avi'
        """
        prakriya = derive_secondary_root('BU', 'Ric', gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'BAvi')
        self.assertEqual(prakriya.terms[0].term_type, 'dhatu')

    def test_causative_ram(self) -> None:
        """
        Tests Causative: ram + Ric -> rAmi.
        1. 'Ric' loses 'R' and 'c' -> 'i' (tagged 'Rit')
        2. Penultimate 'a' gets Vrddhi because of 'Rit' -> 'A'
        """
        prakriya = derive_secondary_root('ram', 'Ric', gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'rAmi')

if __name__ == '__main__':
    unittest.main()