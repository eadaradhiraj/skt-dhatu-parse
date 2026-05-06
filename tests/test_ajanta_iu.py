import unittest
from skt_dhatu_parse.subanta import derive_subanta

class TestAjanta(unittest.TestCase):

    def test_hari_masculine(self) -> None:
        p_nom_pl = derive_subanta('hari', 1, 2, 'm')
        self.assertEqual(p_nom_pl.get_current_string(), 'harayaH')
        
        p_acc_pl = derive_subanta('hari', 2, 2, 'm')
        self.assertEqual(p_acc_pl.get_current_string(), 'harIn')
        
        p_inst_sg = derive_subanta('hari', 3, 0, 'm')
        self.assertEqual(p_inst_sg.get_current_string(), 'hariRA')
        
        p_dat_sg = derive_subanta('hari', 4, 0, 'm')
        self.assertEqual(p_dat_sg.get_current_string(), 'haraye')
        
        p_abl_sg = derive_subanta('hari', 5, 0, 'm')
        self.assertEqual(p_abl_sg.get_current_string(), 'hareH')
        
        p_loc_sg = derive_subanta('hari', 7, 0, 'm')
        self.assertEqual(p_loc_sg.get_current_string(), 'harO')

    def test_guru_masculine(self) -> None:
        p_nom_pl = derive_subanta('guru', 1, 2, 'm')
        self.assertEqual(p_nom_pl.get_current_string(), 'guravaH')
        
        p_dat_sg = derive_subanta('guru', 4, 0, 'm')
        self.assertEqual(p_dat_sg.get_current_string(), 'gurave')
        
        p_gen_pl = derive_subanta('guru', 6, 2, 'm')
        self.assertEqual(p_gen_pl.get_current_string(), 'gurURAm')

    def test_mati_feminine(self) -> None:
        p_acc_pl = derive_subanta('mati', 2, 2, 'f')
        self.assertEqual(p_acc_pl.get_current_string(), 'matIH') # Not n!
        
        p_inst_sg = derive_subanta('mati', 3, 0, 'f')
        self.assertEqual(p_inst_sg.get_current_string(), 'matyA') # No nA!
        
        p_dat_sg = derive_subanta('mati', 4, 0, 'f')
        self.assertEqual(p_dat_sg.get_current_string(), 'matyE')
        
        p_loc_sg = derive_subanta('mati', 7, 0, 'f')
        self.assertEqual(p_loc_sg.get_current_string(), 'matyAm')

    def test_nadi_feminine(self) -> None:
        p_nom_sg = derive_subanta('nadI', 1, 0, 'f')
        self.assertEqual(p_nom_sg.get_current_string(), 'nadI') # su dropped
        
        p_nom_du = derive_subanta('nadI', 1, 1, 'f')
        self.assertEqual(p_nom_du.get_current_string(), 'nadyO')
        
        p_dat_sg = derive_subanta('nadI', 4, 0, 'f')
        self.assertEqual(p_dat_sg.get_current_string(), 'nadyE')

if __name__ == '__main__':
    unittest.main()
