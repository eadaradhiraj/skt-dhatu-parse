import unittest
from skt_dhatu_parse.models import Term, Prakriya
from skt_dhatu_parse.rules import (
    apply_guna, apply_vrddhi, paghra_sthadi_adesha, upasarga_sandhi, 
    jhalam_jas_jhasi, jhasas_tathor_dho_dhah, tasthasthamipam, yuvor_anakau,
    dhatvadeh_sah_sah_no_nah, rashabhyam_no_nah, sna_sandhi, upasarga_satva
)

class TestRules(unittest.TestCase):

    def test_vowel_helpers(self) -> None:
        self.assertEqual(apply_guna('i'), 'e')
        self.assertEqual(apply_guna('u'), 'o')
        self.assertEqual(apply_guna('f'), 'ar')
        self.assertEqual(apply_guna('x'), 'al')
        self.assertEqual(apply_guna('a'), 'a') 

        self.assertEqual(apply_vrddhi('a'), 'A')
        self.assertEqual(apply_vrddhi('i'), 'E')
        self.assertEqual(apply_vrddhi('u'), 'O')
        self.assertEqual(apply_vrddhi('f'), 'Ar')
        self.assertEqual(apply_vrddhi('x'), 'Al')
        self.assertEqual(apply_vrddhi('k'), 'k') 

    def test_paghra_sthadi_adesha(self) -> None:
        mappings =[('pA', 'piba'), ('GrA', 'jiGra'), ('DmA', 'Dama'), 
                    ('mnA', 'mana'), ('dfS', 'pazya'), ('f', 'fcCa'), 
                    ('sf', 'DAva'), ('Sad', 'zIya'), ('sad', 'sIda')]
        for orig, adesha in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            vik = Term('Sap', 'vikaraRa')
            vik.tags.add('Sit')
            p.add_term(vik)
            paghra_sthadi_adesha(p)
            self.assertEqual(p.terms[0].text, adesha)

    def test_upasarga_sandhi_branches(self) -> None:
        tests =[
            ('upa', 'A', 'up', 'A'), 
            ('upa', 'i', 'up', 'e'), 
            ('upa', 'u', 'up', 'o'), 
            ('vi', 'a', 'vy', 'a'),  
            ('su', 'a', 'sv', 'a')   
        ]
        for upa, aug, exp_upa, exp_aug in tests:
            p = Prakriya()
            p.add_term(Term(upa, 'upasarga'))
            p.add_term(Term(aug, 'Agama'))
            upasarga_sandhi(p)
            self.assertEqual(p.terms[0].text, exp_upa)
            self.assertEqual(p.terms[1].text, exp_aug)

    def test_consonant_sandhi_branches(self) -> None:
        p = Prakriya()
        p.add_term(Term('buD', 'dhatu'))
        p.add_term(Term('Ta', 'pratyaya')) 
        jhasas_tathor_dho_dhah(p)
        self.assertEqual(p.terms[1].text, 'Da') 

        mappings =[('vak', 'g'), ('vac', 'j'), ('vaw', 'q'), ('vap', 'b')]
        for orig_jhal, expected_jas in mappings:
            p = Prakriya()
            p.add_term(Term(orig_jhal, 'dhatu'))
            p.add_term(Term('Da', 'pratyaya'))
            jhalam_jas_jhasi(p)
            self.assertEqual(p.terms[0].text, orig_jhal[:-1] + expected_jas)

    def test_tasthasthamipam_branches(self) -> None:
        for orig, expected in[('tas', 'tAm'), ('Ta', 'ta'), ('mip', 'am')]:
            p = Prakriya()
            lak = Term('laN', 'lakara')
            lak.tags.add('laN')
            p.add_term(lak)
            p.add_term(Term(orig, 'pratyaya'))
            tasthasthamipam(p)
            self.assertEqual(p.terms[1].text, expected)

    def test_yuvor_anakau_vu(self) -> None:
        p = Prakriya()
        p.add_term(Term('vu', 'pratyaya'))
        yuvor_anakau(p)
        self.assertEqual(p.terms[0].text, 'aka')

    def test_dhatvadeh_sah_sah_branches(self) -> None:
        """Covers initial z and R substitutions"""
        mappings =[('zWA', 'sTA'), ('zRA', 'snA'), ('zva', 'sva'), ('RI', 'nI')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            dhatvadeh_sah_sah_no_nah(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_rashabhyam_blocking(self) -> None:
        """Tests that Natva Sandhi is properly blocked by specific consonants"""
        # 'r' followed by 'm' (labial) allows 'n' -> 'R'
        p1 = Prakriya()
        p1.add_term(Term('ramana', 'pratyaya'))
        rashabhyam_no_nah(p1)
        self.assertEqual(p1.terms[0].text, 'ramaRa')
        
        # 'r' followed by 'c' (palatal) blocks 'n' -> 'R'!
        p2 = Prakriya()
        p2.add_term(Term('racana', 'pratyaya'))
        rashabhyam_no_nah(p2)
        self.assertEqual(p2.terms[0].text, 'racana')

    def test_sna_sandhi_branches(self) -> None:
        """Covers all 3 states of the Gana 9 'SnA' infix"""
        # 1. Pit affix (strong) -> stays nA
        p1 = Prakriya()
        p1.add_term(Term('nA', 'vikaraRa'))
        suf1 = Term('ti', 'pratyaya')
        suf1.tags.add('pit')
        p1.add_term(suf1)
        sna_sandhi(p1)
        self.assertEqual(p1.terms[0].text, 'nA')

        # 2. Apit vowel (weak) -> n
        p2 = Prakriya()
        p2.add_term(Term('nA', 'vikaraRa'))
        p2.add_term(Term('anti', 'pratyaya'))
        sna_sandhi(p2)
        self.assertEqual(p2.terms[0].text, 'n')

        # 3. Apit consonant (weak) -> nI
        p3 = Prakriya()
        p3.add_term(Term('nA', 'vikaraRa'))
        p3.add_term(Term('tas', 'pratyaya'))
        sna_sandhi(p3)
        self.assertEqual(p3.terms[0].text, 'nI')

    def test_upasarga_satva_stutva(self) -> None:
        """Tests prati + sTA -> pratizWA"""
        p = Prakriya()
        p.add_term(Term('prati', 'upasarga'))
        p.add_term(Term('sTA', 'dhatu'))
        upasarga_satva(p)
        self.assertEqual(p.terms[1].text, 'zWA')

if __name__ == '__main__':
    unittest.main()