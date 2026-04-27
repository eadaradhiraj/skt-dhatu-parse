import unittest
import sqlite3
import os
from engine import derive

class TestPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Setup a temporary test database
        cls.test_db_path = 'test_pipeline.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        # Insert test data:
        # akz (Gana 1, Parasmaipada)
        # aMh (Gana 1, Atmanepada) - Original upadesha is ahi!
        mock_data =[
            ('akz', 1, 'parasmaipada', 'vyAptau', '0742', 'akzU!'),
            ('aMh', 1, 'atmanepada', 'gatau', '0722', 'ahi!'),
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU') # <-- ADD THIS LINE
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_derive_akzati(self):
        """
        Full pipeline test: akzU! + laW -> akz + a + ti = akzati
        """
        prakriya = derive('akz', 'laW', db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'akzati')
        
        # Verify the internal states
        dhatu = prakriya.terms[0]
        self.assertEqual(dhatu.text, 'akz')
        self.assertIn('Udit', dhatu.tags) # Ensures 1.3.2 fired
        
        suffix = prakriya.terms[2]
        self.assertEqual(suffix.text, 'ti')
        self.assertIn('pit', suffix.tags) # Ensures 1.3.3 fired

    def test_derive_aMhate(self):
        """
        Full pipeline test: ahi! + laW -> aMh + a + te = aMhate.
        This tests:
        1. It-lopa (ahi! -> ah + 'idit')
        2. Idito Num DhAtoH (ah -> aMh)
        3. Lakara substitution & Inheritance (laW -> ta + 'Wit')
        4. Atmanepada Tere (ta -> te)
        """
        prakriya = derive('aMh', 'laW', db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'aMhate')
        
        # Verify that the Dhatu got its 'm' augment and 'idit' tag
        dhatu = prakriya.terms[0]
        self.assertEqual(dhatu.text, 'aMh')
        self.assertIn('idit', dhatu.tags) 
        
        # Verify that the suffix became 'te' and inherited 'Wit'
        suffix = prakriya.terms[2]
        self.assertEqual(suffix.text, 'te')
        self.assertIn('Wit', suffix.tags)

    def test_bhavami(self):
        # Pass the uttama purusha to get 'mi'!
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_past_tense_dual(self):
        """
        Rule 3.4.101 (tasthasthamipAM tAMtaMtAmaH): 
        'Tas' should become 'tam' in a Nit lakara (laN).
        BU + laN (Madhyama, Dual) -> aBavatam (Not aBavaTaH)
        """
        prakriya = derive('BU', 'laN', purusha='madhyama', vacana=1, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavatam')

    def test_past_tense_plural_consonant_drop(self):
        """
        Rule 8.2.23 (saMyogAntasya lopaH):
        Terminal consonant clusters drop the last consonant.
        BU + laN (Prathama, Plural) -> aBav + a + ant -> aBavant -> aBavan
        """
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=2, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavan')

    def test_atmanepada_uttama_singular(self):
        """
        Tests that 'a' + 'e' merges properly for the 1st person singular.
        aMh + laW (Uttama, Singular) -> aMhe (Not aMhae)
        """
        prakriya = derive('aMh', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aMhe')

if __name__ == '__main__':
    unittest.main()