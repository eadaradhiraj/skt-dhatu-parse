import unittest
import sqlite3
import os
from skt_dhatu_parse.engine import derive

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
        
        # Insert ALL test data here!
        mock_data =[
            ('akz', 1, 'parasmaipada', 'vyAptau', '0742', 'akzU!'),
            ('aMh', 1, 'atmanepada', 'gatau', '0722', 'ahi!'),
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
            ('div', 4, 'parasmaipada', 'krIqAyAm', '0001', 'divu~'),
            ('tud', 6, 'parasmaipada', 'vyathane', '0001', 'tuda~'),
            ('ji', 1, 'parasmaipada', 'jaye', '0593', 'ji')
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up database after tests
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    # ==========================================
    # REGULAR PRESENT TENSE (laW) TESTS
    # ==========================================

    def test_derive_akzati(self):
        """Full pipeline test: akzU! + laW -> akz + a + ti = akzati"""
        prakriya = derive('akz', 'laW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'akzati')
        
        # Verify the internal states
        dhatu = prakriya.terms[0]
        self.assertEqual(dhatu.text, 'akz')
        self.assertIn('Udit', dhatu.tags) # Ensures 1.3.2 fired
        
        suffix = prakriya.terms[-1]
        self.assertEqual(suffix.text, 'ti')
        self.assertIn('pit', suffix.tags) # Ensures 1.3.3 fired

    def test_derive_aMhate(self):
        """
        Full pipeline test: ahi! + laW -> aMh + a + te = aMhate.
        Tests It-lopa, Idito Num DhAtoH, SthAnivadbhAva, and Atmanepada Tere.
        """
        prakriya = derive('aMh', 'laW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'aMhate')
        
        # Verify that the Dhatu got its 'm' augment and 'idit' tag
        dhatu = prakriya.terms[0]
        self.assertEqual(dhatu.text, 'aMh')
        self.assertIn('idit', dhatu.tags) 
        
        # Verify that the suffix became 'te' and inherited 'Wit'
        suffix = prakriya.terms[-1]
        self.assertEqual(suffix.text, 'te')
        self.assertIn('Wit', suffix.tags) 

    def test_bhavami(self):
        """Tests lengthening of 'a' before 'm' (yaY) for 1st person singular."""
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_atmanepada_uttama_singular(self):
        """Tests that 'a' + 'e' merges properly for the 1st person singular (aMhe)."""
        prakriya = derive('aMh', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aMhe')

    # ==========================================
    # PAST TENSE (laN) TESTS
    # ==========================================

    def test_past_tense_dual(self):
        """
        Rule 3.4.101: 'Tas' should become 'tam' in a Nit lakara (laN).
        BU + laN (Madhyama, Dual) -> aBavatam
        """
        prakriya = derive('BU', 'laN', purusha='madhyama', vacana=1, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavatam')

    def test_past_tense_plural_consonant_drop(self):
        """
        Rule 8.2.23: Terminal consonant clusters drop the last consonant.
        BU + laN (Prathama, Plural) -> aBav + a + ant -> aBavant -> aBavan
        """
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=2, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavan')

    # ==========================================
    # FUTURE TENSE (lfW) & SET/ANIT TESTS
    # ==========================================

    def test_future_tense_set(self):
        """Test SeW (iW augment) Future Tense: BU + lfW -> Bavizyati"""
        prakriya = derive('BU', 'lfW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'Bavizyati')

    def test_future_tense_anit(self):
        """Test AniW (No iW) Future Tense: ji + lfW -> jezyati"""
        prakriya = derive('ji', 'lfW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'jezyati')

    # ==========================================
    # OTHER GANAS (CLASSES) TESTS
    # ==========================================

    def test_gana_4_divyadi(self):
        """Test Gana 4 (Syan vikarana and lengthening): div + laW -> dIvyati"""
        prakriya = derive('div', 'laW', purusha='prathama', vacana=0, gana=4, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'dIvyati')

    def test_gana_6_tudadi(self):
        """Test Gana 6 (Sa vikarana blocking Guna): tud + laW -> tudati"""
        prakriya = derive('tud', 'laW', purusha='prathama', vacana=0, gana=6, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'tudati')

if __name__ == '__main__':
    unittest.main()