import unittest
from skt_dhatu_parse.subanta import derive_subanta

class TestHalanta(unittest.TestCase):

    def test_gacchat_masculine(self) -> None:
        p_nom_sg = derive_subanta('gacCat', 1, 0, 'm')
        self.assertEqual(p_nom_sg.get_current_string(), 'gacCan') # num augment + su lopa + samyoga lopa
        
        p_nom_du = derive_subanta('gacCat', 1, 1, 'm')
        self.assertEqual(p_nom_du.get_current_string(), 'gacCantO') # num augment
        
        p_acc_pl = derive_subanta('gacCat', 2, 2, 'm')
        self.assertEqual(p_acc_pl.get_current_string(), 'gacCataH') # No num augment (weak case)
        
        p_inst_du = derive_subanta('gacCat', 3, 1, 'm')
        self.assertEqual(p_inst_du.get_current_string(), 'gacCadByAm') # Jhal sandhi: t -> d before bh
        
        p_loc_pl = derive_subanta('gacCat', 7, 2, 'm')
        self.assertEqual(p_loc_pl.get_current_string(), 'gacCatsu') # t -> t before s


    def test_gacchat_ablative(self) -> None:
        p_abl_sg = derive_subanta('gacCat', 5, 0, 'm')
        self.assertEqual(p_abl_sg.get_current_string(), 'gacCataH')

if __name__ == '__main__':
    unittest.main()
