import unittest
from skt_dhatu_parse.engine import derive

class TestPipeline(unittest.TestCase):

    def test_derive_akzati(self) -> None:
        prakriya = derive('akz', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'akzati')
        self.assertIn('Udit', prakriya.terms[0].tags) 
        
    def test_derive_aMhate(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aMhate')
        self.assertIn('idit', prakriya.terms[0].tags) 

    def test_bhavami(self) -> None:
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_atmanepada_uttama_singular(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aMhe')

    def test_past_tense_dual(self) -> None:
        prakriya = derive('BU', 'laN', purusha='madhyama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aBavatam')

    def test_past_tense_plural_consonant_drop(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aBavan')

    def test_future_tense_set(self) -> None:
        prakriya = derive('BU', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Bavizyati')

    def test_future_tense_anit(self) -> None:
        prakriya = derive('ji', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jezyati')

    def test_gana_4_divyadi(self) -> None:
        prakriya = derive('div', 'laW', purusha='prathama', vacana=0, gana=4)
        self.assertEqual(prakriya.get_current_string(), 'dIvyati')

    def test_gana_6_tudadi(self) -> None:
        prakriya = derive('tud', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(prakriya.get_current_string(), 'tudati')

    def test_perfect_tense_singular(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUva')

    def test_perfect_tense_dual(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUvatuH')

    def test_perfect_tense_plural(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUvuH')

    def test_invalid_roots_return_none(self) -> None:
        from skt_dhatu_parse.krdanta import derive_krdanta
        from skt_dhatu_parse.sanadi import derive_secondary_root
        self.assertIsNone(derive('xyz_invalid_root'))
        self.assertIsNone(derive_krdanta('xyz_invalid_root', 'kta'))
        self.assertIsNone(derive_secondary_root('xyz_invalid_root', 'Ric'))

    def test_gana_9_vikri_singular(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vikrIRIte')

    def test_gana_9_vikri_plural(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=2, gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vikrIRate')

    def test_dhatvadeh_and_paghra(self) -> None:
        prakriya = derive('sTA', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'tizWati')

    def test_causative_puk_and_upasarga_satva(self) -> None:
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi_prakriya = derive_secondary_root('sTA', 'Ric', gana=1)
        final_prakriya = derive('sTA', 'lfW', purusha='prathama', vacana=0, gana=1, upasargas=['prati'], custom_dhatu=sanadi_prakriya.terms[0])
        self.assertEqual(final_prakriya.get_current_string(), 'pratizWApayizyati')

    def test_multiple_upasargas(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=0, gana=1, upasargas=['vi', 'A'])
        self.assertEqual(prakriya.get_current_string(), 'vyABavat')

    def test_gam_lath(self) -> None:
        prakriya = derive('gam', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gacCati')

    def test_perfect_tense_path(self) -> None:
        prakriya = derive('paW', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'papAWa')

    def test_gana_8_kr_singular(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'karoti')

    def test_gana_8_kr_dual(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurutaH')

    def test_gana_8_kr_plural(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=2, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurvanti')

    def test_gana_8_kr_uttama_dual(self) -> None:
        prakriya = derive('kf', 'laW', purusha='uttama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurvaH')

    def test_perfect_tense_kr_dual(self) -> None:
        prakriya = derive('kf', 'liW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'cakratuH')

    def test_perfect_tense_kr_dual(self) -> None:
        prakriya = derive('kf', 'liW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'cakratuH')

    def test_models_repr_and_history(self) -> None:
        """Covers the __repr__ and stdout logging in models.py"""
        from skt_dhatu_parse.models import Term, Prakriya
        import io
        import sys
        
        t = Term('BU', 'dhatu')
        repr_str = repr(t)
        self.assertTrue(repr_str.startswith("Term(text='BU'"))
        
        p = Prakriya()
        p.add_term(t)
        p.log("Test log entry")
        
        # Capture stdout to test the print statement silently
        captured_output = io.StringIO()
        sys.stdout = captured_output
        p.print_history()
        sys.stdout = sys.__stdout__
        
        self.assertIn("Test log entry", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()