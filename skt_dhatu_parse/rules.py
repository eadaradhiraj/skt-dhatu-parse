"""
rules.py
The comprehensive library of Paninian Sutras.
"""
from .shivasutras import get_pratyahara, is_vowel, SLP1_VOWELS
from .models import Term, Prakriya
from .anubandha import resolve_it_markers

# --- Phonological Sets (Pratyaharas) ---
IK_VOWELS = set(get_pratyahara('i', 'k') + ['I', 'U', 'F', 'X'])
EC_VOWELS = get_pratyahara('e', 'c')
YAY_CONSONANTS = set(get_pratyahara('y', 'Y'))
IN_VOWELS = set(get_pratyahara('i', 'R') + ['I', 'U', 'F', 'X'])
SLP1_CONSONANTS = set(get_pratyahara('h', 'l')) 
VAL_CONSONANTS = set(get_pratyahara('v', 'l')) 
JHAS_CONSONANTS = set(get_pratyahara('J', 'z'))      
JHAL_CONSONANTS = set(get_pratyahara('J', 'l'))      
JHAS_SOFT_CONSONANTS = set(get_pratyahara('J', 'S')) 
KHAR_CONSONANTS = set(get_pratyahara('K', 'r'))      
CHAR_CONSONANTS = set(get_pratyahara('c', 'r'))      
YAY_PRATYAHARA = set(get_pratyahara('y', 'y'))

UPASARGAS =[
    'pra', 'parA', 'apa', 'sam', 'anu', 'ava', 'nis', 'nir', 
    'dus', 'dur', 'vi', 'A', 'ni', 'aDi', 'api', 'ati', 
    'su', 'ud', 'aBi', 'prati', 'pari', 'upa'
]

TIN_PARASMAIPADA = {
    'prathama': ['tip', 'tas', 'Ji'],
    'madhyama': ['sip', 'Tas', 'Ta'],
    'uttama':['mip', 'vas', 'mas']
}
TIN_ATMANEPADA = {
    'prathama':['ta', 'AtAm', 'Ja'],
    'madhyama':['TAs', 'ATAm', 'Dvam'],
    'uttama':   ['iw', 'vahi', 'mahiN']
}
TIN_PARASMAIPADA_LIT = {
    'prathama':['Ral', 'atus', 'us'],
    'madhyama':['Tal', 'aTus', 'a'],
    'uttama':   ['Ral', 'va', 'ma']
}
TIN_ATMANEPADA_LIT = {
    'prathama': ['e', 'Ate', 'ire'],
    'madhyama':['se', 'ATe', 'Dve'],
    'uttama':   ['e', 'vahe', 'mahe']
}

ANIT_ROOTS = {
    'ji', 'nI', 'ci', 'Sru', 'stu', 'su', 'hu', 'dA', 'DA', 'sTA', 'pA', 'GrA', 
    'DmA', 'gA', 'yA', 'vA', 'snA', 'kf', 'hf', 'Df', 'sf', 'smf', 'stf', 'kF', 'jYA',
    'glE', 'gE', 'mlE', 'dE', 'mE', 'sE', 'DyE', 'trE', 'hve', 'Sak', 'pac', 'kram', 'masj', 'muc', 'ric', 'vac', 'vic', 'sic', 'praC', 'tyaj', 'nij', 'BaYj', 
    'Baj', 'Brajj', 'yaj', 'yuj', 'raYj', 'vij', 'svaYj', 'saYj', 'sfj', 'vraSc',
    'ad', 'kzuD', 'Kid', 'Cid', 'tud', 'nud', 'pad', 'Bid', 'vid', 'sad', 
    'svid', 'skand', 'kruD', 'buD', 'banD', 'yuD', 'ruD', 'rAD', 'vyaD', 
    'SuD', 'sAD', 'siD', 'man', 'han', 'Ap', 'kzip', 'Cup', 'tap', 'tip', 'tfp', 'dfp', 'lip', 'lup', 'vap', 
    'Sap', 'svap', 'sfp', 'yaB', 'raB', 'laB', 'gam', 'nam', 'yam', 'ram',
    'kruS', 'daMS', 'diS', 'dfS', 'mfS', 'riS', 'ruS', 'viS', 'spfS',
    'kfz', 'tviz', 'tuz', 'dviz', 'puz', 'piz', 'viz', 'Siz', 'Suz', 'Sliz',
    'Gas', 'vas', 'dah', 'dih', 'nah', 'mih', 'ruh', 'lih', 'vah', 'guh', 'SAs'
}

VET_ROOTS = {
    'syand', 'kxp', 'raD', 'naS', 'tfp', 'dfp', 'druh', 'muh', 'snih', 'snuh'
}

def apply_upasarga_voice_shifts(dhatu_text: str, tags: set, upasargas: list[str], prakriya: Prakriya) -> None:
    """Rules 1.3.14 to 1.3.77: Shifts Parasmaipada/Atmanepada based on Upasargas."""
    if not upasargas: return
    last_upa = upasargas[-1]
    
    shifted = False
    if dhatu_text == 'ji' and last_upa in ['vi', 'parA']: shifted = True
    elif dhatu_text == 'gam' and last_upa == 'sam': shifted = True
    elif dhatu_text == 'sTA' and last_upa in['sam', 'ava', 'pra', 'vi', 'upa']: shifted = True
    elif dhatu_text == 'viS' and last_upa == 'ni': shifted = True
    elif dhatu_text == 'krI' and last_upa in ['vi', 'parA']: shifted = True
        
    if shifted and 'parasmaipada' in tags:
        tags.discard('parasmaipada')
        tags.add('atmanepada')
        prakriya.log(f"Rule 1.3.x (Voice Shift): '{last_upa} + {dhatu_text}' triggers Atmanepada.")

def apply_guna(char: str) -> str:
    if char in['i', 'I']: return 'e'
    if char in ['u', 'U']: return 'o'
    if char in['f', 'F']: return 'ar'
    if char in ['x']: return 'al'
    return char

def apply_vrddhi(char: str) -> str:
    if char in ['a']: return 'A'
    if char in ['i', 'I', 'e']: return 'E'
    if char in['u', 'U', 'o']: return 'O'
    if char in['f', 'F']: return 'Ar'
    if char in ['x']: return 'Al'
    return char

# ==========================================
# VERBAL MORPHOLOGY (TINANTA)
# ==========================================

def substitute_lakara(prakriya: Prakriya, purusha: str = 'prathama', vacana: int = 0) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    lakara = prakriya.terms[-1] 
    is_lit = 'liW' in lakara.tags
    
    if dhatu and 'parasmaipada' in dhatu.tags:
        new_suffix = TIN_PARASMAIPADA_LIT[purusha][vacana] if is_lit else TIN_PARASMAIPADA[purusha][vacana]
    elif dhatu and 'atmanepada' in dhatu.tags:
        new_suffix = TIN_ATMANEPADA_LIT[purusha][vacana] if is_lit else TIN_ATMANEPADA[purusha][vacana]
    else:
        new_suffix = TIN_PARASMAIPADA_LIT[purusha][vacana] if is_lit else TIN_PARASMAIPADA[purusha][vacana]
        
    lakara.text = new_suffix
    lakara.upadeza = new_suffix
    lakara.term_type = 'pratyaya'
    lakara.tags.add('tin') 
    
    if any(lak in lakara.tags for lak in['laW', 'liW', 'luW', 'lfW', 'leW', 'loW']):
        lakara.tags.add('Wit')
        
    if is_lit or 'ASIrliN' in lakara.tags:
        lakara.tags.add('ardhadhatuka')
        if is_lit and new_suffix in['Ral', 'Tal']: lakara.tags.add('pit')
        else: lakara.tags.add('kit')
    else: 
        lakara.tags.add('sarvadhatuka')
    prakriya.log(f"Rule 3.4.78: Substituted lakara with '{new_suffix}'")

