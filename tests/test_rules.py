import unittest
from skt_dhatu_parse.models import Term, Prakriya
from skt_dhatu_parse import rules

class TestRules(unittest.TestCase):

    def test_vowel_helpers(self) -> None:
        self.assertEqual(rules.apply_guna('i'), 'e')
        self.assertEqual(rules.apply_guna('u'), 'o')
        self.assertEqual(rules.apply_guna('f'), 'ar')
        self.assertEqual(rules.apply_guna('x'), 'al')
        self.assertEqual(rules.apply_guna('a'), 'a') 

        self.assertEqual(rules.apply_vrddhi('a'), 'A')
        self.assertEqual(rules.apply_vrddhi('i'), 'E')
        self.assertEqual(rules.apply_vrddhi('u'), 'O')
        self.assertEqual(rules.apply_vrddhi('f'), 'Ar')
        self.assertEqual(rules.apply_vrddhi('x'), 'Al')
        self.assertEqual(rules.apply_vrddhi('k'), 'k') 

    def test_paghra_sthadi_adesha(self) -> None:
        mappings =[
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
            rules.paghra_sthadi_adesha(p)
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
            rules.upasarga_sandhi(p)
            self.assertEqual(p.terms[0].text, exp_upa)
            self.assertEqual(p.terms[1].text, exp_aug)

    def test_consonant_sandhi_branches(self) -> None:
        p = Prakriya()
        p.add_term(Term('buD', 'dhatu'))
        p.add_term(Term('Ta', 'pratyaya')) 
        rules.jhasas_tathor_dho_dhah(p)
        self.assertEqual(p.terms[1].text, 'Da') 

        mappings =[('vak', 'g'), ('vac', 'j'), ('vaw', 'q'), ('vap', 'b')]
        for orig_jhal, expected_jas in mappings:
            p = Prakriya()
            p.add_term(Term(orig_jhal, 'dhatu'))
            p.add_term(Term('Da', 'pratyaya'))
            rules.jhalam_jas_jhasi(p)
            self.assertEqual(p.terms[0].text, orig_jhal[:-1] + expected_jas)

    def test_tasthasthamipam_branches(self) -> None:
        for orig, expected in[('tas', 'tAm'), ('Ta', 'ta'), ('mip', 'am')]:
            p = Prakriya()
            # The engine fuses the lakara and suffix into one term
            suf = Term(orig, 'pratyaya')
            suf.tags.add('laN') 
            p.add_term(suf)
            rules.tasthasthamipam(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_yuvor_anakau_vu(self) -> None:
        p = Prakriya()
        p.add_term(Term('vu', 'pratyaya'))
        rules.yuvor_anakau(p)
        self.assertEqual(p.terms[0].text, 'aka')

    def test_dhatvadeh_sah_sah_branches(self) -> None:
        mappings =[('zWA', 'sTA'), ('zRA', 'snA'), ('zva', 'sva'), ('RI', 'nI')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            rules.dhatvadeh_sah_sah_no_nah(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_rashabhyam_blocking(self) -> None:
        p1 = Prakriya()
        p1.add_term(Term('ramana', 'pratyaya'))
        rules.rashabhyam_no_nah(p1)
        self.assertEqual(p1.terms[0].text, 'ramaRa')
        
        p2 = Prakriya()
        p2.add_term(Term('racana', 'pratyaya'))
        rules.rashabhyam_no_nah(p2)
        self.assertEqual(p2.terms[0].text, 'racana')

    def test_sna_sandhi_branches(self) -> None:
        p1 = Prakriya()
        p1.add_term(Term('nA', 'vikaraRa'))
        suf1 = Term('ti', 'pratyaya')
        suf1.tags.add('pit')
        p1.add_term(suf1)
        rules.sna_sandhi(p1)
        self.assertEqual(p1.terms[0].text, 'nA')

        p2 = Prakriya()
        p2.add_term(Term('nA', 'vikaraRa'))
        p2.add_term(Term('anti', 'pratyaya'))
        rules.sna_sandhi(p2)
        self.assertEqual(p2.terms[0].text, 'n')

        p3 = Prakriya()
        p3.add_term(Term('nA', 'vikaraRa'))
        p3.add_term(Term('tas', 'pratyaya'))
        rules.sna_sandhi(p3)
        self.assertEqual(p3.terms[0].text, 'nI')

    def test_upasarga_satva_stutva(self) -> None:
        p = Prakriya()
        p.add_term(Term('prati', 'upasarga'))
        p.add_term(Term('sTA', 'dhatu'))
        rules.upasarga_satva(p)
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
        rules.anunasikalopo_jhali_kniti(p)
        self.assertEqual(p.terms[0].text, 'ra')

    def test_vacisvapiyajadinam_kiti(self) -> None:
        mappings =[('vac', 'uc'), ('svap', 'sup'), ('yaj', 'ij'), ('vraSc', 'vfSc'), ('praC', 'pfC'), ('Brajj', 'Bfjj')]
        for orig, sampras in mappings:
            p = Prakriya()
            d = Term(orig, 'dhatu')
            d.tags.add(f'clean_{orig}')
            p.add_term(d)
            suf = Term('ta', 'pratyaya')
            suf.tags.add('kit')
            p.add_term(suf)
            rules.vacisvapiyajadinam_kiti(p)
            self.assertEqual(p.terms[0].text, sampras)

    def test_choh_kuh(self) -> None:
        """Covers palatal to velar (c->k, j->g) before jhal."""
        mappings =[('uc', 'uk'), ('ij', 'ig')]
        for orig, kuvarga in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            rules.choh_kuh(p)
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
        
        rules.radabhyam_nishthato_nah(p)
        self.assertEqual(p.terms[0].text, 'Cin')
        self.assertEqual(p.terms[1].text, 'na')

    def test_ho_dhah_dader_ghah(self) -> None:
        # Test 1: d-initial (duh -> duG)
        p1 = Prakriya()
        p1.add_term(Term('duh', 'dhatu'))
        p1.add_term(Term('ta', 'pratyaya'))
        rules.ho_dhah_dader_ghah(p1)
        self.assertEqual(p1.terms[0].text, 'duG')
        
        # Test 2: non-d-initial (lih -> liQ)
        p2 = Prakriya()
        p2.add_term(Term('lih', 'dhatu'))
        p2.add_term(Term('ta', 'pratyaya'))
        rules.ho_dhah_dader_ghah(p2)
        self.assertEqual(p2.terms[0].text, 'liQ')

    def test_vrasca_bhrasja_sruja_mruja(self) -> None:
        """Covers palatal to retroflex (j -> z) before jhal."""
        for root in['sfj', 'dfS', 'praC']:
            p = Prakriya()
            p.add_term(Term('sfj', 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            rules.vrasca_bhrasja_sruja_mruja(p)
            self.assertEqual(p.terms[0].text, 'sfz')

    def test_stuna_stuh(self) -> None:
        """Covers dental to retroflex (t/th -> w/W) after retroflex."""
        p1 = Prakriya()
        p1.add_term(Term('sfz', 'dhatu'))
        p1.add_term(Term('ta', 'pratyaya'))
        rules.stuna_stuh(p1)
        self.assertEqual(p1.terms[1].text, 'wa')

        p2 = Prakriya()
        p2.add_term(Term('sfz', 'dhatu'))
        p2.add_term(Term('Ta', 'pratyaya')) # 'Ta' is SLP1 for 'tha'
        rules.stuna_stuh(p2)
        self.assertEqual(p2.terms[1].text, 'Wa')

    def test_ur_at(self) -> None:
        p = Prakriya()
        p.add_term(Term('kf', 'abhyasa'))
        rules.ur_at(p)
        self.assertEqual(p.terms[0].text, 'ka')

    def test_kuhos_cuh(self) -> None:
        mappings =[('ka', 'ca'), ('Ga', 'Ja'), ('ha', 'ja')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'abhyasa'))
            rules.kuhos_cuh(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_sarvadhatuka_ardhadhatukayoh_laghupadha(self) -> None:
        p = Prakriya()
        p.add_term(Term('buD', 'dhatu'))
        suf = Term('Ric', 'pratyaya')
        suf.tags.add('ardhadhatuka')
        p.add_term(suf)
        rules.sarvadhatuka_ardhadhatukayoh(p)
        self.assertEqual(p.terms[0].text, 'boD')

    def test_vikarana_guna(self) -> None:
        p = Prakriya()
        vik = Term('u', 'vikaraRa')
        p.add_term(vik)
        suf = Term('ti', 'pratyaya')
        suf.tags.add('pit')
        p.add_term(suf)
        rules.vikarana_guna(p)
        self.assertEqual(vik.text, 'o')

    def test_kr_u_morphing(self) -> None:
        p = Prakriya()
        t1 = Term('qukfY', 'dhatu')
        t1.text = 'kf'
        p.add_term(t1)
        p.add_term(Term('u', 'vikaraRa'))
        p.add_term(Term('tas', 'pratyaya')) # No pit tag
        rules.kr_u_morphing(p)
        self.assertEqual(p.terms[0].text, 'kur')
        
        p2 = Prakriya()
        t2 = Term('qukfY', 'dhatu')
        t2.text = 'kf'
        p2.add_term(t2)
        p2.add_term(Term('u', 'vikaraRa'))
        p2.add_term(Term('vas', 'pratyaya'))
        rules.kr_u_morphing(p2)
        self.assertEqual(p2.terms[1].text, '') # u is dropped before v

    def test_srujidrusor_jhaly_amakiti(self) -> None:
        p = Prakriya()
        p.add_term(Term('dfS', 'dhatu'))
        p.add_term(Term('tavya', 'pratyaya')) # non-kit jhal affix
        rules.srujidrusor_jhaly_amakiti(p)
        self.assertEqual(p.terms[0].text, 'draS')
        
        # Should be blocked by a 'kit' affix (like kta)
        p2 = Prakriya()
        p2.add_term(Term('dfS', 'dhatu'))
        suf = Term('ta', 'pratyaya')
        suf.tags.add('kit')
        p2.add_term(suf)
        rules.srujidrusor_jhaly_amakiti(p2)
        self.assertEqual(p2.terms[0].text, 'dfS')

    def test_nascapadantasya_jhali(self) -> None:
        p = Prakriya()
        p.add_term(Term('gam', 'dhatu'))
        p.add_term(Term('tavya', 'pratyaya')) # 't' is jhal
        rules.nascapadantasya_jhali(p)
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
            rules.stha_adi_ita(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_ato_yuk(self) -> None:
        """Covers adding 'yuk' augment to A-ending roots before Nit/Yit affixes."""
        p = Prakriya()
        p.add_term(Term('dA', 'dhatu'))
        suf = Term('aka', 'pratyaya')
        suf.tags.add('Rit')
        p.add_term(suf)
        rules.ato_yuk(p)
        self.assertEqual(p.terms[0].text, 'dAy')

    def test_id_yati(self) -> None:
        """Covers A -> e before 'yat' affix."""
        p = Prakriya()
        p.add_term(Term('dA', 'dhatu'))
        suf = Term('yat', 'pratyaya')
        p.add_term(suf)
        rules.id_yati(p)
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
            rules.akah_savarne_dirghah(p)
            self.assertEqual(p.terms[0].text, e1)
            self.assertEqual(p.terms[1].text, e2)

    def test_gam_hana_jana_lopa(self) -> None:
        """Covers dropping 'a' in gam/han/jan before weak vowel affixes."""
        p = Prakriya()
        dhatu = Term('han', 'dhatu')
        dhatu.tags.add('clean_han') # Required for the rule to identify the original root
        p.add_term(dhatu)
        suf = Term('anti', 'pratyaya')
        suf.tags.add('Nit')
        p.add_term(suf)
        
        rules.gam_hana_jana_lopa(p)
        self.assertEqual(p.terms[0].text, 'Gn') # 'a' dropped, 'hn' became 'Gn'

    def test_che_ca(self) -> None:
        """Covers inserting 'c' before 'C' after a short vowel."""
        p = Prakriya()
        p.add_term(Term('pfC', 'dhatu')) # Intra-term test
        rules.che_ca(p)
        self.assertEqual(p.terms[0].text, 'pfcC')
        
        p2 = Prakriya()
        p2.add_term(Term('a', 'Agama')) # Cross-term test
        p2.add_term(Term('CAdana', 'pratyaya'))
        rules.che_ca(p2)
        self.assertEqual(p2.terms[1].text, 'cCAdana')

    def test_ekaco_baso_bhas(self) -> None:
        """Covers initial aspiration shift before 's' or 'dhv' (duh -> Dhuh)."""
        p = Prakriya()
        p.add_term(Term('duG', 'dhatu')) # ho_dhah converts h -> G first
        p.add_term(Term('si', 'pratyaya'))
        rules.ekaco_baso_bhas(p)
        self.assertEqual(p.terms[0].text, 'DuG')

    def test_sadhoh_kas_si(self) -> None:
        """Covers ṣ, ḍh, gh becoming 'k' before 's'."""
        p = Prakriya()
        p.add_term(Term('DuG', 'dhatu'))
        p.add_term(Term('si', 'pratyaya'))
        rules.sadhoh_kas_si(p)
        self.assertEqual(p.terms[0].text, 'Duk')

    def test_liN_atmanepada_replacements(self) -> None:
        """Covers jhasya ran and iṭo't rules for Atmanepada Optative."""
        p1 = Prakriya()
        s1 = Term('Ja', 'pratyaya')
        s1.tags.add('liN')
        p1.add_term(s1)
        rules.jhasya_ran(p1)
        self.assertEqual(p1.terms[0].text, 'ran')
        
        p2 = Prakriya()
        s2 = Term('iw', 'pratyaya')
        s2.tags.add('liN')
        p2.add_term(s2)
        rules.ito_at(p2)
        self.assertEqual(p2.terms[0].text, 'a')

    def test_utasca_pratyayad(self) -> None:
        """Covers dropping 'hi' after an affix ending in 'u'."""
        p = Prakriya()
        p.add_term(Term('u', 'vikaraRa'))
        p.add_term(Term('hi', 'pratyaya'))
        rules.utasca_pratyayad(p)
        self.assertEqual(p.terms[1].text, '')

    def test_eco_yayavayah_ay_av(self) -> None:
        """Covers E -> Ay and O -> Av before a vowel."""
        # E -> Ay
        p1 = Prakriya()
        p1.add_term(Term('nE', 'dhatu'))
        p1.add_term(Term('aka', 'pratyaya'))
        rules.eco_yayavayah(p1)
        self.assertEqual(p1.terms[0].text, 'nAy')
        
        # O -> Av
        p2 = Prakriya()
        p2.add_term(Term('pO', 'dhatu'))
        p2.add_term(Term('aka', 'pratyaya'))
        rules.eco_yayavayah(p2)
        self.assertEqual(p2.terms[0].text, 'pAv')

    def test_khari_ca_branches(self) -> None:
        """Covers the remaining character maps in khari ca."""
        mappings =[('ad', 'at'), ('Cid', 'Cit'), ('yuB', 'yup')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('ta', 'pratyaya')) # 't' is khar
            rules.khari_ca(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_jhalam_jas_jhasi_branches(self) -> None:
        """Covers remaining character maps in jaś assimilation."""
        mappings =[('laB', 'lab'), ('kruD', 'krud'), ('praC', 'praj')]
        for orig, expected in mappings:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('Da', 'pratyaya')) # 'D' is jhaṣ
            rules.jhalam_jas_jhasi(p)
            self.assertEqual(p.terms[0].text, expected)

    def test_kramah_parasmaipadesu(self) -> None:
        p = Prakriya()
        d = Term('kram', 'dhatu')
        d.tags.add('clean_kram')
        d.tags.add('parasmaipada')
        p.add_term(d)
        vik = Term('Sap', 'vikaraRa')
        vik.tags.add('Sit')
        p.add_term(vik)
        rules.kramah_parasmaipadesu(p)
        self.assertEqual(p.terms[0].text, 'krAm')

    def test_haladi_seshah_sarpuvah(self) -> None:
        p = Prakriya()
        p.add_term(Term('sTA', 'abhyasa'))
        rules.haladi_seshah(p)
        self.assertEqual(p.terms[0].text, 'TA')

    def test_ata_au_nalah(self) -> None:
        p = Prakriya()
        p.add_term(Term('tasTA', 'dhatu'))
        suf = Term('a', 'pratyaya')
        suf.upadeza = 'Ral'
        p.add_term(suf)
        rules.ata_au_nalah(p)
        self.assertEqual(p.terms[1].text, 'O')

    def test_ghvasor_ed_hau(self) -> None:
        p = Prakriya()
        p.add_term(Term('da', 'abhyasa'))
        d = Term('d', 'dhatu') 
        d.tags.add('clean_dA')
        p.add_term(d)
        p.add_term(Term('hi', 'pratyaya'))
        rules.ghvasor_ed_hau(p)
        self.assertEqual(p.terms[1].text, 'de')
        self.assertEqual(p.terms[0].text, '')

    def test_vrddhir_eci(self) -> None:
        mappings =[('tava', 'eva', 'tavE', 'va'), ('sa', 'oDi', 'sO', 'Di')]  # <--- Corrected expectations
        for t1, t2, e1, e2 in mappings:
            p = Prakriya()
            p.add_term(Term(t1, 'dhatu'))
            p.add_term(Term(t2, 'pratyaya'))
            rules.vrddhir_eci(p)
            self.assertEqual(p.terms[0].text, e1)
            self.assertEqual(p.terms[1].text, e2)

if __name__ == '__main__':
    unittest.main()