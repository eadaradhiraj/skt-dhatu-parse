"""
analyzer.py
Reverse Lookup MVP.
"""
def analyze_word(word: str) -> dict:
    results =[]
    # Basic Verbal checks
    if word.endswith('ati'): results.append("Verb: laṭ prathama eka (Parasmaipada)")
    if word.endswith('anti'): results.append("Verb: laṭ prathama bahu (Parasmaipada)")
    if word.endswith('ate'): results.append("Verb: laṭ prathama eka (Ātmanepada)")
    
    # Basic Nominal checks
    if word.endswith('aH') or word.endswith('am') or word.endswith('A'): 
        results.append("Noun: Nominative/Accusative Singular")
    if word.endswith('eRa') or word.endswith('ayA') or word.endswith('RA'): 
        results.append("Noun: Instrumental Singular")
    
    if not results:
        results.append("Unrecognized or ambiguous grammatical form.")
        
    return {"word": word, "analysis": results}
