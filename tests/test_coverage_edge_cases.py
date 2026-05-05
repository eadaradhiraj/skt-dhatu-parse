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

if __name__ == '__main__':
    unittest.main()

    def test_lit_atmanepada_mud(self):
        prakriya = derive('mud', 'liW', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'mumudize')
