import unittest
from skt_dhatu_parse.analyzer import analyze_word

class TestAnalyzer(unittest.TestCase):
    def test_analyze_verb(self):
        res = analyze_word('Bavati')
        self.assertTrue(any('laṭ prathama eka' in s for s in res['analysis']))
        
    def test_analyze_noun(self):
        res = analyze_word('rAmaH')
        self.assertTrue(any('Nominative' in s for s in res['analysis']))
        
    def test_analyze_fail(self):
        res = analyze_word('xyz')
        self.assertTrue(any('Unrecognized' in s for s in res['analysis']))


    def test_analyze_inst(self):
        res = analyze_word('rAmeRa')
        self.assertTrue(any('Instrumental' in s for s in res['analysis']))
