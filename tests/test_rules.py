import unittest
from models import Term, Prakriya
from rules import substitute_lakara, insert_vikarana

class TestRules(unittest.TestCase):

    def test_substitute_lakara_parasmaipada(self):
        """Test Rule 3.4.78 for a Parasmaipada root (e.g., akz)"""
        p = Prakriya()
        dhatu = Term('akz', 'dhatu')
        dhatu.tags.add('parasmaipada')
        p.add_term(dhatu)
        p.add_term(Term('laW', 'lakara'))
        
        # Call the rule
        substitute_lakara(p, purusha='prathama', vacana=0)
        
        # The lakara should now be 'tip'
        self.assertEqual(p.terms[-1].text, 'tip')
        self.assertEqual(p.terms[-1].term_type, 'pratyaya')

    def test_substitute_lakara_atmanepada(self):
        """Test Rule 3.4.78 for an Atmanepada root (e.g., edh/aMh)"""
        p = Prakriya()
        dhatu = Term('aMh', 'dhatu')
        dhatu.tags.add('atmanepada')
        p.add_term(dhatu)
        p.add_term(Term('laW', 'lakara'))
        
        substitute_lakara(p, purusha='prathama', vacana=0)
        
        # The lakara should now be 'ta'
        self.assertEqual(p.terms[-1].text, 'ta')

    def test_insert_vikarana_gana_1(self):
        """Test Rule 3.1.68 (kartari Sap) for Gana 1 roots"""
        p = Prakriya()
        dhatu = Term('akz', 'dhatu')
        dhatu.tags.add('gana_1')
        p.add_term(dhatu)
        p.add_term(Term('tip', 'pratyaya'))
        
        insert_vikarana(p)
        
        # 'Sap' should be inserted in the middle
        self.assertEqual(len(p.terms), 3)
        self.assertEqual(p.terms[1].text, 'Sap')
        self.assertEqual(p.terms[1].term_type, 'vikaraRa')

    def test_no_vikarana_for_gana_2(self):
        """Ensure Gana 2 roots (like ad) do not get 'Sap' here."""
        p = Prakriya()
        dhatu = Term('ad', 'dhatu')
        dhatu.tags.add('gana_2')
        p.add_term(dhatu)
        p.add_term(Term('tip', 'pratyaya'))
        
        insert_vikarana(p)
        
        # Should still just be Dhatu + Suffix
        self.assertEqual(len(p.terms), 2)