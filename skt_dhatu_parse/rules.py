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
        
    if 'ardhadhatuka' in suffix.tags: return
        
    if 'gana_1' in dhatu.tags: vik = Term('Sap', 'vikaraRa')
    elif 'gana_4' in dhatu.tags: vik = Term('Syan', 'vikaraRa')
    elif 'gana_6' in dhatu.tags: vik = Term('Sa', 'vikaraRa')
    elif 'gana_8' in dhatu.tags: vik = Term('u', 'vikaraRa') # <--- NEW: Gana 8
    elif 'gana_9' in dhatu.tags: vik = Term('SnA', 'vikaraRa')
    else: return
        
    prakriya.terms.insert(idx, vik)
    prakriya.log(f"Inserted Vikarana '{vik.upadeza}'")

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
    if suffix.text == 'TAs' and 'Wit' in suffix.tags:
        suffix.text = 'se'
        prakriya.log("Rule 3.4.80: Replaced 'TAs' with 'se'")

def tasthasthamipam(prakriya: Prakriya) -> None:
    lakara = next((t for t in prakriya.terms if t.term_type == 'lakara' or 'laN' in t.tags), None)
    suffix = prakriya.terms[-1]
    if lakara and 'laN' in lakara.tags:
        if suffix.text == 'tas': suffix.text = 'tAm'
        elif suffix.text == 'Tas': suffix.text = 'tam'
        elif suffix.text == 'Ta': suffix.text = 'ta'
        elif suffix.text == 'mip': suffix.text = 'am'
        prakriya.log(f"Rule 3.4.101: Past tense replacement -> '{suffix.text}'")

def jhonta(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
        is_atmanepada = dhatu and 'atmanepada' in dhatu.tags
        is_anat = dhatu and 'gana_9' in dhatu.tags
        
        if is_atmanepada and is_anat: 
            suffix.text = 'at' + suffix.text[1:]
            prakriya.log("Rule 7.1.5: 'Jh' -> 'at'")
        else: 
            suffix.text = 'ant' + suffix.text[1:]
            prakriya.log("Rule 7.1.3: 'Jh' -> 'ant'")

def at_agama(prakriya: Prakriya) -> None:
    lakara = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'laN' in lakara.tags:
        agama = Term('aw', 'Agama')
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, agama)
        prakriya.log("Rule 6.4.71: Inserted 'aw' past tense augment")

