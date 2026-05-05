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

if __name__ == '__main__':
    unittest.main()
