import unittest
from skt_dhatu_parse.sanadi import derive_secondary_root

class TestDesiderative(unittest.TestCase):
    def test_san_path(self) -> None:
        """paṭh -> pipaṭhiṣa (seṭ, sany ataḥ)"""
        prakriya = derive_secondary_root('paW', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'pipaWiza')

    def test_san_gam(self) -> None:
        """gam -> jigamiṣa (seṭ override, jeś ca)"""
        prakriya = derive_secondary_root('gam', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jigamiza')

    def test_san_pa(self) -> None:
        """pā -> pipāsa (aniṭ)"""
        prakriya = derive_secondary_root('pA', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'pipAsa')

    def test_san_kr(self) -> None:
        """kṛ -> cikīrṣa (ṛta id dhātoḥ, hali ca, kuhoś cuḥ)"""
        prakriya = derive_secondary_root('kf', 'san', gana=8)
        self.assertEqual(prakriya.get_current_string(), 'cikIrza')

    def test_san_budh(self) -> None:
        """budh -> bubhutsa (iko jhal -> kit, khari ca)"""
        prakriya = derive_secondary_root('buD', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'buButsa')

    def test_san_sru(self) -> None:
        """śru -> śuśrūṣa (ajjhanagamāṃ sani)"""
        prakriya = derive_secondary_root('Sru', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'SuSrUza')
        
    def test_san_ji(self) -> None:
        """ji -> jigīṣa (ajjhanagamāṃ sani, jeś ca)"""
        prakriya = derive_secondary_root('ji', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'jigIza')

    def test_san_bhu(self) -> None:
        """bhū -> bubhūṣa (ajjhanagamāṃ sani blocked, but no changes needed)"""
        prakriya = derive_secondary_root('BU', 'san', gana=1)
        self.assertEqual(prakriya.get_current_string(), 'buBUza')


    def test_san_pRR(self) -> None:
        """pṝ -> pupūrṣa (ud oṣṭhyapūrvasya)"""
        prakriya = derive_secondary_root('pF', 'san', gana=9)
        self.assertEqual(prakriya.get_current_string(), 'pupUrza')

if __name__ == '__main__':
    unittest.main()
