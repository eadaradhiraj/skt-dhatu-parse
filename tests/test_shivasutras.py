import unittest
from skt_dhatu_parse.shivasutras import get_pratyahara

class TestPratyaharasSLP1(unittest.TestCase):

    def test_vowels_ac_and_subsets(self):
        """Test 'ac' (all vowels) and standard vowel subsets in SLP1."""
        # ac: All vowels
        self.assertEqual(
            get_pratyahara('a', 'c'),['a', 'i', 'u', 'f', 'x', 'e', 'o', 'E', 'O']
        )
        
        # ik: Simple vowels used in 'iko yaRaci' (Sandhi)
        self.assertEqual(
            get_pratyahara('i', 'k'),['i', 'u', 'f', 'x']
        )
        
        # eN (eṅ): Diphthongs e, o
        self.assertEqual(
            get_pratyahara('e', 'N'), 
            ['e', 'o']
        )
        
        # ec: All diphthongs
        self.assertEqual(
            get_pratyahara('e', 'c'), 
            ['e', 'o', 'E', 'O']
        )

    def test_consonants_hal_and_subsets(self):
        """Test 'hal' (all consonants) and consonant subsets in SLP1."""
        hal = get_pratyahara('h', 'l')
        # There are 34 consonants in the hal pratyahara (including the duplicate 'h')
        self.assertEqual(len(hal), 34)
        self.assertEqual(hal[0], 'h')
        self.assertEqual(hal[-1], 'h') # 'h' appears in sutras 5 and 14

        # jaS (jaś): Soft unaspirated consonants
        self.assertEqual(
            get_pratyahara('j', 'S'),['j', 'b', 'g', 'q', 'd']
        )
        
        # Kay (khay): Hard consonants
        self.assertEqual(
            get_pratyahara('K', 'y'),['K', 'P', 'C', 'W', 'T', 'c', 'w', 't', 'k', 'p']
        )

    def test_special_R_marker(self):
        """
        Test the most famous edge case in Panini: 
        The 'ṇ' marker is 'R' in SLP1, and it appears twice (Sutras 1 and 6).
        """
        # aR (aṇ) generally refers to the first sutra (a, i, u)
        self.assertEqual(
            get_pratyahara('a', 'R'), 
            ['a', 'i', 'u']
        )
        
        # iR (iṇ) refers to the second 'R' (up to Sutra 6)
        self.assertEqual(
            get_pratyahara('i', 'R'),['i', 'u', 'f', 'x', 'e', 'o', 'E', 'O', 'h', 'y', 'v', 'r', 'l']
        )
        
        # yaR (yaṇ) refers to the second 'R' (Semi-vowels)
        self.assertEqual(
            get_pratyahara('y', 'R'), 
            ['y', 'v', 'r', 'l']
        )

    def test_invalid_pratyaharas(self):
        """Ensure the engine correctly rejects impossible Pratyaharas."""
        # Non-existent start letter
        with self.assertRaises(ValueError):
            get_pratyahara('X', 'c')
            
        # Non-existent it-marker
        with self.assertRaises(ValueError):
            get_pratyahara('a', 'X')
            
        # Backwards pratyahara (start letter comes AFTER the marker)
        # 'c' is the marker of sutra 4, 'k' is the marker of sutra 2.
        with self.assertRaises(ValueError):
            get_pratyahara('e', 'k') 

if __name__ == '__main__':
    unittest.main()