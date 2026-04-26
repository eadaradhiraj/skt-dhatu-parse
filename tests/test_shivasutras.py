import unittest
from shivasutras import get_pratyahara

class TestPratyaharas(unittest.TestCase):

    def test_vowels_ac_and_subsets(self):
        """Test 'ac' (all vowels) and standard vowel subsets."""
        # ac: All vowels
        self.assertEqual(
            get_pratyahara('a', 'c'),['a', 'i', 'u', 'R', 'lR', 'e', 'o', 'ai', 'au']
        )
        
        # ik: Simple vowels used in 'iko yaNaci' (Sandhi)
        self.assertEqual(
            get_pratyahara('i', 'k'),['i', 'u', 'R', 'lR']
        )
        
        # eG: Diphthongs
        self.assertEqual(
            get_pratyahara('e', 'G'), 
            ['e', 'o']
        )
        
        # ec: All diphthongs
        self.assertEqual(
            get_pratyahara('e', 'c'), 
            ['e', 'o', 'ai', 'au']
        )

    def test_consonants_hal_and_subsets(self):
        """Test 'hal' (all consonants) and consonant subsets."""
        hal = get_pratyahara('h', 'l')
        # There are 34 consonants in the hal pratyahara (including the duplicate 'h')
        self.assertEqual(len(hal), 34)
        self.assertEqual(hal[0], 'h')
        self.assertEqual(hal[-1], 'h') # 'h' appears in sutra 5 and 14

        # jaz: Soft unaspirated consonants (jbaGaDaza)
        self.assertEqual(
            get_pratyahara('j', 'z'),['j', 'b', 'g', 'D', 'd']
        )
        
        # khay: Hard consonants
        self.assertEqual(
            get_pratyahara('kh', 'y'),['kh', 'ph', 'ch', 'Th', 'th', 'c', 'T', 't', 'k', 'p']
        )

    def test_special_N_marker(self):
        """
        Test the most famous edge case in Panini: 
        The 'N' (ṇ) marker appears twice (Sutra 1 and Sutra 6).
        """
        # aN generally refers to the first sutra (a, i, u)
        self.assertEqual(
            get_pratyahara('a', 'N'), 
            ['a', 'i', 'u']
        )
        
        # iN refers to the second 'N' (up to Sutra 6)
        self.assertEqual(
            get_pratyahara('i', 'N'),['i', 'u', 'R', 'lR', 'e', 'o', 'ai', 'au', 'h', 'y', 'v', 'r', 'l']
        )
        
        # yaN refers to the second 'N' (Semi-vowels)
        self.assertEqual(
            get_pratyahara('y', 'N'), 
            ['y', 'v', 'r', 'l']
        )

    def test_invalid_pratyaharas(self):
        """Ensure the engine correctly rejects impossible Pratyaharas."""
        # Non-existent start letter
        with self.assertRaises(ValueError):
            get_pratyahara('x', 'c')
            
        # Non-existent it-marker
        with self.assertRaises(ValueError):
            get_pratyahara('a', 'x')
            
        # Backwards pratyahara (start letter comes AFTER the marker)
        # 'c' is the marker of sutra 4, 'k' is the marker of sutra 2.
        with self.assertRaises(ValueError):
            get_pratyahara('e', 'k') 

if __name__ == '__main__':
    unittest.main()