def itasca(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'laN' in suffix.tags and suffix.text.endswith('i'):
        suffix.text = suffix.text[:-1]
        prakriya.log("Rule 3.4.100: Dropped terminal 'i'")

def hali_ca(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text == 'div':
        dhatu.text = 'dIv'
        prakriya.log("Rule 8.2.77: Lengthened 'div' to 'dIv'")

def it_agama(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    is_anit = False
    if dhatu:
        ANIT_ROOTS =['ji', 'dA', 'Sru', 'pA', 'han', 'dfS', 'buD', 'ram', 'gam', 'nam', 'vac', 'Cid', 'muc', 'svap', 'yaj', 'Bid', 'sfj']
        if dhatu.text in ANIT_ROOTS: is_anit = True
        elif dhatu.text == 'duh' and 'gana_2' in dhatu.tags: is_anit = True
            
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
    if dhatu and dhatu.upadeza == 'BU' and 'liW' in suffix.tags:
        if suffix.text and is_vowel(suffix.text[0]):
            dhatu.text = dhatu.text + 'v'
            prakriya.log("Rule 6.4.88: Added 'vug' augment to BU")

# ==========================================
# VOWEL SANDHI & GUNA/VRDDHI
# ==========================================

def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    is_sarva = 'sarvadhatuka' in next_term.tags or 'tin' in next_term.tags or 'Sit' in next_term.tags
    is_ardha = 'ardhadhatuka' in next_term.tags
    is_apit = 'pit' not in next_term.tags
    
    if is_sarva and is_apit: next_term.tags.add('Nit')
    if 'Nit' in next_term.tags or 'kit' in next_term.tags: return
        
    if is_sarva or is_ardha:
        text = dhatu.text
        # Terminal Vowels (BU -> Bo)
        if text and text[-1] in IK_VOWELS:
            dhatu.text = text[:-1] + apply_guna(text[-1])
        # Penultimate Short Vowels (buD -> boD)
        elif len(text) >= 2 and text[-2] in ['i', 'u', 'f', 'x'] and text[-1] not in SLP1_VOWELS:
            dhatu.text = text[:-2] + apply_guna(text[-2]) + text[-1]

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
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    text = dhatu.text
    if text and text[-1] in EC_VOWELS and next_term.text:
        last_char = text[-1]
        next_char = next_term.text[0]
        rep = None
        
        if is_vowel(next_char):
            if last_char == 'e': rep = 'ay'
            elif last_char == 'o': rep = 'av'
            elif last_char == 'E': rep = 'Ay'
            elif last_char == 'O': rep = 'Av'
            if rep:
                dhatu.text = text[:-1] + rep
                prakriya.log(f"Rule 6.1.78: eco'yavAyAvaH -> '{dhatu.text}'")
                
        elif next_char == 'y' and last_char in ['o', 'O']:
            if last_char == 'o': rep = 'av'
            elif last_char == 'O': rep = 'Av'
            if rep:
                dhatu.text = text[:-1] + rep
                prakriya.log(f"Rule 6.1.79: vAnto yi pratyaye -> '{dhatu.text}'")

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
    
    if dhatu and vikarana and dhatu.text.endswith('a') and vikarana.text[0] in ['a', 'A']:
        dhatu.text = dhatu.text[:-1]
        prakriya.log("Rule 6.1.97: Merged Dhatu 'a' + Vikarana 'a'")
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in ['a', 'e', 'o']:
        vikarana.text = vikarana.text[:-1]
        prakriya.log(f"Rule 6.1.97: Merged Vikarana 'a' + Suffix '{suffix.text[0]}'")

def ato_nitah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 3:
        vikarana = prakriya.terms[1]
        suffix = prakriya.terms[-1]
        if vikarana.text.endswith('a') and suffix.text.startswith('A') and 'pit' not in suffix.tags:
            vikarana.text = vikarana.text[:-1]
            suffix.text = 'e' + suffix.text[1:]
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
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] in JHAS_CONSONANTS:
            if suffix.text.startswith('t'): 
                suffix.text = 'D' + suffix.text[1:]
                prakriya.log("Rule 8.2.40: 't' -> 'D' after jhaz")
            elif suffix.text.startswith('T'): 
                suffix.text = 'D' + suffix.text[1:]
                prakriya.log("Rule 8.2.40: 'T' -> 'D' after jhaz")

def jhalam_jas_jhasi(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] in JHAL_CONSONANTS and suffix.text and suffix.text[0] in JHAS_SOFT_CONSONANTS:
            last_char = dhatu.text[-1]
            jas_char = last_char
            if last_char in ['k', 'K', 'g', 'G', 'h']: jas_char = 'g'
            elif last_char in['c', 'C', 'j', 'J', 'S']: jas_char = 'j'
            elif last_char in['w', 'W', 'q', 'Q', 'z']: jas_char = 'q'
            elif last_char in['t', 'T', 'd', 'D', 's']: jas_char = 'd'
            elif last_char in['p', 'P', 'b', 'B']: jas_char = 'b'
            
            if jas_char != last_char:
                dhatu.text = dhatu.text[:-1] + jas_char
                prakriya.log(f"Rule 8.4.53: Changed '{last_char}' to '{jas_char}' (jaS)")

def khari_ca(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] in JHAL_CONSONANTS and suffix.text and suffix.text[0] in KHAR_CONSONANTS:
            last_char = dhatu.text[-1]
            char_map = {'g':'k', 'G':'k', 'k':'k', 'K':'k', 'j':'c', 'J':'c', 'c':'c', 'C':'c', 'q':'w', 'Q':'w', 'w':'w', 'W':'w', 'd':'t', 'D':'t', 't':'t', 'T':'t', 'b':'p', 'B':'p', 'p':'p', 'P':'p'}
            if last_char in char_map and char_map[last_char] != last_char:
                dhatu.text = dhatu.text[:-1] + char_map[last_char]
                prakriya.log(f"Rule 8.4.55: Changed '{last_char}' to '{char_map[last_char]}' (khari ca)")

def rashabhyam_no_nah(prakriya: Prakriya) -> None:
    has_trigger = False
    blocked = False
    allowed_intervening = set(SLP1_VOWELS).union(set('hyvrkKgGNpPbBmM'))
    for term in prakriya.terms:
        new_text = ""
        for i, char in enumerate(term.text):
            if char in['r', 'z', 'f', 'F']:
                has_trigger = True
                blocked = False 
                new_text += char
            elif has_trigger and not blocked:
                if char == 'n': 
                    # --- NEW: Check if 'n' is immediately followed by a dental (t/th/d/dh/s) ---
                    next_char = term.text[i+1] if i + 1 < len(term.text) else ''
                    if next_char in ['t', 'T', 'd', 'D', 's']:
                        new_text += 'n'  # Blocked by the following dental!
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
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] == 'z':
            if suffix.text.startswith('t'): 
                suffix.text = 'w' + suffix.text[1:]
                prakriya.log("Rule 8.4.41: 't' -> 'w' (zwunA zwuH)")
            elif suffix.text.startswith('T'): 
                suffix.text = 'W' + suffix.text[1:]
                prakriya.log("Rule 8.4.41: 'T' -> 'W' (zwunA zwuH)")

def vrasca_bhrasja_sruja_mruja(prakriya: Prakriya) -> None:
    """Rule 8.2.36: ...cCaSAM zaH. Final palatals/C/S become 'z' before jhal."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    if suffix.text and suffix.text[0] in JHAL_CONSONANTS:
        targets =['vrazc', 'Brajj', 'Brasj', 'sfj', 'mfj', 'yaj', 'rAj', 'BrAj']
        # includes roots ending in 'C' or 'S' ---
        if dhatu.text in targets or dhatu.text.endswith('C') or dhatu.text.endswith('S'):
            dhatu.text = dhatu.text[:-1] + 'z'
            prakriya.log(f"Rule 8.2.36: Final palatal/C/S became 'z' -> '{dhatu.text}'")

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
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and suffix and suffix.text and suffix.text[0] in JHAL_CONSONANTS:
        last_char = dhatu.text[-1]
        if last_char in ['c', 'C', 'j', 'J']:
            map_ku = {'c':'k', 'C':'K', 'j':'g', 'J':'G'}
            dhatu.text = dhatu.text[:-1] + map_ku[last_char]
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
    suffix = prakriya.terms[-1]
    if dhatu and 'kit' in suffix.tags:
        if dhatu.text == 'vac': 
            dhatu.text = 'uc'
            prakriya.log("Rule 6.1.15: Samprasarana (vac -> uc)")
        elif dhatu.text == 'svap': 
            dhatu.text = 'sup'
            prakriya.log("Rule 6.1.15: Samprasarana (svap -> sup)")
        elif dhatu.text == 'yaj': 
            dhatu.text = 'ij'
            prakriya.log("Rule 6.1.15: Samprasarana (yaj -> ij)")

def sanadyanta_dhatavah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[0]
        suffix = prakriya.terms[1]
        dhatu.text = dhatu.text + suffix.text
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
        if dhatu.text in ANUDATTA_NASAL_ROOTS:
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
    """Rule 7.3.84: Applies Guna to Vikarana (e.g., 'u' -> 'o') before strong affixes."""
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text == 'u' and 'pit' in suffix.tags:
        vikarana.text = 'o'
        prakriya.log("Rule 7.3.84: Guna applied to Vikarana 'u' -> 'o'")

def kr_u_morphing(prakriya: Prakriya) -> None:
    """Rule 6.4.110 & 6.4.108: Modifies 'kf' to 'kar' or 'kur' before 'u', and drops 'u'."""
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if dhatu and dhatu.upadeza == 'qukfY' and vikarana and vikarana.upadeza == 'u':
        if 'pit' not in suffix.tags:
            dhatu.text = 'kur'
            prakriya.log("Rule 6.4.110: 'kf' -> 'kur' before weak 'u'")
            # Rule 6.4.108: Drop 'u' before v and m
            if suffix.text.startswith('v') or suffix.text.startswith('m'):
                vikarana.text = ''
                prakriya.log("Rule 6.4.108: Dropped 'u' before 'v/m'")
        else:
            dhatu.text = 'kar'
            prakriya.log("Rule 7.3.84: 'kf' -> 'kar' before strong 'u'")

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