def insert_vikarana(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if not dhatu: return
    idx = prakriya.terms.index(dhatu) + 1 
    
    if 'lfW' in suffix.tags or 'lfN' in suffix.tags:
        vik = Term('sya', 'vikaraRa')
        vik.tags.add('ardhadhatuka')
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.33: Inserted 'sya' for Future/Conditional")
        return
    elif 'luW' in suffix.tags:
        vik = Term('tAsi', 'vikaraRa')
        vik.text = 'tAs'
        vik.tags.add('ardhadhatuka')
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.33: Inserted 'tAsi' for Periphrastic Future")
        return
        
    if 'luN' in suffix.tags: return
    if 'ardhadhatuka' in suffix.tags: return

    is_karmani = 'karmani' in dhatu.tags
    if is_karmani:
        vik = Term('yak', 'vikaraRa')
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.67: sārvadhātuke yak (Passive Vikaraṇa)")
        return

    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    if clean_dhatu == 'Sru':
        vik = Term('Snu', 'vikaraRa')
        dhatu.text = 'Sf'
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.74: śruvaḥ śṛ ca (Sru takes Snu and becomes Sf)")
        return
        
    if 'gana_1' in dhatu.tags: vik = Term('Sap', 'vikaraRa')
    elif 'gana_2' in dhatu.tags:
        vik = Term('Sap', 'vikaraRa')
        vik.text = ''
        vik.tags.add('luk')
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 2.4.72: Inserted 'Sap' with 'luk' (elision)")
        return
    elif 'gana_3' in dhatu.tags:
        vik = Term('Slu', 'vikaraRa')
        vik.text = ''
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 2.4.75: Inserted 'Slu' (elision with reduplication)")
        return
    elif 'gana_4' in dhatu.tags: vik = Term('Syan', 'vikaraRa')
    elif 'gana_5' in dhatu.tags: vik = Term('Snu', 'vikaraRa')
    elif 'gana_6' in dhatu.tags: vik = Term('Sa', 'vikaraRa')
    elif 'gana_7' in dhatu.tags: vik = Term('Snam', 'vikaraRa')
    elif 'gana_8' in dhatu.tags: vik = Term('u', 'vikaraRa')
    elif 'gana_9' in dhatu.tags: vik = Term('SnA', 'vikaraRa')
    else: return
        
    prakriya.terms.insert(idx, vik)
    prakriya.log(f"Inserted Vikarana '{vik.upadeza}'")

def akrtsarvadhatukayor_dirghah(prakriya: Prakriya) -> None:
    """Rule 7.4.25: akṛtsārvadhātukayor dīrghaḥ. Lengthens vowel before yak."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.upadeza == 'yak'), None)
    if dhatu and vikarana and dhatu.text:
        last = dhatu.text[-1]
        if last == 'i': 
            dhatu.text = dhatu.text[:-1] + 'I'
            prakriya.log("Rule 7.4.25: i -> I before yak")
        elif last == 'u': 
            dhatu.text = dhatu.text[:-1] + 'U'
            prakriya.log("Rule 7.4.25: u -> U before yak")

def mit_aco_antyat_parah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.upadeza == 'Snam'), None)
    if dhatu and vikarana and vikarana.text:
        text = dhatu.text
        last_vowel_idx = -1
        for i, char in enumerate(text):
            if is_vowel(char): last_vowel_idx = i
        if last_vowel_idx != -1:
            dhatu.text = text[:last_vowel_idx+1] + vikarana.text + text[last_vowel_idx+1:]
            vikarana.text = ''
            prakriya.log(f"Rule 1.1.47: Inserted 'mit' ({vikarana.upadeza}) into root -> '{dhatu.text}'")

def bruva_it(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    suffix = None
    insert_idx = -1
    for i in range(idx + 1, len(prakriya.terms)):
        if prakriya.terms[i].text:
            suffix = prakriya.terms[i]
            insert_idx = i
            break
    if not suffix: return
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    if clean_dhatu == 'brU' and ('sarvadhatuka' in suffix.tags or 'tin' in suffix.tags) and 'pit' in suffix.tags:
        if suffix.text and suffix.text[0] in SLP1_CONSONANTS:
            agama = Term('I', 'Agama')
            agama.tags.add('sarvadhatuka')
            agama.tags.add('pit')
            prakriya.terms.insert(insert_idx, agama)
            prakriya.log("Rule 7.3.93: bruva Iw (Inserted 'I' before pit sarvadhatuka)")

def atmanepada_tere(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if suffix.upadeza in['qA', 'rO', 'ras']: return 
    if dhatu and 'atmanepada' in dhatu.tags and 'Wit' in suffix.tags:
        text = suffix.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                suffix.text = text[:i] + 'e'
                prakriya.log(f"Rule 3.4.79 (Tere): '{text[i:]}' -> 'e'")
                break

def hujhalbhyo_her_dhih(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t2.text == 'hi':
            is_jhal = t1.text and t1.text[-1] in JHAL_CONSONANTS
            clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), t1.text)
            is_hu_or_sas = t1.term_type == 'dhatu' and clean_dhatu in ['hu', 'SAs']
            if is_jhal or is_hu_or_sas:
                t2.text = 'Di'
                prakriya.log("Rule 6.4.101: hujhalbhyo her dhiH ('hi' -> 'Di')")

def thasah_se(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.upadeza == 'TAs' and 'Wit' in suffix.tags:
        suffix.text = 'se'
        suffix.upadeza = 'se'
        prakriya.log("Rule 3.4.80: Replaced 'TAs' with 'se'")

def jhonta(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text) if dhatu else ''
        is_atmanepada = dhatu and 'atmanepada' in dhatu.tags
        JAKSITYADI =['jakz', 'jAgf', 'daridrA', 'cakAs', 'SAs', 'dIDI', 'vevI']
        is_abhyasta = dhatu and ('gana_3' in dhatu.tags or clean_dhatu in JAKSITYADI)
        is_karmani = dhatu and ('karmani' in dhatu.tags or 'bhave' in dhatu.tags)
        is_anat = dhatu and any(g in dhatu.tags for g in['gana_2', 'gana_3', 'gana_5', 'gana_7', 'gana_8', 'gana_9']) and not is_karmani
        
        if suffix.upadeza == 'Ja' and 'liN' in suffix.tags: pass 
        elif clean_dhatu == 'SI':
            suffix.text = 'rat' + suffix.text[1:]
            prakriya.log("Rule 7.1.6: śiṅo rut (Jh -> rat)")
        elif is_abhyasta:
            suffix.text = 'at' + suffix.text[1:]
            prakriya.log("Rule 7.1.4: ad abhyastAt (Jh -> at)")
        elif is_atmanepada and is_anat: 
            suffix.text = 'at' + suffix.text[1:]
            prakriya.log("Rule 7.1.5: ātmanepadeṣv anataḥ (Jh -> at)")
        else: 
            suffix.text = 'ant' + suffix.text[1:]
            prakriya.log("Rule 7.1.3: jho 'ntaḥ (Jh -> ant)")

def at_agama(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and set(['laN', 'luN', 'lfN']).intersection(suffix.tags):
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if is_vowel(clean_dhatu[0]):
            agama = Term('Aw', 'Agama')
            prakriya.log("Rule 6.4.72: āḍ ajādīnām (Inserted 'Aw' augment)")
        else:
            agama = Term('aw', 'Agama')
            prakriya.log("Rule 6.4.71: Inserted 'aw' past tense augment")
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, agama)

def itasca(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if set(['laN', 'liN', 'luN', 'lfN', 'ASIrliN']).intersection(suffix.tags):
        if suffix.text.endswith('i') and suffix.upadeza in['tip', 'sip', 'mip', 'Ji']:
            suffix.text = suffix.text[:-1]
            prakriya.log("Rule 3.4.100: itaśca (Dropped terminal 'i')")

def hali_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text and t2.text and t2.text[0] in SLP1_CONSONANTS:
            clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), t1.text)
            if clean_dhatu == 'kf' and t1.text.endswith('ur'): continue 
            if t1.text == 'div':
                t1.text = 'dIv'
                prakriya.log("Rule 8.2.77: hali ca (div -> dIv)")
            elif t1.text.endswith('ir') or t1.text.endswith('ur') or t1.text.endswith('iv') or t1.text.endswith('uv'):
                vowel = t1.text[-2]
                cons = t1.text[-1]
                if vowel == 'i':
                    t1.text = t1.text[:-2] + 'I' + cons
                    prakriya.log(f"Rule 8.2.77: hali ca ({t1.text[-2:]} -> I{cons} before hal)")
                elif vowel == 'u':
                    t1.text = t1.text[:-2] + 'U' + cons
                    prakriya.log(f"Rule 8.2.77: hali ca ({t1.text[-2:]} -> U{cons} before hal)")

def it_agama(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    is_anit = False
    clean_dhatu = dhatu.text if dhatu else ''
    if dhatu:
        for tag in dhatu.tags:
            if tag.startswith('clean_'):
                clean_dhatu = tag.split('_')[1]
        if clean_dhatu in ANIT_ROOTS: is_anit = True
        elif clean_dhatu == 'duh' and 'gana_2' in dhatu.tags: is_anit = True
        if 'sanadi' in dhatu.tags: is_anit = False

    has_lrt_lrn = any(lak in term.tags for term in prakriya.terms for lak in ['lfW', 'lfN'])
    is_parasmai = dhatu and 'parasmaipada' in dhatu.tags
    is_lit = any('liW' in term.tags for term in prakriya.terms)
            
    for term in prakriya.terms[1:]:
        if 'ardhadhatuka' in term.tags and term.text and term.text[0] in VAL_CONSONANTS:
            if dhatu and dhatu.text == 'kf' and 'liW' in term.tags: continue
            is_kit = 'kit' in term.tags
            if is_kit and dhatu and dhatu.text and (dhatu.text == 'SrI' or dhatu.text[-1] in['u', 'U', 'f', 'F', 'x', 'X']):
                prakriya.log(f"Rule 7.2.11: sryukah kiti blocked 'iw' for '{term.upadeza}'")
                continue
            is_anit_for_this = is_anit
            if clean_dhatu == 'gam' and has_lrt_lrn and is_parasmai: is_anit_for_this = False
            if clean_dhatu == 'gam' and term.upadeza == 'san': is_anit_for_this = False
            
            is_vet = clean_dhatu in VET_ROOTS
            if is_vet and term.upadeza in['sya', 'tAsi']:
                if prakriya.vikalpa:
                    is_anit_for_this = True
                    prakriya.log(f"Rule 7.2.42-45: Applied Aniṭ vikalpa for Veṭ root '{clean_dhatu}'")
                else:
                    is_anit_for_this = False
                    prakriya.log(f"Rule 7.2.42-45: Applied Seṭ vikalpa for Veṭ root '{clean_dhatu}'")
            elif is_lit:
                KR_ADI =['kf', 'sf', 'Bf', 'vf', 'stu', 'dru', 'sru', 'Sru']
                if clean_dhatu in KR_ADI: is_anit_for_this = True
                else: is_anit_for_this = False
            if clean_dhatu == 'Svi' and term.upadeza in['kta', 'ktavatu']:
                is_anit_for_this = True
            if clean_dhatu == 'vas' and 'gana_1' in dhatu.tags and term.upadeza in ['kta', 'ktavatu', 'ktvA']:
                is_anit_for_this = False


            if not is_anit_for_this: 
                if clean_dhatu == 'grah' and not is_lit:
                    term.text = 'I' + term.text
                    prakriya.log(f"Rule 7.2.37: graho'liṭi dīrghaḥ (Added 'Iw')")
                else:
                    term.text = 'i' + term.text
                    prakriya.log(f"Rule 7.2.35: Added 'iw' augment")

def idito_num_dhatoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'idit' in dhatu.tags:
        if dhatu.text in['Cid', 'Bid']: return 
        text = dhatu.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                dhatu.text = text[:i+1] + 'M' + text[i+1:]
                prakriya.log(f"Rule 7.1.58: Applied 'num' -> {dhatu.text}")
                break

def liti_dhator_anabhyasasya(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and 'liW' in suffix.tags:
        abhyasa = Term(dhatu.upadeza, 'abhyasa')
        abhyasa.text = dhatu.text
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, abhyasa)
        prakriya.log(f"Rule 6.1.8: Reduplicated root -> '{abhyasa.text}'")

def hrasvah(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        short_map = {'A':'a', 'I':'i', 'U':'u', 'F':'f', 'X':'x', 'e':'i', 'o':'u', 'E':'i', 'O':'u'}
        for long_v, short_v in short_map.items():
            text = text.replace(long_v, short_v)
        abhyasa.text = text
        prakriya.log(f"Rule 7.4.59: Shortened Abhyasa -> '{abhyasa.text}'")

def ur_at(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa and ('f' in abhyasa.text or 'F' in abhyasa.text):
        abhyasa.text = abhyasa.text.replace('f', 'a').replace('F', 'a')
        prakriya.log("Rule 7.4.66: 'f' -> 'a' in abhyasa")

def kuhos_cuh(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        char_map = {'k':'c', 'K':'C', 'g':'j', 'G':'J', 'N':'Y', 'h':'j'}
        new_text = "".join([char_map.get(c, c) for c in text])
        if new_text != text:
            abhyasa.text = new_text
            prakriya.log(f"Rule 7.4.62: kuhoS cuH -> '{abhyasa.text}'")

def bhavater_ah(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if abhyasa and dhatu and dhatu.upadeza == 'BU':
        abhyasa.text = abhyasa.text.replace('u', 'a').replace('U', 'a')
        prakriya.log(f"Rule 7.4.73: bhavater aH -> '{abhyasa.text}'")

def abhyase_car_ca(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        deaspirate = {'B':'b', 'D':'d', 'G':'g', 'J':'j', 'Q':'q', 'P':'p', 'T':'t', 'K':'k', 'C':'c', 'W':'w'}
        new_text = "".join([deaspirate.get(c, c) for c in text])
        if new_text != text:
            abhyasa.text = new_text
            prakriya.log(f"Rule 8.4.54: abhyAse car ca -> '{abhyasa.text}'")

def bhuvo_vug_lunlitoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    lakara = next((t for t in prakriya.terms if set(['liW', 'luN']).intersection(t.tags)), None)
    if dhatu and dhatu.upadeza == 'BU' and lakara:
        idx = prakriya.terms.index(dhatu)
        next_val = ''
        for i in range(idx + 1, len(prakriya.terms)):
            if prakriya.terms[i].text:
                next_val = prakriya.terms[i].text
                break
        if next_val and is_vowel(next_val[0]):
            dhatu.text = dhatu.text + 'v'
            prakriya.log("Rule 6.4.88: Added 'vug' augment to BU")

def sarvadhatukam_apit(prakriya: Prakriya) -> None:
    for term in prakriya.terms:
        if 'sarvadhatuka' in term.tags or 'tin' in term.tags or 'Sit' in term.tags:
            if 'pit' not in term.tags:
                term.tags.add('Nit')
                prakriya.log(f"Rule 1.2.4: Added 'Nit' tag to apit sarvadhatuka '{term.upadeza}'")

def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    if 'Nit' in next_term.tags or 'kit' in next_term.tags: return
    is_sarva = 'sarvadhatuka' in next_term.tags or 'tin' in next_term.tags or 'Sit' in next_term.tags
    is_ardha = 'ardhadhatuka' in next_term.tags
    if is_sarva or is_ardha:
        text = dhatu.text
        if text and text[-1] in IK_VOWELS:
            dhatu.text = text[:-1] + apply_guna(text[-1])
            prakriya.log(f"Rule 7.3.84: Guna on terminal vowel -> '{dhatu.text}'")
        elif len(text) >= 2 and text[-2] in['i', 'u', 'f', 'x'] and text[-1] not in SLP1_VOWELS:
            dhatu.text = text[:-2] + apply_guna(text[-2]) + text[-1]
            prakriya.log(f"Rule 7.3.86: Guna on penultimate vowel -> '{dhatu.text}'")

def aco_nniti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]
    if 'Rit' in suffix.tags or 'Yit' in suffix.tags:
        text = dhatu.text
        if text and text[-1] in SLP1_VOWELS:
            dhatu.text = text[:-1] + apply_vrddhi(text[-1])
            prakriya.log(f"Rule 7.2.115: aco YRiti Vrddhi -> '{dhatu.text}'")

def ata_upadhayah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1] 
    if dhatu and ('Yit' in suffix.tags or 'Rit' in suffix.tags):
        text = dhatu.text
        if len(text) >= 2 and text[-2] == 'a':
            dhatu.text = text[:-2] + 'A' + text[-1]
            prakriya.log(f"Rule 7.2.116: ata upadhAyAH Vrddhi -> '{dhatu.text}'")

def eco_yayavayah(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        text = t1.text
        if text and text[-1] in EC_VOWELS and t2.text:
            last_char = text[-1]
            next_char = t2.text[0]
            rep = None
            if is_vowel(next_char):
                if last_char == 'e': rep = 'ay'
                elif last_char == 'o': rep = 'av'
                elif last_char == 'E': rep = 'Ay'
                elif last_char == 'O': rep = 'Av'
                if rep:
                    t1.text = text[:-1] + rep
                    prakriya.log(f"Rule 6.1.78: eco'yavAyAvaH -> '{t1.text}'")
            elif next_char == 'y' and last_char in['o', 'O']:
                if last_char == 'o': rep = 'av'
                elif last_char == 'O': rep = 'Av'
                if rep:
                    t1.text = text[:-1] + rep
                    prakriya.log(f"Rule 6.1.79: vAnto yi pratyaye -> '{t1.text}'")

def iko_yanaci(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms) - 1):
        term1 = prakriya.terms[i]
        term2 = prakriya.terms[i+1]
        if term1.text and term2.text and term1.text[-1] in IK_VOWELS and is_vowel(term2.text[0]):
            last_char = term1.text[-1]
            rep = ''
            if last_char in['i', 'I']: rep = 'y'
            elif last_char in ['u', 'U']: rep = 'v'
            elif last_char in ['f', 'F']: rep = 'r'
            elif last_char == 'x': rep = 'l'
            if rep: 
                term1.text = term1.text[:-1] + rep
                prakriya.log(f"Rule 6.1.77: iko yaRaci -> '{term1.text}'")

def ato_dirgho_yayi(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if not vikarana: return
    idx = prakriya.terms.index(vikarana)
    if idx + 1 < len(prakriya.terms):
        next_term = prakriya.terms[idx + 1]
        if vikarana.text.endswith('a') and next_term.text and next_term.text[0] in YAY_CONSONANTS:
            vikarana.text = vikarana.text[:-1] + 'A'
            prakriya.log("Rule 7.3.101: Lengthened 'a' to 'A'")

def ato_gune(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and dhatu.text.endswith('a') and vikarana.text and vikarana.text.startswith(('a', 'A')):
        if dhatu != vikarana:
            dhatu.text = dhatu.text[:-1]
            prakriya.log("Rule 6.1.97: Merged Dhatu 'a' + Vikarana")
    if vikarana and vikarana.text.endswith('a'):
        idx = prakriya.terms.index(vikarana)
        if idx + 1 < len(prakriya.terms):
            next_term = prakriya.terms[idx + 1]
            if next_term.text:
                first_char = next_term.text[0]
                if first_char in['a', 'e', 'o', 'A']:
                    vikarana.text = vikarana.text[:-1]
                    prakriya.log(f"Rule 6.1.97: Merged Vikarana 'a' + Suffix '{first_char}'")

def ato_nitah(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'vikaraRa' and t1.text.endswith('a') and t2.text.startswith('A') and 'pit' not in t2.tags:
            t1.text = t1.text[:-1]
            t2.text = 'e' + t2.text[1:]
            prakriya.log("Rule 7.2.81: Ato NitaH (a + A -> e)")

def hrasvasya_piti_krti_tuk(prakriya: Prakriya) -> None:
    """Rule 6.1.71: hrasvasya piti kṛti tuk. Adds 't' augment after short vowel before a pit kṛt affix."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text and t1.text[-1] in ['a', 'i', 'u', 'f', 'x']:
            if 'pit' in t2.tags and t2.term_type == 'pratyaya':
                t1.text = t1.text + 't'
                prakriya.log("Rule 6.1.71: hrasvasya piti kṛti tuk (Added 't')")

def aane_muk(prakriya: Prakriya) -> None:
    """Rule 7.2.82: āne muk. Adds 'm' (muk) before 'Ana' after 'a'."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text.endswith('a') and t2.text and t2.text.startswith('Ana'):
            t2.text = 'm' + t2.text
            prakriya.log("Rule 7.2.82: āne muk (Added 'm' before 'Ana')")

def adesa_pratyayayoh(prakriya: Prakriya) -> None:
    for i, curr_term in enumerate(prakriya.terms):
        if curr_term.term_type in ['dhatu', 'upasarga', 'abhyasa']: continue
        text = curr_term.text
        if 's' in text:
            idx = text.find('s')
            is_last_term = (i == len(prakriya.terms) - 1)
            is_last_char = (idx == len(text) - 1)
            if is_last_term and is_last_char: continue 
            if idx > 0: prev_char = text[idx-1]
            else:
                if i > 0 and prakriya.terms[i-1].text: prev_char = prakriya.terms[i-1].text[-1]
                else: continue 
            if prev_char in IN_VOWELS or prev_char in['k', 'K', 'g', 'G', 'N']:
                curr_term.text = text[:idx] + 'z' + text[idx+1:]
                prakriya.log(f"Rule 8.3.59: Changed 's' to 'z' after '{prev_char}'")

def jhasas_tathor_dho_dhah(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text[-1] in JHAS_CONSONANTS:
            if t1.term_type == 'dhatu' and t1.text == 'D':
                if i > 0 and prakriya.terms[i-1].text in ['da', 'Da']:
                    continue
            if t2.text.startswith('t'): 
                t2.text = 'D' + t2.text[1:]
                prakriya.log("Rule 8.2.40: 't' -> 'D' after jhaz")
            elif t2.text.startswith('T'): 
                t2.text = 'D' + t2.text[1:]
                prakriya.log("Rule 8.2.40: 'T' -> 'D' after jhaz")

def dadhas_tathor_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text == 'D':
            if i > 0 and prakriya.terms[i-1].text == 'da':
                if t2.text and t2.text.startswith(('t', 'T')):
                    prakriya.terms[i-1].text = 'Da'
                    prakriya.log("Rule 8.2.38: dadhas tathorś ca (daD -> DaD before t/T)")

def mo_no_dhatoh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text.endswith('m'):
            if t2.text and t2.text[0] in['m', 'v']:
                t1.text = t1.text[:-1] + 'n'
                prakriya.log("Rule 8.2.64: mo no dhātoḥ (m -> n before m/v)")

def jhalam_jas_jhasi(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text[-1] in JHAL_CONSONANTS and t2.text and t2.text[0] in JHAS_SOFT_CONSONANTS:
            last_char = t1.text[-1]
            jas_char = last_char
            if last_char in ['k', 'K', 'g', 'G', 'h']: jas_char = 'g'
            elif last_char in['c', 'C', 'j', 'J', 'S']: jas_char = 'j'
            elif last_char in['w', 'W', 'q', 'Q', 'z']: jas_char = 'q'
            elif last_char in['t', 'T', 'd', 'D', 's']: jas_char = 'd'
            elif last_char in['p', 'P', 'b', 'B']: jas_char = 'b'
            if jas_char != last_char:
                t1.text = t1.text[:-1] + jas_char
                prakriya.log(f"Rule 8.4.53: Changed '{last_char}' to '{jas_char}' (jaS)")

def khari_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text[-1] in JHAL_CONSONANTS and t2.text and t2.text[0] in KHAR_CONSONANTS:
            last_char = t1.text[-1]
            char_map = {'g':'k', 'G':'k', 'k':'k', 'K':'k', 'j':'c', 'J':'c', 'c':'c', 'C':'c', 'q':'w', 'Q':'w', 'w':'w', 'W':'w', 'd':'t', 'D':'t', 't':'t', 'T':'t', 'b':'p', 'B':'p', 'p':'p', 'P':'p'}
            if last_char in char_map and char_map[last_char] != last_char:
                t1.text = t1.text[:-1] + char_map[last_char]
                prakriya.log(f"Rule 8.4.55: Changed '{last_char}' to '{char_map[last_char]}' (khari ca)")


def stuna_stuh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text:
            last_char = t1.text[-1]
            first_char = t2.text[0]
            if last_char in ['z', 'w', 'W', 'q', 'Q', 'R']:
                stu_map = {'s': 'z', 't': 'w', 'T': 'W', 'd': 'q', 'D': 'Q', 'n': 'R'}
                if first_char in stu_map:
                    t2.text = stu_map[first_char] + t2.text[1:]
                    prakriya.log(f"Rule 8.4.41: '{first_char}' -> '{stu_map[first_char]}' (zwunA zwuH)")

def vrasca_bhrasja_sruja_mruja(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t2.text and t2.text[0] in JHAL_CONSONANTS:
            clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), t1.text)
            targets =['vraSc', 'Brajj', 'sfj', 'mfj', 'yaj', 'rAj', 'BrAj']
            if clean_dhatu in targets or t1.text.endswith('C') or t1.text.endswith('S') or t1.text.endswith('cC'):
                if t1.text.endswith('Sc') or t1.text.endswith('jj') or t1.text.endswith('cC'):
                    t1.text = t1.text[:-2] + 'z'
                else:
                    t1.text = t1.text[:-1] + 'z'
                prakriya.log(f"Rule 8.2.36: Final palatal/C/S became 'z' -> '{t1.text}'")

def ho_dhah_dader_ghah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    if dhatu.text.endswith('h') and suffix.text and suffix.text[0] in JHAL_CONSONANTS:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'nah':
            dhatu.text = dhatu.text[:-1] + 'D'
            prakriya.log("Rule 8.2.34: nho dhaḥ (nah -> naD)")
        elif dhatu.text.startswith('d'):
            dhatu.text = dhatu.text[:-1] + 'G'
            prakriya.log("Rule 8.2.32: 'h' -> 'G' (dAder dhAtor ghaH)")
        else:
            dhatu.text = dhatu.text[:-1] + 'Q'
            prakriya.log("Rule 8.2.31: 'h' -> 'Q' (ho DhaH)")



def samyogantasya_lopah(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    text = suffix.text
    if len(text) >= 2 and text[-1] in SLP1_CONSONANTS and text[-2] in SLP1_CONSONANTS:
        suffix.text = text[:-1]
        prakriya.log(f"Rule 8.2.23: Dropped final consonant -> '{suffix.text}'")

def rutva_visarga(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text.endswith('s'):
        suffix.text = suffix.text[:-1] + 'H'
        prakriya.log("Rule 8.3.15: Terminal 's' -> Visarga 'H'")

def dhatvadeh_sah_sah_no_nah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text:
        text = dhatu.text
        if text.startswith('z'):
            dhatu.tags.add('original_sh')
            text = 's' + text[1:]
            if text.startswith('sW'): text = 'sT' + text[2:]
            elif text.startswith('sw'): text = 'st' + text[2:]
            elif text.startswith('sR'): text = 'sn' + text[2:]
            dhatu.text = text
            prakriya.log("Rule 6.1.64: Initial 'z' -> 's'")
        elif text.startswith('R'):
            dhatu.text = 'n' + text[1:]
            prakriya.log("Rule 6.1.65: Initial 'R' -> 'n'")

def paghra_sthadi_adesha(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    if 'Sit' in next_term.tags:
        adesha_map = {
            'pA': 'piba', 'GrA': 'jiGra', 'DmA': 'Dama', 
            'sTA': 'tizWa', 'mnA': 'mana', 'dfS': 'pazya', 
            'f': 'fcCa', 'sf': 'DAva', 'Sad': 'zIya', 'sad': 'sIda',
            'gam': 'gacCa', 'yam': 'yacCa', 'iz': 'icCa'
        }
        if dhatu.text in adesha_map:
            dhatu.text = adesha_map[dhatu.text]
            prakriya.log(f"Rule 7.3.78: Root replaced -> '{dhatu.text}'")

def pug_nau(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    ric_term = next((t for t in prakriya.terms if t.upadeza == 'Ric'), None)
    if ric_term and dhatu.text.endswith('A'):
        dhatu.text = dhatu.text + 'p'
        prakriya.log(f"Rule 7.3.36: Added 'puk' augment -> '{dhatu.text}'")

def yuvor_anakau(prakriya: Prakriya) -> None:
    for term in prakriya.terms:
        if term.term_type == 'pratyaya':
            if term.text == 'yu': 
                term.text = 'ana'
                prakriya.log("Rule 7.1.1: 'yu' -> 'ana'")
            elif term.text == 'vu': 
                term.text = 'aka'
                prakriya.log("Rule 7.1.1: 'vu' -> 'aka'")


def sanadyanta_dhatavah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), prakriya.terms[0])
        new_text = "".join(t.text for t in prakriya.terms)
        dhatu.text = new_text
        dhatu.upadeza = new_text
        tags_to_remove =[t for t in dhatu.tags if t.startswith('gana_') or t.startswith('clean_')]
        for t in tags_to_remove:
            dhatu.tags.remove(t)
        dhatu.tags.add('gana_1')
        dhatu.tags.add('sanadi')
        prakriya.terms = [dhatu]
        prakriya.log(f"Rule 3.1.32: Merged into Secondary Root -> '{dhatu.text}'")

def sna_sandhi(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text == 'nA': 
        is_weak = 'pit' not in suffix.tags
        if is_weak:
            if suffix.text and is_vowel(suffix.text[0]):
                vikarana.text = 'n'
                prakriya.log("Rule 6.4.112: 'nA' -> 'n' before vowel")
            else:
                vikarana.text = 'nI'
                prakriya.log("Rule 6.4.113: 'nA' -> 'nI' before consonant")

def anunasikalopo_jhali_kniti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    is_kit_or_nit = 'kit' in suffix.tags or 'Nit' in suffix.tags
    starts_with_jhal = suffix.text and suffix.text[0] in JHAL_CONSONANTS
    ends_with_nasal = dhatu.text and dhatu.text[-1] in['m', 'n']

    if is_kit_or_nit and starts_with_jhal and ends_with_nasal:
        ANUDATTA_NASAL_ROOTS =['ram', 'gam', 'han', 'man', 'yam', 'van', 'tan', 'nam']
        clean_dhatu = dhatu.text
        for tag in dhatu.tags:
            if tag.startswith('clean_'): clean_dhatu = tag.split('_')[1]
        
        if clean_dhatu in ANUDATTA_NASAL_ROOTS:
            dhatu.text = dhatu.text[:-1]
            prakriya.log(f"Rule 6.4.37: Dropped nasal -> '{dhatu.text}'")

def se_mucadinam(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and vikarana.upadeza == 'Sa':
        MUC_ADI =['muc', 'lup', 'vid', 'lip', 'sic', 'kft', 'Kid', 'piz']
        if dhatu.text in MUC_ADI:
            text = dhatu.text
            for i in range(len(text)-1, -1, -1):
                if is_vowel(text[i]):
                    dhatu.text = text[:i+1] + 'M' + text[i+1:]
                    prakriya.log(f"Rule 7.1.59: Added 'num' -> '{dhatu.text}'")
                    break

def anusvarasya_yayi_parasavarnah(prakriya: Prakriya) -> None:
    for i, term in enumerate(prakriya.terms):
        if 'M' in term.text:
            text = term.text
            new_text = ""
            for j in range(len(text)):
                if text[j] == 'M':
                    next_char = ''
                    if j + 1 < len(text):
                        next_char = text[j+1]
                    elif i + 1 < len(prakriya.terms) and prakriya.terms[i+1].text:
                        next_char = prakriya.terms[i+1].text[0]
                    
                    if next_char in YAY_PRATYAHARA:
                        if next_char in['k', 'K', 'g', 'G', 'N']: new_text += 'N'
                        elif next_char in['c', 'C', 'j', 'J', 'Y']: new_text += 'Y'
                        elif next_char in['w', 'W', 'q', 'Q', 'R']: new_text += 'R'
                        elif next_char in['t', 'T', 'd', 'D', 'n']: new_text += 'n'
                        elif next_char in ['p', 'P', 'b', 'B', 'm']: new_text += 'm'
                        else: new_text += 'M'
                    else:
                        new_text += 'M'
                else:
                    new_text += text[j]
            if term.text != new_text:
                term.text = new_text
                prakriya.log(f"Rule 8.4.58: Parasavarna Sandhi -> '{term.text}'")

def upasarga_satva(prakriya: Prakriya) -> None:
    upasargas =[t for t in prakriya.terms if t.term_type == 'upasarga']
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if upasargas and dhatu and upasargas[-1].text:
        if upasargas[-1].text[-1] in IN_VOWELS:
            if dhatu.text.startswith('sT'):
                dhatu.text = 'zW' + dhatu.text[2:]
                prakriya.log("Rule 8.3.65: Upasarga Satva (sT -> zW)")
            elif dhatu.text.startswith('s') and any(dhatu.text.startswith(stem) for stem in['sId', 'su', 'stu', 'sic', 'saYj']):
                dhatu.text = 'z' + dhatu.text[1:]
                prakriya.log("Rule 8.3.65/66: Upasarga Satva (s -> z)")


def vikarana_guna(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text in ['u', 'nu'] and 'pit' in suffix.tags:
        if vikarana.text == 'u': vikarana.text = 'o'
        elif vikarana.text == 'nu': vikarana.text = 'no'
        prakriya.log(f"Rule 7.3.84: Guna applied to Vikarana -> '{vikarana.text}'")

def kr_u_morphing(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if dhatu and dhatu.upadeza == 'qukfY' and vikarana and vikarana.upadeza == 'u':
        if 'pit' not in suffix.tags:
            dhatu.text = 'kur'
            prakriya.log("Rule 6.4.110: 'kf' -> 'kur' before weak 'u'")
        else:
            dhatu.text = 'kar'
            prakriya.log("Rule 7.3.84: 'kf' -> 'kar' before strong 'u'")
            
    if vikarana and vikarana.upadeza in ['u', 'Snu'] and 'pit' not in suffix.tags:
        if suffix.text.startswith('v') or suffix.text.startswith('m'):
            if vikarana.text.endswith('u'):
                vikarana.text = vikarana.text[:-1]
                prakriya.log("Rule 6.4.107/108: Dropped 'u' before 'v/m'")

def haladi_seshah(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        SAR = ['S', 'z', 's']
        KHAY =['K', 'P', 'C', 'W', 'T', 'c', 'w', 't', 'k', 'p']
        
        initial_cluster =[]
        for i, char in enumerate(text):
            if is_vowel(char):
                break
            initial_cluster.append(char)
            
        first_v = next((c for c in text if is_vowel(c)), '')
        
        if not initial_cluster:
            abhyasa.text = first_v
            return
            
        surviving_cons = initial_cluster[0]
        if len(initial_cluster) >= 2 and initial_cluster[0] in SAR and initial_cluster[1] in KHAY:
            surviving_cons = initial_cluster[1]
            prakriya.log(f"Rule 7.4.61: śarpūrvāḥ khayaḥ -> '{surviving_cons}'")
        else:
            prakriya.log(f"Rule 7.4.60: halādi śeṣaḥ -> '{surviving_cons}'")
            
        abhyasa.text = surviving_cons + first_v

def srujidrusor_jhaly_amakiti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    is_jhal = suffix.text and suffix.text[0] in JHAL_CONSONANTS
    is_akit = 'kit' not in suffix.tags and 'Nit' not in suffix.tags

    if is_jhal and is_akit:
        if dhatu.text == 'dfS':
            dhatu.text = 'draS'
            prakriya.log("Rule 6.1.58: 'dfS' -> 'draS' (am augment)")
        elif dhatu.text == 'sfj':
            dhatu.text = 'sraj'
            prakriya.log("Rule 6.1.58: 'sfj' -> 'sraj' (am augment)")

def nascapadantasya_jhali(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)):
        term = prakriya.terms[i]
        text = term.text
        new_text = ""
        for j, char in enumerate(text):
            if char in['m', 'n']:
                if j + 1 < len(text) and text[j+1] in JHAL_CONSONANTS:
                    new_text += 'M'
                    prakriya.log(f"Rule 8.3.24: '{char}' -> 'M' before jhal '{text[j+1]}'")
                elif j == len(text) - 1 and i + 1 < len(prakriya.terms) and prakriya.terms[i+1].text and prakriya.terms[i+1].text[0] in JHAL_CONSONANTS:
                    new_text += 'M'
                    prakriya.log(f"Rule 8.3.24: '{char}' -> 'M' before jhal '{prakriya.terms[i+1].text[0]}'")
                else:
                    new_text += char
            else:
                new_text += char
        term.text = new_text


def ato_yuk(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    if dhatu.text.endswith('A') and ('Rit' in next_term.tags or 'Yit' in next_term.tags) and 'tin' not in next_term.tags:
        dhatu.text = dhatu.text + 'y'
        prakriya.log("Rule 7.3.33: āto yuk ciṇkṛtoḥ (Added 'yuk')")

def id_yati(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    if dhatu.text.endswith('A') and next_term.upadeza == 'yat':
        dhatu.text = dhatu.text[:-1] + 'e'
        prakriya.log("Rule 6.4.65: A -> e before 'yat'")

def akah_savarne_dirghah(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms) - 1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text:
            v1 = t1.text[-1]
            v2 = t2.text[0]
            if v1 in ['a', 'A'] and v2 in['a', 'A']:
                t1.text = t1.text[:-1] + 'A'
                t2.text = t2.text[1:]
                prakriya.log("Rule 6.1.101: Savarna Dirgha (A)")
            elif v1 in ['i', 'I'] and v2 in ['i', 'I']:
                t1.text = t1.text[:-1] + 'I'
                t2.text = t2.text[1:]
                prakriya.log("Rule 6.1.101: Savarna Dirgha (I)")
            elif v1 in['u', 'U'] and v2 in ['u', 'U']:
                t1.text = t1.text[:-1] + 'U'
                t2.text = t2.text[1:]
                prakriya.log("Rule 6.1.101: Savarna Dirgha (U)")

def slau_reduplication(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and vikarana.upadeza == 'Slu':
        if not any(t.term_type == 'abhyasa' for t in prakriya.terms):
            abhyasa = Term(dhatu.upadeza, 'abhyasa')
            abhyasa.text = dhatu.text
            idx = prakriya.terms.index(dhatu)
            prakriya.terms.insert(idx, abhyasa)
            prakriya.log(f"Rule 6.1.10: Reduplicated root for Slu -> '{abhyasa.text}'")

def snasor_allopah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and ('sarvadhatuka' in suffix.tags or 'tin' in suffix.tags):
        is_weak = ('kit' in suffix.tags or 'Nit' in suffix.tags) and 'pit' not in suffix.tags
        if is_weak:
            if dhatu.text == 'as':
                dhatu.text = 's'
                prakriya.log("Rule 6.4.111: śnasor allopaḥ ('as' -> 's')")
            elif 'gana_7' in dhatu.tags and 'na' in dhatu.text:
                idx = dhatu.text.rfind('na')
                if idx != -1:
                    dhatu.text = dhatu.text[:idx] + 'n' + dhatu.text[idx+2:]
                    prakriya.log("Rule 6.4.111: śnasor allopaḥ ('na' -> 'n')")

def tasyasti_lopa(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('s') and t1.upadeza in ['as', 'tAsi']:
            if t2.text.startswith('s'):
                t1.text = t1.text[:-1]
                prakriya.log("Rule 7.4.50: tāsyastilopaḥ ('s' deleted before 's')")

def lin_agamas(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if 'liN' in suffix.tags or 'ASIrliN' in suffix.tags:
        if dhatu and 'atmanepada' in dhatu.tags:
            agama = Term('sIy', 'Agama')
            if 'ASIrliN' in suffix.tags: agama.tags.add('kit')
            prakriya.terms.insert(-1, agama)
            prakriya.log("Rule 3.4.102: sIyuW augment for Atmanepada")
        else:
            agama = Term('yAs', 'Agama')
            agama.tags.add('yAsuW')
            if 'ASIrliN' in suffix.tags: agama.tags.add('kit')
            prakriya.terms.insert(-1, agama)
            prakriya.log("Rule 3.4.103: yAsuW augment for Parasmaipada")

def cli_agama(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if 'luN' in suffix.tags and dhatu:
        idx = prakriya.terms.index(dhatu) + 1
        is_karmani = 'karmani' in dhatu.tags
        if is_karmani and suffix.upadeza == 'ta': 
            cli = Term('ciR', 'vikaraRa')
            cli.text = 'i'
            cli.tags.add('Rit')
            cli.tags.add('cit')
            prakriya.log("Rule 3.1.66: ciṇ bhāvakarmaṇoḥ (Passive Aorist ciN)")
            suffix.text = '' 
            prakriya.terms.insert(idx, cli)
            return

        cli = Term('cli', 'vikaraRa')
        cli.tags.add('ardhadhatuka')
        clean_dhatu = ''
        for tag in dhatu.tags:
            if tag.startswith('clean_'): clean_dhatu = tag.split('_')[1]
            
        SAL_CONSONANTS = ['S', 'z', 's', 'h']
        IK_VOWELS =['i', 'I', 'u', 'U', 'f', 'F', 'x', 'X']
        upadha = dhatu.text[-2] if len(dhatu.text) > 1 else ''
        ends_in_sal = dhatu.text[-1] in SAL_CONSONANTS if dhatu.text else False
        
        is_anit = clean_dhatu in ANIT_ROOTS or (clean_dhatu == 'duh' and 'gana_2' in dhatu.tags) or clean_dhatu in['ruh', 'lih', 'kfS']
        
        if 'sanadi' in dhatu.tags:
            cli.text = 'a'
            cli.tags.add('caN')
            cli.tags.add('Nit')
            prakriya.log("Rule 3.1.48: ṇiśridrusrubhyaḥ kartari caṅ (cli -> caṅ)")
        elif clean_dhatu == 'vac':
            cli.text = 'a'
            cli.tags.add('Nit')
            cli.tags.add('aN')
            dhatu.text = 'voc'
            prakriya.log("Rule 3.1.52 & 7.4.20: asyati... & vacum um (vac -> voc)")
        elif clean_dhatu in ['gam', 'dfS'] or ('irit' in dhatu.tags and prakriya.vikalpa):
            cli.text = 'a'
            cli.tags.add('Nit')
            cli.tags.add('aN') 
            if 'irit' in dhatu.tags and prakriya.vikalpa:
                prakriya.log("Rule 3.1.57: irito vā (Optional cli -> aN triggered)")
            else:
                prakriya.log("Rule 3.1.55: puṣādi... cli -> aN")
        elif ends_in_sal and upadha in IK_VOWELS and is_anit:
            cli.text = 'sa'
            cli.tags.add('ksa')
            cli.tags.add('kit')
            prakriya.log("Rule 3.1.45: śala igupadhādaṇiṭaḥ ksaḥ (cli -> ksa)")
        else:
            cli.text = 's'
            prakriya.log("Rule 3.1.44: cleH sic (cli -> siC)")
        prakriya.terms.insert(idx, cli)

def gatistha_sic_lopa(prakriya: Prakriya) -> None:
    sic = next((t for t in prakriya.terms if t.upadeza == 'cli' and t.text == 's'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if sic and dhatu:
        clean_dhatu = ''
        for tag in dhatu.tags:
            if tag.startswith('clean_'): clean_dhatu = tag.split('_')[1]
        if clean_dhatu in['BU', 'sTA', 'dA', 'pA', 'gA']:
            sic.text = ''
            prakriya.log("Rule 2.4.77: sic elided after gA, sTA, dA, pA, BU")

def ato_heh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('a') and t2.text == 'hi':
            t2.text = ''
            prakriya.log("Rule 6.4.105: ato heH (dropped 'hi' after 'a')")

def ato_yeyah(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    yas = next((t for t in prakriya.terms if 'yAsuW' in t.tags), None)
    if vikarana and vikarana.text.endswith('a') and yas:
        yas.text = 'iy'
        prakriya.log("Rule 7.2.80: ato yeyaH (yAs -> iy after 'a')")

def lin_salopo_anantyasya(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'ASIrliN' in suffix.tags: return 
    for term in prakriya.terms:
        if 'yAsuW' in term.tags or term.upadeza == 'sIy':
            if 's' in term.text:
                term.text = term.text.replace('s', '')
                prakriya.log("Rule 7.2.79: liNaH salopo'nantyasya (dropped non-final 's')")

def ad_gunah(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text:
            if t1.text[-1] in['a', 'A'] and t2.text[0] in['i', 'I', 'u', 'U', 'f', 'F']:
                old_char = t2.text[0]
                rep = apply_guna(old_char)
                t1.text = t1.text[:-1] + rep
                t2.text = t2.text[1:]
                prakriya.log(f"Rule 6.1.87: Ad guNaH (a + {old_char} -> {rep})")

def lopo_vyorvali(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text[-1] in ['v', 'y'] and t2.text and t2.text[0] in VAL_CONSONANTS:
            dropped = t1.text[-1]
            t1.text = t1.text[:-1]
            prakriya.log(f"Rule 6.1.66: lopo vyorvali (dropped {dropped} before val)")

def usy_apadantat(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('A') and t2.text.startswith('us'):
            t1.text = t1.text[:-1]
            prakriya.log("Rule 6.1.96: usy apadAntAt (A + us -> us)")

def jher_jus(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.upadeza == 'Ji':
        if 'liN' in suffix.tags or 'ASIrliN' in suffix.tags:
            suffix.text = 'us'
            suffix.upadeza = 'us' 
            prakriya.log("Rule 3.4.108: jher jus (Ji -> us)")
        elif 'luN' in suffix.tags:
            has_sic = any(t.upadeza == 'cli' and t.text == 's' for t in prakriya.terms)
            dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
            is_abhyasta = dhatu and 'gana_3' in dhatu.tags
            is_vid = dhatu and dhatu.text == 'vid'
            is_aa_ending = dhatu and dhatu.text.endswith('A') and not has_sic
            if has_sic or is_abhyasta or is_vid or is_aa_ending:
                suffix.text = 'us'
                suffix.upadeza = 'us' 
                prakriya.log("Rule 3.4.109: sicabhyastavidibhyaś ca (Ji -> us)")

def jhasya_ran(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'liN' in suffix.tags and suffix.upadeza == 'Ja':
        suffix.text = 'ran'
        suffix.upadeza = 'ran'
        prakriya.log("Rule 3.4.105: jhasya ran (Ja -> ran for liN)")

def ito_at(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'liN' in suffix.tags and suffix.upadeza == 'iw':
        suffix.text = 'a'
        suffix.upadeza = 'a'
        prakriya.log("Rule 3.4.106: iwo't (iw -> a for liN)")

def utasca_pratyayad(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text.endswith('u') and suffix.text == 'hi':
        suffix.text = ''
        prakriya.log("Rule 6.4.106: utaśca (dropped 'hi' after 'u')")

def mer_nih(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'loW' in suffix.tags and suffix.upadeza == 'mip':
        suffix.text = 'ni'
        suffix.upadeza = 'ni' 
        prakriya.log("Rule 3.4.89: mer niH (mip -> ni)")

def ser_hi(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'loW' in suffix.tags and suffix.upadeza == 'sip':
        suffix.text = 'hi'
        suffix.upadeza = 'hi' 
        if 'pit' in suffix.tags: suffix.tags.remove('pit')
        prakriya.log("Rule 3.4.87: ser hy apic ca (sip -> hi, apit)")

def at_uttasya(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'loW' in suffix.tags and suffix.upadeza in['mip', 'ni', 'vas', 'mas']:
        suffix.text = 'A' + suffix.text
        suffix.tags.add('pit')
        if 'Nit' in suffix.tags: suffix.tags.remove('Nit')
        prakriya.log("Rule 3.4.92: Aw uttasya picca (Aw augment)")

def nityam_nitah(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if set(['laN', 'liN', 'luN', 'loW', 'lfN', 'ASIrliN']).intersection(suffix.tags) and suffix.text.endswith('s') and suffix.upadeza in['vas', 'mas']: 
        suffix.text = suffix.text[:-1]
        prakriya.log("Rule 3.4.99: nityaM NitaH (dropped final 's')")

def tasthasthamipam(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if set(['laN', 'liN', 'luN', 'loW', 'lfN', 'ASIrliN']).intersection(suffix.tags):
        if suffix.text == 'tas': suffix.text = 'tAm'
        elif suffix.text == 'Tas': suffix.text = 'tam'
        elif suffix.text == 'Ta': suffix.text = 'ta'
        elif suffix.text == 'mip' and 'loW' not in suffix.tags: 
            suffix.text = 'am'
        prakriya.log(f"Rule 3.4.101: Past/Opt/Aorist/Cond replacement -> '{suffix.text}'")

def er_uh(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'loW' in suffix.tags and suffix.text.endswith('i') and suffix.upadeza in['tip', 'Ji']:
        suffix.text = suffix.text[:-1] + 'u'
        prakriya.log("Rule 3.4.86: er uH (i -> u for loW)")

def gam_hana_jana_lopa(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]
    
    clean_dhatu = ''
    for tag in dhatu.tags:
        if tag.startswith('clean_'): clean_dhatu = tag.split('_')[1]
        
    is_kit_or_nit = 'kit' in suffix.tags or 'Nit' in suffix.tags
    is_vowel_initial = suffix.text and is_vowel(suffix.text[0])
    is_anang = 'aN' not in suffix.tags
    
    if clean_dhatu in['gam', 'han', 'jan', 'Kan', 'Gas'] and is_kit_or_nit and is_vowel_initial and is_anang:
        if dhatu.text.endswith('am') or dhatu.text.endswith('an') or dhatu.text.endswith('as'):
            dhatu.text = dhatu.text[:-2] + dhatu.text[-1]
            prakriya.log(f"Rule 6.4.98: Dropped penultimate 'a' -> '{dhatu.text}'")
            
        if clean_dhatu == 'han' and dhatu.text == 'hn':
            dhatu.text = 'Gn'
            prakriya.log("Rule 7.3.54 (implied for hn): 'hn' -> 'Gn'")

def che_ca(prakriya: Prakriya) -> None:
    for term in prakriya.terms:
        new_text = ""
        for i, char in enumerate(term.text):
            if char == 'C' and i > 0 and term.text[i-1] in['a', 'i', 'u', 'f', 'x']:
                new_text += 'cC'
            else:
                new_text += char
        if new_text != term.text:
            term.text = new_text
            prakriya.log("Rule 6.1.73: che ca (inserted 'c' before 'C')")
            
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text and t2.text.startswith('C') and t1.text[-1] in['a', 'i', 'u', 'f', 'x']:
            t2.text = 'c' + t2.text
            prakriya.log("Rule 6.1.73: che ca (inserted 'c' before 'C' across terms)")

def ekaco_baso_bhas(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]
    
    if dhatu.text and dhatu.text[-1] in['B', 'G', 'Q', 'D']:
        if suffix.text.startswith('s') or suffix.text.startswith('Dv'):
            bas_bhas = {'b': 'B', 'g': 'G', 'q': 'Q', 'd': 'D'}
            if dhatu.text[0] in bas_bhas:
                dhatu.text = bas_bhas[dhatu.text[0]] + dhatu.text[1:]
                prakriya.log(f"Rule 8.2.37: ekāco baśo bhaṣ -> '{dhatu.text}'")

def sadhoh_kas_si(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text and t2.text.startswith('s'):
            if t1.text[-1] in ['z', 'Q', 'G']:
                t1.text = t1.text[:-1] + 'k'
                prakriya.log("Rule 8.2.41: ṣaḍhoḥ kas si -> 'k' before 's'")

def sici_vrddhih(prakriya: Prakriya) -> None:
    sic = next((t for t in prakriya.terms if t.upadeza == 'cli' and t.text == 's'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if sic and dhatu and 'parasmaipada' in dhatu.tags:
        if dhatu.text[-1] in IK_VOWELS:
            dhatu.text = dhatu.text[:-1] + apply_vrddhi(dhatu.text[-1])
            prakriya.log("Rule 7.2.1: sici vṛddhiḥ -> Vṛddhi before sic")
        elif dhatu.text[-1] not in SLP1_VOWELS:
            clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
            if clean_dhatu == 'vaD':
                prakriya.log("Rule 7.2.4: neṭi (No vṛddhi for seṭ root vaD)")
            else:
                text = dhatu.text
                for i in range(len(text)-1, -1, -1):
                    if is_vowel(text[i]):
                        dhatu.text = text[:i] + apply_vrddhi(text[i]) + text[i+1:]
                        prakriya.log("Rule 7.2.3: vadavrajahalantasyācaḥ -> Vṛddhi before sic")
                        break

def asti_sico_aprkte(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = None
        insert_idx = -1
        for j in range(i+1, len(prakriya.terms)):
            if prakriya.terms[j].text:
                t2 = prakriya.terms[j]
                insert_idx = j
                break
        if not t2: continue

        clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), t1.text)
        is_as_or_sic = (t1.term_type == 'dhatu' and clean_dhatu == 'as') or (t1.upadeza == 'cli' and t1.text == 's')
        
        if is_as_or_sic and t2.text in['t', 's']:
            agama = Term('I', 'Agama')
            prakriya.terms.insert(insert_idx, agama)
            prakriya.log("Rule 7.3.96: astisico'pṛkte (Inserted 'I' augment)")
            break

def do_dad_ghoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if not dhatu or not abhyasa: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    is_weak = 'kit' in next_term.tags or 'Nit' in next_term.tags
    is_cons = next_term.text and next_term.text[0] not in SLP1_VOWELS

    if is_weak and is_cons:
        if clean_dhatu == 'dA':
            dhatu.text = 'd'
            prakriya.log("Rule 7.4.46: do dad ghoH (dA -> d)")
        elif clean_dhatu == 'DA':
            dhatu.text = 'D'
            prakriya.log("Rule 7.4.46: do dad ghoH (DA -> D)")

def snabhyastayor_atah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if not dhatu or not abhyasa: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    is_weak = 'kit' in next_term.tags or 'Nit' in next_term.tags
    is_vowel = next_term.text and next_term.text[0] in SLP1_VOWELS
    
    if is_weak and is_vowel and dhatu.text.endswith('A'):
        dhatu.text = dhatu.text[:-1]
        prakriya.log("Rule 6.4.112: śnābhyastayor ātaḥ (Dropped A)")


def sino_gunah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and ('sarvadhatuka' in suffix.tags or 'tin' in suffix.tags):
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'SI':
            dhatu.text = 'Se'
            prakriya.log("Rule 7.4.22: śiṅo guṇaḥ (SI -> Se)")


def dho_dhe_lopah(prakriya: Prakriya) -> None:
    """Rule 8.3.13: ḍho ḍhe lopaḥ & Rule 6.3.111: ḍhralope pūrvasya dīrgho'ṇaḥ"""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('Q') and t2.text.startswith('Q'):
            t1.text = t1.text[:-1]
            prakriya.log("Rule 8.3.13: dho dhe lopah (dropped 'Q' before 'Q')")
            
            if t1.text and t1.text[-1] in['a', 'i', 'u']:
                clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), '')
                if clean_dhatu in ['sah', 'vah'] and t1.text[-1] == 'a':
                    t1.text = t1.text[:-1] + 'o'
                    prakriya.log("Rule 6.3.112: sahivahor od avarṇasya (a -> o instead of A)")
                else:
                    dirgha_map = {'a': 'A', 'i': 'I', 'u': 'U'}
                    old_vowel = t1.text[-1]
                    t1.text = t1.text[:-1] + dirgha_map[old_vowel]
                    prakriya.log(f"Rule 6.3.111: dhralope purvasya dirgho'nah ({old_vowel} -> {dirgha_map[old_vowel]})")
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        pass

