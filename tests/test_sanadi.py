import unittest
from skt_dhatu_parse.sanadi import derive_secondary_root

class TestSanadi(unittest.TestCase):

    def test_causative_bhu(self) -> None:
        """Tests Causative: BU + Ric -> BAvi."""
        prakriya = derive_secondary_root('BU', 'Ric', gana=1)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'BAvi')
        self.assertEqual(prakriya.terms[0].term_type, 'dhatu')

    def test_causative_ram(self) -> None:
        """Tests Causative: ram + Ric -> rAmi."""
        prakriya = derive_secondary_root('ram', 'Ric', gana=1)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'rAmi')

    def test_causative_budh(self) -> None:
        """Tests buD + Ric -> boDi (Penultimate Guna)."""
        prakriya = derive_secondary_root('buD', 'Ric', gana=1)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'boDi')

    def test_causative_han(self) -> None:
        """Tests Causative: han + Ric -> GAti (ho hanter & hanato ṇinnali)."""
        prakriya = derive_secondary_root('han', 'Ric', gana=2)
        self.assertIsNotNone(prakriya)
        self.assertEqual(prakriya.get_current_string(), 'GAti')

if __name__ == '__main__':
    unittest.main()