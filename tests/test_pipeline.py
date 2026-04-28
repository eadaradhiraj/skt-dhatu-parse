import unittest
import sqlite3
import os
from skt_dhatu_parse.engine import derive

class TestPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = 'test_pipeline.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # Added krI and sTA to the mock database!
        mock_data =[
            ('akz', 1, 'parasmaipada', 'vyAptau', '0742', 'akzU!'),
            ('aMh', 1, 'atmanepada', 'gatau', '0722', 'ahi!'),
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
            ('div', 4, 'parasmaipada', 'krIqAyAm', '0001', 'divu~'),
            ('tud', 6, 'parasmaipada', 'vyathane', '0001', 'tuda~'),
            ('ji', 1, 'parasmaipada', 'jaye', '0593', 'ji'),
            ('krI', 9, 'ubhayapada', 'dravyavinimaye', '0001', 'qukrIY'),
            ('sTA', 1, 'parasmaipada', 'gatinivRttau', '1077', 'zWA')
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    # ==========================================
    # EXISTING TESTS
    # ==========================================
    def test_derive_akzati(self) -> None:
        prakriya = derive('akz', 'laW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'akzati')

    def test_derive_aMhate(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aMhate')

    def test_bhavami(self) -> None:
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_atmanepada_uttama_singular(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='uttama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aMhe')

    def test_past_tense_dual(self) -> None:
        prakriya = derive('BU', 'laN', purusha='madhyama', vacana=1, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavatam')

    def test_past_tense_plural_consonant_drop(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=2, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'aBavan')

    def test_future_tense_set(self) -> None:
        prakriya = derive('BU', 'lfW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'Bavizyati')

    def test_future_tense_anit(self) -> None:
        prakriya = derive('ji', 'lfW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'jezyati')

    def test_gana_4_divyadi(self) -> None:
        prakriya = derive('div', 'laW', purusha='prathama', vacana=0, gana=4, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'dIvyati')

    def test_gana_6_tudadi(self) -> None:
        prakriya = derive('tud', 'laW', purusha='prathama', vacana=0, gana=6, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'tudati')

    def test_perfect_tense_singular(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'baBUva')

    def test_perfect_tense_dual(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=1, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'baBUvatuH')

    def test_perfect_tense_plural(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=2, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'baBUvuH')

    def test_invalid_roots_return_none(self) -> None:
        from skt_dhatu_parse.krdanta import derive_krdanta
        from skt_dhatu_parse.sanadi import derive_secondary_root
        self.assertIsNone(derive('xyz', db_path=self.test_db_path))
        self.assertIsNone(derive_krdanta('xyz', 'kta', db_path=self.test_db_path))
        self.assertIsNone(derive_secondary_root('xyz', 'Ric', db_path=self.test_db_path))

    # ==========================================
    # NEW TESTS FOR 100% COVERAGE
    # ==========================================
    def test_gana_9_vikri_singular(self) -> None:
        """Test Gana 9 (SnA -> nI), Natva Sandhi, and Upasarga Atmanepada override: vi-krI + laW -> vikrIRIte"""
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['vi'], db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vikrIRIte')

    def test_gana_9_vikri_plural(self) -> None:
        """Test Gana 9 plural (Jh -> at) and dropping of 'A' before vowel: vi-krI + laW (plural) -> vikrIRate"""
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=2, gana=9, upasargas='vi', db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vikrIRate')

    def test_dhatvadeh_and_paghra(self) -> None:
        """Test zWA -> sTA (dhatvadeh) and sTA -> tizWa (paghra): sTA + laW -> tizWati"""
        prakriya = derive('sTA', 'laW', purusha='prathama', vacana=0, gana=1, db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'tizWati')

    def test_causative_puk_and_upasarga_satva(self) -> None:
        """Test sTA + puk + Ric -> sTApi, and prati + sTApi -> pratizWApayizyati"""
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi_prakriya = derive_secondary_root('sTA', 'Ric', gana=1, db_path=self.test_db_path)
        final_prakriya = derive('sTA', 'lfW', purusha='prathama', vacana=0, gana=1, upasargas='prati', custom_dhatu=sanadi_prakriya.terms[0], db_path=self.test_db_path)
        self.assertEqual(final_prakriya.get_current_string(), 'pratizWApayizyati')

    def test_multiple_upasargas(self) -> None:
        """Test vi + A + BU + laN -> vyABavat"""
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=0, gana=1, upasargas=['vi', 'A'], db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vyABavat')

    def test_gana_9_vikri_singular(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['vi'], db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vikrIRIte')

    def test_gana_9_vikri_plural(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=2, gana=9, upasargas=['vi'], db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vikrIRate')

    def test_causative_puk_and_upasarga_satva(self) -> None:
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi_prakriya = derive_secondary_root('sTA', 'Ric', gana=1, db_path=self.test_db_path)
        final_prakriya = derive('sTA', 'lfW', purusha='prathama', vacana=0, gana=1, upasargas=['prati'], custom_dhatu=sanadi_prakriya.terms[0], db_path=self.test_db_path)
        self.assertEqual(final_prakriya.get_current_string(), 'pratizWApayizyati')

    def test_multiple_upasargas(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=0, gana=1, upasargas=['vi', 'A'], db_path=self.test_db_path)
        self.assertEqual(prakriya.get_current_string(), 'vyABavat')


if __name__ == '__main__':
    unittest.main()