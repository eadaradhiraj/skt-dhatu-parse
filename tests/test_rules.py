import unittest
from skt_dhatu_parse.models import Term, Prakriya
from skt_dhatu_parse.rules import (
    substitute_lakara, insert_vikarana, apply_guna, apply_vrddhi,
    paghra_sthadi_adesha, upasarga_sandhi, jhalam_jas_jhasi, 
    jhasas_tathor_dho_dhah, tasthasthamipam, yuvor_anakau
)

class TestRules(unittest.TestCase):

    def test_vowel_helpers(self) -> None:
        """Covers all branches of apply_guna and apply_vrddhi"""
        self.assertEqual(apply_guna('i'), 'e')
        self.assertEqual(apply_guna('u'), 'o')
        self.assertEqual(apply_guna('f'), 'ar')
        self.assertEqual(apply_guna('x'), 'al')
        self.assertEqual(apply_guna('a'), 'a') # Fallback

        self.assertEqual(apply_vrddhi('a'), 'A')
        self.assertEqual(apply_vrddhi('i'), 'E')
        self.assertEqual(apply_vrddhi('u'), 'O')
        self.assertEqual(apply_vrddhi('f'), 'Ar')
        self.assertEqual(apply_vrddhi('x'), 'Al')
        self.assertEqual(apply_vrddhi('k'), 'k') # Fallback

    def test_paghra_sthadi_adesha(self) -> None:
        """Covers all the stem replacements (pA -> piba, etc.)"""
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
        """Covers a+A, a+i, a+u, i+a, u+a sandhis"""
        tests =[
            ('upa', 'A', 'up', 'A'), # a + A -> A (Fixed!)
            ('upa', 'i', 'up', 'e'), # a + i -> e (Fixed!)
            ('upa', 'u', 'up', 'o'), # a + u -> o (Fixed!)
            ('vi', 'a', 'vy', 'a'),  # i -> y
            ('su', 'a', 'sv', 'a')   # u -> v
        ]
        for upa, aug, exp_upa, exp_aug in tests:
            p = Prakriya()
            p.add_term(Term(upa, 'upasarga'))
            p.add_term(Term(aug, 'Agama'))
            upasarga_sandhi(p)
            self.assertEqual(p.terms[0].text, exp_upa)
            self.assertEqual(p.terms[1].text, exp_aug)

    def test_consonant_sandhi_branches(self) -> None:
        """Covers all Jas sandhi mappings and T -> D"""
        p = Prakriya()
        p.add_term(Term('buD', 'dhatu'))
        p.add_term(Term('Ta', 'pratyaya')) # Fixed: 'Ta' is SLP1 for 'tha'
        jhasas_tathor_dho_dhah(p)
        self.assertEqual(p.terms[1].text, 'Da') # Ta -> Da

        mappings =[('vak', 'g'), ('vac', 'j'), ('vaw', 'q'), ('vap', 'b')]
        for orig_jhal, expected_jas in mappings:
            p = Prakriya()
            p.add_term(Term(orig_jhal, 'dhatu'))
            p.add_term(Term('Da', 'pratyaya'))
            jhalam_jas_jhasi(p)
            self.assertEqual(p.terms[0].text, orig_jhal[:-1] + expected_jas)

    def test_tasthasthamipam_branches(self) -> None:
        """Covers the remaining past tense suffix replacements"""
        # Fixed: 'Ta' is SLP1 for 'tha'
        for orig, expected in[('tas', 'tAm'), ('Ta', 'ta'), ('mip', 'am')]:
            p = Prakriya()
            lak = Term('laN', 'lakara')
            lak.tags.add('laN')
            p.add_term(lak)
            p.add_term(Term(orig, 'pratyaya'))
            tasthasthamipam(p)
            self.assertEqual(p.terms[1].text, expected)

    def test_yuvor_anakau_vu(self) -> None:
        """Covers vu -> aka"""
        p = Prakriya()
        p.add_term(Term('vu', 'pratyaya'))
        yuvor_anakau(p)
        self.assertEqual(p.terms[0].text, 'aka')

if __name__ == '__main__':
    unittest.main()