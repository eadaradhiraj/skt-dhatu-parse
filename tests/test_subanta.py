import unittest
from skt_dhatu_parse.subanta import derive_subanta

class TestSubanta(unittest.TestCase):

    def test_rama_nominative(self) -> None:
        p1 = derive_subanta('rAma', 1, 0)
        self.assertEqual(p1.get_current_string(), 'rAmaH')
        p2 = derive_subanta('rAma', 1, 1)
        self.assertEqual(p2.get_current_string(), 'rAmO')
        p3 = derive_subanta('rAma', 1, 2)
        self.assertEqual(p3.get_current_string(), 'rAmAH')

    def test_rama_accusative(self) -> None:
        p1 = derive_subanta('rAma', 2, 0)
        self.assertEqual(p1.get_current_string(), 'rAmam')
        p2 = derive_subanta('rAma', 2, 1)
        self.assertEqual(p2.get_current_string(), 'rAmO')
        p3 = derive_subanta('rAma', 2, 2)
        self.assertEqual(p3.get_current_string(), 'rAmAn') # tasmācchaśo naḥ puṃsi!

    def test_rama_instrumental(self) -> None:
        p1 = derive_subanta('rAma', 3, 0)
        self.assertEqual(p1.get_current_string(), 'rAmeRa') # ina + natva!
        p2 = derive_subanta('rAma', 3, 1)
        self.assertEqual(p2.get_current_string(), 'rAmAByAm')
        p3 = derive_subanta('rAma', 3, 2)
        self.assertEqual(p3.get_current_string(), 'rAmEH')

    def test_rama_dative(self) -> None:
        p1 = derive_subanta('rAma', 4, 0)
        self.assertEqual(p1.get_current_string(), 'rAmAya')
        p3 = derive_subanta('rAma', 4, 2)
        self.assertEqual(p3.get_current_string(), 'rAmeByaH')

    def test_rama_ablative(self) -> None:
        p1 = derive_subanta('rAma', 5, 0)
        self.assertEqual(p1.get_current_string(), 'rAmAt')

    def test_rama_genitive(self) -> None:
        p1 = derive_subanta('rAma', 6, 0)
        self.assertEqual(p1.get_current_string(), 'rAmasya')
        p2 = derive_subanta('rAma', 6, 1)
        self.assertEqual(p2.get_current_string(), 'rAmayoH')
        p3 = derive_subanta('rAma', 6, 2)
        self.assertEqual(p3.get_current_string(), 'rAmARAm') # nuṭ + nāmi + ṇatva!

    def test_rama_locative(self) -> None:
        p1 = derive_subanta('rAma', 7, 0)
        self.assertEqual(p1.get_current_string(), 'rAme')
        p3 = derive_subanta('rAma', 7, 2)
        self.assertEqual(p3.get_current_string(), 'rAmezu') # ṣatva!


    def test_phala_neuter(self) -> None:
        p1 = derive_subanta('Pala', 1, 0, 'n')
        self.assertEqual(p1.get_current_string(), 'Palam')
        p2 = derive_subanta('Pala', 1, 1, 'n')
        self.assertEqual(p2.get_current_string(), 'Pale')
        p3 = derive_subanta('Pala', 1, 2, 'n')
        self.assertEqual(p3.get_current_string(), 'PalAni')
        # Check an oblique case to ensure fallback to masculine works
        p4 = derive_subanta('Pala', 3, 0, 'n')
        self.assertEqual(p4.get_current_string(), 'Palena')

    def test_rama_feminine(self) -> None:
        p1 = derive_subanta('ramA', 1, 0, 'f')
        self.assertEqual(p1.get_current_string(), 'ramA')
        p2 = derive_subanta('ramA', 1, 1, 'f')
        self.assertEqual(p2.get_current_string(), 'rame')
        p3 = derive_subanta('ramA', 1, 2, 'f')
        self.assertEqual(p3.get_current_string(), 'ramAH')
        
        p4 = derive_subanta('ramA', 3, 0, 'f')
        self.assertEqual(p4.get_current_string(), 'ramayA')
        p5 = derive_subanta('ramA', 4, 0, 'f')
        self.assertEqual(p5.get_current_string(), 'ramAyE')
        p6 = derive_subanta('ramA', 6, 0, 'f')
        self.assertEqual(p6.get_current_string(), 'ramAyAH')
        p7 = derive_subanta('ramA', 7, 0, 'f')
        self.assertEqual(p7.get_current_string(), 'ramAyAm')
        
        p8 = derive_subanta('ramA', 6, 2, 'f')
        self.assertEqual(p8.get_current_string(), 'ramARAm')

if __name__ == '__main__':
    unittest.main()
