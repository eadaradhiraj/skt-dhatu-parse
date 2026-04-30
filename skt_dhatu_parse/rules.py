"""
rules.py
The comprehensive library of Paninian Sutras.
"""
from .shivasutras import get_pratyahara, is_vowel, SLP1_VOWELS
from .models import Term, Prakriya

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
    if char in ['f', 'F']: return 'Ar'
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
        new_suffix = TIN_ATMANEPADA[purusha][vacana]
    else:
        new_suffix = TIN_PARASMAIPADA_LIT[purusha][vacana] if is_lit else TIN_PARASMAIPADA[purusha][vacana]
        
    lakara.text = new_suffix
    lakara.upadeza = new_suffix
    lakara.term_type = 'pratyaya'
    lakara.tags.add('tin') 
    
    # Add Wit tag to lakara if it's a Tit lakara (laW, liW, luW, lfW, leW, loW)
    if any(lak in lakara.tags for lak in['laW', 'liW', 'luW', 'lfW', 'leW', 'loW']):
        lakara.tags.add('Wit')
        
    if is_lit: 
        lakara.tags.add('ardhadhatuka')
        if new_suffix in['Ral', 'Tal']: lakara.tags.add('pit')
        else: lakara.tags.add('kit')
    else: 
        lakara.tags.add('sarvadhatuka')
    prakriya.log(f"Rule 3.4.78: Substituted lakara with '{new_suffix}'")

def insert_vikarana(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if not dhatu: return
    idx = prakriya.terms.index(dhatu) + 1 
    
    if 'lfW' in suffix.tags:
        vik = Term('sya', 'vikaraRa')
        vik.tags.add('ardhadhatuka')
        prakriya.terms.insert(idx, vik)
        prakriya.log("Rule 3.1.33: Inserted 'sya' for Future Tense")
        return
        
    if 'luN' in suffix.tags:
        return # cli is handled natively as a lakara-specific augment

    if 'ardhadhatuka' in suffix.tags: return

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

def mit_aco_antyat_parah(prakriya: Prakriya) -> None:
    """Rule 1.1.47: mid aco'ntyāt paraḥ. Inserts 'mit' augment after the last vowel of the root."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.upadeza == 'Snam'), None)
    if dhatu and vikarana and vikarana.text:
        text = dhatu.text
        last_vowel_idx = -1
        for i, char in enumerate(text):
            if is_vowel(char):
                last_vowel_idx = i
        if last_vowel_idx != -1:
            dhatu.text = text[:last_vowel_idx+1] + vikarana.text + text[last_vowel_idx+1:]
            vikarana.text = ''
            prakriya.log(f"Rule 1.1.47: Inserted 'mit' ({vikarana.upadeza}) into root -> '{dhatu.text}'")

def bruva_it(prakriya: Prakriya) -> None:
    """Rule 7.3.93: bruva īṭ. Adds 'I' augment before halādi pit sārvadhātuka."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    
    # Must jump over empty 'luk' vikarana to find the actual suffix
    suffix = None
    insert_idx = -1
    for i in range(idx + 1, len(prakriya.terms)):
        if prakriya.terms[i].text:
            suffix = prakriya.terms[i]
            insert_idx = i
            break
            
    if not suffix: return

    # Use the clean tag to match against 'brU' regardless of original upadeśa markers (like brUY)
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
    if dhatu and 'atmanepada' in dhatu.tags and 'Wit' in suffix.tags:
        text = suffix.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                suffix.text = text[:i] + 'e'
                prakriya.log(f"Rule 3.4.79 (Tere): '{text[i:]}' -> 'e'")
                break

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
        is_abhyasta = dhatu and 'gana_3' in dhatu.tags
        is_anat = dhatu and any(g in dhatu.tags for g in['gana_2', 'gana_3', 'gana_5', 'gana_7', 'gana_8', 'gana_9'])
        
        if suffix.upadeza == 'Ja' and 'liN' in suffix.tags:
            pass # Handled by jhasya_ran
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
    if dhatu and set(['laN', 'luN']).intersection(suffix.tags):
        agama = Term('aw', 'Agama')
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, agama)
        prakriya.log("Rule 6.4.71: Inserted 'aw' past tense augment")

