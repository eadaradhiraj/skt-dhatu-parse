import unittest
from skt_dhatu_parse.dhatu_loader import get_dhatu

class TestDhatuLoader(unittest.TestCase):

    def test_fetch_single_dhatu(self) -> None:
        """Test fetching a root (akz) that only exists in one Gaṇa"""
        results = get_dhatu("akz", gana=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].upadeza, "akzU!")
        self.assertIn("parasmaipada", results[0].tags)

    def test_fetch_multiple_ganas(self) -> None:
        """Test fetching a homonym root (aMh)"""
        results = get_dhatu("aMh")
        self.assertTrue(len(results) >= 2)

    def test_fetch_filtered_gana(self) -> None:
        """Test fetching a homonym root (aMh) while specifying Gaṇa"""
        results = get_dhatu("aMh", gana=1)
        self.assertEqual(len(results), 1)
        self.assertIn("atmanepada", results[0].tags)

if __name__ == '__main__':
    unittest.main()