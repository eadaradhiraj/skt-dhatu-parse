import unittest
from unittest.mock import patch, MagicMock
import sys
from skt_dhatu_parse.cli import resolve_gana, main

class DummyPrakriya:
    def __init__(self, string_val="Bavati"):
        self.string_val = string_val
        self.terms = [1]
        
    def get_current_string(self): return self.string_val
    def print_history(self): pass

class TestCLI(unittest.TestCase):

    def test_resolve_gana_single_match(self) -> None:
        # 'akz' is only in Gana 1 in the TSV
        self.assertEqual(resolve_gana('akz'), 1)

    @patch('builtins.print')  
    def test_resolve_gana_default_to_one(self, mock_print) -> None:
        # 'BU' is in multiple ganas. Defaults to 1.
        self.assertEqual(resolve_gana('BU'), 1)
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("Warning: 'BU' belongs to multiple classes" in s for s in prints))

    def test_resolve_gana_user_specified(self) -> None:
        self.assertEqual(resolve_gana('BU', user_gana=10), 10)

    @patch('builtins.print') 
    def test_resolve_gana_not_found(self, mock_print) -> None:
        with self.assertRaises(SystemExit):
            resolve_gana('xyz_invalid_root_123')
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("not found" in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '-l', 'laW'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('builtins.print')
    def test_main_single_derivation(self, mock_print, mock_derive) -> None:
        mock_derive.return_value = DummyPrakriya('Bavati')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Bavati' in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '--history'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('builtins.print')
    def test_main_with_history(self, mock_print, mock_derive) -> None:
        mock_p = MagicMock()
        mock_p.__bool__.return_value = True
        mock_p.get_current_string.return_value = 'Bavati'
        mock_derive.return_value = mock_p
        main()
        mock_p.print_history.assert_called_once()

    @patch('sys.argv',['cli.py', 'BU', '--table'])
    @patch('skt_dhatu_parse.cli.print_conjugation')
    def test_main_table(self, mock_print_conj) -> None:
        main()
        mock_print_conj.assert_called_once()

    @patch('sys.argv',['cli.py', 'BU', '--causative', '--table'])
    @patch('skt_dhatu_parse.cli.derive_secondary_root')
    @patch('skt_dhatu_parse.cli.print_conjugation')
    @patch('builtins.print')
    def test_main_causative_table(self, mock_print, mock_print_conj, mock_derive_sec) -> None:
        mock_p = MagicMock()
        mock_p.__bool__.return_value = True
        mock_p.terms =[MagicMock(text='BAvi')]
        mock_derive_sec.return_value = mock_p
        main()
        mock_derive_sec.assert_called_once()
        mock_print_conj.assert_called_once()

    @patch('sys.argv',['cli.py', 'buD', '--krt', 'kta'])
    @patch('skt_dhatu_parse.cli.derive_krdanta')
    @patch('builtins.print')
    def test_main_krdanta(self, mock_print, mock_derive_krt) -> None:
        mock_derive_krt.return_value = DummyPrakriya('budDa')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('budDa' in s for s in prints))

    @patch('sys.argv',['cli.py', 'vi-krI', '-l', 'laW'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('builtins.print')
    def test_main_upasarga_parsing(self, mock_print, mock_derive) -> None:
        mock_derive.return_value = DummyPrakriya('vikrIRIte')
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('vikrIRIte' in s for s in prints))

    @patch('sys.argv',['cli.py', 'xyz-BU'])
    @patch('skt_dhatu_parse.cli.derive')
    @patch('builtins.print')
    def test_main_invalid_upasarga(self, mock_print, mock_derive) -> None:
        mock_derive.return_value = DummyPrakriya('Bavati')
        main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('not a recognized Pāṇinian Upasarga' in s for s in prints))

    @patch('skt_dhatu_parse.conjugate.derive')
    @patch('builtins.print')
    def test_conjugate_failure(self, mock_print, mock_derive) -> None:
        mock_derive.return_value = None
        from skt_dhatu_parse.conjugate import print_conjugation
        print_conjugation('xyz_invalid_root')
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed to derive forms' in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '--all-krt'])
    @patch('skt_dhatu_parse.cli.derive_krdanta')
    @patch('builtins.print')
    def test_main_all_krt(self, mock_print, mock_derive_krt) -> None:
        mock_prakriya = MagicMock()
        mock_prakriya.get_current_string.return_value = 'BUta'
        mock_derive_krt.return_value = mock_prakriya
        main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('BUta' in s for s in prints))

    @patch('sys.argv', ['cli.py', 'BU', '--all-krt'])
    @patch('skt_dhatu_parse.cli.derive_krdanta')
    @patch('builtins.print')
    def test_main_all_krt_failure(self, mock_print, mock_derive_krt) -> None:
        mock_derive_krt.return_value = None
        main()
        prints =[str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed' in s for s in prints))

    @patch('sys.argv', ['cli.py', 'xyz_invalid', '--causative'])
    @patch('skt_dhatu_parse.cli.derive_secondary_root')
    @patch('builtins.print')
    def test_main_causative_failure(self, mock_print, mock_derive_sec) -> None:
        mock_derive_sec.return_value = None
        with self.assertRaises(SystemExit):
            main()

    @patch('sys.argv',['cli.py', 'BU', '--causative'])
    @patch('skt_dhatu_parse.cli.derive_secondary_root', return_value=None)
    @patch('builtins.print')
    def test_cli_causative_failure(self, mock_print, mock_derive_sec) -> None:
        """Forces the causative generator to fail after passing the DB check."""
        with self.assertRaises(SystemExit):
            main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed to generate causative' in s for s in prints))

    @patch('sys.argv', ['cli.py', 'BU', '-g', '99'])
    @patch('builtins.print')
    def test_cli_invalid_user_gana(self, mock_print) -> None:
        with self.assertRaises(SystemExit):
            main()

    def test_resolve_gana_multiple_no_gana_1(self) -> None:
        """Covers when a root has multiple ganas but Gana 1 is NOT one of them."""
        with patch('skt_dhatu_parse.cli.get_dhatu') as mock_get:
            t1 = MagicMock()
            t1.tags = ['gana_4']
            t2 = MagicMock()
            t2.tags =['gana_6']
            mock_get.return_value = [t1, t2]
            with patch('builtins.print'):
                from skt_dhatu_parse.cli import resolve_gana
                gana = resolve_gana('mock_root')
                self.assertEqual(gana, 4) # Should default to the first available

    @patch('sys.argv',['cli.py', 'BU', '--voice', 'atmanepada'])
    @patch('builtins.print')
    def test_cli_voice_override(self, mock_print) -> None:
        main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Bavate' in s for s in prints))

    @patch('sys.argv',['cli.py', 'BU', '--all-krt'])
    @patch('skt_dhatu_parse.cli.derive_krdanta', return_value=None)
    @patch('builtins.print')
    def test_cli_all_krt_failure(self, mock_print, mock_derive) -> None:
        main()
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed' in s for s in prints))

    @patch('skt_dhatu_parse.conjugate.derive', return_value=None)
    @patch('builtins.print')
    def test_conjugate_failure(self, mock_print, mock_derive) -> None:
        """Hits line 52 in conjugate.py where the 3x3 table fails to build."""
        from skt_dhatu_parse.conjugate import print_conjugation
        print_conjugation('BU', lakara_name='laW', gana=1)
        prints = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any('Failed to derive forms' in s for s in prints))

if __name__ == '__main__':
    unittest.main()