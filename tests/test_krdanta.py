import unittest
from skt_dhatu_parse.krdanta import derive_krdanta

class TestKrdanta(unittest.TestCase):

    def test_buddha_derivation(self) -> None:
        prakriya = derive_krdanta('buD', 'kta', gana=1)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'budDa')

    def test_rama_ghany(self) -> None:
        prakriya = derive_krdanta('ram', 'GaY', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'rAma')

    def test_ramana_lyut(self) -> None:
        prakriya = derive_krdanta('ram', 'lyuW', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'ramaRa')

    def test_ram_ktva_nasal_drop(self) -> None:
        prakriya = derive_krdanta('ram', 'ktvA', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'ratvA')

    def test_gam_kta_nasal_drop(self) -> None:
        prakriya = derive_krdanta('gam', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gata')

    def test_vac_kta_samprasarana(self) -> None:
        prakriya = derive_krdanta('vac', 'kta', gana=2)
        self.assertEqual(prakriya.get_current_string(), 'ukta')

    def test_chid_kta_nishtha(self) -> None:
        prakriya = derive_krdanta('Cid', 'kta', gana=7)
        self.assertEqual(prakriya.get_current_string(), 'Cinna')

    def test_path_kta_set(self) -> None:
        prakriya = derive_krdanta('paW', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'paWita')

    def test_duh_kta_gana_2_anit(self) -> None:
        prakriya = derive_krdanta('duh', 'kta', gana=2)
        self.assertEqual(prakriya.get_current_string(), 'dugDa')

    def test_duh_kta_gana_1_set(self) -> None:
        prakriya = derive_krdanta('duh', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'duhita')

    def test_bhu_tavya_guna_sandhi(self) -> None:
        prakriya = derive_krdanta('BU', 'tavya', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Bavitavya')

    def test_svap_kta_samprasarana(self) -> None:
        prakriya = derive_krdanta('svap', 'kta', gana=2)
        self.assertEqual(prakriya.get_current_string(), 'supta')

    def test_srj_kta_retroflexion(self) -> None:
        prakriya = derive_krdanta('sfj', 'kta', gana=6)
        self.assertEqual(prakriya.get_current_string(), 'sfzwa')

    def test_muc_sa_num_parasavarna(self) -> None:
        from skt_dhatu_parse.engine import derive
        prakriya = derive('muc', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(prakriya.get_current_string(), 'muYcati')

    def test_bhu_satr_present_participle(self) -> None:
        prakriya = derive_krdanta('BU', 'Satf', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Bavat')
        
    def test_drs_kta_retroflexion(self) -> None:
        prakriya = derive_krdanta('dfS', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'dfzwa')

    def test_gam_tavya_anusvara_parasavarna(self) -> None:
        """Tests gam + tavya -> gantavya (m -> M -> n)."""
        prakriya = derive_krdanta('gam', 'tavya', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gantavya')

    def test_bhu_all_krdantas(self) -> None:
        """Tests the comprehensive generation of Krdantas for BU."""
        expected_forms = {
            'kta': 'BUta', 'ktavatu': 'BUtavat', 'ktvA': 'BUtvA',
            'tumun': 'Bavitum', 'tavya': 'Bavitavya', 'anIyar': 'BavanIya',
            'yat': 'Bavya', 'Ryat': 'BAvya', 'Satf': 'Bavat',
            'lyuW': 'Bavana', 'Rvul': 'BAvaka', 'tfc': 'Bavitf', 'GaY': 'BAva'
        }
        for affix, expected in expected_forms.items():
            with self.subTest(affix=affix):
                prakriya = derive_krdanta('BU', affix, gana=1)
                self.assertEqual(prakriya.get_current_string(), expected)

    def test_upasarga_krdanta(self) -> None:
        prakriya = derive_krdanta('gam', 'kta', gana=1, upasargas=['A'])
        self.assertEqual(prakriya.get_current_string(), 'Agata')
        
    def test_pa_kta(self) -> None:
        prakriya = derive_krdanta('pA', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'pIta')
        
    def test_da_kta(self) -> None:
        prakriya = derive_krdanta('dA', 'kta', gana=3)
        self.assertEqual(prakriya.get_current_string(), 'datta')

    def test_da_yat(self) -> None:
        prakriya = derive_krdanta('dA', 'yat', gana=3)
        self.assertEqual(prakriya.get_current_string(), 'deya')

    def test_da_rvul(self) -> None:
        prakriya = derive_krdanta('dA', 'Rvul', gana=3)
        self.assertEqual(prakriya.get_current_string(), 'dAyaka')

    def test_vrasc_samprasarana_and_retroflexion(self) -> None:
        """Tests vraSc + kta -> vfzwa (samprasarana + cCh squashing)."""
        prakriya = derive_krdanta('vraSc', 'kta', gana=6)
        # Note: upadesa has nasal markers o!vraScU!, which strip cleanly to vraSc
        self.assertEqual(prakriya.get_current_string(), 'vfzwa')

    def test_prac_tavya_and_satr(self) -> None:
        """Tests praC with both jhal retroflexion and che-ca 'c' augment."""
        p_tavya = derive_krdanta('praC', 'tavya', gana=6)
        self.assertEqual(p_tavya.get_current_string(), 'prazwavya')
        
        p_satr = derive_krdanta('praC', 'Satf', gana=6)
        self.assertEqual(p_satr.get_current_string(), 'pfcCat')

    def test_kr_satr(self) -> None:
        """Tests kṛ + Śatṛ -> kurvat (u-morphing and yaṇ sandhi)."""
        prakriya = derive_krdanta('kf', 'Satf', gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurvat')

if __name__ == '__main__':
    unittest.main()