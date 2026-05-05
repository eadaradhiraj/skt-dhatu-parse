import unittest
from skt_dhatu_parse.subanta import derive_subanta

class TestSubanta(unittest.TestCase):
    def test_prathama_ekavacana_visarga(self):
        prakriya = derive_subanta('rAma', 'pum', 'prathama', 0)
        self.assertEqual(prakriya.get_current_string(), 'rAmaH')
        self.assertIn('ajanta', prakriya.terms[0].tags)

    def test_halanta_tagging(self):
        prakriya = derive_subanta('marut', 'pum', 'prathama', 0)
        self.assertIn('halanta', prakriya.terms[0].tags)

    def test_sambuddhi_tagging(self):
        prakriya = derive_subanta('rAma', 'pum', 'sambodhana', 0)
        self.assertIn('sambuddhi', prakriya.terms[1].tags)