def kramah_parasmaipadesu(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and 'Sit' in vikarana.tags:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'kram' and 'parasmaipada' in dhatu.tags:
            dhatu.text = 'krAm'
            prakriya.log("Rule 7.3.76: kramaḥ parasmaipadeṣu (kram -> krAm)")

def ata_au_nalah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and dhatu.text.endswith('A') and suffix.upadeza == 'Ral':
        suffix.text = 'O'
        prakriya.log("Rule 7.1.34: āta au ṇalaḥ (ṇal -> au)")

def ghvasor_ed_hau(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text in ['hi', 'Di']:
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
        abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
        if dhatu:
            clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
            if clean_dhatu in ['dA', 'DA']:
                dhatu.text = 'de' if clean_dhatu == 'dA' else 'De'
                if abhyasa:
                    abhyasa.text = ''
                suffix.text = 'hi' 
                prakriya.log("Rule 6.4.119: ghvāsor eddhāv (ghu -> e, abhyāsa dropped)")
            elif clean_dhatu == 'as':
                dhatu.text = 'e'
                suffix.text = 'Di'
                prakriya.log("Rule 6.4.119: ghvāsor eddhāv (as -> e)")

def vrddhir_eci(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text:
            if t1.text[-1] in ['a', 'A'] and t2.text[0] in['e', 'o', 'E', 'O']:
                old_t2_start = t2.text[0]
                rep = apply_vrddhi(old_t2_start)
                t1.text = t1.text[:-1] + rep
                t2.text = t2.text[1:]
                prakriya.log(f"Rule 6.1.88: vrddhir eci (a/A + {old_t2_start} -> {rep})")

def jna_janor_ja(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and 'Sit' in vikarana.tags:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu in['jYA', 'jan']:
            dhatu.text = 'jA'
            prakriya.log(f"Rule 7.3.79: jñājanor jā ({clean_dhatu} -> jA)")

def lity_abhyasasya(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if abhyasa and dhatu and any('liW' in t.tags for t in prakriya.terms):
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'vac':
            abhyasa.text = 'u'
            prakriya.log("Rule 6.1.17: liṭy abhyāsasyobhayeṣām (vac -> u)")
        elif clean_dhatu == 'svap':
            abhyasa.text = 'su'
            prakriya.log("Rule 6.1.17: liṭy abhyāsasyobhayeṣām (svap -> su)")
        elif clean_dhatu == 'yaj':
            abhyasa.text = 'i'
            prakriya.log("Rule 6.1.17: liṭy abhyāsasyobhayeṣām (yaj -> i)")

def lut_prathamasya_daraurasah(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'luW' in suffix.tags:
        if suffix.upadeza in['tip', 'ta']:
            suffix.text = 'A'
            suffix.upadeza = 'qA'
            suffix.tags.add('qit')
            prakriya.log("Rule 2.4.85: luṭaḥ prathamasya (tip/ta -> ḍā)")
        elif suffix.upadeza in ['tas', 'AtAm']:
            suffix.text = 'rO'
            suffix.upadeza = 'rO'
            prakriya.log("Rule 2.4.85: luṭaḥ prathamasya (tas/ātām -> rau)")
        elif suffix.upadeza in ['Ji', 'Ja']:
            suffix.text = 'ras'
            suffix.upadeza = 'ras'
            prakriya.log("Rule 2.4.85: luṭaḥ prathamasya (jhi/jha -> ras)")

def diti_teh_lopa(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if 'qit' in t2.tags and t1.text:
            text = t1.text
            ti_index = -1
            for j in range(len(text)-1, -1, -1):
                if is_vowel(text[j]):
                    ti_index = j
                    break
            if ti_index != -1:
                t1.text = text[:ti_index]
                prakriya.log(f"Rule 6.4.143: ṭeḥ lopa (Deleted '{text[ti_index:]}')")

def ri_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('s') and t1.upadeza in ['as', 'tAsi']:
            if t2.text.startswith('r'):
                t1.text = t1.text[:-1]
                prakriya.log("Rule 7.4.51: ri ca ('s' deleted before 'r')")

def h_eti(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text.endswith('s') and t1.upadeza == 'tAsi':
            if t2.text.startswith('e'):
                t1.text = t1.text[:-1] + 'h'
                prakriya.log("Rule 7.4.52: h eṭi (s -> h before e)")

def rin_sayaglinksu(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text and t1.text[-1] == 'f':
            if ('yAsuW' in t2.tags and 'kit' in t2.tags) or t2.upadeza == 'yak':
                t1.text = t1.text[:-1] + 'ri'
                prakriya.log("Rule 7.4.28: riṅ śayaglinkṣu (ṛ -> ri)")



def damsa_sanja_svanjam_sapi(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and vikarana.upadeza == 'Sap':
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu in ['daMS', 'saYj', 'svaYj']:
            dhatu.text = dhatu.text.replace('M', '').replace('Y', '')
            prakriya.log(f"Rule 6.4.25: daṃśa-sañja-svañjāṃ śapi (Dropped nasal in {clean_dhatu})")

def hanter_jah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix.text == 'hi':
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'han':
            dhatu.text = 'ja'
            prakriya.log("Rule 6.4.36: hanter jaḥ (han -> ja)")

def hrasvad_angat(prakriya: Prakriya) -> None:
    for i in range(1, len(prakriya.terms)-1):
        t_prev = prakriya.terms[i-1]
        t_curr = prakriya.terms[i]
        t_next = prakriya.terms[i+1]
        
        if t_curr.upadeza == 'cli' and t_curr.text == 's':
            if t_prev.text and t_prev.text[-1] in ['a', 'i', 'u', 'f', 'x']:
                if t_next.text and t_next.text[0] in JHAL_CONSONANTS:
                    t_curr.text = ''
                    prakriya.log("Rule 8.2.27: hrasvād aṅgāt (Dropped sic after short vowel before jhal)")

def atas_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = None
        for j in range(i+1, len(prakriya.terms)):
            if prakriya.terms[j].text:
                t2 = prakriya.terms[j]
                break
                
        if t1.upadeza == 'Aw' and t1.text == 'A' and t2 and t2.text and is_vowel(t2.text[0]):
            old_vowel = t2.text[0]
            rep = apply_vrddhi(old_vowel)
            t1.text = rep
            t2.text = t2.text[1:]
            prakriya.log(f"Rule 6.1.90: āṭaś ca (A + {old_vowel} -> {rep})")


def rdriso_ngi_gunah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]

    if next_term.term_type == 'vikaraRa' and 'aN' in next_term.tags:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'dfS':
            dhatu.text = 'darS'
            prakriya.log("Rule 7.4.16: ṛdṛśo'ṅi guṇaḥ (dfS -> darS)")
        elif dhatu.text.endswith('f') or dhatu.text.endswith('F'):
            dhatu.text = dhatu.text[:-1] + apply_guna(dhatu.text[-1])
            prakriya.log("Rule 7.4.16: ṛdṛśo'ṅi guṇaḥ (Guna before aN)")

def rta_id_dhatoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text.endswith('F'):
        text = dhatu.text
        if len(text) >= 2 and text[-2] in['p', 'P', 'b', 'B', 'm', 'v']:
            dhatu.text = text[:-1] + 'ur'
            prakriya.log("Rule 7.1.102: ud oṣṭhyapūrvasya (F -> ur)")
        else:
            dhatu.text = text[:-1] + 'ir'
            prakriya.log("Rule 7.1.100: ṝta id dhātoḥ (F -> ir)")

def jhalo_jhali(prakriya: Prakriya) -> None:
    for i in range(1, len(prakriya.terms)-1):
        t_prev = prakriya.terms[i-1]
        t_curr = prakriya.terms[i]
        t_next = prakriya.terms[i+1]
        
        if t_curr.text == 's':
            prev_char = t_prev.text[-1] if t_prev.text else ''
            next_char = t_next.text[0] if t_next.text else ''
            if prev_char in JHAL_CONSONANTS and next_char in JHAL_CONSONANTS:
                t_curr.text = ''
                prakriya.log("Rule 8.2.26: jhalo jhali (Dropped 's' between jhals)")

def revert_sh_after_abhyasa(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if abhyasa and dhatu and abhyasa.text and dhatu.text:
        if abhyasa.text[-1] in IN_VOWELS:
            clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), '')
            if 'original_sh' in dhatu.tags and dhatu.text.startswith('s'):
                dhatu.text = 'z' + dhatu.text[1:]
                if dhatu.text.startswith('zT'): dhatu.text = 'zW' + dhatu.text[2:]
                elif dhatu.text.startswith('zt'): dhatu.text = 'zw' + dhatu.text[2:]
                elif dhatu.text.startswith('zn'): dhatu.text = 'zR' + dhatu.text[2:]
                prakriya.log("Rule 8.3.116: Reverted 's' to 'z' after abhyasa")

def sasa_id_anghaloh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    is_kit_or_nit = 'kit' in next_term.tags or 'Nit' in next_term.tags
    is_haladi = next_term.text and next_term.text[0] not in SLP1_VOWELS
    
    if clean_dhatu == 'SAs':
        if next_term.text in ['hi', 'Di']:
            dhatu.text = 'SA'
            prakriya.log("Rule 6.4.35: śā hau (SAs -> SA before hi/dhi)")
        elif is_kit_or_nit and is_haladi:
            dhatu.text = 'Siz'
            prakriya.log("Rule 6.4.34: śāsa id aṅhaloḥ (SAs -> Siz)")

    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    is_kit_or_nit = 'kit' in next_term.tags or 'Nit' in next_term.tags
    is_haladi = next_term.text and next_term.text[0] not in SLP1_VOWELS
    
    if clean_dhatu == 'SAs':
        if next_term.text in['hi', 'Di']:
            dhatu.text = 'SA'
            prakriya.log("Rule 6.4.35: śā hau (SAs -> SA before hi/dhi)")
        elif is_kit_or_nit and is_haladi:
            dhatu.text = 'Siz'
            prakriya.log("Rule 6.4.34: śāsa id aṅhaloḥ (SAs -> Siz)")

def ita_iti(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms) - 1):
        curr = prakriya.terms[i]
        next_term = prakriya.terms[i+1]
        if curr.upadeza == 'cli' and curr.text == 'is':
            if next_term.text.startswith('I'):
                curr.text = 'i'
                prakriya.log("Rule 8.2.28: iṭa īṭi (Deleted 's' between iṭ and īṭ)")

def nisthayam_seti(prakriya: Prakriya) -> None:
    """Rule 6.4.52: niṣṭhāyāṃ seṭi. Drops ṇi (final 'i') before seṭ niṣṭhā."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and 'sanadi' in dhatu.tags and dhatu.text.endswith('i'):
        if suffix.upadeza in ['kta', 'ktavatu'] and suffix.text.startswith('i'):
            dhatu.text = dhatu.text[:-1]
            prakriya.log("Rule 6.4.52: niṣṭhāyāṃ seṭi (Dropped ṇi before seṭ niṣṭhā)")

def labh_rabh_num(prakriya: Prakriya) -> None:
    """Rule 7.1.64: labheś ca. Adds 'num' to rabh/labh before Ṇic."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    ric_term = next((t for t in prakriya.terms if t.upadeza == 'Ric'), None)
    if dhatu and ric_term:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu in['laB', 'raB'] and 'M' not in dhatu.text:
            text = dhatu.text
            for i in range(len(text)-1, -1, -1):
                if is_vowel(text[i]):
                    dhatu.text = text[:i+1] + 'M' + text[i+1:]
                    prakriya.log(f"Rule 7.1.64: labheś ca (Added 'num' -> '{dhatu.text}')")
                    break

def er_lini(prakriya: Prakriya) -> None:
    """Rule 6.4.67: er liṅi. ā -> e before y-initial ārdhadhātuka liṅ for specific roots."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and 'ASIrliN' in suffix.tags and 'parasmaipada' in dhatu.tags:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        # Inherits root list from 6.4.66
        GHU_MA_STHA =['dA', 'DA', 'do', 'de', 'De', 'mA', 'me', 'sTA', 'gA', 'pA', 'hA', 'sA', 'so']
        if clean_dhatu in GHU_MA_STHA and dhatu.text.endswith('A'):
            dhatu.text = dhatu.text[:-1] + 'e'
            prakriya.log("Rule 6.4.67: er liṅi (A -> e before yAs)")

def aniditam_hala_upadhayah_kniti(prakriya: Prakriya) -> None:
    """Rule 6.4.24: aniditāṃ hala upadhāyāḥ kṅiti. Drops penultimate nasal in anidit halanta roots before kit/ṅit."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    if 'kit' in suffix.tags or 'Nit' in suffix.tags:
        if 'idit' not in dhatu.tags:
            # Protect roots that didn't ORIGINALLY have a nasal (like muc/chid)
            clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
            if len(clean_dhatu) >= 2 and clean_dhatu[-2] not in['M', 'Y', 'R', 'n', 'm']: return
            
            if dhatu.text and dhatu.text[-1] not in SLP1_VOWELS:
                text = dhatu.text
                if len(text) >= 2:
                    penultimate = text[-2]
                    if penultimate in['M', 'Y', 'R', 'n', 'm']:
                        dhatu.text = text[:-2] + text[-1]
                        prakriya.log(f"Rule 6.4.24: aniditāṃ hala upadhāyāḥ (Dropped penultimate nasal '{penultimate}')")

def mrjer_vrddhih(prakriya: Prakriya) -> None:
    """Rule 7.2.114: mṛjer vṛddhiḥ."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    if 'Nit' in next_term.tags or 'kit' in next_term.tags: return
    
    is_sarva_ardha = 'sarvadhatuka' in next_term.tags or 'ardhadhatuka' in next_term.tags or 'tin' in next_term.tags or 'Sit' in next_term.tags
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    
    if clean_dhatu == 'mfj' and is_sarva_ardha:
        dhatu.text = 'mArj'
        prakriya.log("Rule 7.2.114: mṛjer vṛddhiḥ (mfj -> mArj)")


def can_abhyasa_vowel(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if 'can_abhyasa' in t.tags), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if abhyasa and dhatu:
        root_vowel = next((c for c in dhatu.text if is_vowel(c)), 'a')
        abh_vowel = 'U' if root_vowel in ['u', 'U'] else 'I'
        
        text = abhyasa.text
        new_text = ""
        vowel_seen = False
        for char in text:
            if is_vowel(char):
                if not vowel_seen:
                    new_text += abh_vowel
                    vowel_seen = True
            else:
                new_text += char
        abhyasa.text = new_text
        prakriya.log(f"Sanvadbhāva & Dīrgho Laghoḥ for caṅ -> '{abhyasa.text}'")

def jes_ca(prakriya: Prakriya) -> None:
    """Rule 7.3.57: jeś ca. 'j' of 'ji' becomes 'g' after abhyāsa."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if dhatu and abhyasa:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), '')
        if clean_dhatu == 'ji' and dhatu.text.startswith('j'):
            dhatu.text = 'g' + dhatu.text[1:]
            prakriya.log("Rule 7.3.57: jeś ca (ji -> gi after abhyāsa)")
def stha_adi_ita(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    if 'kit' in next_term.tags or 'Nit' in next_term.tags:
        if next_term.upadeza == 'yak':
            if dhatu.text in['dA', 'DA', 'sTA', 'pA', 'mA', 'gA', 'hA']:
                dhatu.text = dhatu.text[:-1] + 'I'
                prakriya.log("Rule 6.4.66: ghumāsthāgāpā... I before yak")
        elif next_term.text and next_term.text.startswith('t'):
            if dhatu.text == 'sTA':
                dhatu.text = 'sTi'
                prakriya.log("Rule 7.4.40: sTA -> sTi before kit starting with t")
            elif dhatu.text == 'pA':
                dhatu.text = 'pI'
                prakriya.log("Rule 6.4.66: pA -> pI before kit")
            elif dhatu.text == 'dA':
                dhatu.text = 'dat'
                prakriya.log("Rule 7.4.46: dA -> dat before kit")
            elif dhatu.text == 'mA':
                dhatu.text = 'mi'
                prakriya.log("Rule 7.4.40: mA -> mi before kit")
            elif dhatu.text == 'DA':
                dhatu.text = 'hi'
                prakriya.log("Rule 7.4.42: dadhāter hiḥ (DA -> hi before ta)")
            elif dhatu.text == 'gA':
                dhatu.text = 'gI'
                prakriya.log("Rule 6.4.66: ghumāsthāgāpā... (gA -> gI before kit)")

def adeca_upadese_asiti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    is_ardha = any('ardhadhatuka' in t.tags for t in prakriya.terms[idx+1:])
    
    if is_ardha and 'Sit' not in next_term.tags:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu and clean_dhatu[-1] in ['e', 'o', 'E', 'O']:
            text = dhatu.text
            if text and text[-1] in ['e', 'o', 'E', 'O']:
                dhatu.text = text[:-1] + 'A'
                prakriya.log("Rule 6.1.45: ādeca upadeśe'śiti (ec -> A)")

def can_reduplication(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    can = next((t for t in prakriya.terms if 'caN' in t.tags), None)
    if dhatu and can:
        if dhatu.text.endswith('i'):
            dhatu.text = dhatu.text[:-1]
            prakriya.log("Rule 6.4.51: ṇer aniṭi (Dropped Ṇic before caṅ)")
        
        text = dhatu.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                short_vowel = {'A':'a', 'I':'i', 'U':'u', 'F':'f', 'X':'x', 'e':'i', 'o':'u', 'E':'i', 'O':'u'}.get(text[i], text[i])
                if short_vowel != text[i]:
                    dhatu.text = text[:i] + short_vowel + text[i+1:]
                    prakriya.log("Rule 7.4.1: ṇau caṅy upadhāyā hrasvaḥ (Shortened root vowel)")
                break
                
        # Now that svApi -> svAp -> svap, we can check for it perfectly!
        if dhatu.text == 'svap':
            dhatu.text = 'sup'
            prakriya.log("Rule 6.1.18: svapi... caṅi samprasāraṇam (svap -> sup)")
            
        abhyasa = Term(dhatu.upadeza, 'abhyasa')
        abhyasa.tags.add('can_abhyasa')
        abhyasa.text = dhatu.text
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, abhyasa)
        prakriya.log(f"Rule 6.1.11: caṅi (Reduplicated root -> '{abhyasa.text}')")

def vacisvapiyajadinam_kiti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1] 
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    is_kit = 'kit' in next_term.tags
    is_nit = 'Nit' in next_term.tags
    
    if is_kit:
        if clean_dhatu == 'vac': 
            dhatu.text = 'uc'
            prakriya.log("Rule 6.1.15: Samprasarana (vac -> uc)")
        elif clean_dhatu == 'svap': 
            dhatu.text = 'sup'
            prakriya.log("Rule 6.1.15: Samprasarana (svap -> sup)")
        elif clean_dhatu == 'yaj': 
            dhatu.text = 'ij'
            prakriya.log("Rule 6.1.15: Samprasarana (yaj -> ij)")
        elif clean_dhatu == 'vap': 
            dhatu.text = 'up'
            prakriya.log("Rule 6.1.15: Samprasarana (vap -> up)")
        elif clean_dhatu == 'vah': 
            dhatu.text = 'uh'
            prakriya.log("Rule 6.1.15: Samprasarana (vah -> uh)")
        elif clean_dhatu == 'vad': 
            dhatu.text = 'ud'
            prakriya.log("Rule 6.1.15: Samprasarana (vad -> ud)")
        elif clean_dhatu == 'vas': 
            dhatu.text = 'us'
            prakriya.log("Rule 6.1.15: Samprasarana (vas -> us)")
        elif clean_dhatu == 'hve':
            dhatu.text = 'hU'
            prakriya.log("Rule 6.1.32: hvaḥ samprasāraṇam (hve -> hU before kit)")
        elif clean_dhatu == 'Svi':
            dhatu.text = 'SU'
            prakriya.log("Rule 6.1.30 & 6.4.2: śvayaḥ samprasāraṇam & halaḥ (Svi -> SU)")

    if is_kit or is_nit:
        if clean_dhatu == 'vraSc':
            dhatu.text = 'vfSc'
            prakriya.log("Rule 6.1.16: Samprasarana (vraSc -> vfSc)")
        elif clean_dhatu == 'praC':
            dhatu.text = 'pfC'
            prakriya.log("Rule 6.1.16: Samprasarana (praC -> pfC)")
        elif clean_dhatu == 'Brajj':
            dhatu.text = 'Bfjj'
            prakriya.log("Rule 6.1.16: Samprasarana (Brajj -> Bfjj)")
        elif clean_dhatu == 'vyaD':
            dhatu.text = 'viD'
            prakriya.log("Rule 6.1.16: Samprasarana (vyaD -> viD)")

    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1] 
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    is_kit = 'kit' in next_term.tags
    is_nit = 'Nit' in next_term.tags
    
    if is_kit:
        if clean_dhatu == 'vac': 
            dhatu.text = 'uc'
            prakriya.log("Rule 6.1.15: Samprasarana (vac -> uc)")
        elif clean_dhatu == 'svap': 
            dhatu.text = 'sup'
            prakriya.log("Rule 6.1.15: Samprasarana (svap -> sup)")
        elif clean_dhatu == 'yaj': 
            dhatu.text = 'ij'
            prakriya.log("Rule 6.1.15: Samprasarana (yaj -> ij)")
        elif clean_dhatu == 'vap': 
            dhatu.text = 'up'
            prakriya.log("Rule 6.1.15: Samprasarana (vap -> up)")
        elif clean_dhatu == 'vah': 
            dhatu.text = 'uh'
            prakriya.log("Rule 6.1.15: Samprasarana (vah -> uh)")
        elif clean_dhatu == 'vad': 
            dhatu.text = 'ud'
            prakriya.log("Rule 6.1.15: Samprasarana (vad -> ud)")
        elif clean_dhatu == 'grah':
            dhatu.text = 'gfh'
            prakriya.log("Rule 6.1.16: Samprasarana (grah -> gfh)")
        elif clean_dhatu == 'hve':
            dhatu.text = 'hU'
            prakriya.log("Rule 6.1.32: hvaḥ samprasāraṇam (hve -> hU before kit)")
        elif clean_dhatu == 'Svi':
            dhatu.text = 'SU'
            prakriya.log("Rule 6.1.30 & 6.4.2: śvayaḥ samprasāraṇam & halaḥ (Svi -> SU)")

    if is_kit or is_nit:
        if clean_dhatu == 'vraSc':
            dhatu.text = 'vfSc'
            prakriya.log("Rule 6.1.16: Samprasarana (vraSc -> vfSc)")
        elif clean_dhatu == 'praC':
            dhatu.text = 'pfC'
            prakriya.log("Rule 6.1.16: Samprasarana (praC -> pfC)")
        elif clean_dhatu == 'Brajj':
            dhatu.text = 'Bfjj'
            prakriya.log("Rule 6.1.16: Samprasarana (Brajj -> Bfjj)")
        elif clean_dhatu == 'vyaD':
            dhatu.text = 'viD'
            prakriya.log("Rule 6.1.16: Samprasarana (vyaD -> viD)")



def krpo_ro_lah(prakriya: Prakriya) -> None:
    """Rule 8.2.18: kṛpo ro laḥ."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), '')
        if clean_dhatu == 'kxp':
            new_text = dhatu.text.replace('r', 'l').replace('f', 'x').replace('F', 'X')
            if new_text != dhatu.text:
                dhatu.text = new_text
                prakriya.log("Rule 8.2.18: kṛpo ro laḥ (r -> l)")

def sasivasighasinam_ca(prakriya: Prakriya) -> None:
    """Rule 8.3.60: śāsivasighasīnāṃ ca. ṣatva for śās, vas, ghas after iṇ/ku."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 's' in dhatu.text:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), '')
        if clean_dhatu in['SAs', 'vas', 'Gas']:
            idx = dhatu.text.find('s')
            if idx > 0 and dhatu.text[idx-1] in IN_VOWELS.union(set(['k','K','g','G','N'])):
                dhatu.text = dhatu.text[:idx] + 'z' + dhatu.text[idx+1:]
                prakriya.log("Rule 8.3.60: śāsivasighasīnāṃ ca (s -> ṣ)")

def anunasikasya_kvijhaloh_kniti(prakriya: Prakriya) -> None:
    """Rule 6.4.15: anunāsikasya kvijhaloḥ kṅiti. Lengthens penultimate vowel of nasal roots before jhal kit/ṅit."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    if ('kit' in next_term.tags or 'Nit' in next_term.tags) and next_term.text and next_term.text[0] in JHAL_CONSONANTS:
        if dhatu.text.endswith('m') or dhatu.text.endswith('n'):
            text = dhatu.text
            if len(text) >= 2 and text[-2] == 'a':
                dhatu.text = text[:-2] + 'A' + text[-1]
                prakriya.log("Rule 6.4.15: anunāsikasya kvijhaloḥ kṅiti (a -> A)")








def ardhadhatuke_mula_parivartanam(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    lakara = next((t for t in prakriya.terms if t.term_type == 'lakara' or t.term_type == 'pratyaya'), None)
    if not dhatu: return
    
    is_ardha_lakara = lakara and any(lak in lakara.tags for lak in['liW', 'luW', 'lfW', 'luN', 'lfN', 'ASIrliN'])
    is_ardha = is_ardha_lakara or any('ardhadhatuka' in t.tags for t in prakriya.terms) or any(t.upadeza == 'cli' for t in prakriya.terms)
    
    if is_ardha:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'as':
            dhatu.text = 'BU'
            dhatu.upadeza = 'BU'
            dhatu.tags = set([t for t in dhatu.tags if not t.startswith('clean_')])
            dhatu.tags.add('clean_BU')
            prakriya.log("Rule 2.4.52: aster bhūḥ (as -> BU)")
        elif clean_dhatu == 'brU':
            dhatu.text = 'vac'
            dhatu.upadeza = 'vac'
            dhatu.tags = set([t for t in dhatu.tags if not t.startswith('clean_')])
            dhatu.tags.add('clean_vac')
            prakriya.log("Rule 2.4.53: bruvo vaciḥ (brU -> vac)")

    is_lun = any('luN' in t.tags for t in prakriya.terms)
    if is_lun:
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        is_karmani = 'karmani' in dhatu.tags or 'bhave' in dhatu.tags
        if clean_dhatu == 'han' and not is_karmani:
            dhatu.text = 'vaD'
            dhatu.upadeza = 'vaD'
            tags_to_remove =[t for t in dhatu.tags if t.startswith('clean_')]
            for t in tags_to_remove: dhatu.tags.remove(t)
            dhatu.tags.add('clean_vaD')
            prakriya.log("Rule 2.4.43: luṅi ca (han -> vaD in Aorist)")
        elif clean_dhatu == 'i' and 'parasmaipada' in dhatu.tags:
            dhatu.text = 'gA'
            dhatu.upadeza = 'gA'
            tags_to_remove =[t for t in dhatu.tags if t.startswith('clean_')]
            for t in tags_to_remove: dhatu.tags.remove(t)
            dhatu.tags.add('clean_gA')
            prakriya.log("Rule 2.4.45: iṇo gā luṅi (i -> gA)")

def han_ghatva_tatva(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    
    if clean_dhatu == 'han':
        if ('Rit' in next_term.tags or 'Yit' in next_term.tags) and next_term.upadeza not in['Ral', 'ciR']:
            if dhatu.text.endswith('n'):
                dhatu.text = dhatu.text[:-1] + 't'
                prakriya.log("Rule 7.3.32: hanato ñṇinnali (n -> t)")
                
        if ('Rit' in next_term.tags or 'Yit' in next_term.tags or (next_term.text and next_term.text.startswith('n'))):
            if dhatu.text.startswith('h'):
                dhatu.text = 'G' + dhatu.text[1:]
                prakriya.log("Rule 7.3.54: ho hanter ñṇinneṣu (h -> G)")
                
        if any(t.term_type == 'abhyasa' for t in prakriya.terms):
            if dhatu.text.startswith('h'):
                dhatu.text = 'G' + dhatu.text[1:]
                prakriya.log("Rule 7.3.55: abhyāsād dhasya (h -> G after abhyasa)")

def upasarga_sandhi(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    upasarga_indices =[i for i, t in enumerate(prakriya.terms) if t.term_type == 'upasarga']
    
    if dhatu and upasarga_indices:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        upa_term = prakriya.terms[upasarga_indices[-1]]
        if clean_dhatu == 'kf' and upa_term.text in ['sam', 'saM', 'saN', 'pari', 'upa']:
            dhatu.text = 's' + dhatu.text
            if upa_term.text.startswith('sa'):
                upa_term.text = 'saM' # Revert to saM before suT
            prakriya.log("Rule 6.1.137: samparyupebhyaḥ... (suṭ augment for kṛ)")
            
    for idx in reversed(upasarga_indices):
        upasarga = prakriya.terms[idx]
        next_term = None
        for j in range(idx + 1, len(prakriya.terms)):
            if prakriya.terms[j].text:
                next_term = prakriya.terms[j]
                break
                
        if next_term and is_vowel(next_term.text[0]):
            first_vowel = next_term.text[0]
            if upasarga.text.endswith('a') or upasarga.text.endswith('A'):
                if first_vowel in['a', 'A']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'A' + next_term.text[1:]
                elif first_vowel in ['i', 'I']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'e' + next_term.text[1:]
                elif first_vowel in ['u', 'U']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'o' + next_term.text[1:]
                elif first_vowel in ['f', 'F']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'Ar' + next_term.text[1:]
            elif upasarga.text.endswith('i') or upasarga.text.endswith('I'):
                upasarga.text = upasarga.text[:-1] + 'y'
            elif upasarga.text.endswith('u') or upasarga.text.endswith('U'):
                upasarga.text = upasarga.text[:-1] + 'v'
        
        if upasarga.text == 'sam' and next_term and next_term.text and next_term.text[0] not in SLP1_VOWELS:
            upasarga.text = 'saM'

def rashabhyam_no_nah(prakriya: Prakriya) -> None:
    has_trigger = False
    blocked = False
    allowed_intervening = set(SLP1_VOWELS).union(set('hyvrkKgGNpPbBmM'))
    
    full_str = "".join(t.text for t in prakriya.terms)
    char_idx = 0
    for term_idx, term in enumerate(prakriya.terms):
        new_text = ""
        for i, char in enumerate(term.text):
            if char in['r', 'z', 'f', 'F']:
                has_trigger = True
                blocked = False 
                new_text += char
            elif has_trigger and not blocked:
                if char == 'n':
                    next_char = full_str[char_idx+1] if char_idx + 1 < len(full_str) else ''
                    is_padanta = (char_idx == len(full_str) - 1)
                    if is_padanta:
                        new_text += 'n'
                    elif next_char in['t', 'T', 'd', 'D', 's']:
                        new_text += 'n'
                    else:
                        new_text += 'R'
                elif char not in allowed_intervening:
                    blocked = True
                    new_text += char
                else: new_text += char
            else: new_text += char
            char_idx += 1
            
        if term.text != new_text:
            term.text = new_text


def cjoh_ku_ghinnyatoh(prakriya: Prakriya) -> None:
    """Rule 7.3.52: cjoḥ ku ghiṇṇyatoḥ. c/j -> k/g before ghit or ṇyat."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    if 'Git' in suffix.tags or suffix.upadeza == 'Ryat':
        if dhatu.text.endswith('c'):
            dhatu.text = dhatu.text[:-1] + 'k'
            prakriya.log("Rule 7.3.52: cjoḥ ku ghiṇṇyatoḥ (c -> k)")
        elif dhatu.text.endswith('j'):
            dhatu.text = dhatu.text[:-1] + 'g'
            prakriya.log("Rule 7.3.52: cjoḥ ku ghiṇṇyatoḥ (j -> g)")

def aci_snu_dhatu_bhruvam(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        if not t1.text: continue
        t2 = None
        for j in range(i+1, len(prakriya.terms)):
            if prakriya.terms[j].text:
                t2 = prakriya.terms[j]
                break
        if t1.term_type == 'dhatu' and t2 and t2.text and t2.text[0] in['a', 'A', 'i', 'I', 'u', 'U', 'f', 'F', 'e', 'o', 'E', 'O', 'x', 'X']:
            clean_dhatu = next((tag.split('_')[1] for tag in t1.tags if tag.startswith('clean_')), t1.text)
            is_lit = any('liW' in t.tags for t in prakriya.terms)
            if t1.text[-1] in ['u', 'U']:
                if clean_dhatu == 'brU' or (is_lit and clean_dhatu in['Sru', 'stu', 'su', 'hu']):
                    t1.text = t1.text[:-1] + 'uv'
                    prakriya.log("Rule 6.4.77: aci śnudhātubhruvāṃ (u/U -> uv)")
            elif t1.text[-1] in ['i', 'I']:
                if clean_dhatu == 'i' and 'atmanepada' in t1.tags:
                    t1.text = t1.text[:-1] + 'iy'
                    prakriya.log("Rule 6.4.77: aci śnudhātubhruvāṃ (i/I -> iy)")

def choh_kuh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)):
        t = prakriya.terms[i]
        if not t.text: continue
        last_char = t.text[-1]
        if last_char in['c', 'C', 'j', 'J']:
            next_term = None
            for j in range(i+1, len(prakriya.terms)):
                if prakriya.terms[j].text:
                    next_term = prakriya.terms[j]
                    break
            is_padanta = not next_term
            next_char_is_jhal_or_n = False
            if next_term:
                nc = next_term.text[0]
                # JHAL_CONSONANTS or 'n' or 'm'
                next_char_is_jhal_or_n = nc in['J', 'B', 'G', 'Q', 'D', 'j', 'b', 'g', 'q', 'd', 'K', 'P', 'C', 'W', 'T', 'c', 'w', 't', 'k', 'p', 'S', 'z', 's', 'h', 'n', 'm']
            
            if is_padanta or next_char_is_jhal_or_n:
                map_ku = {'c':'k', 'C':'K', 'j':'g', 'J':'G'}
                if t.text.endswith('Sc'):
                    t.text = t.text[:-2] + 'k'
                else:
                    t.text = t.text[:-1] + map_ku[last_char]
                prakriya.log(f"Rule 8.2.30: coH kuH ({last_char} -> {map_ku.get(last_char, 'k')})")


def radabhyam_nishthato_nah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and suffix.upadeza in ['kta', 'ktavatu']:
        text = dhatu.text
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if text.endswith('d') or text.endswith('r') or 'odit' in dhatu.tags or clean_dhatu == 'Svi':
            if suffix.text.startswith('t'):
                suffix.text = 'n' + suffix.text[1:]
                if text.endswith('d'): dhatu.text = text[:-1] + 'n'
                prakriya.log("Rule 8.2.42/45: niṣṭhā 't' -> 'n'")

def skoh_samyogadyor_ante_ca(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)):
        t1 = prakriya.terms[i]
        if not t1.text: continue
        if t1.term_type == 'dhatu' and t1.text.startswith('mas') and t1.text[-1] in['j', 'g', 'c', 'k']:
            next_term = None
            for j in range(i+1, len(prakriya.terms)):
                if prakriya.terms[j].text:
                    next_term = prakriya.terms[j]
                    break
            if next_term and next_term.text[0] not in['a','A','i','I','u','U','f','F','e','o','E','O','x','X']:
                t1.text = 'ma' + t1.text[-1]
                prakriya.log("Rule 8.2.29: skoḥ saṃyogādyor ante ca (masj -> maj)")

    word = "".join(t.text for t in prakriya.terms)
    if len(word) >= 2 and word[-1] not in['a','A','i','I','u','U','f','F','e','o','E','O','x','X'] and word[-2] in ['s', 'k']:
        for i in range(len(prakriya.terms)):
            if 'yAsuW' in prakriya.terms[i].tags and prakriya.terms[i].text.endswith('s'):
                subs = "".join(t.text for t in prakriya.terms[i+1:])
                if len(subs) >= 1 and subs[0] not in['a','A','i','I','u','U','f','F','e','o','E','O','x','X']:
                    prakriya.terms[i].text = prakriya.terms[i].text[:-1]
                    prakriya.log("Rule 8.2.29: skoḥ saṃyogādyor ante ca (Dropped 's')")
                    break


def sanyan_reduplication(prakriya: Prakriya) -> None:
    """Rule 6.1.9: sanyaṅoḥ. Reduplicates the root for san and yaṅ."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    san_or_yan = next((t for t in prakriya.terms if t.upadeza in['san', 'yaN']), None)
    if dhatu and san_or_yan:
        abhyasa = Term(dhatu.upadeza, 'abhyasa')
        abhyasa.text = dhatu.text
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, abhyasa)
        prakriya.log(f"Rule 6.1.9: sanyaṅoḥ (Reduplicated root -> '{abhyasa.text}')")

def sany_atah(prakriya: Prakriya) -> None:
    """Rule 7.4.79: sany ataḥ. 'a' in the abhyāsa becomes 'i' before san."""
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    san = next((t for t in prakriya.terms if t.upadeza == 'san'), None)
    if abhyasa and san:
        if abhyasa.text.endswith('a'):
            abhyasa.text = abhyasa.text[:-1] + 'i'
            prakriya.log("Rule 7.4.79: sany ataḥ (abhyāsa 'a' -> 'i')")

def iko_jhal(prakriya: Prakriya) -> None:
    """Rule 1.2.9: iko jhal. san becomes kit after iganta roots or jhal-ending roots with ik penultimate."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    san = next((t for t in prakriya.terms if t.upadeza == 'san'), None)
    if dhatu and san and 'i' not in san.text:
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        is_iganta = clean_dhatu[-1] in IK_VOWELS
        is_igupadha_jhalanta = len(clean_dhatu) >= 2 and clean_dhatu[-1] in JHAL_CONSONANTS and clean_dhatu[-2] in IK_VOWELS
        if is_iganta or is_igupadha_jhalanta:
            san.tags.add('kit')
            prakriya.log("Rule 1.2.9: iko jhal (san becomes kit)")

def ajjhanagamam_sani(prakriya: Prakriya) -> None:
    """Rule 6.4.16: aj hanagamāṃ sani. Lengthens ajanta, han, gam before kit/ṅit/aniṭ san."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    san = next((t for t in prakriya.terms if t.upadeza == 'san'), None)
    if dhatu and san and 'i' not in san.text: # Must be aniṭ (iṭ wasn't added)
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if dhatu.text[-1] in SLP1_VOWELS or clean_dhatu in ['han', 'gam']:
            if dhatu.text[-1] in['i', 'u', 'f', 'x', 'a']:
                dirgha_map = {'a': 'A', 'i': 'I', 'u': 'U', 'f': 'F', 'x': 'X'}
                dhatu.text = dhatu.text[:-1] + dirgha_map[dhatu.text[-1]]
                prakriya.log("Rule 6.4.16: ajjhanagamāṃ sani (Lengthened before san)")

def sanyan_rta_id_dhatoh(prakriya: Prakriya) -> None:
    """Rule 7.1.100: ṛta id dhātoḥ. ṛ/ṝ -> ir/ur before san."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    san = next((t for t in prakriya.terms if t.upadeza == 'san'), None)
    if dhatu and san and (dhatu.text.endswith('f') or dhatu.text.endswith('F')):
        text = dhatu.text
        if len(text) >= 2 and text[-2] in['p', 'P', 'b', 'B', 'm', 'v']:
            dhatu.text = text[:-1] + 'ur'
            prakriya.log("Rule 7.1.102: ud oṣṭhyapūrvasya (ṛ/ṝ -> ur)")
        else:
            dhatu.text = text[:-1] + 'ir'
            prakriya.log("Rule 7.1.100: ṛta id dhātoḥ (ṛ/ṝ -> ir)")
