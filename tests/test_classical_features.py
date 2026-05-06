import unittest
from skt_dhatu_parse.engine import derive
from skt_dhatu_parse.krdanta import derive_krdanta

class TestClassicalFeatures(unittest.TestCase):

    def test_krdanta_ktin_gati(self) -> None:
        """gam + ktin -> gati (anunāsika lopa)"""
        prakriya = derive_krdanta('gam', 'ktin', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'gati')

    def test_krdanta_ktin_krti(self) -> None:
        """kṛ + ktin -> kṛti (kit blocks guna)"""
        prakriya = derive_krdanta('kf', 'ktin', gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kfti')

    def test_krdanta_kyap_krtya(self) -> None:
        """kṛ + kyap -> kṛtya (tuk augment due to pit/kit)"""
        prakriya = derive_krdanta('kf', 'kyap', gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kftya')

    def test_krdanta_namul_karam(self) -> None:
        """kṛ + ṇamul -> kāram (ṇit triggers vṛddhi)"""
        prakriya = derive_krdanta('kf', 'Ramul', gana=8)
        self.assertEqual(prakriya.get_current_string(), 'kAram')

    def test_upasarga_voice_shift(self) -> None:
        """vi + ji + laṭ -> vijayate (Not vijayati)"""
        prakriya = derive('ji', 'laW', purusha='prathama', vacana=0, gana=1, upasargas=['vi'])
        self.assertEqual(prakriya.get_current_string(), 'vijayate')

    def test_upasarga_voice_shift_sam_gam(self) -> None:
        """sam + gam + laṭ -> saṅgacchate (Not saṅgacchati)"""
        prakriya = derive('gam', 'laW', purusha='prathama', vacana=0, gana=1, upasargas=['sam'])
        self.assertEqual(prakriya.get_current_string(), 'saNgacCate')

    def test_vet_optional_it_syand(self) -> None:
        """syand + lṛṭ -> syantsyate (aniṭ) OR syandiṣyate (seṭ)"""
        # Primary timeline (Seṭ vikalpa)
        p_set = derive('syand', 'lfW', purusha='prathama', vacana=0, gana=1, vikalpa=False)
        self.assertEqual(p_set.get_current_string(), 'syandizyate')

        # Alternative timeline (Aniṭ vikalpa via khari ca consonant sandhi)
        p_anit = derive('syand', 'lfW', purusha='prathama', vacana=0, gana=1, vikalpa=True)
        self.assertEqual(p_anit.get_current_string(), 'syantsyate')

if __name__ == '__main__':
    unittest.main()
