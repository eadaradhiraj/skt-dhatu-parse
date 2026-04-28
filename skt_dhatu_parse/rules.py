from .shivasutras import get_pratyahara, is_vowel, SLP1_VOWELS
from .models import Term, Prakriya

IK_VOWELS = set(get_pratyahara('i', 'k') + ['I', 'U', 'F', 'X'])
EC_VOWELS = get_pratyahara('e', 'c')
YAY_CONSONANTS = set(get_pratyahara('y', 'Y'))
IN_VOWELS = set(get_pratyahara('i', 'R') + ['I', 'U', 'F', 'X'])
SLP1_CONSONANTS = set(get_pratyahara('h', 'l')) 
VAL_CONSONANTS = set(get_pratyahara('v', 'l')) 
JHAS_CONSONANTS = set(get_pratyahara('J', 'z'))      
JHAL_CONSONANTS = set(get_pratyahara('J', 'l'))      
JHAS_SOFT_CONSONANTS = set(get_pratyahara('J', 'S')) 

TIN_PARASMAIPADA = {
    'prathama': ['tip', 'tas', 'Ji'],
    'madhyama':['sip', 'Tas', 'Ta'],
    'uttama':   ['mip', 'vas', 'mas']
}
TIN_ATMANEPADA = {
    'prathama':['ta', 'AtAm', 'Ja'],
    'madhyama': ['TAs', 'ATAm', 'Dvam'],
    'uttama':   ['iw', 'vahi', 'mahiN']
}
TIN_PARASMAIPADA_LIT = {
    'prathama': ['Ral', 'atus', 'us'],
    'madhyama': ['Tal', 'aTus', 'a'],
    'uttama':['Ral', 'va', 'ma']
}


# Pāṇini Rule 1.4.58: prādayaḥ
UPASARGAS =[
    'pra', 'parA', 'apa', 'sam', 'anu', 'ava', 'nis', 'nir', 
    'dus', 'dur', 'vi', 'A', 'ni', 'aDi', 'api', 'ati', 
    'su', 'ud', 'aBi', 'prati', 'pari', 'upa'
]

def apply_guna(char: str) -> str:
    if char in ['i', 'I']: return 'e'
    if char in['u', 'U']: return 'o'
    if char in ['f', 'F']: return 'ar'
    if char in ['x']: return 'al'
    return char

def apply_vrddhi(char: str) -> str:
    if char in ['a']: return 'A'
    if char in['i', 'I', 'e']: return 'E'
    if char in ['u', 'U', 'o']: return 'O'
    if char in ['f', 'F']: return 'Ar'
    if char in['x']: return 'Al'
    return char

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
    
    if is_lit: lakara.tags.add('ardhadhatuka')
    else: lakara.tags.add('sarvadhatuka')

