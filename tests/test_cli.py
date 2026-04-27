import unittest
from unittest.mock import patch
import sys
import io

# Import the functions from our cli
from cli import resolve_gana, main

class TestCLI(unittest.TestCase):

    @patch('cli.get_dhatu')
    def test_resolve_gana_single_match(self, mock_get_dhatu):
        """Test that if a root only has one Gana, it returns that Gana."""
        # Mocking a Dhatu object with a gana_4 tag
        class MockDhatu:
            tags = {'gana_4'}
            
        mock_get_dhatu.return_value = [MockDhatu()]
        
        gana = resolve_gana('div')
        self.assertEqual(gana, 4)

    @patch('cli.get_dhatu')
    def test_resolve_gana_default_to_one(self, mock_get_dhatu):
        """Test that if a root has multiple Ganas including 1, it defaults to 1."""
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        
        gana = resolve_gana('BU')
        self.assertEqual(gana, 1)

    @patch('cli.get_dhatu')
    def test_resolve_gana_user_specified(self, mock_get_dhatu):
        """Test that user can manually override the default Gana."""
        class MockDhatu1: tags = {'gana_10'}
        class MockDhatu2: tags = {'gana_1'}
        
        mock_get_dhatu.return_value =[MockDhatu1(), MockDhatu2()]
        
        gana = resolve_gana('BU', user_gana=10)
        self.assertEqual(gana, 10)

    @patch('cli.get_dhatu')
    def test_resolve_gana_not_found(self, mock_get_dhatu):
        """Test that the app exits safely with code 1 if root doesn't exist."""
        mock_get_dhatu.return_value =[]
        
        # We expect sys.exit(1) to be called
        with self.assertRaises(SystemExit) as cm:
            resolve_gana('xyz')
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.argv',['cli.py', 'BU', '-l', 'laW', '-p', 'prathama', '-v', '0'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_single_derivation(self, mock_stdout):
        """Simulate running: python cli.py BU -l laW -p prathama -v 0"""
        main()
        output = mock_stdout.getvalue()
        
        # It should successfully derive Bavati
        self.assertIn('Bavati', output)
        self.assertNotIn('Derivation History', output) # History flag wasn't passed

    @patch('sys.argv', ['cli.py', 'BU', '--history'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_history(self, mock_stdout):
        """Simulate running: python cli.py BU --history"""
        main()
        output = mock_stdout.getvalue()
        
        self.assertIn('Bavati', output)
        self.assertIn('Derivation History', output)
        self.assertIn('Added dhatu: BU', output)

if __name__ == '__main__':
    unittest.main()