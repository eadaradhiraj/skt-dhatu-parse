"""
engine.py
The main orchestrator for the Paninian derivation pipeline (Prakriya).
"""
from .dhatu_loader import get_dhatu, DEFAULT_DB_PATH
from .models import Term, Prakriya
from .anubandha import resolve_it_markers
from . import rules

def derive(dhatu_slp1: str = None, lakara_name: str = 'laW', purusha: str = 'prathama', vacana: int = 0,
           gana: int = None, db_path: str = DEFAULT_DB_PATH, custom_dhatu: Term = None,
           upasargas: list[str] = None, voice: str = None, vikalpa: bool = False) -> Prakriya:
           
    prakriya = Prakriya()
    prakriya.vikalpa = vikalpa
    
    if upasargas:
        for u in upasargas: prakriya.add_term(Term(u, 'upasarga'))
        
    if custom_dhatu:
        dhatu = custom_dhatu
        if not any(tag.startswith('gana_') for tag in dhatu.tags): dhatu.tags.add('gana_1')
        if 'parasmaipada' not in dhatu.tags and 'atmanepada' not in dhatu.tags: dhatu.tags.add('parasmaipada')
    else:
        dhatus = get_dhatu(dhatu_slp1, gana=gana, db_path=db_path)
        if not dhatus: return None
        dhatu = dhatus[0] 
        
        # Trigger Gana 10 (Curādi) Ṇic suffix insertion automatically
        if any(t == 'gana_10' for t in dhatu.tags) and 'sanadi' not in dhatu.tags:
            from .sanadi import derive_secondary_root
            clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.upadeza)
            sanadi_prakriya = derive_secondary_root(clean_dhatu, 'Ric', gana=10, db_path=db_path)
            if sanadi_prakriya: dhatu = sanadi_prakriya.terms[0]
            
        if voice == 'karmani' or voice == 'bhave':
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add('atmanepada')
            dhatu.tags.add('karmani')
        elif voice:
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('atmanepada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add(voice)
        elif 'ubhayapada' in dhatu.tags:
            dhatu.tags.add('parasmaipada') 
            
        if dhatu_slp1 == 'krI' and upasargas and upasargas[-1] in['vi', 'parA'] and voice != 'karmani':
            dhatu.tags.discard('parasmaipada')
            dhatu.tags.discard('ubhayapada')
            dhatu.tags.add('atmanepada')
            prakriya.log(f"Rule 1.3.44: 'krI' becomes Atmanepada after '{upasargas[-1]}'")

    prakriya.add_term(dhatu)
    
    resolve_it_markers(dhatu)
    rules.dhatvadeh_sah_sah_no_nah(prakriya)  
    rules.idito_num_dhatoh(prakriya)  
    
    lakara = Term(lakara_name, 'lakara')
    lakara.tags.add(lakara_name) 
    prakriya.add_term(lakara)
    
    rules.ardhadhatuke_mula_parivartanam(prakriya)
    rules.at_agama(prakriya)           
    
    for term in prakriya.terms:
        if term.term_type != 'dhatu': resolve_it_markers(term)
    
    rules.substitute_lakara(prakriya, purusha=purusha, vacana=vacana)

    rules.cli_agama(prakriya)
    rules.gatistha_sic_lopa(prakriya)
    
    rules.mer_nih(prakriya)
    rules.lut_prathamasya_daraurasah(prakriya)
    rules.jher_jus(prakriya)
    rules.jhasya_ran(prakriya)
    rules.ito_at(prakriya)
    rules.jhonta(prakriya)            
    rules.thasah_se(prakriya)         
    rules.tasthasthamipam(prakriya)
    rules.ser_hi(prakriya)
    rules.at_uttasya(prakriya)
    
    suffix = prakriya.terms[-1]
    resolve_it_markers(suffix)
    rules.atmanepada_tere(prakriya)   
    rules.itasca(prakriya)            
    rules.nityam_nitah(prakriya)
    rules.er_uh(prakriya)

    rules.insert_vikarana(prakriya)
    rules.lin_agamas(prakriya)
    
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa' and t.upadeza not in ['cli', 'ciR']), None)
    if vikarana: resolve_it_markers(vikarana)
    
    rules.mit_aco_antyat_parah(prakriya)
    rules.akrtsarvadhatukayor_dirghah(prakriya)

    rules.bruva_it(prakriya)
    rules.sici_vrddhih(prakriya)
    rules.asti_sico_aprkte(prakriya)
    rules.hrasvad_angat(prakriya)
    
    rules.sarvadhatukam_apit(prakriya)
    rules.adeca_upadese_asiti(prakriya)
    rules.ata_au_nalah(prakriya)
    rules.rin_sayaglinksu(prakriya)
    rules.rta_id_dhatoh(prakriya)
    rules.sna_sandhi(prakriya)
    rules.se_mucadinam(prakriya)
    rules.paghra_sthadi_adesha(prakriya)
    rules.jna_janor_ja(prakriya)
    rules.damsa_sanja_svanjam_sapi(prakriya)
    rules.kramah_parasmaipadesu(prakriya)
    rules.vacisvapiyajadinam_kiti(prakriya)
    rules.sino_gunah(prakriya)
    rules.han_ghatva_tatva(prakriya)
    rules.vikarana_guna(prakriya)
    rules.kr_u_morphing(prakriya)
    rules.snasor_allopah(prakriya)
    rules.stha_adi_ita(prakriya)
    rules.er_lini(prakriya)
    rules.it_agama(prakriya)          
    rules.ita_iti(prakriya)

    rules.liti_dhator_anabhyasasya(prakriya)
    rules.lity_abhyasasya(prakriya)
    rules.slau_reduplication(prakriya)
    rules.can_reduplication(prakriya)
    rules.jes_ca(prakriya)

    prakriya.terms =[t for t in prakriya.terms if t.text]

    rules.haladi_seshah(prakriya)            
    rules.do_dad_ghoh(prakriya)
    rules.snabhyastayor_atah(prakriya)
    rules.hrasvah(prakriya)
    rules.ur_at(prakriya)                    
    rules.bhavater_ah(prakriya)              
    rules.abhyase_car_ca(prakriya)
    rules.kuhos_cuh(prakriya)
    rules.can_abhyasa_vowel(prakriya)
    rules.bhuvo_vug_lunlitoh(prakriya)
    rules.revert_sh_after_abhyasa(prakriya)

    prakriya.terms =[t for t in prakriya.terms if t.text]

    rules.gam_hana_jana_lopa(prakriya)
    rules.aniditam_hala_upadhayah_kniti(prakriya)
    rules.sasa_id_anghaloh(prakriya)
    rules.rdriso_ngi_gunah(prakriya)
    rules.ato_yeyah(prakriya)
    rules.lin_salopo_anantyasya(prakriya)
    rules.ato_heh(prakriya)
    rules.utasca_pratyayad(prakriya)
    rules.hanter_jah(prakriya)
    rules.hujhalbhyo_her_dhih(prakriya)
    rules.ghvasor_ed_hau(prakriya)
    rules.tasyasti_lopa(prakriya)
    rules.ri_ca(prakriya)
    rules.h_eti(prakriya)
    rules.diti_teh_lopa(prakriya)
    rules.jhalo_jhali(prakriya)
    prakriya.terms =[t for t in prakriya.terms if t.text]
    rules.hali_ca(prakriya)
    rules.srujidrusor_jhaly_amakiti(prakriya)
    rules.ato_yuk(prakriya)
    rules.aco_nniti(prakriya)
    rules.ata_upadhayah(prakriya)           
    rules.mrjer_vrddhih(prakriya)
    rules.sarvadhatuka_ardhadhatukayoh(prakriya)  
    rules.eco_yayavayah(prakriya)                 
    rules.aci_snu_dhatu_bhruvam(prakriya)
    
    rules.ato_dirgho_yayi(prakriya)               
    rules.ato_nitah(prakriya) 
    rules.usy_apadantat(prakriya)                 
    rules.ato_gune(prakriya)
    rules.atas_ca(prakriya)
    rules.ad_gunah(prakriya)
    rules.vrddhir_eci(prakriya)
    rules.akah_savarne_dirghah(prakriya)
    rules.iko_yanaci(prakriya)
    rules.skoh_samyogadyor_ante_ca(prakriya)
    rules.lopo_vyorvali(prakriya)
    
    rules.anunasikalopo_jhali_kniti(prakriya)
    rules.vrasca_bhrasja_sruja_mruja(prakriya)
    rules.choh_kuh(prakriya)
    rules.che_ca(prakriya)
    rules.ho_dhah_dader_ghah(prakriya)
    rules.ekaco_baso_bhas(prakriya)
    rules.sadhoh_kas_si(prakriya)
    rules.mo_no_dhatoh(prakriya)
    rules.adesa_pratyayayoh(prakriya)             
    rules.rashabhyam_no_nah(prakriya)
    rules.dadhas_tathor_ca(prakriya)
    rules.jhasas_tathor_dho_dhah(prakriya)        
    
    rules.stuna_stuh(prakriya)
    rules.dho_dhe_lopah(prakriya)                 
    rules.jhalam_jas_jhasi(prakriya)              
    
    rules.khari_ca(prakriya)                      
    rules.samyogantasya_lopah(prakriya)
    rules.nascapadantasya_jhali(prakriya)         
    rules.anusvarasya_yayi_parasavarnah(prakriya)
    rules.upasarga_satva(prakriya)                
    rules.upasarga_sandhi(prakriya)               
    rules.rutva_visarga(prakriya)                 
    
    return prakriya