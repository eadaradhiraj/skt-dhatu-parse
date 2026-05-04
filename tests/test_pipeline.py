import unittest
from skt_dhatu_parse.engine import derive

class TestPipeline(unittest.TestCase):

    def test_derive_akzati(self) -> None:
        prakriya = derive('akz', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'akzati')
        self.assertIn('Udit', prakriya.terms[0].tags) 
        
    def test_derive_aMhate(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aMhate')
        self.assertIn('idit', prakriya.terms[0].tags) 

    def test_bhavami(self) -> None:
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_atmanepada_uttama_singular(self) -> None:
        prakriya = derive('aMh', 'laW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aMhe')

    def test_past_tense_dual(self) -> None:
        prakriya = derive('BU', 'laN', purusha='madhyama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aBavatam')

    def test_past_tense_plural_consonant_drop(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'aBavan')

    def test_future_tense_set(self) -> None:
        prakriya = derive('BU', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Bavizyati')

    def test_future_tense_anit(self) -> None:
        prakriya = derive('ji', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jezyati')

    def test_gana_4_divyadi(self) -> None:
        prakriya = derive('div', 'laW', purusha='prathama', vacana=0, gana=4)
        self.assertEqual(prakriya.get_current_string(), 'dIvyati')

    def test_gana_6_tudadi(self) -> None:
        prakriya = derive('tud', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(prakriya.get_current_string(), 'tudati')

    def test_perfect_tense_singular(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUva')

    def test_perfect_tense_dual(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUvatuH')

    def test_perfect_tense_plural(self) -> None:
        prakriya = derive('BU', 'liW', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'baBUvuH')

    def test_invalid_roots_return_none(self) -> None:
        from skt_dhatu_parse.krdanta import derive_krdanta
        from skt_dhatu_parse.sanadi import derive_secondary_root
        self.assertIsNone(derive('xyz_invalid_root'))
        self.assertIsNone(derive_krdanta('xyz_invalid_root', 'kta'))
        self.assertIsNone(derive_secondary_root('xyz_invalid_root', 'Ric'))

    def test_gana_9_vikri_singular(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vikrIRIte')

    def test_gana_9_vikri_plural(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=2, gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vikrIRate')

    def test_dhatvadeh_and_paghra(self) -> None:
        prakriya = derive('sTA', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'tizWati')

    def test_causative_puk_and_upasarga_satva(self) -> None:
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi_prakriya = derive_secondary_root('sTA', 'Ric', gana=1)
        final_prakriya = derive('sTA', 'lfW', purusha='prathama', vacana=0, gana=1, upasargas=['prati'], custom_dhatu=sanadi_prakriya.terms[0])
        self.assertEqual(final_prakriya.get_current_string(), 'pratizWApayizyati')

    def test_multiple_upasargas(self) -> None:
        prakriya = derive('BU', 'laN', purusha='prathama', vacana=0, gana=1, upasargas=['vi', 'A'])
        self.assertEqual(prakriya.get_current_string(), 'vyABavat')

    def test_gam_lath(self) -> None:
        prakriya = derive('gam', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gacCati')

    def test_perfect_tense_path(self) -> None:
        prakriya = derive('paW', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'papAWa')

    def test_gana_8_kr_singular(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'karoti')

    def test_gana_8_kr_dual(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurutaH')

    def test_gana_8_kr_plural(self) -> None:
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=2, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurvanti')

    def test_gana_8_kr_uttama_dual(self) -> None:
        prakriya = derive('kf', 'laW', purusha='uttama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kurvaH')

    def test_perfect_tense_kr_dual(self) -> None:
        prakriya = derive('kf', 'liW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'cakratuH')

    def test_gana_2_ad(self) -> None:
        """Gaṇa 2: Suffix attaches directly. ad + ti -> atti (khari ca)."""
        prakriya = derive('ad', 'laW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'atti')

    def test_gana_2_as(self) -> None:
        """Gaṇa 2: 'as' drops 'a' before weak affixes (śnasor allopaḥ)."""
        p1 = derive('as', 'laW', purusha='prathama', vacana=0, gana=2) # Strong
        self.assertEqual(p1.get_current_string(), 'asti')
        
        p2 = derive('as', 'laW', purusha='prathama', vacana=2, gana=2) # Weak
        self.assertEqual(p2.get_current_string(), 'santi')
        
        p3 = derive('as', 'laW', purusha='uttama', vacana=0, gana=2)   # Strong
        self.assertEqual(p3.get_current_string(), 'asmi')

    def test_gana_3_hu(self) -> None:
        """Gaṇa 3: ślu elision triggers reduplication and vowel morphing."""
        p1 = derive('hu', 'laW', purusha='prathama', vacana=0, gana=3) # Strong -> Guna
        self.assertEqual(p1.get_current_string(), 'juhoti')
        
        p2 = derive('hu', 'laW', purusha='prathama', vacana=2, gana=3) # Weak -> Jh -> at + Yan
        self.assertEqual(p2.get_current_string(), 'juhvati')

    def test_gana_5_su(self) -> None:
        """Gaṇa 5: śnu augment and u-lopa morphing."""
        p1 = derive('su', 'laW', purusha='prathama', vacana=0, gana=5) # Strong -> Guna
        self.assertEqual(p1.get_current_string(), 'sunoti')
        
        p2 = derive('su', 'laW', purusha='prathama', vacana=2, gana=5) # Weak -> Yan sandhi
        self.assertEqual(p2.get_current_string(), 'sunvanti')
        
        p3 = derive('su', 'laW', purusha='uttama', vacana=1, gana=5)   # Weak -> 'u' drops before 'v'
        self.assertEqual(p3.get_current_string(), 'sunvaH')
    
    def test_imperative_lot(self) -> None:
        """Tests the generation of loW (Imperative)."""
        # Prathama: BU + tu -> Bavatu
        p1 = derive('BU', 'loW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'Bavatu')
        
        # Madhyama: BU + hi -> Bava ('hi' drops after 'a')
        p2 = derive('BU', 'loW', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p2.get_current_string(), 'Bava')
        
        # Uttama: BU + Ani -> BavAni
        p3 = derive('BU', 'loW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'BavAni')

    def test_optative_lin(self) -> None:
        """Tests the generation of liN (Optative) using yAsuW augments."""
        # Prathama Eka: Bava + iy + t -> Bavet
        p1 = derive('BU', 'liN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'Bavet')
        
        # Prathama Bahu: Bava + iy + us -> BaveyuH
        p2 = derive('BU', 'liN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p2.get_current_string(), 'BaveyuH')
        
        # Madhyama Eka: Bava + iy + s -> BaveH
        p3 = derive('BU', 'liN', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'BaveH')

    def test_aorist_lun(self) -> None:
        """Tests the luN (Aorist) past tense."""
        # sic-lopa: a + BU + s(drops) + t -> aBUt
        p1 = derive('BU', 'luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'aBUt')
        
        # puSAdi aN augment: a + gam + a(N) + t -> agamat
        p2 = derive('gam', 'luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p2.get_current_string(), 'agamat')

    def test_models_repr_and_history(self) -> None:
        """Covers the __repr__ and stdout logging in models.py"""
        from skt_dhatu_parse.models import Term, Prakriya
        import io
        import sys
        
        t = Term('BU', 'dhatu')
        repr_str = repr(t)
        self.assertTrue(repr_str.startswith("Term(text='BU'"))
        
        p = Prakriya()
        p.add_term(t)
        p.log("Test log entry")
        
        # Capture stdout to test the print statement silently
        captured_output = io.StringIO()
        sys.stdout = captured_output
        p.print_history()
        sys.stdout = sys.__stdout__
        
        self.assertIn("Test log entry", captured_output.getvalue())

    def test_gana_2_han(self) -> None:
        """Gaṇa 2: han drops 'a' and shifts to 'Gn' before weak vowel affixes."""
        p1 = derive('han', 'laW', purusha='prathama', vacana=0, gana=2) # Strong
        self.assertEqual(p1.get_current_string(), 'hanti')
        
        p2 = derive('han', 'laW', purusha='prathama', vacana=2, gana=2) # Weak + Vowel
        self.assertEqual(p2.get_current_string(), 'Gnanti')
    
    def test_optative_atmanepada(self) -> None:
        """Tests liN for Atmanepada (eDeta, eDeran)."""
        p1 = derive('eD', 'liN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'eDeta')
        
        p2 = derive('eD', 'liN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p2.get_current_string(), 'eDeran')

    def test_imperative_gana_5(self) -> None:
        """Tests loW for Gaṇa 5 (sunotu, sunu)."""
        p1 = derive('su', 'loW', purusha='prathama', vacana=0, gana=5)
        self.assertEqual(p1.get_current_string(), 'sunotu')
        
        p2 = derive('su', 'loW', purusha='madhyama', vacana=0, gana=5)
        self.assertEqual(p2.get_current_string(), 'sunu') # 'hi' drops after 'u'
        
        p3 = derive('su', 'loW', purusha='uttama', vacana=0, gana=5)
        self.assertEqual(p3.get_current_string(), 'sunavAni')

    def test_gana_2_duh(self) -> None:
        """Gaṇa 2: duh tests aspiration shifts and khari-ca/jhalam-jaś."""
        p1 = derive('duh', 'laW', purusha='prathama', vacana=0, gana=2) # dogdhi
        self.assertEqual(p1.get_current_string(), 'dogDi')
        
        p2 = derive('duh', 'laW', purusha='madhyama', vacana=0, gana=2) # dhokṣi
        self.assertEqual(p2.get_current_string(), 'Dokzi')
        
        p3 = derive('duh', 'laW', purusha='prathama', vacana=1, gana=2) # dugdhaḥ
        self.assertEqual(p3.get_current_string(), 'dugDaH')

    def test_dfS_future(self) -> None:
        """Tests dfS + lfW -> drakzyati (am augment + retroflexion + ṣaḍhoḥ kas si + ādeśa)."""
        p1 = derive('dfS', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'drakzyati')

    def test_gana_3_dA(self) -> None:
        """Gaṇa 3: dA tests do dad ghoH and Slu elision."""
        p1 = derive('dA', 'laW', purusha='prathama', vacana=0, gana=3) # Strong
        self.assertEqual(p1.get_current_string(), 'dadAti')
        
        p2 = derive('dA', 'laW', purusha='prathama', vacana=1, gana=3) # Weak cons
        self.assertEqual(p2.get_current_string(), 'dattaH')
        
        p3 = derive('dA', 'laW', purusha='prathama', vacana=2, gana=3) # Weak vowel
        self.assertEqual(p3.get_current_string(), 'dadati')

    def test_aorist_kr(self) -> None:
        """Tests luN for kf (sici vrddhih and astisico'pṛkte)."""
        p1 = derive('kf', 'luN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'akArzIt')
        
        p2 = derive('kf', 'luN', purusha='prathama', vacana=2, gana=8)
        self.assertEqual(p2.get_current_string(), 'akArzuH')

    def test_gana_7_chid(self) -> None:
        """Gaṇa 7: Cid tests Śnam (infix) insertion."""
        p1 = derive('Cid', 'laW', purusha='prathama', vacana=0, gana=7) 
        self.assertEqual(p1.get_current_string(), 'Cinatti')
        p2 = derive('Cid', 'laW', purusha='prathama', vacana=1, gana=7) 
        self.assertEqual(p2.get_current_string(), 'CinttaH')

    def test_gana_2_bru(self) -> None:
        """Gaṇa 2: brU tests bruva Iw augment and YaN sandhi."""
        p1 = derive('brU', 'laW', purusha='prathama', vacana=0, gana=2) 
        self.assertEqual(p1.get_current_string(), 'bravIti')
        p2 = derive('brU', 'laW', purusha='prathama', vacana=1, gana=2) 
        self.assertEqual(p2.get_current_string(), 'brUtaH')

    def test_gana_3_dha(self) -> None:
        """Gaṇa 3: DA tests do dad ghoH and dadhas tathorś ca."""
        p1 = derive('DA', 'laW', purusha='prathama', vacana=0, gana=3) 
        self.assertEqual(p1.get_current_string(), 'daDAti')
        p2 = derive('DA', 'laW', purusha='prathama', vacana=1, gana=3) 
        self.assertEqual(p2.get_current_string(), 'DattaH')

    def test_lit_gam(self) -> None:
        """Tests liW for gam (kuhos cuh and mo no dhatoh)."""
        p1 = derive('gam', 'liW', purusha='prathama', vacana=0, gana=1) 
        self.assertEqual(p1.get_current_string(), 'jagAma')
        p2 = derive('gam', 'liW', purusha='uttama', vacana=1, gana=1) 
        self.assertEqual(p2.get_current_string(), 'jaganva')

    def test_gana_2_si_atmanepada(self) -> None:
        p1 = derive('SI', 'laW', purusha='prathama', vacana=0, gana=2, voice='atmanepada')
        self.assertEqual(p1.get_current_string(), 'Sete')
        p2 = derive('SI', 'laW', purusha='prathama', vacana=1, gana=2, voice='atmanepada')
        self.assertEqual(p2.get_current_string(), 'SayAte')
        p3 = derive('SI', 'laW', purusha='prathama', vacana=2, gana=2, voice='atmanepada')
        self.assertEqual(p3.get_current_string(), 'Serate')
        p4 = derive('SI', 'laW', purusha='madhyama', vacana=2, gana=2, voice='atmanepada')
        self.assertEqual(p4.get_current_string(), 'SeDve')

    def test_sru_lat(self) -> None:
        p1 = derive('Sru', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'SfRoti')
        p2 = derive('Sru', 'laW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(p2.get_current_string(), 'SfRutaH')
        p3 = derive('Sru', 'laW', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p3.get_current_string(), 'SfRvanti')

    def test_duh_lun(self) -> None:
        p1 = derive('duh', 'luN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'aDukzat')
        p2 = derive('duh', 'luN', purusha='prathama', vacana=1, gana=2)
        self.assertEqual(p2.get_current_string(), 'aDukzatAm')
        p3 = derive('duh', 'luN', purusha='prathama', vacana=2, gana=2)
        self.assertEqual(p3.get_current_string(), 'aDukzan')

    def test_han_lin(self) -> None:
        p1 = derive('han', 'liN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'hanyAt')
        p2 = derive('han', 'liN', purusha='uttama', vacana=0, gana=2)
        self.assertEqual(p2.get_current_string(), 'hanyAm')
        p3 = derive('han', 'liN', purusha='uttama', vacana=1, gana=2)
        self.assertEqual(p3.get_current_string(), 'hanyAva')

    def test_bhu_lun_plural(self) -> None:
        p1 = derive('BU', 'luN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p1.get_current_string(), 'aBUvan')

    def test_drs_causative_lat(self) -> None:
        from skt_dhatu_parse.sanadi import derive_secondary_root
        sanadi_prakriya = derive_secondary_root('dfS', 'Ric', gana=1)
        p1 = derive(custom_dhatu=sanadi_prakriya.terms[0], lakara_name='laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'darSayati')

    def test_prach_lat_samprasarana(self) -> None:
        p1 = derive('praC', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(p1.get_current_string(), 'pfcCati')

    def test_pranam_lat_natva(self) -> None:
        p1 = derive('nam', 'laW', purusha='prathama', vacana=0, gana=1, upasargas=['pra'])
        self.assertEqual(p1.get_current_string(), 'praRamati')

    def test_muc_lat_num(self) -> None:
        p1 = derive('muc', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(p1.get_current_string(), 'muYcati')

    def test_han_lat_full(self) -> None:
        p1 = derive('han', 'laW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'hanti')
        p2 = derive('han', 'laW', purusha='prathama', vacana=2, gana=2)
        self.assertEqual(p2.get_current_string(), 'Gnanti')
        p3 = derive('han', 'laW', purusha='madhyama', vacana=0, gana=2)
        self.assertEqual(p3.get_current_string(), 'haMsi')

    def test_kr_lan_full(self) -> None:
        p1 = derive('kf', 'laN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'akarot')
        p2 = derive('kf', 'laN', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(p2.get_current_string(), 'akurutAm')
        p3 = derive('kf', 'laN', purusha='prathama', vacana=2, gana=8)
        self.assertEqual(p3.get_current_string(), 'akurvan')

    def test_kr_lot_full(self) -> None:
        p1 = derive('kf', 'loW', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'karotu')
        p2 = derive('kf', 'loW', purusha='madhyama', vacana=0, gana=8)
        self.assertEqual(p2.get_current_string(), 'kuru')  # hi drops after u
        p3 = derive('kf', 'loW', purusha='uttama', vacana=0, gana=8)
        self.assertEqual(p3.get_current_string(), 'karavARi') # Natva

    def test_da_lat_full(self) -> None:
        p1 = derive('dA', 'laW', purusha='prathama', vacana=0, gana=3)
        self.assertEqual(p1.get_current_string(), 'dadAti')
        p2 = derive('dA', 'laW', purusha='prathama', vacana=1, gana=3)
        self.assertEqual(p2.get_current_string(), 'dattaH')
        p3 = derive('dA', 'laW', purusha='prathama', vacana=2, gana=3)
        self.assertEqual(p3.get_current_string(), 'dadati')

    def test_nisad_lat(self) -> None:
        p1 = derive('sad', 'laW', purusha='prathama', vacana=0, gana=1, upasargas=['ni'])
        self.assertEqual(p1.get_current_string(), 'nizIdati')

    def test_dah_future_anit_consonant_sandhi(self) -> None:
        """
        Tests dah + lfW -> Dakzyati
        Rule Chain: Aniṭ -> ho dhah -> ekaco baso bhas -> sadhoh kas si -> satva
        """
        prakriya = derive('dah', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Dakzyati')

    def test_yuj_future_anit_consonant_sandhi(self) -> None:
        """
        Tests yuj + lfW -> yokzyati
        Rule Chain: Aniṭ -> Guna -> choh kuh -> khari ca -> satva
        """
        prakriya = derive('yuj', 'lfW', purusha='prathama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'yokzyati')

    def test_sam_ci_lat(self) -> None:
        """
        Tests sam + ci + laW -> saYcinoti
        Rule Chain: Snu Vikarana -> Guna -> anusvarasya yayi parasavarnah (m -> M -> Y)
        """
        prakriya = derive('ci', 'laW', purusha='prathama', vacana=0, gana=5, upasargas=['sam'])
        self.assertEqual(prakriya.get_current_string(), 'saYcinoti')

    def test_chid_lun_vrddhi(self) -> None:
        """
        Tests Cid + luN -> acCEtsIt 
        Rule Chain: cli -> sic -> vadavrajahalantasyacah (halanta vrddhi before sic) -> astisico'prkte (I augment)
        """
        prakriya = derive('Cid', 'luN', purusha='prathama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'acCEtsIt')

    def test_chid_lot_madhyama(self) -> None:
        """
        Tests Cid + loW (madhyama ekavacana) -> CindDi
        Rule Chain: Śnam infix -> snasor allopah (Cinad -> Cind) -> hujhalbhyo her dhih (hi -> Di)
        """
        prakriya = derive('Cid', 'loW', purusha='madhyama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'CindDi')

    def test_stha_lit_prathama(self) -> None:
        """
        Tests sTA + liW -> tasTO
        Rule Chain: Reduplication -> haladi seshah (sarpuvah khayah: T survives) -> 
        abhyase car ca (T -> t) -> ata au nalah (a -> O) -> vrddhir eci (A + O -> O)
        """
        prakriya = derive('sTA', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'tasTO')

    def test_kram_parasmaipada_lengthening(self) -> None:
        """Tests kram + laW -> krAmati (kramah parasmaipadesu)"""
        prakriya = derive('kram', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'krAmati')

    def test_stha_lit_reduplication_and_au(self) -> None:
        """
        Tests sTA + liW -> tasTO
        Rule Chain: śarpūrvāḥ khayaḥ (T survives) -> abhyāse car ca (T -> t) -> āta au ṇalaḥ (a -> O) -> vṛddhir eci
        """
        prakriya = derive('sTA', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'tasTO')

    def test_dha_lot_madhyama_eka(self) -> None:
        """
        Tests DA + loW (Madhyama Ekavacana) -> Dehi
        Rule Chain: ghvāsor eddhāv abhyāsalopaśca (reduplication drops, root becomes e)
        """
        prakriya = derive('DA', 'loW', purusha='madhyama', vacana=0, gana=3)
        self.assertEqual(prakriya.get_current_string(), 'Dehi')

    def test_kri_para_atmanepada_shift(self) -> None:
        """Covers krI + parA forcing Atmanepada."""
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['parA'])
        self.assertEqual(prakriya.get_current_string(), 'parAkrIRIte')

    def test_engine_voice_override(self) -> None:
        """Covers explicit voice override inside the engine pipeline."""
        prakriya = derive('BU', 'laW', purusha='prathama', vacana=0, gana=1, voice='atmanepada')
        self.assertEqual(prakriya.get_current_string(), 'Bavate')

    def test_lun_ksa_augment(self) -> None:
        """
        Tests diS + luN -> adikzat
        Rule Chain: cli -> ksa (sa) -> vrasc-bhrasj... (S -> z) -> sadhoh kas si (z -> k) -> satva (s -> z)
        """
        prakriya = derive('diS', 'luN', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(prakriya.get_current_string(), 'adikzat')

    def test_jna_janor_ja_substitution(self) -> None:
        """Tests jñā + laW -> jAnAti (Rule 7.3.79: jñājanor jā)"""
        prakriya = derive('jYA', 'laW', purusha='prathama', vacana=0, gana=9)
        self.assertEqual(prakriya.get_current_string(), 'jAnAti')

    def test_sru_lit_uvan_sandhi(self) -> None:
        """Tests Sru + liW (Dual) -> SuSruvatuH (Rule 6.4.77: uvaṅ substitute)"""
        prakriya = derive('Sru', 'liW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SuSruvatuH')

    def test_luW_periphrastic_future(self) -> None:
        """Tests BU + luW -> BavitA, BavitArO, BavitAsi, BavitAsmi."""
        p1 = derive('BU', 'luW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'BavitA')
        
        p2 = derive('BU', 'luW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(p2.get_current_string(), 'BavitArO')
        
        p3 = derive('BU', 'luW', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'BavitAsi')

        p4 = derive('BU', 'luW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(p4.get_current_string(), 'BavitAsmi')

    def test_lfN_conditional(self) -> None:
        """Tests BU + lfN -> aBavizyat, aBavizyan, aBavizyaH."""
        p1 = derive('BU', 'lfN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'aBavizyat')
        
        p2 = derive('BU', 'lfN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p2.get_current_string(), 'aBavizyan')
        
        p3 = derive('BU', 'lfN', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'aBavizyaH')

    def test_asirlin_bhu_table(self) -> None:
        """Tests BU + ASIrliN -> BUyAt, BUyAstAm, BUyAsuH."""
        p1 = derive('BU', 'ASIrliN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'BUyAt')

        p2 = derive('BU', 'ASIrliN', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(p2.get_current_string(), 'BUyAstAm')

        p3 = derive('BU', 'ASIrliN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p3.get_current_string(), 'BUyAsuH')

    def test_asirlin_kr(self) -> None:
        """Tests kf + ASIrliN -> kriyAt (riṅ śayaglinkṣu)."""
        p1 = derive('kf', 'ASIrliN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'kriyAt')

    def test_asirlin_glai(self) -> None:
        """Tests glE + ASIrliN -> glAyAt (ādeca upadeśe'śiti)."""
        p1 = derive('glE', 'ASIrliN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'glAyAt')

    def test_gai_lit_prathama(self) -> None:
        """Tests gE + liW -> jagO (ādeca upadeśe'śiti -> āta au ṇalaḥ)."""
        prakriya = derive('gE', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jagO')

    def test_dams_lat_prathama(self) -> None:
        """Tests daMS + laW -> daSati."""
        prakriya = derive('daMS', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'daSati')

    def test_as_lan_full(self) -> None:
        """Tests as + laN -> AsIt, AstAm, Asan (āḍ ajādīnām & astisico'pṛkte)."""
        p1 = derive('as', 'laN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'AsIt')
        
        p2 = derive('as', 'laN', purusha='prathama', vacana=1, gana=2)
        self.assertEqual(p2.get_current_string(), 'AstAm')
        
        p3 = derive('as', 'laN', purusha='prathama', vacana=2, gana=2)
        self.assertEqual(p3.get_current_string(), 'Asan')

    def test_i_lan_full(self) -> None:
        """Tests i + laN -> Et, EtAm, Ayan (āṭaś ca)."""
        p1 = derive('i', 'laN', purusha='prathama', vacana=0, gana=2, voice='parasmaipada')
        self.assertEqual(p1.get_current_string(), 'Et')

if __name__ == '__main__':
    unittest.main()