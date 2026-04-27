import unittest
import sqlite3
import os
from skt_dhatu_parse.engine import derive
from skt_dhatu_parse.sanadi import derive_secondary_root

class TestRecursion(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = 'test_recursion.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # Insert BU
        mock_data =[
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU')
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_causative_conjugation(self) -> None:
        """
        Tests the ultimate Pāṇinian recursion:
        1. Generates Causative root (BU + Ric -> BAvi)
        2. Feeds 'BAvi' back into the Tiṅanta engine for laW.
        3. BAvi + Sap + tip -> BAve + a + ti -> BAvayati!
        """
        # Step 1: Generate the secondary root
        sanadi_prakriya = derive_secondary_root('BU', 'Ric', gana=1, db_path=self.test_db_path)
        new_root_term = sanadi_prakriya.terms[0]
        
        # Step 2: Feed it into the verbal engine
        final_prakriya = derive(custom_dhatu=new_root_term, lakara_name='laW', db_path=self.test_db_path)
        
        self.assertIsNotNone(final_prakriya)
        self.assertEqual(final_prakriya.get_current_string(), 'BAvayati')

if __name__ == '__main__':
    unittest.main()