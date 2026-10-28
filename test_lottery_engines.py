"""
Testes Automatizados para o Motor de Loterias Caixa Expert.
Valida geração, fechamentos, auditoria e API para todas as 9 loterias.
"""

import unittest
from lottery_rules import LOTTERIES_CONFIG
from lottery_engine import LotteryAnalyzer, LotteryGenerator, LotteryClosings, LotteryChecker
from caixa_api import CaixaLoteriasAPI

class TestLotteryEngines(unittest.TestCase):

    def test_all_lotteries_configured(self):
        expected_lotteries = {
            "megasena", "lotofacil", "quina", "lotomania",
            "duplasena", "diadesorte", "timemania", "maismilionaria", "supersete"
        }
        self.assertEqual(set(LOTTERIES_CONFIG.keys()), expected_lotteries)

    def test_generation_all_lotteries(self):
        for lottery_id, cfg in LOTTERIES_CONFIG.items():
            game = LotteryGenerator.generate_single_game(lottery_id, min_score=60)
            self.assertIn("score", game)
            self.assertGreaterEqual(game["score"], 30)
            self.assertEqual(game["lottery_id"], lottery_id)

            if lottery_id == "supersete":
                self.assertEqual(len(game["numbers"]), 7)
            else:
                self.assertEqual(len(game["numbers"]), cfg["default_pick"])
                # Confere se os números estão no range
                for n in game["numbers"]:
                    self.assertGreaterEqual(n, cfg["min_number"])
                    self.assertLessEqual(n, cfg["max_number"])

    def test_fixed_and_excluded_numbers(self):
        # Testa fixação e exclusão na Mega-Sena
        fixed = [10, 20]
        excluded = [5, 15, 25, 30]
        game = LotteryGenerator.generate_single_game(
            "megasena",
            fixed_numbers=fixed,
            excluded_numbers=excluded
        )
        self.assertTrue(set(fixed).issubset(set(game["numbers"])))
        for ex in excluded:
            self.assertNotIn(ex, game["numbers"])

    def test_closings_generation(self):
        # Fechamento com 10 dezenas na Mega-Sena
        pool = [2, 14, 23, 31, 38, 42, 45, 50, 55, 60]
        closing = LotteryClosings.generate_closing("megasena", pool, max_tickets=4)
        self.assertGreaterEqual(len(closing["tickets"]), 1)
        self.assertEqual(closing["total_selected"], 10)
        self.assertEqual(closing["ticket_size"], 6)

    def test_checker(self):
        # Bilhete da Quina
        ticket = [10, 20, 30, 40, 50]
        drawn = [10, 20, 30, 71, 75]
        res = LotteryChecker.check_ticket("quina", ticket, drawn)
        self.assertEqual(res["acertos"], 3)
        self.assertTrue(res["premiado"])
        self.assertIn("Terno", res["faixa"])

    def test_caixa_api_baseline(self):
        for lottery_id in LOTTERIES_CONFIG.keys():
            res = CaixaLoteriasAPI.get_latest_result(lottery_id)
            self.assertIn("numero", res)
            self.assertIn("listaDezenas", res)
            self.assertGreater(len(res["listaDezenas"]), 0)

if __name__ == "__main__":
    unittest.main()
