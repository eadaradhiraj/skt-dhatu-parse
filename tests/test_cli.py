import unittest
from unittest.mock import patch
import sys
import io
from skt_dhatu_parse.cli import resolve_gana, main

class TestCLI(unittest.TestCase):

    @patch('skt_dhatu_parse.cli.get_dhatu')
    def test_resolve_gana_single_match(self, mock_get_dhatu) -> None:
        class MockDhatu: tags = {'gana_4'}
        mock_get_dhatu.return_value = [MockDhatu()]
        self.assertEqual(resolve_gana('div'), 4)

    @patch('skt_dhatu_parse.cli.get_dhatu')
    @patch('sys.stdout', new_callable=io.StringIO)  
    def test_resolve_gana_default_to_one(self, mock_stdout, mock_get_dhatu) -> None:
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        self.assertEqual(resolve_gana('BU'), 1)

    @patch('skt_dhatu_parse.cli.get_dhatu')
    def test_resolve_gana_user_specified(self, mock_get_dhatu) -> None:
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        self.assertEqual(resolve_gana('BU', user_gana=10), 10)

    @patch('skt_dhatu_parse.cli.get_dhatu')
    @patch('sys.stdout', new_callable=io.StringIO) 
    def test_resolve_gana_not_found(self, mock_stdout, mock_get_dhatu) -> None:
        mock_get_dhatu.return_value =[]
        with self.assertRaises(SystemExit):
            resolve_gana('xyz')

    @patch('sys.argv',['cli.py', 'BU', '-l', 'laW'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_single_derivation(self, mock_stdout) -> None:
        main()
        self.assertIn('Bavati', mock_stdout.getvalue())

    @patch('sys.argv',['cli.py', 'BU', '--history'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_history(self, mock_stdout) -> None:
        main()
        self.assertIn('Derivation History', mock_stdout.getvalue())

    # --- NEW: COVERAGE FOR CONJUGATE.PY AND CLI FLAGS ---
    
    @patch('sys.argv',['cli.py', 'BU', '--table'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_table(self, mock_stdout) -> None:
        main()
        self.assertIn('Bavati', mock_stdout.getvalue())
        self.assertIn('Bavanti', mock_stdout.getvalue())

    @patch('sys.argv',['cli.py', 'BU', '--causative', '--table'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_causative_table(self, mock_stdout) -> None:
        main()
        self.assertIn('BAvayati', mock_stdout.getvalue())

    @patch('sys.argv',['cli.py', 'buD', '--krt', 'kta'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_krdanta(self, mock_stdout) -> None:
        main()
        self.assertIn('budDa', mock_stdout.getvalue())

    @patch('skt_dhatu_parse.conjugate.derive')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_conjugate_failure(self, mock_stdout, mock_derive) -> None:
        mock_derive.return_value = None
        from skt_dhatu_parse.conjugate import print_conjugation
        print_conjugation('xyz')
        self.assertIn('Failed to derive forms', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()