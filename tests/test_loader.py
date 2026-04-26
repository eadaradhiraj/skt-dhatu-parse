import unittest
import sqlite3
from dhatu_loader import get_dhatu

class TestDhatuLoader(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database specifically for testing
        cls.test_db_path = ':memory:'
        cls.conn = sqlite3.connect(cls.test_db_path)
        c = cls.conn.cursor()
        
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # Insert our mock SLP1 data
        mock_data =[
            ('aMh', 10, 'ubhayapada', 'bhASArthaH ca', '0328', 'ahi!'),
            ('aMh', 1, 'atmanepada', 'gatau', '0722', 'ahi!'),
            ('akz', 1, 'parasmaipada', 'vyAptau', '0742', 'akzU!')
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        cls.conn.commit()

        # IMPORTANT: We have to override the loader's connection 
        # so it uses our in-memory DB. We'll pass test_db_path as an argument.

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_fetch_single_dhatu(self):
        """Test fetching a root (akz) that only exists in one Gaṇa"""
        # Note: We pass the test DB path to the function
        # Because in-memory DBs are isolated to the connection, 
        # we must physically share the connection or URI. 
        # For simplicity in this test structure, let's write the mock to a tmp file.
        pass