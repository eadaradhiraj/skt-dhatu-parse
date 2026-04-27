"""
models.py
Core data structures for the Paninian derivation engine.
"""

from typing import List, Set

class Term:
    """
    Represents a single grammatical element (Root, Infix, Suffix, etc.).
    """
    def __init__(self, upadeza: str, term_type: str) -> None:
        # The original pedagogical instruction (e.g., 'tip', 'zap', 'akzU!')
        self.upadeza: str = upadeza 
        
        # The current working string. This will mutate as rules apply.
        self.text: str = upadeza    
        
        # Type of the term: 'dhatu', 'pratyaya', 'vikaraRa', 'Agama'
        self.term_type: str = term_type
        
        # A set to store tags like 'pit', 'Rit', 'sarvadhatuka', 'gana_1', etc.
        self.tags: Set[str] = set()
        
    def __repr__(self) -> None:
        return f"Term(text='{self.text}', tags={self.tags})"


class Prakriya:
    """
    Represents the derivation process. It acts as a State Machine.
    """
    def __init__(self):
        # The sequence of terms. E.g.,[Term('BU'), Term('zap'), Term('tip')]
        self.terms: List[Term] =[]
        self.history: List[str] =[]

    def add_term(self, term: Term) -> None:
        self.terms.append(term)
        self.log(f"Added {term.term_type}: {term.upadeza}")

    def log(self, message: str) -> None:
        self.history.append(message)
        
    def get_current_string(self) -> str:
        """Returns the concatenated word as it currently stands."""
        return "".join([t.text for t in self.terms])

    def print_history(self) -> None:
        print("--- Derivation History ---")
        for step in self.history:
            print(step)
        print(f"Result: {self.get_current_string()}")