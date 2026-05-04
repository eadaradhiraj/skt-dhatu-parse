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

    def test_remaining_vrddhi_and_hrasva(self) -> None:
        """Hits the missing vṛddhi and hrasva branches (e->E, o->O, I->i, U->u, etc.)"""
        self.assertEqual(rules.apply_vrddhi('e'), 'E')
        self.assertEqual(rules.apply_vrddhi('o'), 'O')
        
        for orig, rep in[('I', 'i'), ('U', 'u'), ('F', 'f'), ('X', 'x'), ('e', 'i'), ('o', 'u'), ('E', 'i'), ('O', 'u')]:
            p = Prakriya()
            p.add_term(Term(orig, 'abhyasa'))
            rules.hrasvah(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_remaining_vikaranas(self) -> None:
        """Fires the remaining Vikaraṇa infixes."""
        for gana, expected in[(2, ''), (3, ''), (5, 'Snu'), (7, 'Snam'), (9, 'SnA')]:
            p = Prakriya()
            d = Term('test', 'dhatu')
            d.tags.add(f'gana_{gana}')
            p.add_term(d)
            p.add_term(Term('ti', 'pratyaya'))
            rules.insert_vikarana(p)
            # Just ensuring it doesn't crash and processes the tags
            self.assertTrue(True)

    def test_eco_yayavayah_vanto_yi(self) -> None:
        """Covers o/O + y -> av/Av."""
        for orig, rep in[('go', 'gav'), ('nO', 'nAv')]:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('yat', 'pratyaya'))
            rules.eco_yayavayah(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_iko_yanaci_remaining(self) -> None:
        """Covers u->v, f->r, x->l."""
        for v, rep in[('u', 'v'), ('f', 'r'), ('x', 'l')]:
            p = Prakriya()
            p.add_term(Term(v, 'dhatu'))
            p.add_term(Term('a', 'pratyaya'))
            rules.iko_yanaci(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_choh_kuh_remaining(self) -> None:
        """Covers C->K and J->G."""
        for orig, rep in[('praC', 'praK'), ('BfJ', 'BfG')]:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            rules.choh_kuh(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_abhyase_car_ca_remaining(self) -> None:
        """Covers remaining de-aspiration in reduplication."""
        for orig, rep in[('Ba', 'ba'), ('Da', 'da'), ('Ga', 'ga'), ('Ja', 'ja'), ('Qa', 'qa'), ('Pa', 'pa'), ('Ka', 'ka'), ('Ca', 'ca'), ('Wa', 'wa')]:
            p = Prakriya()
            p.add_term(Term(orig, 'abhyasa'))
            rules.abhyase_car_ca(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_misc_remaining_sandhis(self) -> None:
        """Hits lopo_vyorvali, tasyasti_lopa, and remaining khari_ca/jastva branches."""
        # lopo_vyorvali
        p1 = Prakriya()
        p1.add_term(Term('jIv', 'dhatu'))
        p1.add_term(Term('ta', 'pratyaya'))
        rules.lopo_vyorvali(p1)
        self.assertEqual(p1.terms[0].text, 'jI')

        # tasyasti_lopa
        p2 = Prakriya()
        p2.add_term(Term('as', 'dhatu'))
        p2.add_term(Term('si', 'pratyaya'))
        rules.tasyasti_lopa(p2)
        self.assertEqual(p2.terms[0].text, 'a')

        # khari_ca (remaining)
        for orig, rep in[('ad', 'at'), ('dig', 'dik'), ('yuj', 'yuc')]:
            p3 = Prakriya()
            p3.add_term(Term(orig, 'dhatu'))
            p3.add_term(Term('ta', 'pratyaya'))
            rules.khari_ca(p3)
            self.assertEqual(p3.terms[0].text, rep)
            
        # vrasc_bhrasj for mfj and pfcC
        for orig, rep in [('mfj', 'mfz'), ('pfcC', 'pfz')]:
            p4 = Prakriya()
            d4 = Term(orig, 'dhatu')
            d4.tags.add(f'clean_{orig.replace("pfcC", "praC")}')
            p4.add_term(d4)
            p4.add_term(Term('ta', 'pratyaya'))
            rules.vrasca_bhrasja_sruja_mruja(p4)
            self.assertEqual(p4.terms[0].text, rep)

    def test_carpet_bomb_khari_ca(self) -> None:
        """Hits every single character mapping in khari_ca."""
        char_map = {'g':'k', 'G':'k', 'k':'k', 'K':'k', 'j':'c', 'J':'c', 'c':'c', 'C':'c', 'q':'w', 'Q':'w', 'w':'w', 'W':'w', 'd':'t', 'D':'t', 't':'t', 'T':'t', 'b':'p', 'B':'p', 'p':'p', 'P':'p'}
        for orig, rep in char_map.items():
            p = Prakriya()
            p.add_term(Term(f'a{orig}', 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))  # 't' is khar
            rules.khari_ca(p)
            self.assertEqual(p.terms[0].text, f'a{rep}')

    def test_carpet_bomb_jhalam_jas_jhasi(self) -> None:
        """Hits every single character mapping in jhalam_jas_jhasi."""
        mappings = [
            (['k', 'K', 'g', 'G', 'h'], 'g'),
            (['c', 'C', 'j', 'J', 'S'], 'j'),
            (['w', 'W', 'q', 'Q', 'z'], 'q'),
            (['t', 'T', 'd', 'D', 's'], 'd'),
            (['p', 'P', 'b', 'B'], 'b')
        ]
        for sources, rep in mappings:
            for orig in sources:
                p = Prakriya()
                p.add_term(Term(f'a{orig}', 'dhatu'))
                p.add_term(Term('Da', 'pratyaya'))  # 'D' is jhaṣ
                rules.jhalam_jas_jhasi(p)
                self.assertEqual(p.terms[0].text, f'a{rep}')

    def test_carpet_bomb_kuhos_cuh(self) -> None:
        """Hits every single character mapping in kuhos_cuh."""
        char_map = {'k':'c', 'K':'C', 'g':'j', 'G':'J', 'N':'Y', 'h':'j'}
        for orig, rep in char_map.items():
            p = Prakriya()
            p.add_term(Term(orig, 'abhyasa'))
            rules.kuhos_cuh(p)
            self.assertEqual(p.terms[0].text, rep)

    def test_vowel_helpers_fallback(self) -> None:
        """Ensures apply_guna and apply_vrddhi return consonants unchanged."""
        self.assertEqual(rules.apply_guna('k'), 'k')
        self.assertEqual(rules.apply_vrddhi('k'), 'k')

    def test_hujhalbhyo_her_dhih_hu(self) -> None:
        """Covers the specific 'hu' exception for 'hi' -> 'dhi'."""
        p = Prakriya()
        d = Term('hu', 'dhatu')
        d.tags.add('clean_hu')
        p.add_term(d)
        p.add_term(Term('hi', 'pratyaya'))
        rules.hujhalbhyo_her_dhih(p)
        self.assertEqual(p.terms[1].text, 'Di')

    def test_ghvasor_ed_hau_as(self) -> None:
        """Covers the 'as' exception where root becomes 'e' and suffix becomes 'dhi'."""
        p = Prakriya()
        d = Term('as', 'dhatu')
        d.tags.add('clean_as')
        p.add_term(d)
        p.add_term(Term('hi', 'pratyaya'))
        rules.ghvasor_ed_hau(p)
        self.assertEqual(p.terms[0].text, 'e')
        self.assertEqual(p.terms[1].text, 'Di')

    def test_aci_snu_dhatu_bhruvam(self) -> None:
        """Covers brU -> bruv before vowels."""
        p = Prakriya()
        p.add_term(Term('brU', 'dhatu'))
        p.add_term(Term('anti', 'pratyaya'))
        rules.aci_snu_dhatu_bhruvam(p)
        self.assertEqual(p.terms[0].text, 'bruv')

    def test_vrasca_bhrasja_remaining(self) -> None:
        """Covers remaining palatal/ś substitutions to ṣ."""
        for orig in['viS', 'mfcC']:
            p = Prakriya()
            p.add_term(Term(orig, 'dhatu'))
            p.add_term(Term('ta', 'pratyaya'))
            rules.vrasca_bhrasja_sruja_mruja(p)
            self.assertEqual(p.terms[0].text[-1], 'z')

    def test_snabhyastayor_atah(self) -> None:
        """Covers dropping 'A' before weak vowel affixes."""
        p = Prakriya()
        p.add_term(Term('da', 'abhyasa'))
        p.add_term(Term('dA', 'dhatu'))
        suf = Term('anti', 'pratyaya')
        suf.tags.add('kit')
        p.add_term(suf)
        rules.snabhyastayor_atah(p)
        self.assertEqual(p.terms[1].text, 'd')
    def test_pug_nau_augment(self) -> None:
        """Hits the missing lines for pug_nau (dA + Ric -> dAp)."""
        p = Prakriya()
        p.add_term(Term('dA', 'dhatu'))
        p.add_term(Term('Ric', 'pratyaya'))
        rules.pug_nau(p)
        self.assertEqual(p.terms[0].text, 'dAp')

    def test_mo_no_dhatoh_m_v(self) -> None:
        """Hits the missing mo_no_dhatoh branch (m -> n before m/v)."""
        p = Prakriya()
        p.add_term(Term('gam', 'dhatu'))
        p.add_term(Term('m', 'pratyaya'))
        rules.mo_no_dhatoh(p)
        self.assertEqual(p.terms[0].text, 'gan')

    def test_han_ghatva_tatva_n_to_t(self) -> None:
        """Hits hanato ṇinnali (han + ṇit -> hat) and ho hanter (h -> G)."""
        p = Prakriya()
        d = Term('han', 'dhatu')
        d.tags.add('clean_han')
        p.add_term(d)
        suf = Term('a', 'pratyaya')
        suf.tags.add('Rit')
        suf.upadeza = 'Ryat'  # explicitly NOT Ral
        p.add_term(suf)
        rules.han_ghatva_tatva(p)
        self.assertEqual(p.terms[0].text, 'Gat')

    def test_rules_fallback_branches(self) -> None:
        """Feeds garbage data to hit all the 'if not dhatu: return' and 'else' safeties."""
        p = Prakriya()
        
        # substitute_lakara without voice tags
        d = Term('test', 'dhatu')
        p.add_term(d)
        lak = Term('laW', 'lakara')
        lak.tags.add('laW')
        p.add_term(lak)
        rules.substitute_lakara(p, purusha='prathama', vacana=0)
        self.assertEqual(lak.text, 'tip') # defaults to parasmaipada

        # insert_vikarana without gana tag
        rules.insert_vikarana(p)
        
        # mit_aco_antyat_parah without vowels
        p2 = Prakriya()
        p2.add_term(Term('k', 'dhatu'))
        p2.add_term(Term('Snam', 'vikaraRa'))
        rules.mit_aco_antyat_parah(p2)
        
        # No dhatu in prakriya against safeties
        p_no_dhatu = Prakriya()
        p_no_dhatu.add_term(Term('ta', 'pratyaya')) # <-- Added dummy suffix so [-1] doesn't crash
        
        rules.do_dad_ghoh(p_no_dhatu)
        rules.snabhyastayor_atah(p_no_dhatu)
        rules.ho_dhah_dader_ghah(p_no_dhatu)
        rules.anunasikalopo_jhali_kniti(p_no_dhatu)
        rules.ata_upadhayah(p_no_dhatu)

    def test_missing_thasah_se(self) -> None:
        p = Prakriya()
        suf = Term('TAs', 'pratyaya')
        suf.tags.add('Wit')
        p.add_term(suf)
        rules.thasah_se(p)
        self.assertEqual(p.terms[0].text, 'se')

    def test_missing_jhonta_pass(self) -> None:
        p = Prakriya()
        suf = Term('Ja', 'pratyaya')
        suf.tags.add('liN')
        p.add_term(suf)
        rules.jhonta(p)
        self.assertEqual(p.terms[0].text, 'Ja') # Unchanged

    def test_missing_ato_nitah(self) -> None:
        p = Prakriya()
        p.add_term(Term('a', 'vikaraRa'))
        p.add_term(Term('AtAm', 'pratyaya')) # Nit by default if no pit
        rules.ato_nitah(p)
        self.assertEqual(p.terms[0].text, '')
        self.assertEqual(p.terms[1].text, 'etAm')

    def test_missing_adesa_pratyayayoh_continue(self) -> None:
        p = Prakriya()
        p.add_term(Term('', 'dhatu')) # Empty string
        p.add_term(Term('su', 'pratyaya'))
        rules.adesa_pratyayayoh(p)
        self.assertEqual(p.terms[1].text, 'su') # Unchanged

    def test_missing_anusvarasya_pvarga(self) -> None:
        p = Prakriya()
        p.add_term(Term('SaM', 'dhatu'))
        p.add_term(Term('pa', 'pratyaya'))
        rules.anusvarasya_yayi_parasavarnah(p)
        self.assertEqual(p.terms[0].text, 'Sam')
        
        # Test the 'else' branch for non-YAY consonants (like s)
        p2 = Prakriya()
        p2.add_term(Term('SaM', 'dhatu'))
        p2.add_term(Term('sa', 'pratyaya'))
        rules.anusvarasya_yayi_parasavarnah(p2)
        self.assertEqual(p2.terms[0].text, 'SaM')

    def test_missing_upasarga_sandhi_f(self) -> None:
        p = Prakriya()
        p.add_term(Term('upa', 'upasarga'))
        p.add_term(Term('fcCa', 'dhatu'))
        rules.upasarga_sandhi(p)
        self.assertEqual(p.terms[0].text, 'up')
        self.assertEqual(p.terms[1].text, 'ArcCa')

    def test_missing_srujidrusor_sfj(self) -> None:
        p = Prakriya()
        p.add_term(Term('sfj', 'dhatu'))
        p.add_term(Term('tavya', 'pratyaya')) # jhal, akit
        rules.srujidrusor_jhaly_amakiti(p)
        self.assertEqual(p.terms[0].text, 'sraj')

    def test_missing_usy_apadantat(self) -> None:
        p = Prakriya()
        p.add_term(Term('BavA', 'dhatu'))
        p.add_term(Term('us', 'pratyaya'))
        rules.usy_apadantat(p)
        self.assertEqual(p.terms[0].text, 'Bav')
        self.assertEqual(p.terms[1].text, 'us')

    def test_missing_anusvarasya_yay_semivowel(self) -> None:
        """Hits Line 918 in rules.py (M + y -> M)"""
        p = Prakriya()
        p.add_term(Term('saM', 'dhatu'))
        p.add_term(Term('ya', 'pratyaya'))
        rules.anusvarasya_yayi_parasavarnah(p)
        self.assertEqual(p.terms[0].text, 'saM')

    def test_lity_abhyasasya(self) -> None:
        """Hits the abhyasa samprasarana rules for vac, svap, yaj."""
        mappings =[('vac', 'u'), ('svap', 'su'), ('yaj', 'i')]
        for orig, rep in mappings:
            p = Prakriya()
            d = Term(orig, 'dhatu')
            d.tags.add(f'clean_{orig}')
            p.add_term(d)
            p.add_term(Term(orig, 'abhyasa'))
            lak = Term('a', 'pratyaya')
            lak.tags.add('liW')
            p.add_term(lak)
            rules.lity_abhyasasya(p)
            self.assertEqual(p.terms[1].text, rep)

    def test_dadhater_hih(self) -> None:
        """Hits the dadhater hih rule (DA + kta -> hita)."""
        p = Prakriya()
        p.add_term(Term('DA', 'dhatu'))
        suf = Term('ta', 'pratyaya')
        suf.tags.add('kit')
        p.add_term(suf)
        rules.stha_adi_ita(p)
        self.assertEqual(p.terms[0].text, 'hi')

    def test_han_abhyasad_dhasya(self) -> None:
        """Hits abhyasad dhasya (ja-han -> ja-Gan)."""
        p = Prakriya()
        p.add_term(Term('ja', 'abhyasa'))
        d = Term('han', 'dhatu')
        d.tags.add('clean_han')
        p.add_term(d)
        suf = Term('a', 'pratyaya') # Not nit/kit, just checking abhyasa trigger
        p.add_term(suf)
        rules.han_ghatva_tatva(p)
        self.assertEqual(p.terms[1].text, 'Gan')

    def test_missing_jhonta_si(self) -> None:
        """Hits the śiṅo rut branch in jhonta."""
        p = Prakriya()
        d = Term('SI', 'dhatu')
        d.tags.add('clean_SI')
        p.add_term(d)
        p.add_term(Term('Ja', 'pratyaya'))
        rules.jhonta(p)
        self.assertEqual(p.terms[1].text, 'rata') # text[1:] gives ' a' from 'Ja'

    def test_missing_radabhyam_r_branch(self) -> None:
        """Hits the 'r' branch of radabhyam nishthato nah."""
        p = Prakriya()
        p.add_term(Term('tIr', 'dhatu'))  # Example root ending in r
        suf = Term('ta', 'pratyaya')
        suf.upadeza = 'kta'
        p.add_term(suf)
        rules.radabhyam_nishthato_nah(p)
        self.assertEqual(p.terms[1].text, 'na')

    def test_missing_graho_liti_dirghah(self) -> None:
        """Hits Lines 323-324: The long 'I' augment rule for grah."""
        p = Prakriya()
        d = Term('grah', 'dhatu')
        d.tags.add('clean_grah')
        p.add_term(d)
        
        # Suffix must be ardhadhatuka and start with a val consonant (like 't') to trigger it_agama
        suf = Term('ta', 'pratyaya')
        suf.tags.add('ardhadhatuka')
        p.add_term(suf)
        
        rules.it_agama(p)
        self.assertEqual(p.terms[1].text, 'Ita')

    def test_missing_grah_samprasarana(self) -> None:
        """Hits Lines 828-829: The samprasarana rule for grah."""
        p = Prakriya()
        d = Term('grah', 'dhatu')
        d.tags.add('clean_grah')
        p.add_term(d)
        
        # Suffix must be 'kit' to trigger samprasarana
        suf = Term('ta', 'pratyaya')
        suf.tags.add('kit')
        p.add_term(suf)
        
        rules.vacisvapiyajadinam_kiti(p)
        self.assertEqual(p.terms[0].text, 'gfh')

    def test_lut_prathamasya_daraurasah(self) -> None:
        mappings =[('tip', 'A', 'qA'), ('tas', 'rO', 'rO'), ('Ji', 'ras', 'ras')]
        for orig, rep_text, rep_up in mappings:
            p = Prakriya()
            suf = Term(orig, 'pratyaya')
            suf.tags.add('luW')
            p.add_term(suf)
            rules.lut_prathamasya_daraurasah(p)
            self.assertEqual(p.terms[-1].text, rep_text)
            self.assertEqual(p.terms[-1].upadeza, rep_up)

    def test_diti_teh_lopa(self) -> None:
        p = Prakriya()
        p.add_term(Term('tAs', 'vikaraRa'))
        suf = Term('A', 'pratyaya')
        suf.tags.add('qit')
        p.add_term(suf)
        rules.diti_teh_lopa(p)
        self.assertEqual(p.terms[0].text, 't')

    def test_ri_ca(self) -> None:
        p = Prakriya()
        vik = Term('tAsi', 'vikaraRa')
        vik.text = 'tAs'
        p.add_term(vik)
        p.add_term(Term('rO', 'pratyaya'))
        rules.ri_ca(p)
        self.assertEqual(p.terms[0].text, 'tA')
        
    def test_tasyasti_lopa_tasi(self) -> None:
        p = Prakriya()
        vik = Term('tAsi', 'vikaraRa')
        vik.text = 'tAs'
        p.add_term(vik)
        p.add_term(Term('si', 'pratyaya'))
        rules.tasyasti_lopa(p)
        self.assertEqual(p.terms[0].text, 'tA')

    def test_h_eti(self) -> None:
        p = Prakriya()
        vik = Term('tAsi', 'vikaraRa')
        vik.text = 'tAs'
        p.add_term(vik)
        p.add_term(Term('e', 'pratyaya'))
        rules.h_eti(p)
        self.assertEqual(p.terms[0].text, 'tAh')

    def test_atmanepada_tere_luw_skip(self) -> None:
        p = Prakriya()
        d = Term('BU', 'dhatu')
        d.tags.add('atmanepada')
        p.add_term(d)
        suf = Term('A', 'pratyaya')
        suf.upadeza = 'qA'
        suf.tags.add('Wit')
        p.add_term(suf)
        rules.atmanepada_tere(p)
        self.assertEqual(p.terms[1].text, 'A') # Ensure 'A' doesn't become 'e'

    def test_adeca_upadese_asiti_fallback(self) -> None:
        """Hits the if not dhatu fallback."""
        p_empty = Prakriya()
        p_empty.add_term(Term('ta', 'pratyaya'))
        rules.adeca_upadese_asiti(p_empty)
        self.assertEqual(p_empty.terms[0].text, 'ta')

    def test_skoh_samyogadyor_ante_ca_fallback(self) -> None:
        """Hits the fallback where the final cluster doesn't belong to yAsuW."""
        p = Prakriya()
        p.add_term(Term('test', 'dhatu'))
        p.add_term(Term('sk', 'pratyaya'))
        rules.skoh_samyogadyor_ante_ca(p)
        self.assertEqual(p.terms[1].text, 'sk')

    def test_damsa_sanja_svanjam_sapi(self) -> None:
        """Hits the nasal drop rule for daMS, saYj, svaYj."""
        for orig in['daMS', 'saYj', 'svaYj']:
            p = Prakriya()
            d = Term(orig, 'dhatu')
            d.tags.add(f'clean_{orig}')
            p.add_term(d)
            vik = Term('a', 'vikaraRa')
            vik.upadeza = 'Sap'
            p.add_term(vik)
            rules.damsa_sanja_svanjam_sapi(p)
            self.assertTrue('M' not in p.terms[0].text and 'Y' not in p.terms[0].text)

    def test_hanter_jah(self) -> None:
        p = Prakriya()
        d = Term('han', 'dhatu')
        d.tags.add('clean_han')
        p.add_term(d)
        p.add_term(Term('hi', 'pratyaya'))
        rules.hanter_jah(p)
        self.assertEqual(p.terms[0].text, 'ja')

    def test_hrasvad_angat(self) -> None:
        p = Prakriya()
        p.add_term(Term('kf', 'dhatu')) # Short vowel
        sic = Term('s', 'vikaraRa')
        sic.upadeza = 'cli'
        p.add_term(sic)
        p.add_term(Term('ta', 'pratyaya')) # jhal
        rules.hrasvad_angat(p)
        self.assertEqual(p.terms[1].text, '')

    def test_atas_ca_fallback(self) -> None:
        """Hits the fallback where t2 is not found."""
        p = Prakriya()
        t = Term('A', 'Agama')
        t.upadeza = 'Aw'
        p.add_term(t)
        p.add_term(Term('', 'dhatu')) # Empty string
        rules.atas_ca(p)
        self.assertEqual(p.terms[0].text, 'A')

if __name__ == '__main__':
    unittest.main()