def insert_vikarana(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if not dhatu: return
    idx = prakriya.terms.index(dhatu) + 1 
    
    if 'lfW' in suffix.tags:
        vik = Term('sya', 'vikaraRa')
        vik.tags.add('ardhadhatuka')
        prakriya.terms.insert(idx, vik)
        return
        
    if 'ardhadhatuka' in suffix.tags: return
        
    if 'gana_1' in dhatu.tags: vik = Term('Sap', 'vikaraRa')
    elif 'gana_4' in dhatu.tags: vik = Term('Syan', 'vikaraRa')
    elif 'gana_6' in dhatu.tags: vik = Term('Sa', 'vikaraRa')
    elif 'gana_9' in dhatu.tags: vik = Term('SnA', 'vikaraRa')
    else: return
        
    prakriya.terms.insert(idx, vik)

def atmanepada_tere(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and 'atmanepada' in dhatu.tags and 'Wit' in suffix.tags:
        text = suffix.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                suffix.text = text[:i] + 'e'
                break

def idito_num_dhatoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'idit' in dhatu.tags:
        text = dhatu.text
        for i in range(len(text)-1, -1, -1):
            if is_vowel(text[i]):
                dhatu.text = text[:i+1] + 'M' + text[i+1:]
                break

def sarvadhatuka_ardhadhatukayoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    is_sarva = 'tin' in next_term.tags or 'Sit' in next_term.tags
    is_ardha = 'ardhadhatuka' in next_term.tags
    is_apit = 'pit' not in next_term.tags
    
    if is_sarva and is_apit:
        next_term.tags.add('Nit')
        
    if 'Nit' in next_term.tags or 'kit' in next_term.tags:
        return
        
    if is_sarva or is_ardha:
        text = dhatu.text
        if text and text[-1] in IK_VOWELS:
            dhatu.text = text[:-1] + apply_guna(text[-1])

def eco_yayavayah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    next_term = prakriya.terms[idx + 1]
    
    text = dhatu.text
    if text and text[-1] in EC_VOWELS and next_term.text and is_vowel(next_term.text[0]):
        last_char = text[-1]
        if last_char == 'e': rep = 'ay'
        elif last_char == 'o': rep = 'av'
        elif last_char == 'E': rep = 'Ay'
        elif last_char == 'O': rep = 'Av'
        dhatu.text = text[:-1] + rep

def ato_dirgho_yayi(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in YAY_CONSONANTS:
        vikarana.text = vikarana.text[:-1] + 'A'

def rutva_visarga(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text.endswith('s'):
        suffix.text = suffix.text[:-1] + 'H'

def jhonta(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text.startswith('J'):
        dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
        is_atmanepada = dhatu and 'atmanepada' in dhatu.tags
        is_anat = dhatu and 'gana_9' in dhatu.tags
        
        if is_atmanepada and is_anat:
            suffix.text = 'at' + suffix.text[1:]
        else:
            suffix.text = 'ant' + suffix.text[1:]

def thasah_se(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if suffix.text == 'TAs' and 'Wit' in suffix.tags:
        suffix.text = 'se'

def ato_gune(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    
    if dhatu and vikarana and dhatu.text.endswith('a') and vikarana.text.startswith('a'):
        dhatu.text = dhatu.text[:-1]
    if vikarana and vikarana.text.endswith('a') and suffix.text and suffix.text[0] in ['a', 'e', 'o']:
        vikarana.text = vikarana.text[:-1]

def ato_nitah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 3:
        vikarana = prakriya.terms[1]
        suffix = prakriya.terms[-1]
        if vikarana.text.endswith('a') and suffix.text.startswith('A') and 'pit' not in suffix.tags:
            vikarana.text = vikarana.text[:-1]
            suffix.text = 'e' + suffix.text[1:]

def at_agama(prakriya: Prakriya) -> None:
    lakara = prakriya.terms[-1]
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and 'laN' in lakara.tags:
        agama = Term('aw', 'Agama')
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, agama)

def itasca(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    if 'laN' in suffix.tags and suffix.text.endswith('i'):
        suffix.text = suffix.text[:-1]

def hali_ca(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text == 'div':
        dhatu.text = 'dIv'

def tasthasthamipam(prakriya: Prakriya) -> None:
    lakara = next((t for t in prakriya.terms if t.term_type == 'lakara' or 'laN' in t.tags), None)
    suffix = prakriya.terms[-1]
    if lakara and 'laN' in lakara.tags:
        if suffix.text == 'tas': suffix.text = 'tAm'
        elif suffix.text == 'Tas': suffix.text = 'tam'
        elif suffix.text == 'Ta': suffix.text = 'ta'
        elif suffix.text == 'mip': suffix.text = 'am'

def samyogantasya_lopah(prakriya: Prakriya) -> None:
    suffix = prakriya.terms[-1]
    text = suffix.text
    if len(text) >= 2 and text[-1] in SLP1_CONSONANTS and text[-2] in SLP1_CONSONANTS:
        suffix.text = text[:-1]

def it_agama(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    ANIT_ROOTS = ['ji', 'dA', 'Sru', 'pA', 'han', 'dfS', 'buD']
    is_anit = dhatu and (dhatu.text in ANIT_ROOTS)
    
    for term in prakriya.terms[1:]:
        if 'ardhadhatuka' in term.tags and term.text and term.text[0] in VAL_CONSONANTS:
            if not is_anit:
                term.text = 'i' + term.text

def adesa_pratyayayoh(prakriya: Prakriya) -> None:
    for i, curr_term in enumerate(prakriya.terms):
        if curr_term.term_type in['dhatu', 'upasarga', 'abhyasa']:
            continue
        text = curr_term.text
        if 's' in text:
            idx = text.find('s')
            is_last_term = (i == len(prakriya.terms) - 1)
            is_last_char = (idx == len(text) - 1)
            if is_last_term and is_last_char:
                continue 
            
            if idx > 0: prev_char = text[idx-1]
            else:
                if i > 0 and prakriya.terms[i-1].text:
                    prev_char = prakriya.terms[i-1].text[-1]
                else: continue 
            
            if prev_char in IN_VOWELS or prev_char in['k', 'K', 'g', 'G', 'N']:
                curr_term.text = text[:idx] + 'z' + text[idx+1:]

def jhasas_tathor_dho_dhah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] in JHAS_CONSONANTS:
            if suffix.text.startswith('t'): suffix.text = 'D' + suffix.text[1:]
            elif suffix.text.startswith('T'): suffix.text = 'D' + suffix.text[1:]

def jhalam_jas_jhasi(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[-2]
        suffix = prakriya.terms[-1]
        if dhatu.text and dhatu.text[-1] in JHAL_CONSONANTS and suffix.text and suffix.text[0] in JHAS_SOFT_CONSONANTS:
            last_char = dhatu.text[-1]
            jas_char = last_char
            if last_char in['k', 'K', 'g', 'G', 'h']: jas_char = 'g'
            elif last_char in ['c', 'C', 'j', 'J', 'S']: jas_char = 'j'
            elif last_char in ['w', 'W', 'q', 'Q', 'z']: jas_char = 'q'
            elif last_char in['t', 'T', 'd', 'D', 's']: jas_char = 'd'
            elif last_char in['p', 'P', 'b', 'B']: jas_char = 'b'
            if jas_char != last_char:
                dhatu.text = dhatu.text[:-1] + jas_char

def yuvor_anakau(prakriya: Prakriya) -> None:
    for term in prakriya.terms:
        if term.term_type == 'pratyaya':
            if term.text == 'yu': term.text = 'ana'
            elif term.text == 'vu': term.text = 'aka'

def ata_upadhayah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1] 
    if dhatu and ('Yit' in suffix.tags or 'Rit' in suffix.tags):
        text = dhatu.text
        if len(text) >= 2 and text[-2] == 'a':
            dhatu.text = text[:-2] + 'A' + text[-1]

def rashabhyam_no_nah(prakriya: Prakriya) -> None:
    has_trigger = False
    blocked = False
    allowed_intervening = set(SLP1_VOWELS).union(set('hyvrkKgGNpPbBmM'))
    for term in prakriya.terms:
        new_text = ""
        for char in term.text:
            if char in['r', 'z', 'f', 'F']:
                has_trigger = True
                blocked = False 
                new_text += char
            elif has_trigger and not blocked:
                if char == 'n': new_text += 'R'
                elif char not in allowed_intervening:
                    blocked = True
                    new_text += char
                else: new_text += char
            else: new_text += char
        if term.text != new_text:
            term.text = new_text

def dhatvadeh_sah_sah_no_nah(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if dhatu and dhatu.text:
        text = dhatu.text
        if text.startswith('z'):
            text = 's' + text[1:]
            if text.startswith('sW'): text = 'sT' + text[2:]
            elif text.startswith('sR'): text = 'sn' + text[2:]
            dhatu.text = text
        elif text.startswith('R'):
            dhatu.text = 'n' + text[1:]

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
            'f': 'fcCa', 'sf': 'DAva', 'Sad': 'zIya', 'sad': 'sIda'
        }
        if dhatu.text in adesha_map:
            dhatu.text = adesha_map[dhatu.text]

def upasarga_sandhi(prakriya: Prakriya) -> None:
    """Handles Vowel Sandhi folding multiple Upasargas from right to left."""
    upasarga_indices =[i for i, t in enumerate(prakriya.terms) if t.term_type == 'upasarga']
    
    for idx in reversed(upasarga_indices):
        upasarga = prakriya.terms[idx]
        
        # Find the next NON-EMPTY term (skips terms that were emptied by previous sandhis!)
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
                elif first_vowel in['i', 'I']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'e' + next_term.text[1:]
                elif first_vowel in['u', 'U']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'o' + next_term.text[1:]
                elif first_vowel in['f', 'F']:
                    upasarga.text = upasarga.text[:-1]
                    next_term.text = 'Ar' + next_term.text[1:]
            elif upasarga.text.endswith('i') or upasarga.text.endswith('I'):
                upasarga.text = upasarga.text[:-1] + 'y'
            elif upasarga.text.endswith('u') or upasarga.text.endswith('U'):
                upasarga.text = upasarga.text[:-1] + 'v'

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

def sanadyanta_dhatavah(prakriya: Prakriya) -> None:
    if len(prakriya.terms) >= 2:
        dhatu = prakriya.terms[0]
        suffix = prakriya.terms[1]
        dhatu.text = dhatu.text + suffix.text
        prakriya.terms = [dhatu]

def liti_dhator_anabhyasasya(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and 'liW' in suffix.tags:
        abhyasa = Term(dhatu.upadeza, 'abhyasa')
        abhyasa.text = dhatu.text
        idx = prakriya.terms.index(dhatu)
        prakriya.terms.insert(idx, abhyasa)

def hrasvah(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        short_map = {'A':'a', 'I':'i', 'U':'u', 'F':'f', 'X':'x', 'e':'i', 'o':'u', 'E':'i', 'O':'u'}
        for long_v, short_v in short_map.items():
            text = text.replace(long_v, short_v)
        abhyasa.text = text

def bhavater_ah(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if abhyasa and dhatu and dhatu.upadeza == 'BU':
        abhyasa.text = abhyasa.text.replace('u', 'a').replace('U', 'a')

def abhyase_car_ca(prakriya: Prakriya) -> None:
    abhyasa = next((t for t in prakriya.terms if t.term_type == 'abhyasa'), None)
    if abhyasa:
        text = abhyasa.text
        deaspirate = {'B':'b', 'D':'d', 'G':'g', 'J':'j', 'Q':'q', 'P':'p', 'T':'t', 'K':'k', 'C':'c', 'W':'w'}
        abhyasa.text = "".join([deaspirate.get(c, c) for c in text])

def bhuvo_vug_lunlitoh(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    suffix = prakriya.terms[-1]
    if dhatu and dhatu.upadeza == 'BU' and 'liW' in suffix.tags:
        if suffix.text and is_vowel(suffix.text[0]):
            dhatu.text = dhatu.text + 'v'

def pug_nau(prakriya: Prakriya) -> None:
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    ric_term = next((t for t in prakriya.terms if t.upadeza == 'Ric'), None)
    if ric_term and dhatu.text.endswith('A'):
        dhatu.text = dhatu.text + 'p'

def upasarga_satva(prakriya: Prakriya) -> None:
    """Rule 8.3.65: Upasarga Satva (e.g., prati + sTA -> pratizWA)"""
    upasargas =[t for t in prakriya.terms if t.term_type == 'upasarga']
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    
    # We only look at the LAST upasarga (the one closest to the root)
    if upasargas and dhatu and upasargas[-1].text:
        if upasargas[-1].text[-1] in IN_VOWELS:
            if dhatu.text.startswith('sT'):
                dhatu.text = 'zW' + dhatu.text[2:]


def sna_sandhi(prakriya: Prakriya) -> None:
    vikarana = next((t for t in prakriya.terms if t.term_type == 'vikaraRa'), None)
    suffix = prakriya.terms[-1]
    if vikarana and vikarana.text == 'nA': 
        is_weak = 'pit' not in suffix.tags
        if is_weak:
            if suffix.text and is_vowel(suffix.text[0]):
                vikarana.text = 'n'
            else:
                vikarana.text = 'nI'

def anunasikalopo_jhali_kniti(prakriya: Prakriya) -> None:
    """
    Rule 6.4.37: anunAsikalopo jhali kNiti
    Deletes the final nasal (m, n) of specific roots before a jhal-initial kit/Nit affix.
    e.g., ram + ktvA -> ra + tvA -> ratvA
    """
    dhatu = next((t for t in prakriya.terms if t.term_type == 'dhatu'), None)
    if not dhatu: return
    idx = prakriya.terms.index(dhatu)
    if idx + 1 >= len(prakriya.terms): return
    suffix = prakriya.terms[idx + 1]

    # Check if the affix is kit or Nit
    is_kit_or_nit = 'kit' in suffix.tags or 'Nit' in suffix.tags
    # Check if the affix starts with a jhal consonant (like 't' in tvA)
    starts_with_jhal = suffix.text and suffix.text[0] in JHAL_CONSONANTS
    # Check if the root ends in a nasal
    ends_with_nasal = dhatu.text and dhatu.text[-1] in ['m', 'n']

    if is_kit_or_nit and starts_with_jhal and ends_with_nasal:
        # Pāṇini specifies anudātta roots and a few others (van, tan, etc.)
        # We handle the most common ones here for safety.
        ANUDATTA_NASAL_ROOTS =['ram', 'gam', 'han', 'man', 'yam', 'van', 'tan', 'nam']
        if dhatu.text in ANUDATTA_NASAL_ROOTS:
            dhatu.text = dhatu.text[:-1]
            prakriya.log(f"Rule 6.4.37: Dropped final nasal before jhal+kit/Nit -> '{dhatu.text}'")