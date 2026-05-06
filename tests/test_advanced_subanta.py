import unittest
from skt_dhatu_parse.subanta import derive_subanta

class TestAdvancedSubanta(unittest.TestCase):
    def test_sarva_pronoun(self):
        p = derive_subanta('sarva', 4, 0, 'p') # Dative sg
        self.assertEqual(p.get_current_string(), 'sarvasmE')
        p2 = derive_subanta('sarva', 1, 2, 'p') # Nom pl
        self.assertEqual(p2.get_current_string(), 'sarve')

    def test_rajan_stem(self):
        p1 = derive_subanta('rAjan', 1, 0, 'm')
        self.assertEqual(p1.get_current_string(), 'rAjA')
        p2 = derive_subanta('rAjan', 3, 0, 'm')
        self.assertEqual(p2.get_current_string(), 'rAjYA')
        p3 = derive_subanta('rAjan', 3, 2, 'm')
        self.assertEqual(p3.get_current_string(), 'rAjaBiH')

    def test_manas_stem(self):
        p1 = derive_subanta('manas', 3, 2, 'n')
        self.assertEqual(p1.get_current_string(), 'manoBiH')
