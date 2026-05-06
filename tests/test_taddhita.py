import unittest
from skt_dhatu_parse.taddhita import derive_taddhita

class TestTaddhita(unittest.TestCase):
    def test_ziva_an(self):
        p = derive_taddhita('ziva', 'aR')
        self.assertEqual(p.get_current_string(), 'zEva') # Ādivṛddhi & bha lopa
        
    def test_pandu_an(self):
        p = derive_taddhita('pARqu', 'aR')
        self.assertEqual(p.get_current_string(), 'pARqava') # or guṇaḥ + ayavāyāvaḥ
        
    def test_guru_tva(self):
        p = derive_taddhita('guru', 'tva')
        self.assertEqual(p.get_current_string(), 'gurutva')
