import unittest
import sqlite3
import os
from skt_dhatu_parse.krdanta import derive_krdanta

class TestKrdanta(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = 'test_krdanta.db'
        conn = sqlite3.connect(cls.test_db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE dhatu (
            dhatu_slp1 TEXT, gana INTEGER, pada TEXT, 
            meaning_en TEXT, number TEXT, dhatu_with_anubandha TEXT
        )''')
        
        # Insert ALL required roots
        mock_data =[
            ('buD', 1, 'parasmaipada', 'avagamane', '0994', 'buDa~'),
            ('ram', 1, 'atmanepada', 'krIDAyAm', '0989', 'ramu~'),
            ('gam', 1, 'parasmaipada', 'gatau', '1037', 'gamx~'),
            ('vac', 2, 'parasmaipada', 'paribhASaNe', '0058', 'vaca~'),
            ('Cid', 7, 'ubhayapada', 'dvaidhIkaraNe', '0003', 'Cidi!r'),
            ('paW', 1, 'parasmaipada', 'vyaktAyAM vAci', '0381', 'paWa~'),
            ('duh', 2, 'ubhayapada', 'prapUraNe', '0004', 'duha~'),
            ('duh', 1, 'parasmaipada', 'ardane', '0839', 'duhi!r'),
            ('svap', 2, 'parasmaipada', 'zaye', '0063', 'Yizvapa!'),
            ('sfj', 6, 'parasmaipada', 'visarge', '0150', 'sfja!'),
            ('BU', 1, 'parasmaipada', 'sattAyAm', '0001', 'BU'),
            ('muc', 6, 'ubhayapada', 'mokSaNe', '0166', 'mucx!')  # Added for muYcati test
        ]
        c.executemany("INSERT INTO dhatu VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_buddha_derivation(self) -> None:
        """Tests buD + kta -> budDa (buddha)."""
        prakriya = derive_krdanta('buD', 'kta', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'budDa')

    def test_rama_ghany(self) -> None:
        """Tests ram + GaY -> rAma."""
        prakriya = derive_krdanta('ram', 'GaY', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'rAma')

    def test_ramana_lyut(self) -> None:
        """Tests ram + lyuW -> ramaRa."""
        prakriya = derive_krdanta('ram', 'lyuW', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'ramaRa')

    def test_ram_ktva_nasal_drop(self) -> None:
        """Tests ram + ktvA -> ratvA."""
        prakriya = derive_krdanta('ram', 'ktvA', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'ratvA')

    def test_gam_kta_nasal_drop(self) -> None:
        """Tests gam + kta -> gata."""
        prakriya = derive_krdanta('gam', 'kta', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'gata')

    def test_vac_kta_samprasarana(self) -> None:
        """Tests vac + kta -> ukta."""
        prakriya = derive_krdanta('vac', 'kta', gana=2, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'ukta')

    def test_chid_kta_nishtha(self) -> None:
        """Tests Cid + kta -> Cinna."""
        prakriya = derive_krdanta('Cid', 'kta', gana=7, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'Cinna')

    def test_path_kta_set(self) -> None:
        """Tests paW + kta -> paWita."""
        prakriya = derive_krdanta('paW', 'kta', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'paWita')

    def test_duh_kta_gana_2_anit(self) -> None:
        """Tests duh (Gana 2) + kta -> dugDa."""
        prakriya = derive_krdanta('duh', 'kta', gana=2, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'dugDa')

    def test_duh_kta_gana_1_set(self) -> None:
        """Tests duh (Gana 1) + kta -> duhita."""
        prakriya = derive_krdanta('duh', 'kta', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'duhita')

    def test_bhu_tavya_guna_sandhi(self) -> None:
        """Tests BU + tavya -> Bavitavya."""
        prakriya = derive_krdanta('BU', 'tavya', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'Bavitavya')

    def test_svap_kta_samprasarana(self) -> None:
        """Tests svap + kta -> supta."""
        prakriya = derive_krdanta('svap', 'kta', gana=2, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'supta')

    def test_srj_kta_retroflexion(self) -> None:
        """Tests sfj + kta -> sfzwa."""
        prakriya = derive_krdanta('sfj', 'kta', gana=6, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'sfzwa')

    def test_muc_sa_num_parasavarna(self) -> None:
        """Tests muc + Sa + ti -> muYcati."""
        from skt_dhatu_parse.engine import derive
        prakriya = derive('muc', 'laW', purusha='prathama', vacana=0, gana=6, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'muYcati')

    def test_bhu_satr_present_participle(self) -> None:
        """Tests BU + Satf -> Bavat."""
        prakriya = derive_krdanta('BU', 'Satf', gana=1, db_path=self.test_db_path)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'Bavat')

if __name__ == '__main__':
    unittest.main()