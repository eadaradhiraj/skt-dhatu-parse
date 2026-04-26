import unittest
from models import Term
from anubandha import resolve_it_markers

class TestAnubandha(unittest.TestCase):

    def test_upadese_ajanunasika_it(self):
        """Rule 1.3.2: Nasalized vowels (marked with !) are 'it'."""
        
        # Test 1: akzU! -> akz + Udit
        t1 = Term('akzU!', 'dhatu')
        resolve_it_markers(t1)
        self.assertEqual(t1.text, 'akz')
        self.assertIn('Udit', t1.tags) # Udit roots optionally take 'iw' augment!

        # Test 2: ahi! -> ah + idit
        t2 = Term('ahi!', 'dhatu')
        resolve_it_markers(t2)
        self.assertEqual(t2.text, 'ah')
        self.assertIn('idit', t2.tags) # idit roots get 'num' augment!

    def test_hal_antyam(self):
        """Rule 1.3.3: Final consonants are 'it'."""
        # 3rd person singular suffix (tiP)
        t = Term('tip', 'pratyaya')
        resolve_it_markers(t)
        self.assertEqual(t.text, 'ti')
        self.assertIn('pit', t.tags) # pit affixes prevent certain vowel modifications

    def test_lasakvataddhite_and_hal_antyam(self):
        """Rule 1.3.8 & 1.3.3: Handling multiple markers on one term."""
        # The class 1 vikaraNa infix is 'Sap' (śap)
        t = Term('Sap', 'vikaraRa')
        resolve_it_markers(t)
        
        self.assertEqual(t.text, 'a') # Both S and p are removed
        self.assertIn('Sit', t.tags)  # Sit tags trigger 'SArvadhAtuka' operations
        self.assertIn('pit', t.tags)


if __name__ == '__main__':
    unittest.main()