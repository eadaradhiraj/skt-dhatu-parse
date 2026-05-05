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

    def test_bhavami(self) -> None:
        prakriya = derive('BU', 'laW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'BavAmi')

    def test_gana_10_cur(self) -> None:
        """Tests that Curādi automatically applies Ṇic: cur + laW -> corayati."""
        prakriya = derive('cur', 'laW', purusha='prathama', vacana=0, gana=10)
        self.assertEqual(prakriya.get_current_string(), 'corayati')

    def test_passive_voice_kr(self) -> None:
        """Tests the insertion of the yak vikaraṇa in Karmaṇi prayoga: kf + yak + te -> kriyate."""
        prakriya = derive('kf', 'laW', purusha='prathama', vacana=0, gana=8, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'kriyate')

    def test_passive_voice_da(self) -> None:
        """Tests the insertion of yak on an A-ending root: dA + yak + te -> dIyate."""
        prakriya = derive('dA', 'laW', purusha='prathama', vacana=0, gana=3, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'dIyate')

    def test_passive_voice_vac(self) -> None:
        """Tests the insertion of yak causing samprasarana: vac + yak + te -> ucyate."""
        prakriya = derive('vac', 'laW', purusha='prathama', vacana=0, gana=2, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'ucyate')

    def test_passive_voice_aorist_cin(self) -> None:
        """Tests the passive 3rd person singular Aorist taking ciṆ: kf + luN (karmani) -> akAri."""
        prakriya = derive('kf', 'luN', purusha='prathama', vacana=0, gana=8, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'akAri')

    def test_passive_voice_aorist_cin_bhu(self) -> None:
        """Tests the passive 3rd person singular Aorist taking ciṆ: BU + luN (karmani) -> aBAvi."""
        prakriya = derive('BU', 'luN', purusha='prathama', vacana=0, gana=1, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'aBAvi')

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

    def test_invalid_roots_return_none(self) -> None:
        from skt_dhatu_parse.krdanta import derive_krdanta
        from skt_dhatu_parse.sanadi import derive_secondary_root
        self.assertIsNone(derive('xyz_invalid_root'))
        self.assertIsNone(derive_krdanta('xyz_invalid_root', 'kta'))
        self.assertIsNone(derive_secondary_root('xyz_invalid_root', 'Ric'))

    def test_gana_9_vikri_singular(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vikrIRIte')

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

    def test_perfect_tense_kr_dual(self) -> None:
        prakriya = derive('kf', 'liW', purusha='prathama', vacana=1, gana=8)
        self.assertEqual(prakriya.get_current_string(), 'cakratuH')

    def test_gana_2_ad(self) -> None:
        prakriya = derive('ad', 'laW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'atti')

    def test_gana_2_as(self) -> None:
        p1 = derive('as', 'laW', purusha='prathama', vacana=0, gana=2) 
        self.assertEqual(p1.get_current_string(), 'asti')
        
        p2 = derive('as', 'laW', purusha='prathama', vacana=2, gana=2) 
        self.assertEqual(p2.get_current_string(), 'santi')
        
        p3 = derive('as', 'laW', purusha='uttama', vacana=0, gana=2)   
        self.assertEqual(p3.get_current_string(), 'asmi')

    def test_gana_3_hu(self) -> None:
        p1 = derive('hu', 'laW', purusha='prathama', vacana=0, gana=3) 
        self.assertEqual(p1.get_current_string(), 'juhoti')
        
        p2 = derive('hu', 'laW', purusha='prathama', vacana=2, gana=3) 
        self.assertEqual(p2.get_current_string(), 'juhvati')

    def test_gana_5_su(self) -> None:
        p1 = derive('su', 'laW', purusha='prathama', vacana=0, gana=5) 
        self.assertEqual(p1.get_current_string(), 'sunoti')
        
        p2 = derive('su', 'laW', purusha='prathama', vacana=2, gana=5) 
        self.assertEqual(p2.get_current_string(), 'sunvanti')

    def test_imperative_lot(self) -> None:
        p1 = derive('BU', 'loW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'Bavatu')
        
        p2 = derive('BU', 'loW', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p2.get_current_string(), 'Bava')
        
        p3 = derive('BU', 'loW', purusha='uttama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'BavAni')

    def test_optative_lin(self) -> None:
        p1 = derive('BU', 'liN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'Bavet')
        
        p2 = derive('BU', 'liN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p2.get_current_string(), 'BaveyuH')
        
        p3 = derive('BU', 'liN', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(p3.get_current_string(), 'BaveH')

    def test_aorist_lun(self) -> None:
        p1 = derive('BU', 'luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'aBUt')
        
        p2 = derive('gam', 'luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p2.get_current_string(), 'agamat')

    def test_gana_2_han(self) -> None:
        p1 = derive('han', 'laW', purusha='prathama', vacana=0, gana=2) 
        self.assertEqual(p1.get_current_string(), 'hanti')
        
        p2 = derive('han', 'laW', purusha='prathama', vacana=2, gana=2) 
        self.assertEqual(p2.get_current_string(), 'Gnanti')
    
    def test_optative_atmanepada(self) -> None:
        p1 = derive('eD', 'liN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'eDeta')
        
        p2 = derive('eD', 'liN', purusha='prathama', vacana=2, gana=1)
        self.assertEqual(p2.get_current_string(), 'eDeran')

    def test_imperative_gana_5(self) -> None:
        p1 = derive('su', 'loW', purusha='prathama', vacana=0, gana=5)
        self.assertEqual(p1.get_current_string(), 'sunotu')
        
        p2 = derive('su', 'loW', purusha='madhyama', vacana=0, gana=5)
        self.assertEqual(p2.get_current_string(), 'sunu') 

    def test_gana_2_duh(self) -> None:
        p1 = derive('duh', 'laW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'dogDi')
        
        p2 = derive('duh', 'laW', purusha='madhyama', vacana=0, gana=2) 
        self.assertEqual(p2.get_current_string(), 'Dokzi')
        
        p3 = derive('duh', 'laW', purusha='prathama', vacana=1, gana=2) 
        self.assertEqual(p3.get_current_string(), 'dugDaH')

    def test_dfS_future(self) -> None:
        p1 = derive('dfS', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'drakzyati')

    def test_gana_3_dA(self) -> None:
        p1 = derive('dA', 'laW', purusha='prathama', vacana=0, gana=3) 
        self.assertEqual(p1.get_current_string(), 'dadAti')
        
        p2 = derive('dA', 'laW', purusha='prathama', vacana=1, gana=3) 
        self.assertEqual(p2.get_current_string(), 'dattaH')

    def test_aorist_kr(self) -> None:
        p1 = derive('kf', 'luN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'akArzIt')

    def test_gana_7_chid(self) -> None:
        p1 = derive('Cid', 'laW', purusha='prathama', vacana=0, gana=7) 
        self.assertEqual(p1.get_current_string(), 'Cinatti')

    def test_gana_2_bru(self) -> None:
        p1 = derive('brU', 'laW', purusha='prathama', vacana=0, gana=2) 
        self.assertEqual(p1.get_current_string(), 'bravIti')

    def test_gana_3_dha(self) -> None:
        p1 = derive('DA', 'laW', purusha='prathama', vacana=0, gana=3) 
        self.assertEqual(p1.get_current_string(), 'daDAti')

    def test_lit_gam(self) -> None:
        p1 = derive('gam', 'liW', purusha='prathama', vacana=0, gana=1) 
        self.assertEqual(p1.get_current_string(), 'jagAma')

    def test_gana_2_si_atmanepada(self) -> None:
        p1 = derive('SI', 'laW', purusha='prathama', vacana=0, gana=2, voice='atmanepada')
        self.assertEqual(p1.get_current_string(), 'Sete')

    def test_sru_lat(self) -> None:
        p1 = derive('Sru', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'SfRoti')

    def test_duh_lun(self) -> None:
        p1 = derive('duh', 'luN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'aDukzat')

    def test_han_lin(self) -> None:
        p1 = derive('han', 'liN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'hanyAt')

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

    def test_muc_lat_num(self) -> None:
        p1 = derive('muc', 'laW', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(p1.get_current_string(), 'muYcati')

    def test_kr_lan_full(self) -> None:
        p1 = derive('kf', 'laN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'akarot')

    def test_kr_lot_full(self) -> None:
        p1 = derive('kf', 'loW', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'karotu')

    def test_da_lat_full(self) -> None:
        p1 = derive('dA', 'laW', purusha='prathama', vacana=0, gana=3)
        self.assertEqual(p1.get_current_string(), 'dadAti')

    def test_nisad_lat(self) -> None:
        p1 = derive('sad', 'laW', purusha='prathama', vacana=0, gana=1, upasargas=['ni'])
        self.assertEqual(p1.get_current_string(), 'nizIdati')

    def test_dah_future_anit_consonant_sandhi(self) -> None:
        prakriya = derive('dah', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'Dakzyati')

    def test_yuj_future_anit_consonant_sandhi(self) -> None:
        prakriya = derive('yuj', 'lfW', purusha='prathama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'yokzyati')

    def test_sam_ci_lat(self) -> None:
        prakriya = derive('ci', 'laW', purusha='prathama', vacana=0, gana=5, upasargas=['sam'])
        self.assertEqual(prakriya.get_current_string(), 'saYcinoti')

    def test_chid_lun_vrddhi(self) -> None:
        prakriya = derive('Cid', 'luN', purusha='prathama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'acCEtsIt')

    def test_chid_lot_madhyama(self) -> None:
        prakriya = derive('Cid', 'loW', purusha='madhyama', vacana=0, gana=7)
        self.assertEqual(prakriya.get_current_string(), 'CindDi')

    def test_stha_lit_prathama(self) -> None:
        prakriya = derive('sTA', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'tasTO')

    def test_kram_parasmaipada_lengthening(self) -> None:
        prakriya = derive('kram', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'krAmati')

    def test_dha_lot_madhyama_eka(self) -> None:
        prakriya = derive('DA', 'loW', purusha='madhyama', vacana=0, gana=3)
        self.assertEqual(prakriya.get_current_string(), 'Dehi')

    def test_kri_para_atmanepada_shift(self) -> None:
        prakriya = derive('krI', 'laW', purusha='prathama', vacana=0, gana=9, upasargas=['parA'])
        self.assertEqual(prakriya.get_current_string(), 'parAkrIRIte')

    def test_engine_voice_override(self) -> None:
        prakriya = derive('BU', 'laW', purusha='prathama', vacana=0, gana=1, voice='atmanepada')
        self.assertEqual(prakriya.get_current_string(), 'Bavate')

    def test_lun_ksa_augment(self) -> None:
        prakriya = derive('diS', 'luN', purusha='prathama', vacana=0, gana=6)
        self.assertEqual(prakriya.get_current_string(), 'adikzat')

    def test_jna_janor_ja_substitution(self) -> None:
        prakriya = derive('jYA', 'laW', purusha='prathama', vacana=0, gana=9)
        self.assertEqual(prakriya.get_current_string(), 'jAnAti')

    def test_sru_lit_uvan_sandhi(self) -> None:
        prakriya = derive('Sru', 'liW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SuSruvatuH')

    def test_luW_periphrastic_future(self) -> None:
        p1 = derive('BU', 'luW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'BavitA')
        p2 = derive('BU', 'luW', purusha='prathama', vacana=1, gana=1)
        self.assertEqual(p2.get_current_string(), 'BavitArO')

    def test_lfN_conditional(self) -> None:
        p1 = derive('BU', 'lfN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'aBavizyat')

    def test_asirlin_bhu_table(self) -> None:
        p1 = derive('BU', 'ASIrliN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'BUyAt')

    def test_asirlin_kr(self) -> None:
        p1 = derive('kf', 'ASIrliN', purusha='prathama', vacana=0, gana=8)
        self.assertEqual(p1.get_current_string(), 'kriyAt')

    def test_asirlin_glai(self) -> None:
        p1 = derive('glE', 'ASIrliN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p1.get_current_string(), 'glAyAt')

    def test_gai_lit_prathama(self) -> None:
        prakriya = derive('gE', 'liW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jagO')

    def test_dams_lat_prathama(self) -> None:
        prakriya = derive('daMS', 'laW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'daSati')

    def test_as_lan_full(self) -> None:
        p1 = derive('as', 'laN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p1.get_current_string(), 'AsIt')

    def test_i_lan_full(self) -> None:
        p1 = derive('i', 'laN', purusha='prathama', vacana=0, gana=2, voice='parasmaipada')
        self.assertEqual(p1.get_current_string(), 'Et')

    def test_as_lit(self) -> None:
        p = derive('as', 'liW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p.get_current_string(), 'baBUva')

    def test_bru_lit(self) -> None:
        p = derive('brU', 'liW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(p.get_current_string(), 'uvAca')

    def test_drs_lun(self) -> None:
        p = derive('dfS', 'luN', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(p.get_current_string(), 'adarSat')

    def test_vikalpa_dual_output(self) -> None:
        p_norm = derive('Cid', 'luN', purusha='prathama', vacana=0, gana=7, vikalpa=False)
        p_vik = derive('Cid', 'luN', purusha='prathama', vacana=0, gana=7, vikalpa=True)
        self.assertEqual(p_norm.get_current_string(), 'acCEtsIt')
        self.assertEqual(p_vik.get_current_string(), 'acCidat')

    def test_gam_future_set(self) -> None:
        prakriya = derive('gam', 'lfW', purusha='prathama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gamizyati')

    def test_svap_lit_reduplication_and_set(self) -> None:
        prakriya = derive('svap', 'liW', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'suzvApa')
        
    def test_han_lun_vadh(self) -> None:
        prakriya = derive('han', 'luN', purusha='prathama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'avaDIt')

    def test_sru_lit_uttama_dual_anit(self) -> None:
        prakriya = derive('Sru', 'liW', purusha='uttama', vacana=1, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SuSruva')

    def test_sru_lit_madhyama_singular_anit(self) -> None:
        prakriya = derive('Sru', 'liW', purusha='madhyama', vacana=0, gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SuSroTa')
        
    def test_stu_lit_madhyama_singular_anit(self) -> None:
        prakriya = derive('stu', 'liW', purusha='madhyama', vacana=0, gana=2)
        self.assertEqual(prakriya.get_current_string(), 'tuzwoTa')

if __name__ == '__main__':
    unittest.main()


    def test_da_aorist_passive_yuk(self) -> None:
        prakriya = derive('dA', 'luN', purusha='prathama', vacana=0, gana=3, voice='karmani')
        self.assertEqual(prakriya.get_current_string(), 'adAyi')
