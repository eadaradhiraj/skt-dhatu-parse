import unittest
from skt_dhatu_parse.models import Term, Prakriya
from skt_dhatu_parse import rules

class TestCoverageEdgeCases(unittest.TestCase):
    def test_akrtsarvadhatukayor_dirghah(self):
        p = Prakriya()
        p.add_term(Term('ji', 'dhatu'))
        p.add_term(Term('yak', 'vikaraRa'))
        rules.akrtsarvadhatukayor_dirghah(p)
        self.assertEqual(p.terms[0].text, 'jI')
        
        p2 = Prakriya()
        p2.add_term(Term('stu', 'dhatu'))
        p2.add_term(Term('yak', 'vikaraRa'))
        rules.akrtsarvadhatukayor_dirghah(p2)
        self.assertEqual(p2.terms[0].text, 'stU')

    def test_jhonta_atmanepada_anat(self):
        p = Prakriya()
        d = Term('As', 'dhatu')
        d.tags.add('atmanepada')
        d.tags.add('gana_2')
        p.add_term(d)
        suf = Term('Ja', 'pratyaya')
        p.add_term(suf)
        rules.jhonta(p)
        self.assertEqual(p.terms[1].text, 'ata')

    def test_it_agama_lit_not_kradi(self):
        p = Prakriya()
        d = Term('BU', 'dhatu')
        d.tags.add('clean_BU')
        p.add_term(d)
        suf = Term('Ta', 'pratyaya')
        suf.tags.add('ardhadhatuka')
        suf.tags.add('liW')
        p.add_term(suf)
        rules.it_agama(p)
        self.assertEqual(p.terms[1].text, 'iTa')

    def test_jhasas_tathor_dho_dhah_dad_exception(self):
        p = Prakriya()
        p.add_term(Term('da', 'abhyasa'))
        d = Term('D', 'dhatu')
        p.add_term(d)
        p.add_term(Term('tas', 'pratyaya'))
        rules.jhasas_tathor_dho_dhah(p)
        self.assertEqual(p.terms[2].text, 'tas')

    def test_dadhas_tathor_ca_dad_exception(self):
        p = Prakriya()
        p.add_term(Term('da', 'abhyasa'))
        p.add_term(Term('D', 'dhatu'))
        p.add_term(Term('tas', 'pratyaya'))
        rules.dadhas_tathor_ca(p)
        self.assertEqual(p.terms[0].text, 'Da')

    def test_labh_rabh_num_coverage(self):
        from skt_dhatu_parse.sanadi import derive_secondary_root
        prakriya = derive_secondary_root('laB', 'Ric', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'laMBi')


    def test_jhonta_passive_plural(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('ci', 'laW', purusha='prathama', vacana=2, gana=5, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'cIyante')

    def test_er_lini_benedictive(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('dA', 'ASIrliN', purusha='prathama', vacana=0, gana=3)
        self.assertEqual(prakriya.get_current_string(), 'deyAt')


    def test_stha_lun_plural(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('sTA', 'luN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'asTuH')

    def test_as_lun_identity_change(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('as', 'luN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'aBUt')

    def test_jna_satr(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('jYA', 'Satf', gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vijAnat')


    def test_jaksityadi_plural(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('SAs', 'laW', purusha='prathama', vacana=2, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'SAsati')


    def test_aniditam_nasal_drop(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('daMS', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'dazwa')
        
    def test_vah_samprasarana_and_o(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        p_kta = derive_krdanta('vah', 'kta', gana=1)
        self.assertEqual(p_kta.get_current_string(), 'UQa')
        p_tumun = derive_krdanta('vah', 'tumun', gana=1)
        self.assertEqual(p_tumun.get_current_string(), 'voQum')


    def test_vap_vad_samprasarana(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        p_vap = derive_krdanta('vap', 'kta', gana=1)
        self.assertEqual(p_vap.get_current_string(), 'upta')
        p_vad = derive_krdanta('vad', 'kta', gana=1)
        self.assertEqual(p_vad.get_current_string(), 'udita')


    def test_mrjer_vrddhih(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('mfj', 'laW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'mArzwi')

    def test_vyadh_samprasarana(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('vyaD', 'laW', purusha='prathama', vacana=0, gana=4)
        self.assertEqual(prakriya.get_current_string(), 'viDyati')

    def test_can_aorist(self):
        from skt_dhatu_parse.engine import derive
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi = derive_secondary_root('kf', 'Ric', gana=8)
        prakriya = derive(custom_dhatu=sanadi.terms[0], lakara_name='luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'acIkarat')


    def test_vac_aorist(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('vac', 'luN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'avocat')
        
    def test_ji_lit_g(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('ji', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jigAya')
        
    def test_sas_hi(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('SAs', 'loW', purusha='madhyama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'SADi')
        
    def test_gai_kta(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('gE', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gIta')


    def test_sas_hi_nameerror(self):
        from skt_dhatu_parse.engine import derive
        prakriya = derive('SAs', 'loW', purusha='madhyama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'SADi')
        
    def test_gai_kta_ordering(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('gE', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gIta')


    def test_brute_force_coverage_adeca(self):
        from skt_dhatu_parse import rules
        from skt_dhatu_parse.models import Term, Prakriya
        p = Prakriya()
        d = Term('gE', 'dhatu')
        d.tags.add('clean_gE')
        p.add_term(d)
        s = Term('ta', 'pratyaya')
        s.tags.add('ardhadhatuka')
        p.add_term(s)
        rules.adeca_upadese_asiti(p)
        self.assertEqual(p.terms[0].text, 'gA')

    def test_brute_force_coverage_stha(self):
        from skt_dhatu_parse import rules
        from skt_dhatu_parse.models import Term, Prakriya
        p = Prakriya()
        d = Term('gA', 'dhatu')
        p.add_term(d)
        s = Term('ta', 'pratyaya')
        s.tags.add('kit')
        p.add_term(s)
        rules.stha_adi_ita(p)
        self.assertEqual(p.terms[0].text, 'gI')


    def test_hve_samprasarana(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('hve', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'hUta')


    def test_svap_can_aorist(self):
        from skt_dhatu_parse.engine import derive
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi = derive_secondary_root('svap', 'Ric', gana=2)
        prakriya = derive(custom_dhatu=sanadi.terms[0], lakara_name='luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'asUzupat')

    def test_svi_kta_samprasarana(self):
        from skt_dhatu_parse.krdanta import derive_krdanta
        prakriya = derive_krdanta('Svi', 'kta', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SUna')

if __name__ == '__main__':
    unittest.main()
