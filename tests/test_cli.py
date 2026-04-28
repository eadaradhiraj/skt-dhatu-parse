import unittest
from unittest.mock import patch
import sys
from skt_dhatu_parse.cli import resolve_gana, main

class DummyTerm:
    def __init__(self, text):
        self.text = text

class DummyPrakriya:
    """A concrete dummy class to bypass MagicMock quirks."""
    def __init__(self, string_val="Bavati"):
        self.string_val = string_val
        self.terms =[DummyTerm(string_val)] # <-- FIXED: It now has a real 'text' attribute!
        
    def get_current_string(self): 
        return self.string_val
        
    def print_history(self): 
        print("Derivation History")

class TestCLI(unittest.TestCase):

    @patch('skt_dhatu_parse.cli.get_dhatu')
    def test_resolve_gana_single_match(self, mock_get_dhatu) -> None:
        class MockDhatu: tags = {'gana_4'}
        mock_get_dhatu.return_value =[MockDhatu()]
        self.assertEqual(resolve_gana('div'), 4)

    @patch('skt_dhatu_parse.cli.get_dhatu')
    @patch('builtins.print')  
    def test_resolve_gana_default_to_one(self, mock_print, mock_get_dhatu) -> None:
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        self.assertEqual(resolve_gana('BU'), 1)
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("belongs to multiple classes" in s for s in prints))

    @patch('skt_dhatu_parse.cli.get_dhatu')
    def test_resolve_gana_user_specified(self, mock_get_dhatu) -> None:
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        self.assertEqual(resolve_gana('BU', user_gana=10), 10)

    @patch('skt_dhatu_parse.cli.get_dhatu')
    @patch('builtins.print') 
    def test_resolve_gana_not_found(self, mock_print, mock_get_dhatu) -> None:
        mock_get_dhatu.return_value =[]
        with self.assertRaises(SystemExit):
            resolve_gana('xyz')
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("not found" in s for s in prints))

    # ==========================================
    # ISOLATED CLI ROUTING TESTS
    # ==========================================

    @patch('sys.argv',['cli.py', 'BU', '-l', 'laW'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_single_derivation(self, mock_print, mock_resolve, mock_derive) -> None:
        mock_resolve.return_value = 1
        mock_derive.return_value = DummyPrakriya('Bavati')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Bavati' in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '--history'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_with_history(self, mock_print, mock_resolve, mock_derive) -> None:
        mock_resolve.return_value = 1
        mock_derive.return_value = DummyPrakriya('Bavati')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Derivation History' in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '--table'])
    @patch('skt_dhatu_parse.cli.print_conjugation')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    def test_main_table(self, mock_resolve, mock_print_conj) -> None:
        mock_resolve.return_value = 1
        main()
        mock_print_conj.assert_called_once()

    @patch('sys.argv', ['cli.py', 'BU', '--causative', '--table'])
    @patch('skt_dhatu_parse.cli.derive_secondary_root')
    @patch('skt_dhatu_parse.cli.print_conjugation')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_causative_table(self, mock_print, mock_resolve, mock_print_conj, mock_derive_sec) -> None:
        mock_resolve.return_value = 1
        mock_derive_sec.return_value = DummyPrakriya('BAvi')
        main()
        mock_derive_sec.assert_called_once()
        mock_print_conj.assert_called_once()

    @patch('sys.argv',['cli.py', 'buD', '--krt', 'kta'])
    @patch('skt_dhatu_parse.cli.derive_krdanta')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_krdanta(self, mock_print, mock_resolve, mock_derive_krt) -> None:
        mock_resolve.return_value = 1
        mock_derive_krt.return_value = DummyPrakriya('budDa')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('budDa' in s for s in prints))

    @patch('sys.argv',['cli.py', 'vi-krI', '-l', 'laW'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_upasarga_parsing(self, mock_print, mock_resolve, mock_derive) -> None:
        mock_resolve.return_value = 1
        mock_derive.return_value = DummyPrakriya('vikrIRIte')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('vikrIRIte' in s for s in prints))

    @patch('sys.argv',['cli.py', 'xyz-BU'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('skt_dhatu_parse.cli.resolve_gana')
    @patch('builtins.print')
    def test_main_invalid_upasarga(self, mock_print, mock_resolve, mock_derive) -> None:
        mock_resolve.return_value = 1
        mock_derive.return_value = DummyPrakriya('Bavati')
        main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('not a recognized Pāṇinian Upasarga' in s for s in prints))

    @patch('skt_dhatu_parse.conjugate.derive')
    @patch('builtins.print')
    def test_conjugate_failure(self, mock_print, mock_derive) -> None:
        mock_derive.return_value = None
        from skt_dhatu_parse.conjugate import print_conjugation
        print_conjugation('xyz')
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed to derive forms' in s for s in prints))

if __name__ == '__main__':
    unittest.main()