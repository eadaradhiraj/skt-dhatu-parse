import unittest
from skt_dhatu_parse.models import Term, Prakriya
from skt_dhatu_parse.rules import (
    apply_guna, apply_vrddhi, paghra_sthadi_adesha, upasarga_sandhi, 
    jhalam_jas_jhasi, jhasas_tathor_dho_dhah, tasthasthamipam, yuvor_anakau,
    dhatvadeh_sah_sah_no_nah, rashabhyam_no_nah, sna_sandhi, upasarga_satva,
    anunasikalopo_jhali_kniti, vacisvapiyajadinam_kiti, choh_kuh, radabhyam_nishthato_nah,
    vrasca_bhrasja_sruja_mruja, stuna_stuh, nascapadantasya_jhali,
    ho_dhah_dader_ghah, ur_at, srujidrusor_jhaly_amakiti, kr_u_morphing, vikarana_guna,
    sarvadhatuka_ardhadhatukayoh, kuhos_cuh, stha_adi_ita, ato_yuk, id_yati, akah_savarne_dirghah
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
        mappings = [
            ('pA', 'piba'), ('GrA', 'jiGra'), ('DmA', 'Dama'), 
            ('mnA', 'mana'), ('dfS', 'pazya'), ('f', 'fcCa'), 
            ('sf', 'DAva'), ('Sad', 'zIya'), ('sad', 'sIda'),
            ('gam', 'gacCa'), ('yam', 'yacCa'), ('iz', 'icCa')
        ]
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
        for orig, expected in [('tas', 'tAm'), ('Ta', 'ta'), ('mip', 'am')]:
            p = Prakriya()
            # The engine fuses the lakara and suffix into one term
            suf = Term(orig, 'pratyaya')
            suf.tags.add('laN') 
            p.add_term(suf)
            tasthasthamipam(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_yuvor_anakau_vu(self) -> None:
        p = Prakriya()
        p.add_term(Term('vu', 'pratyaya'))
        yuvor_anakau(p)
        self.assertEqual(p.terms[0].text, 'aka')

    def test_dhatvadeh_sah_sah_branches(self) -> None:
        mappings =[('zWA', 'sTA'), ('zRA', 'snA'), ('zva', 'sva'), ('RI', 'nI')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            dhatvadeh_sah_sah_no_nah(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_rashabhyam_blocking(self) -> None:
        p1 = Prakriya()
        p1.add_term(Term('ramana', 'pratyaya'))
        rashabhyam_no_nah(p1)
        self.assertEqual(p1.terms[0].text, 'ramaRa')
        
        p2 = Prakriya()
        p2.add_term(Term('racana', 'pratyaya'))
        rashabhyam_no_nah(p2)
        self.assertEqual(p2.terms[0].text, 'racana')

    def test_sna_sandhi_branches(self) -> None:
        p1 = Prakriya()
        p1.add_term(Term('nA', 'vikaraRa'))
        suf1 = Term('ti', 'pratyaya')
        suf1.tags.add('pit')
        p1.add_term(suf1)
        sna_sandhi(p1)
        self.assertEqual(p1.terms[0].text, 'nA')

        p2 = Prakriya()
        p2.add_term(Term('nA', 'vikaraRa'))
        p2.add_term(Term('anti', 'pratyaya'))
        sna_sandhi(p2)
        self.assertEqual(p2.terms[0].text, 'n')

        p3 = Prakriya()
        p3.add_term(Term('nA', 'vikaraRa'))
        p3.add_term(Term('tas', 'pratyaya'))
        sna_sandhi(p3)
        self.assertEqual(p3.terms[0].text, 'nI')

    def test_upasarga_satva_stutva(self) -> None:
        p = Prakriya()
        p.add_term(Term('prati', 'upasarga'))
        p.add_term(Term('sTA', 'dhatu'))
        upasarga_satva(p)
        self.assertEqual(p.terms[1].text, 'zWA')

    # ==========================================
    # NEW TESTS (KRDANTA SPECIFIC RULES)
    # ==========================================

    def test_anunasikalopo_jhali_kniti(self) -> None:
        """Covers dropping 'm' and 'n' before jhal kit/Nit affixes."""
        p = Prakriya()
        p.add_term(Term('ram', 'dhatu'))
        suf = Term('tvA', 'pratyaya')
        suf.tags.add('kit')
        p.add_term(suf)
        anunasikalopo_jhali_kniti(p)
        self.assertEqual(p.terms[0].text, 'ra')

    def test_vacisvapiyajadinam_kiti(self) -> None:
        """Covers samprasarana for vac, svap, yaj."""
        mappings =[('vac', 'uc'), ('svap', 'sup'), ('yaj', 'ij')]
        for orig, sampras in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            suf = Term('ta', 'pratyaya')
            suf.tags.add('kit')
            p.add_term(suf)
            vacisvapiyajadinam_kiti(p)
            self.assertEqual(p.terms[0].text, sampras)

    def test_choh_kuh(self) -> None:
        """Covers palatal to velar (c->k, j->g) before jhal."""
        mappings =[('uc', 'uk'), ('ij', 'ig')]
        for orig, kuvarga in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            choh_kuh(p)
            self.assertEqual(p.terms[0].text, kuvarga)

    def test_radabhyam_nishthato_nah(self) -> None:
        """Covers d/r + ta -> n + na."""
        p = Prakriya()
        p.add_term(Term('Cid', 'dhatu'))
        
        # FIXED: Initialize with 'kta' as upadesa, then artificially set text to 'ta' 
        # to simulate what anubandha.py would do!
        suf = Term('kta', 'pratyaya')
        suf.text = 'ta'
        p.add_term(suf)
        
        radabhyam_nishthato_nah(p)
        self.assertEqual(p.terms[0].text, 'Cin')
        self.assertEqual(p.terms[1].text, 'na')

    # In tests/test_rules.py:
    def test_ho_dhah_dader_ghah(self) -> None:
        # Test 1: d-initial (duh -> duG)
        p1 = Prakriya()
        p1.add_term(Term('duh', 'dhatu'))
        p1.add_term(Term('ta', 'pratyaya'))
        ho_dhah_dader_ghah(p1)
        self.assertEqual(p1.terms[0].text, 'duG')
        
        # Test 2: non-d-initial (lih -> liQ)
        p2 = Prakriya()
        p2.add_term(Term('lih', 'dhatu'))
        p2.add_term(Term('ta', 'pratyaya'))
        ho_dhah_dader_ghah(p2)
        self.assertEqual(p2.terms[0].text, 'liQ')

    def test_vrasca_bhrasja_sruja_mruja(self) -> None:
        """Covers palatal to retroflex (j -> z) before jhal."""
        for root in['sfj', 'dfS', 'praC']:
            p = Prakriya()
            p.add_term(Term('sfj', 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            vrasca_bhrasja_sruja_mruja(p)
            self.assertEqual(p.terms[0].text, 'sfz')

    def test_stuna_stuh(self) -> None:
        """Covers dental to retroflex (t/th -> w/W) after retroflex."""
        p1 = Prakriya()
        p1.add_term(Term('sfz', 'dhatu'))
        p1.add_term(Term('ta', 'pratyaya'))
        stuna_stuh(p1)
        self.assertEqual(p1.terms[1].text, 'wa')

        p2 = Prakriya()
        p2.add_term(Term('sfz', 'dhatu'))
        p2.add_term(Term('Ta', 'pratyaya')) # 'Ta' is SLP1 for 'tha'
        stuna_stuh(p2)
        self.assertEqual(p2.terms[1].text, 'Wa')

    def test_ur_at(self) -> None:
        p = Prakriya()
        p.add_term(Term('kf', 'abhyasa'))
        ur_at(p)
        self.assertEqual(p.terms[0].text, 'ka')

    def test_kuhos_cuh(self) -> None:
        mappings =[('ka', 'ca'), ('Ga', 'Ja'), ('ha', 'ja')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'abhyasa'))
            kuhos_cuh(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_sarvadhatuka_ardhadhatukayoh_laghupadha(self) -> None:
        p = Prakriya()
        p.add_term(Term('buD', 'dhatu'))
        suf = Term('Ric', 'pratyaya')
        suf.tags.add('ardhadhatuka')
        p.add_term(suf)
        sarvadhatuka_ardhadhatukayoh(p)
        self.assertEqual(p.terms[0].text, 'boD')

    def test_vikarana_guna(self) -> None:
        p = Prakriya()
        vik = Term('u', 'vikaraRa')
        p.add_term(vik)
        suf = Term('ti', 'pratyaya')
        suf.tags.add('pit')
        p.add_term(suf)
        vikarana_guna(p)
        self.assertEqual(vik.text, 'o')

    def test_kr_u_morphing(self) -> None:
        p = Prakriya()
        t1 = Term('qukfY', 'dhatu')
        t1.text = 'kf'
        p.add_term(t1)
        p.add_term(Term('u', 'vikaraRa'))
        p.add_term(Term('tas', 'pratyaya')) # No pit tag
        kr_u_morphing(p)
        self.assertEqual(p.terms[0].text, 'kur')
        
        p2 = Prakriya()
        t2 = Term('qukfY', 'dhatu')
        t2.text = 'kf'
        p2.add_term(t2)
        p2.add_term(Term('u', 'vikaraRa'))
        p2.add_term(Term('vas', 'pratyaya'))
        kr_u_morphing(p2)
        self.assertEqual(p2.terms[1].text, '') # u is dropped before v

    def test_srujidrusor_jhaly_amakiti(self) -> None:
        p = Prakriya()
        p.add_term(Term('dfS', 'dhatu'))
        p.add_term(Term('tavya', 'pratyaya')) # non-kit jhal affix
        srujidrusor_jhaly_amakiti(p)
        self.assertEqual(p.terms[0].text, 'draS')
        
        # Should be blocked by a 'kit' affix (like kta)
        p2 = Prakriya()
        p2.add_term(Term('dfS', 'dhatu'))
        suf = Term('ta', 'pratyaya')
        suf.tags.add('kit')
        p2.add_term(suf)
        srujidrusor_jhaly_amakiti(p2)
        self.assertEqual(p2.terms[0].text, 'dfS')

    def test_nascapadantasya_jhali(self) -> None:
        p = Prakriya()
        p.add_term(Term('gam', 'dhatu'))
        p.add_term(Term('tavya', 'pratyaya')) # 't' is jhal
        nascapadantasya_jhali(p)
        self.assertEqual(p.terms[0].text, 'gaM')

    def test_stha_adi_ita(self) -> None:
        """Covers A -> i / a substitutions for specific roots."""
        mappings =[('sTA', 'sTi'), ('pA', 'pI'), ('dA', 'dat'), ('mA', 'mi')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            suf = Term('ta', 'pratyaya')
            suf.tags.add('kit')
            p.add_term(suf)
            stha_adi_ita(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_ato_yuk(self) -> None:
        """Covers adding 'yuk' augment to A-ending roots before Nit/Yit affixes."""
        p = Prakriya()
        p.add_term(Term('dA', 'dhatu'))
        suf = Term('aka', 'pratyaya')
        suf.tags.add('Rit')
        p.add_term(suf)
        ato_yuk(p)
        self.assertEqual(p.terms[0].text, 'dAy')

    def test_id_yati(self) -> None:
        """Covers A -> e before 'yat' affix."""
        p = Prakriya()
        p.add_term(Term('dA', 'dhatu'))
        suf = Term('yat', 'pratyaya')
        p.add_term(suf)
        id_yati(p)
        self.assertEqual(p.terms[0].text, 'de')

    def test_akah_savarne_dirghah(self) -> None:
        """Covers Universal Savarna Dirgha Sandhi (Long Vowel Sandhi)."""
        tests =[
            ('sTA', 'anIya', 'sTA', 'nIya'),
            ('pari', 'iz', 'parI', 'z'),
            ('BAnu', 'udaya', 'BAnU', 'daya')
        ]
        for t1_text, t2_text, e1, e2 in tests:
            p = Prakriya()
            p.add_term(Term(t1_text, 'dhatu'))
            p.add_term(Term(t2_text, 'pratyaya'))
            akah_savarne_dirghah(p)
            self.assertEqual(p.terms[0].text, e1)
            self.assertEqual(p.terms[1].text, e2)

if __name__ == '__main__':
    unittest.main()