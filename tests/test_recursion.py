import unittest
from skt_dhatu_parse.engine import derive
from skt_dhatu_parse.sanadi import derive_secondary_root

class TestRecursion(unittest.TestCase):

    def test_causative_conjugation(self) -> None:
        """
        Tests the ultimate Pāṇinian recursion:
        1. Generates Causative root (BU + Ric -> BAvi)
        2. Feeds 'BAvi' back into the Tiṅanta engine for laW.
        3. BAvi + Sap + tip -> BAve + a + ti -> BAvayati!
        """
        sanadi_prakriya = derive_secondary_root('BU', 'Ric', gana=1)
        new_root_term = sanadi_prakriya.terms[0]
        
        final_prakriya = derive(custom_dhatu=new_root_term, lakara_name='laW')
        self.assertIsNotNone(final_prakriya)
        self.assertEqual(final_prakriya.get_current_string(), 'BAvayati')

if __name__ == '__main__':
    unittest.main()