def itasca(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if set(['laN', 'liN', 'luN']).intersection(suffix.tags):
        if suffix.text.endswith('i') and suffix.upadeza in['tip', 'sip', 'mip', 'Ji']:
            suffix.text = suffix.text[:-1]
            prakriya.log("Rule 3.4.100: itaśca (Dropped terminal 'i')")

def hali_ca(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text == 'div':
        dhatu.text = 'dIv'
        prakriya.log("Rule 8.2.77: Lengthened 'div' to 'dIv'")

def it_agama(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    is_anit = False
    clean_dhatu = dhatu.text if dhatu else ''
    
    if dhatu:
        # Check original clean root tag (to survive text mutations like sTA -> sTi)
        for tag in dhatu.tags:
            if tag.startswith('clean_'):
                clean_dhatu = tag.split('_')[1]
                
        # Expanded Core AniW roots
        ANIT_ROOTS =[
            'ji', 'dA', 'Sru', 'pA', 'han', 'dfS', 'buD', 'ram', 'gam', 'nam', 'vac', 
            'Cid', 'muc', 'svap', 'yaj', 'Bid', 'sfj', 'sTA', 'jJA', 'snA', 'kf', 'kF',
            'vraSc', 'praC'
        ]
        if clean_dhatu in ANIT_ROOTS: is_anit = True
        elif clean_dhatu == 'duh' and 'gana_2' in dhatu.tags: is_anit = True
            
        # Causatives and Secondary Roots (sanādi) are polysyllabic and thus always Seṭ
        if 'sanadi' in dhatu.tags:
            is_anit = False
            
    for term in prakriya.terms[1:]:
        if 'ardhadhatuka' in term.tags and term.text and term.text[0] in VAL_CONSONANTS:
            if dhatu and dhatu.text == 'kf' and 'liW' in term.tags: continue
            
            # Rule 7.2.11 sryukah kiti: Block 'iw' for roots ending in 'uk' or 'SrI' when affix is 'kit'
            is_kit = 'kit' in term.tags
            if is_kit and dhatu and dhatu.text and (dhatu.text == 'SrI' or dhatu.text[-1] in['u', 'U', 'f', 'F', 'x', 'X']):
                prakriya.log(f"Rule 7.2.11: sryukah kiti blocked 'iw' for '{term.upadeza}'")
                continue
                
            if not is_anit: 
                term.text = 'i' + term.text
                prakriya.log(f"Rule 7.2.35: Added 'iw' augment to '{term.upadeza}'")
            else:
                prakriya.log(f"Rule 7.2.10: AniW blocked 'iw' for '{term.upadeza}'")

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

# ==========================================
# REDUPLICATION (ABHYASA)
# ==========================================

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
        # Scan for the next surviving textual element after BU to check for a vowel
        idx = prakriya.terms.index(dhatu)
        next_val = ''
        for i in range(idx + 1, len(prakriya.terms)):
            if prakriya.terms[i].text:
                next_val = prakriya.terms[i].text
                break
                
        if next_val and is_vowel(next_val[0]):
            dhatu.text = dhatu.text + 'v'
            prakriya.log("Rule 6.4.88: Added 'vug' augment to BU")

# ==========================================
# VOWEL SANDHI & GUNA/VRDDHI
# ==========================================

def sarvadhatukam_apit(prakriya: Prakriya) -> None:
    """Rule 1.2.4: sārvadhātukam apit. Sārvadhātuka affixes without 'pit' are 'ṅit'."""
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
        # Terminal Vowels (BU -> Bo)
        if text and text[-1] in IK_VOWELS:
            dhatu.text = text[:-1] + apply_guna(text[-1])
            prakriya.log(f"Rule 7.3.84: Guna on terminal vowel -> '{dhatu.text}'")
        # Penultimate Short Vowels (buD -> boD)
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
                    
            elif next_char == 'y' and last_char in ['o', 'O']:
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
            if last_char in ['i', 'I']: rep = 'y'
            elif last_char in ['u', 'U']: rep = 'v'
            elif last_char in ['f', 'F']: rep = 'r'
            elif last_char == 'x': rep = 'l'
            if rep: 
                term1.text = term1.text[:-1] + rep
                prakriya.log(f"Rule 6.1.77: iko yaRaci -> '{term1.text}'")

def ato_dirgho_yayi(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in YAY_CONSONANTS:
        vikarana.text = vikarana.text[:-1] + 'A'
        prakriya.log("Rule 7.3.101: Lengthened 'a' to 'A'")

def ato_gune(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if dhatu and vikarana and dhatu.text.endswith('a') and vikarana.text and vikarana.text[0] in ['a', 'A']:
        dhatu.text = dhatu.text[:-1]
        prakriya.log("Rule 6.1.97: Merged Dhatu 'a' + Vikarana")
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in['a', 'e', 'o', 'A']:
        vikarana.text = vikarana.text[:-1]
        prakriya.log(f"Rule 6.1.97: Merged Vikarana 'a' + Suffix '{suffix.text[0]}'")

def ato_nitah(prakriya: Prakriya) -> None:
    """Rule 7.2.81: Ato NitaH. a + A -> e for Nit affixes."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'vikaraRa' and t1.text.endswith('a') and t2.text.startswith('A') and 'pit' not in t2.tags:
            t1.text = t1.text[:-1]
            t2.text = 'e' + t2.text[1:]
            prakriya.log("Rule 7.2.81: Ato NitaH (a + A -> e)")

# ==========================================
# CONSONANT SANDHI
# ==========================================

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
            # Rule 8.2.38 (dadhas tathorś ca) blocks 8.2.40 for daD + t/T!
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
    """Rule 8.2.38: dadhas tathorś ca. For 'daD' before 't'/'th', initial 'd' becomes 'D' (dh)."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text == 'D':
            if i > 0 and prakriya.terms[i-1].text == 'da':
                if t2.text and t2.text.startswith(('t', 'T')):
                    prakriya.terms[i-1].text = 'Da'
                    prakriya.log("Rule 8.2.38: dadhas tathorś ca (daD -> DaD before t/T)")

def mo_no_dhatoh(prakriya: Prakriya) -> None:
    """Rule 8.2.64: mo no dhātoḥ. Root-final 'm' becomes 'n' before 'm' or 'v'."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text.endswith('m'):
            if t2.text and t2.text[0] in ['m', 'v']:
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
            elif last_char in ['p', 'P', 'b', 'B']: jas_char = 'b'
            
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

def rashabhyam_no_nah(prakriya: Prakriya) -> None:
    has_trigger = False
    blocked = False
    allowed_intervening = set(SLP1_VOWELS).union(set('hyvrkKgGNpPbBmM'))
    for term_idx, term in enumerate(prakriya.terms):
        new_text = ""
        for i, char in enumerate(term.text):
            if char in['r', 'z', 'f', 'F']:
                has_trigger = True
                blocked = False 
                new_text += char
            elif has_trigger and not blocked:
                if char == 'n': 
                    next_char = term.text[i+1] if i + 1 < len(term.text) else ''
                    
                    # Check padānta (word-final): Is this the last character of the final term?
                    is_padanta = (term_idx == len(prakriya.terms) - 1) and (i == len(term.text) - 1)
                    
                    if is_padanta:
                        new_text += 'n'
                        prakriya.log("Rule 8.4.37: padAntasya blocked Natva at word-end")
                    elif next_char in['t', 'T', 'd', 'D', 's']:
                        new_text += 'n'  # Blocked by the following dental
                    else:
                        new_text += 'R'
                        prakriya.log("Rule 8.4.1 (Natva): 'n' -> 'R'")
                elif char not in allowed_intervening:
                    blocked = True
                    new_text += char
                else: new_text += char
            else: new_text += char
        if term.text != new_text:
            term.text = new_text

def stuna_stuh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t1.text[-1] == 'z':
            if t2.text.startswith('t'): 
                t2.text = 'w' + t2.text[1:]
                prakriya.log("Rule 8.4.41: 't' -> 'w' (zwunA zwuH)")
            elif t2.text.startswith('T'): 
                t2.text = 'W' + t2.text[1:]
                prakriya.log("Rule 8.4.41: 'T' -> 'W' (zwunA zwuH)")

def vrasca_bhrasja_sruja_mruja(prakriya: Prakriya) -> None:
    """Rule 8.2.36: ...cCaSAM zaH. Final palatals/cCh/S become 'z' before jhal."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t2.text and t2.text[0] in JHAL_CONSONANTS:
            # Must check clean tag to survive samprasarana (like yaj -> ij)
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
        if dhatu.text.startswith('d'):
            dhatu.text = dhatu.text[:-1] + 'G'
            prakriya.log("Rule 8.2.32: 'h' -> 'G' (dAder dhAtor ghaH)")
        else:
            dhatu.text = dhatu.text[:-1] + 'Q'
            prakriya.log("Rule 8.2.31: 'h' -> 'Q' (ho DhaH)")

def choh_kuh(prakriya: Prakriya) -> None:
    for i in range(len(prakriya.terms)):
        t = prakriya.terms[i]
        if not t.text: continue
        last_char = t.text[-1]
        if last_char in ['c', 'C', 'j', 'J']:
            is_padanta = (i == len(prakriya.terms) - 1)
            next_char_is_jhal = False
            if not is_padanta and prakriya.terms[i+1].text:
                next_char_is_jhal = prakriya.terms[i+1].text[0] in JHAL_CONSONANTS
            
            if is_padanta or next_char_is_jhal:
                map_ku = {'c':'k', 'C':'K', 'j':'g', 'J':'G'}
                t.text = t.text[:-1] + map_ku[last_char]
                prakriya.log(f"Rule 8.2.30: coH kuH ({last_char} -> {map_ku[last_char]})")

def radabhyam_nishthato_nah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and suffix.upadeza in['kta', 'ktavatu']:
        text = dhatu.text
        if text.endswith('d') or text.endswith('r'):
            if suffix.text.startswith('t'):
                suffix.text = 'n' + suffix.text[1:]
                if text.endswith('d'): dhatu.text = text[:-1] + 'n'
                prakriya.log("Rule 8.2.42: nizThA 't' -> 'n'")

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

# ==========================================
# MISC SUBSTITUTIONS & ROOT-SPECIFIC RULES
# ==========================================

def dhatvadeh_sah_sah_no_nah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text:
        text = dhatu.text
        if text.startswith('z'):
            text = 's' + text[1:]
            if text.startswith('sW'): text = 'sT' + text[2:]
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

def vacisvapiyajadinam_kiti(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1] # MUST check adjacent term, not the final suffix!
    
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    
    if 'kit' in next_term.tags or 'Nit' in next_term.tags:
        if clean_dhatu == 'vac': 
            dhatu.text = 'uc'
            prakriya.log("Rule 6.1.15: Samprasarana (vac -> uc)")
        elif clean_dhatu == 'svap': 
            dhatu.text = 'sup'
            prakriya.log("Rule 6.1.15: Samprasarana (svap -> sup)")
        elif clean_dhatu == 'yaj': 
            dhatu.text = 'ij'
            prakriya.log("Rule 6.1.15: Samprasarana (yaj -> ij)")
        elif clean_dhatu == 'vraSc':
            dhatu.text = 'vfSc'
            prakriya.log("Rule 6.1.16: Samprasarana (vraSc -> vfSc)")
        elif clean_dhatu == 'praC':
            dhatu.text = 'pfC'
            prakriya.log("Rule 6.1.16: Samprasarana (praC -> pfC)")

def sanadyanta_dhatavah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[0]
        suffix = prakriya.terms[1]
        dhatu.text = dhatu.text + suffix.text
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
    """
    Rule 8.4.58: anusvArasya yayi parasavarNaH
    Anusvara (M) becomes the nasal of the following yay-consonant's class.
    Handles both intra-term (muMc -> muYc) and cross-term (gaM + tavya -> gantavya) boundaries.
    """
    for i, term in enumerate(prakriya.terms):
        if 'M' in term.text:
            text = term.text
            new_text = ""
            for j in range(len(text)):
                if text[j] == 'M':
                    next_char = ''
                    # 1. Check intra-term (inside the same term)
                    if j + 1 < len(text):
                        next_char = text[j+1]
                    # 2. Check cross-term (the first letter of the next term)
                    elif i + 1 < len(prakriya.terms) and prakriya.terms[i+1].text:
                        next_char = prakriya.terms[i+1].text[0]
                    
                    if next_char in YAY_PRATYAHARA:
                        if next_char in ['k', 'K', 'g', 'G', 'N']: new_text += 'N'
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

# ==========================================
# UPASARGA (PREFIX) RULES
# ==========================================

def upasarga_satva(prakriya: Prakriya) -> None:
    upasargas =[t for t in prakriya.terms if t.term_type == 'upasarga']
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if upasargas and dhatu and upasargas[-1].text:
        if upasargas[-1].text[-1] in IN_VOWELS:
            if dhatu.text.startswith('sT'):
                dhatu.text = 'zW' + dhatu.text[2:]
                prakriya.log("Rule 8.3.65: Upasarga Satva (sT -> zW)")

def upasarga_sandhi(prakriya: Prakriya) -> None:
    upasarga_indices =[i for i, t in enumerate(prakriya.terms) if t.term_type == 'upasarga']
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
                if first_vowel in ['a', 'A']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'A' + next_term.text[1:]
                    prakriya.log("Rule 6.1.101: Upasarga Savarna Dirgha (A)")
                elif first_vowel in ['i', 'I']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'e' + next_term.text[1:]
                    prakriya.log("Rule 6.1.87: Upasarga Guna (e)")
                elif first_vowel in ['u', 'U']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'o' + next_term.text[1:]
                    prakriya.log("Rule 6.1.87: Upasarga Guna (o)")
                elif first_vowel in ['f', 'F']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'Ar' + next_term.text[1:]
                    prakriya.log("Rule 6.1.87: Upasarga Guna (Ar)")
            elif upasarga.text.endswith('i') or upasarga.text.endswith('I'):
                upasarga.text = upasarga.text[:-1] + 'y'
                prakriya.log("Rule 6.1.77: Upasarga YaN (y)")
            elif upasarga.text.endswith('u') or upasarga.text.endswith('U'):
                upasarga.text = upasarga.text[:-1] + 'v'
                prakriya.log("Rule 6.1.77: Upasarga YaN (v)")

def vikarana_guna(prakriya: Prakriya) -> None:
    """Rule 7.3.84: Applies Guna to Vikarana (e.g., 'u' -> 'o', 'nu' -> 'no') before strong affixes."""
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text in ['u', 'nu'] and 'pit' in suffix.tags:
        if vikarana.text == 'u': vikarana.text = 'o'
        elif vikarana.text == 'nu': vikarana.text = 'no'
        prakriya.log(f"Rule 7.3.84: Guna applied to Vikarana -> '{vikarana.text}'")

def kr_u_morphing(prakriya: Prakriya) -> None:
    """Rule 6.4.110 & 6.4.107: Modifies 'kf', drops 'u'/'nu' before 'v' and 'm'."""
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
    """Rule 7.4.60: halAdi zezaH. Only the first consonant remains in the abhyasa."""
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        new_text = ""
        cons_seen = False
        for char in text:
            if is_vowel(char):
                new_text += char
            elif not cons_seen:
                new_text += char
                cons_seen = True
        if new_text != text:
            abhyasa.text = new_text
            prakriya.log(f"Rule 7.4.60 (halAdi zezaH): -> '{abhyasa.text}'")

def srujidrusor_jhaly_amakiti(prakriya: Prakriya) -> None:
    """
    Rule 6.1.58: sfjidfSojhalyamakiti
    Adds the 'am' augment (which shifts 'f' to 'ra') to sfj and dfS 
    before jhal-initial non-kit affixes (like tavya or tumun).
    """
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
    """
    Rule 8.3.24: naScApadAntasya jhali
    A non-word-final 'm' or 'n' becomes anusvara ('M') before a jhal consonant.
    """
    for i in range(len(prakriya.terms)):
        term = prakriya.terms[i]
        text = term.text
        new_text = ""
        for j, char in enumerate(text):
            if char in['m', 'n']:
                # Check intra-term boundary
                if j + 1 < len(text) and text[j+1] in JHAL_CONSONANTS:
                    new_text += 'M'
                    prakriya.log(f"Rule 8.3.24: '{char}' -> 'M' before jhal '{text[j+1]}'")
                # Check cross-term boundary
                elif j == len(text) - 1 and i + 1 < len(prakriya.terms) and prakriya.terms[i+1].text and prakriya.terms[i+1].text[0] in JHAL_CONSONANTS:
                    new_text += 'M'
                    prakriya.log(f"Rule 8.3.24: '{char}' -> 'M' before jhal '{prakriya.terms[i+1].text[0]}'")
                else:
                    new_text += char
            else:
                new_text += char
        term.text = new_text

# --- New Krdanta & Sandhi Rules ---

def stha_adi_ita(prakriya: Prakriya) -> None:
    """Rule 7.4.40 & 7.4.46: A -> i/a before 'kit' affixes starting with 't'"""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and 'kit' in suffix.tags:
        if suffix.text.startswith('t'):
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

def ato_yuk(prakriya: Prakriya) -> None:
    """Rule 7.3.33: āto yuk ciṇkṛtoḥ (adds 'yuk' augment to A-ending roots before ṇit/ñit)"""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    if dhatu.text.endswith('A') and ('Rit' in next_term.tags or 'Yit' in next_term.tags):
        dhatu.text = dhatu.text + 'y'
        prakriya.log("Rule 7.3.33: Added 'yuk' augment to root ending in 'A'")

def id_yati(prakriya: Prakriya) -> None:
    """Rule 6.4.65: id yati (A -> I/e before 'yat' affix)"""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    if dhatu.text.endswith('A') and next_term.upadeza == 'yat':
        dhatu.text = dhatu.text[:-1] + 'e'
        prakriya.log("Rule 6.4.65: A -> e before 'yat'")

def akah_savarne_dirghah(prakriya: Prakriya) -> None:
    """Rule 6.1.101: akaḥ savarṇe dīrghaḥ (Universal Savarṇa Dīrgha Sandhi)"""
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
    """Rule 6.1.10: Root reduplicates before Slu."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    if dhatu and vikarana and vikarana.upadeza == 'Slu':
        # Check if not already reduplicated
        if not any(t.term_type == 'abhyasa' for t in prakriya.terms):
            abhyasa = Term(dhatu.upadeza, 'abhyasa')
            abhyasa.text = dhatu.text
            idx = prakriya.terms.index(dhatu)
            prakriya.terms.insert(idx, abhyasa)
            prakriya.log(f"Rule 6.1.10: Reduplicated root for Slu -> '{abhyasa.text}'")

def snasor_allopah(prakriya: Prakriya) -> None:
    """Rule 6.4.111: Drops 'a' of 'as' and 'śnam' before weak Sārvadhātuka affix."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    
    if dhatu and ('sarvadhatuka' in suffix.tags or 'tin' in suffix.tags):
        is_weak = 'kit' in suffix.tags or 'Nit' in suffix.tags
        if is_weak:
            if dhatu.text == 'as':
                dhatu.text = 's'
                prakriya.log("Rule 6.4.111: śnasor allopaḥ -> 'as' becomes 's'")
            elif 'gana_7' in dhatu.tags and 'na' in dhatu.text:
                # Target the 'na' inserted by Snam
                idx = dhatu.text.rfind('na')
                if idx != -1:
                    dhatu.text = dhatu.text[:idx] + 'n' + dhatu.text[idx+2:]
                    prakriya.log("Rule 6.4.111: śnasor allopaḥ -> 'na' (śnam) becomes 'n'")

def tasyasti_lopa(prakriya: Prakriya) -> None:
    """Rule 7.4.50: tāsyastilopaḥ. Elides the 's' of 'as' before 's'."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and dhatu.text == 'as' and suffix.text.startswith('s'):
        dhatu.text = 'a'
        prakriya.log("Rule 7.4.50: tāsyastilopaḥ -> 'as' becomes 'a' before 's'")

def lin_agamas(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if 'liN' in suffix.tags:
        if dhatu and 'atmanepada' in dhatu.tags:
            agama = Term('sIy', 'Agama')
            prakriya.terms.insert(-1, agama)
            prakriya.log("Rule 3.4.102: sIyuW augment for Atmanepada liN")
        else:
            agama = Term('yAs', 'Agama')
            agama.tags.add('yAsuW')
            prakriya.terms.insert(-1, agama)
            prakriya.log("Rule 3.4.103: yAsuW augment for Parasmaipada liN")

def cli_agama(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if 'luN' in suffix.tags and dhatu:
        cli = Term('cli', 'vikaraRa')
        clean_dhatu = ''
        for tag in dhatu.tags:
            if tag.startswith('clean_'): clean_dhatu = tag.split('_')[1]
            
        SAL_CONSONANTS = ['S', 'z', 's', 'h']
        IK_VOWELS =['i', 'I', 'u', 'U', 'f', 'F', 'x', 'X']
        upadha = dhatu.text[-2] if len(dhatu.text) > 1 else ''
        ends_in_sal = dhatu.text[-1] in SAL_CONSONANTS if dhatu.text else False
        
        ANIT_ROOTS =[
            'ji', 'dA', 'Sru', 'pA', 'han', 'dfS', 'buD', 'ram', 'gam', 'nam', 'vac', 
            'Cid', 'muc', 'svap', 'yaj', 'Bid', 'sfj', 'sTA', 'jJA', 'snA', 'kf', 'kF',
            'vraSc', 'praC'
        ]
        is_anit = clean_dhatu in ANIT_ROOTS or (clean_dhatu == 'duh' and 'gana_2' in dhatu.tags) or clean_dhatu in ['ruh', 'lih', 'kfiS']
        
        if clean_dhatu in['gam']:
            cli.text = 'a'
            cli.tags.add('Nit')
            cli.tags.add('aN') # Mark explicitly as the aN augment!
            prakriya.log("Rule 3.1.55: puSAdi... cli -> aN")
        elif ends_in_sal and upadha in IK_VOWELS and is_anit:
            cli.text = 'sa'
            cli.tags.add('ksa')
            prakriya.log("Rule 3.1.45: śala igupadhādaṇiṭaḥ ksaḥ (cli -> ksa)")
        else:
            cli.text = 's'
            prakriya.log("Rule 3.1.44: cleH sic (cli -> siC)")
        idx = prakriya.terms.index(dhatu) + 1
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
            if t1.text[-1] in ['a', 'A'] and t2.text[0] in['i', 'I', 'u', 'U', 'f', 'F']:
                rep = apply_guna(t2.text[0])
                t1.text = t1.text[:-1] + rep
                t2.text = t2.text[1:]
                prakriya.log(f"Rule 6.1.87: Ad guNaH (a + {t2.text[0]} -> {rep})")

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

# ==========================================
# LOṬ (IMPERATIVE) & LIṄ (OPTATIVE) & LUṄ (AORIST)
# ==========================================

def jher_jus(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.upadeza == 'Ji':
        if 'liN' in suffix.tags:
            suffix.text = 'us'
            suffix.upadeza = 'us' 
            prakriya.log("Rule 3.4.108: jher jus (Ji -> us)")
        elif 'luN' in suffix.tags:
            has_sic = any(t.upadeza == 'cli' and t.text == 's' for t in prakriya.terms)
            dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
            is_abhyasta = dhatu and 'gana_3' in dhatu.tags
            is_vid = dhatu and dhatu.text == 'vid'
            if has_sic or is_abhyasta or is_vid:
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
    """Rule 6.4.106: utaś ca pratyayād. Drops 'hi' after an affix ending in 'u'."""
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
    if set(['laN', 'liN', 'luN', 'loW']).intersection(suffix.tags) and suffix.text.endswith('s') and suffix.upadeza in ['vas', 'mas']:
        suffix.text = suffix.text[:-1]
        prakriya.log("Rule 3.4.99: nityaM NitaH (dropped final 's')")

def tasthasthamipam(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if set(['laN', 'liN', 'luN', 'loW']).intersection(suffix.tags):
        if suffix.text == 'tas': suffix.text = 'tAm'
        elif suffix.text == 'Tas': suffix.text = 'tam'
        elif suffix.text == 'Ta': suffix.text = 'ta'
        elif suffix.text == 'mip' and 'loW' not in suffix.tags: 
            suffix.text = 'am'
        prakriya.log(f"Rule 3.4.101: Past/Opt/Aorist replacement -> '{suffix.text}'")

def er_uh(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'loW' in suffix.tags and suffix.text.endswith('i') and suffix.upadeza in ['tip', 'Ji']:
        suffix.text = suffix.text[:-1] + 'u'
        prakriya.log("Rule 3.4.86: er uH (i -> u for loW)")

def gam_hana_jana_lopa(prakriya: Prakriya) -> None:
    """Rule 6.4.98: gam-hana-jana-khan-ghasāṃ lopaḥ kṅity anaṅi. Drops 'a' before vowel weak affixes."""
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
    
    if clean_dhatu in ['gam', 'han', 'jan', 'Kan', 'Gas'] and is_kit_or_nit and is_vowel_initial and is_anang:
        if dhatu.text.endswith('am') or dhatu.text.endswith('an') or dhatu.text.endswith('as'):
            dhatu.text = dhatu.text[:-2] + dhatu.text[-1]
            prakriya.log(f"Rule 6.4.98: Dropped penultimate 'a' -> '{dhatu.text}'")
            
        if clean_dhatu == 'han' and dhatu.text == 'hn':
            dhatu.text = 'Gn'
            prakriya.log("Rule 7.3.54 (implied for hn): 'hn' -> 'Gn'")

def che_ca(prakriya: Prakriya) -> None:
    """Rule 6.1.73: che ca. Adds 'tuk' (c) after a short vowel before 'C'."""
    # 1. Intra-term insertion (e.g. pfC -> pfcC)
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
            
    # 2. Cross-term insertion (e.g. a + CAdya -> acCAdya)
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text and t2.text.startswith('C') and t1.text[-1] in['a', 'i', 'u', 'f', 'x']:
            t2.text = 'c' + t2.text
            prakriya.log("Rule 6.1.73: che ca (inserted 'c' before 'C' across terms)")

def ekaco_baso_bhas(prakriya: Prakriya) -> None:
    """Rule 8.2.37: ekāco baśo bhaṣ... Initial b/g/ḍ/d becomes bh/gh/ḍh/dh before 's'."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]
    
    # If the root ends in a heavy aspirate and is followed by 's'
    if dhatu.text and dhatu.text[-1] in['B', 'G', 'Q', 'D']:
        if suffix.text.startswith('s') or suffix.text.startswith('Dv'):
            bas_bhas = {'b': 'B', 'g': 'G', 'q': 'Q', 'd': 'D'}
            if dhatu.text[0] in bas_bhas:
                dhatu.text = bas_bhas[dhatu.text[0]] + dhatu.text[1:]
                prakriya.log(f"Rule 8.2.37: ekāco baśo bhaṣ -> '{dhatu.text}'")

def sadhoh_kas_si(prakriya: Prakriya) -> None:
    """Rule 8.2.41: ṣaḍhoḥ kas si. ṣ, ḍh (and gh) become 'k' before 's'."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.text and t2.text and t2.text.startswith('s'):
            if t1.text[-1] in ['z', 'Q', 'G']:
                t1.text = t1.text[:-1] + 'k'
                prakriya.log("Rule 8.2.41: ṣaḍhoḥ kas si -> 'k' before 's'")

def sici_vrddhih(prakriya: Prakriya) -> None:
    """Rule 7.2.1: sici vṛddhiḥ parasmaipadeṣu. Vrddhi before sic."""
    sic = next((t for t in prakriya.terms if t.upadeza == 'cli' and t.text == 's'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if sic and dhatu and 'parasmaipada' in dhatu.tags:
        if dhatu.text[-1] in IK_VOWELS:
            dhatu.text = dhatu.text[:-1] + apply_vrddhi(dhatu.text[-1])
            prakriya.log("Rule 7.2.1: sici vṛddhiḥ -> Vṛddhi before sic")

def asti_sico_aprkte(prakriya: Prakriya) -> None:
    """Rule 7.3.96: astisico'pṛkte. Adds 'I' augment before apṛkta (single letter) t/s after sic."""
    sic_idx = next((i for i, t in enumerate(prakriya.terms) if t.upadeza == 'cli' and t.text == 's'), -1)
    if sic_idx != -1 and sic_idx + 1 < len(prakriya.terms):
        suffix = prakriya.terms[sic_idx + 1]
        if suffix.text in ['t', 's']:
            agama = Term('I', 'Agama')
            prakriya.terms.insert(sic_idx + 1, agama)
            prakriya.log("Rule 7.3.96: astisico'pṛkte (Inserted 'I' augment)")

def do_dad_ghoh(prakriya: Prakriya) -> None:
    """Rule 7.4.46: do dad ghoḥ. dA/DA -> dad/daD before weak affixes in abhyasta."""
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
    """Rule 6.4.112: śnābhyastayor ātaḥ. Drops 'A' before weak vowel affixes."""
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

def aci_snu_dhatu_bhruvam(prakriya: Prakriya) -> None:
    """Rule 6.4.77: aci śnudhātubhruvāṃ... Root 'U' becomes 'uv' before vowels."""
    for i in range(len(prakriya.terms)-1):
        t1 = prakriya.terms[i]
        t2 = prakriya.terms[i+1]
        if t1.term_type == 'dhatu' and t1.text.endswith('U') and t2.text and is_vowel(t2.text[0]):
            # Pāṇini 6.4.87 (huśnuvoḥ) forces yaṇ for Snu, but brU gets normal uvaṅ
            if t1.text == 'brU':
                t1.text = t1.text[:-1] + 'uv'
                prakriya.log("Rule 6.4.77: aci śnudhātubhruvāṃ (U -> uv before vowel)")

def sino_gunah(prakriya: Prakriya) -> None:
    """Rule 7.4.22: śiṅo guṇaḥ. śī gets guṇa before all Sārvadhātuka affixes."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and ('sarvadhatuka' in suffix.tags or 'tin' in suffix.tags):
        clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
        if clean_dhatu == 'SI':
            dhatu.text = 'Se'
            prakriya.log("Rule 7.4.22: śiṅo guṇaḥ (SI -> Se)")

def han_ghatva_tatva(prakriya: Prakriya) -> None:
    """Rule 7.3.54 & 7.3.32: han -> ghāt before ṇit/ñit."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    clean_dhatu = next((tag.split('_')[1] for tag in dhatu.tags if tag.startswith('clean_')), dhatu.text)
    
    if clean_dhatu == 'han' and ('Rit' in next_term.tags or 'Yit' in next_term.tags):
        if dhatu.text.startswith('h'):
            dhatu.text = 'G' + dhatu.text[1:]
            prakriya.log("Rule 7.3.54: ho hanter ñṇinneṣu (h -> G)")
        if dhatu.text.endswith('n'):
            dhatu.text = dhatu.text[:-1] + 't'
            prakriya.log("Rule 7.3.32: hanato ṇinnali (n -> t)")