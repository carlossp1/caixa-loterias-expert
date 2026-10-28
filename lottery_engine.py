"""
Motor Estatístico e Combinatório Unificado para as 9 Loterias Oficiais da Caixa.
Realiza geração de palpites calibrados (Score 0-100), fechamentos matemáticos,
auditoria de conformidade e conferência de bilhetes.
"""

import random
from itertools import combinations
from typing import List, Dict, Any, Tuple, Optional, Set

from lottery_rules import LOTTERIES_CONFIG, ALL_PRIMES_UP_TO_100, FIBONACCI_NUMBERS

class LotteryAnalyzer:
    """Análise estatística e cálculo de score para qualquer loteria da Caixa."""

    @staticmethod
    def max_consecutive(numbers: List[int]) -> int:
        """Calcula o maior número de dezenas consecutivas no jogo."""
        if not numbers or len(numbers) < 2:
            return 1
        s = sorted(numbers)
        max_c = 1
        curr = 1
        for i in range(1, len(s)):
            if s[i] == s[i - 1] + 1:
                curr += 1
                if curr > max_c:
                    max_c = curr
            else:
                curr = 1
        return max_c

    @classmethod
    def analyze_game(cls, lottery_id: str, numbers: List[int], extras: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Realiza a auditoria estatística completa e atribui Score de 0 a 100."""
        cfg = LOTTERIES_CONFIG.get(lottery_id, LOTTERIES_CONFIG["megasena"])
        filters = cfg.get("stat_filters", {})
        
        # Caso especial: Super Sete
        if cfg.get("special_type") == "columns_matrix":
            return cls._analyze_supersete(numbers, filters)

        sorted_nums = sorted(numbers)
        s_nums = set(numbers)
        total = len(sorted_nums)

        # 1. Paridade
        pares_count = sum(1 for n in sorted_nums if n % 2 == 0)
        impares_count = total - pares_count

        # 2. Primos
        primos_count = len(s_nums.intersection(ALL_PRIMES_UP_TO_100))

        # 3. Fibonacci
        fib_count = len(s_nums.intersection(FIBONACCI_NUMBERS))

        # 4. Soma
        soma = sum(sorted_nums)

        # 5. Consecutivos
        max_seq = cls.max_consecutive(sorted_nums)

        # 6. Moldura / Miolo (Específico para Lotofácil)
        frame_count = 0
        core_count = 0
        if "frame_numbers" in cfg:
            frame_count = len(s_nums.intersection(cfg["frame_numbers"]))
            core_count = len(s_nums.intersection(cfg["core_numbers"]))

        # Cálculo de Score e Alertas
        score = 100
        alerts: List[str] = []
        praises: List[str] = []

        # Validação de Soma
        sum_min, sum_max = filters.get("sum_range", (0, 999999))
        if soma < sum_min:
            penalidade = min(25, int((sum_min - soma) / 2))
            score -= penalidade
            alerts.append(f"Soma baixa ({soma}). A média ideal é entre {sum_min} e {sum_max}.")
        elif soma > sum_max:
            penalidade = min(25, int((soma - sum_max) / 2))
            score -= penalidade
            alerts.append(f"Soma alta ({soma}). A média ideal é entre {sum_min} e {sum_max}.")
        else:
            praises.append(f"Soma perfeita: {soma} (dentro do intervalo ideal de {sum_min}-{sum_max})")

        # Validação de Par/Ímpar
        even_odd_ratios = filters.get("even_odd_ratio", [])
        if even_odd_ratios:
            ratio_match = (pares_count, impares_count) in even_odd_ratios or (impares_count, pares_count) in even_odd_ratios
            if not ratio_match:
                score -= 15
                alerts.append(f"Equilíbrio de {pares_count} pares e {impares_count} ímpares é incomum nos sorteios.")
            else:
                praises.append(f"Paridade equilibrada: {pares_count} pares e {impares_count} ímpares")

        # Validação de Primos
        if "primes_ideal" in filters:
            p_min, p_max = filters["primes_ideal"]
            if primos_count < p_min or primos_count > p_max:
                score -= 10
                alerts.append(f"Quantidade de primos ({primos_count}) fora da faixa mais sorteada ({p_min} a {p_max}).")
            else:
                praises.append(f"Excelente contagem de primos: {primos_count}")

        # Validação de Consecutivos
        max_allowed_seq = filters.get("max_consecutive", 3)
        if max_seq > max_allowed_seq:
            score -= (max_seq - max_allowed_seq) * 10
            alerts.append(f"Sequência consecutiva longa identificada ({max_seq} números seguidos).")

        # Validação Moldura (Lotofácil)
        if "frame_ideal" in filters and frame_count > 0:
            f_min, f_max = filters["frame_ideal"]
            if frame_count < f_min or frame_count > f_max:
                score -= 10
                alerts.append(f"Moldura com {frame_count} números (o padrão em >75% dos jogos é {f_min} a {f_max}).")
            else:
                praises.append(f"Moldura calibrada com {frame_count} dezenas")

        score = max(30, min(100, score))

        # Classificação de Nível
        if score >= 90:
            level = "OURO (Altíssima Probabilidade)"
            level_color = "#2ecc71"
        elif score >= 75:
            level = "PRATA (Muito Bom)"
            level_color = "#3498db"
        elif score >= 60:
            level = "BRONZE (Regular)"
            level_color = "#f39c12"
        else:
            level = "ALERTA (Desvio Estatístico Alto)"
            level_color = "#e74c3c"

        result = {
            "lottery_id": lottery_id,
            "numbers": sorted_nums,
            "total_numbers": total,
            "score": score,
            "level": level,
            "level_color": level_color,
            "soma": soma,
            "pares": pares_count,
            "impares": impares_count,
            "primos": primos_count,
            "fibonacci": fib_count,
            "max_consecutive": max_seq,
            "alerts": alerts,
            "praises": praises
        }

        if frame_count > 0:
            result["moldura"] = frame_count
            result["miolo"] = core_count

        if extras:
            result["extras"] = extras

        return result

    @classmethod
    def _analyze_supersete(cls, numbers: List[int], filters: Dict[str, Any]) -> Dict[str, Any]:
        """Auditoria específica para o Super Sete (7 colunas de 0 a 9)."""
        soma = sum(numbers)
        pares = sum(1 for n in numbers if n % 2 == 0)
        impares = len(numbers) - pares
        distintos = len(set(numbers))

        score = 100
        alerts: List[str] = []
        praises: List[str] = []

        sum_min, sum_max = filters.get("sum_range", (24, 38))
        if soma < sum_min or soma > sum_max:
            score -= 15
            alerts.append(f"Soma das colunas ({soma}) fora da curva normal ({sum_min} a {sum_max}).")
        else:
            praises.append(f"Soma calibrada: {soma}")

        if distintos < 4:
            score -= 25
            alerts.append(f"Muitos números repetidos ({distintos} distintos). Evite concentrar no mesmo dígito.")
        else:
            praises.append(f"Boa dispersão entre as 7 colunas ({distintos} dígitos distintos)")

        score = max(35, min(100, score))

        return {
            "lottery_id": "supersete",
            "numbers": numbers,
            "total_numbers": len(numbers),
            "score": score,
            "level": "OURO" if score >= 85 else "PRATA",
            "level_color": "#2ecc71" if score >= 85 else "#3498db",
            "soma": soma,
            "pares": pares,
            "impares": impares,
            "distintos": distintos,
            "alerts": alerts,
            "praises": praises
        }


class LotteryGenerator:
    """Gerador estocástico com filtros combinatórios para as 9 loterias."""

    @classmethod
    def generate_single_game(
        cls,
        lottery_id: str,
        pick_size: Optional[int] = None,
        fixed_numbers: Optional[List[int]] = None,
        excluded_numbers: Optional[List[int]] = None,
        min_score: int = 75,
        max_attempts: int = 400
    ) -> Dict[str, Any]:
        cfg = LOTTERIES_CONFIG.get(lottery_id, LOTTERIES_CONFIG["megasena"])
        special = cfg.get("special_type", "standard")

        # Tratamento especial do Super Sete
        if special == "columns_matrix":
            return cls._generate_supersete_game(cfg)

        min_n = cfg["min_number"]
        max_n = cfg["max_number"]
        size = pick_size or cfg["default_pick"]
        
        # Garante limites válidos
        size = max(cfg["min_pick"], min(size, cfg["max_pick"]))

        fixed_set = set(fixed_numbers or [])
        excluded_set = set(excluded_numbers or [])

        # Pool de números disponíveis
        pool = [n for n in range(min_n, max_n + 1) if n not in excluded_set and n not in fixed_set]

        needed = size - len(fixed_set)
        if needed < 0 or needed > len(pool):
            # Fallback seguro caso os filtros do usuário sejam impossíveis
            pool = [n for n in range(min_n, max_n + 1) if n not in fixed_set]
            needed = max(0, size - len(fixed_set))

        best_game = None
        best_score = -1

        for _ in range(max_attempts):
            sampled = random.sample(pool, needed)
            full_game = sorted(list(fixed_set) + sampled)
            
            # Gera extras se houver
            extras = cls._generate_extras(lottery_id, cfg)
            
            analysis = LotteryAnalyzer.analyze_game(lottery_id, full_game, extras)
            if analysis["score"] >= min_score:
                analysis["extras"] = extras
                return analysis

            if analysis["score"] > best_score:
                best_score = analysis["score"]
                analysis["extras"] = extras
                best_game = analysis

        return best_game or LotteryAnalyzer.analyze_game(lottery_id, sorted(list(fixed_set) + pool[:needed]))

    @classmethod
    def _generate_extras(cls, lottery_id: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
        extras: Dict[str, Any] = {}
        if lottery_id == "diadesorte":
            months = cfg.get("months", ["Janeiro"])
            extras["mes_da_sorte"] = random.choice(months)
        elif lottery_id == "timemania":
            teams = cfg.get("teams_sample", ["Flamengo / RJ"])
            extras["time_do_coracao"] = random.choice(teams)
        elif lottery_id == "maismilionaria":
            # Escolhe 2 trevos de 1 a 6
            trevos = sorted(random.sample(range(1, 7), 2))
            extras["trevos"] = trevos
        return extras

    @classmethod
    def _generate_supersete_game(cls, cfg: Dict[str, Any]) -> Dict[str, Any]:
        """Gera 1 número entre 0 e 9 para cada uma das 7 colunas."""
        # Tenta gerar um com boa soma e boa variedade
        for _ in range(100):
            cols = [random.randint(0, 9) for _ in range(7)]
            analysis = LotteryAnalyzer.analyze_game("supersete", cols)
            if analysis["score"] >= 80:
                return analysis
        return LotteryAnalyzer.analyze_game("supersete", [random.randint(0, 9) for _ in range(7)])

    @classmethod
    def generate_batch(
        cls,
        lottery_id: str,
        count: int = 5,
        pick_size: Optional[int] = None,
        fixed_numbers: Optional[List[int]] = None,
        excluded_numbers: Optional[List[int]] = None,
        min_score: int = 75
    ) -> List[Dict[str, Any]]:
        """Gera múltiplos palpites calibrados e sem duplicatas."""
        games: List[Dict[str, Any]] = []
        seen_signatures: Set[str] = set()

        attempts = 0
        while len(games) < count and attempts < (count * 20):
            attempts += 1
            game = cls.generate_single_game(
                lottery_id=lottery_id,
                pick_size=pick_size,
                fixed_numbers=fixed_numbers,
                excluded_numbers=excluded_numbers,
                min_score=min_score
            )
            sig = "-".join(str(n) for n in game["numbers"])
            if "extras" in game and "trevos" in game["extras"]:
                sig += f"|T:{game['extras']['trevos']}"
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                games.append(game)

        return games


class LotteryClosings:
    """Fechamentos e Desdobramentos Matemáticos Reduzidos."""

    @classmethod
    def generate_closing(
        cls,
        lottery_id: str,
        selected_numbers: List[int],
        ticket_size: Optional[int] = None,
        max_tickets: int = 12
    ) -> Dict[str, Any]:
        """
        Gera desdobramento matemático inteligente a partir de um conjunto ampliado de números.
        Garante alta cobertura combinatória de pares e trios sem explosão de custos.
        """
        cfg = LOTTERIES_CONFIG.get(lottery_id, LOTTERIES_CONFIG["megasena"])
        size = ticket_size or cfg["default_pick"]
        s_nums = sorted(list(set(selected_numbers)))
        total_selected = len(s_nums)

        if total_selected < size:
            return {
                "error": f"Para esta loteria você deve selecionar no mínimo {size} dezenas para desdobrar.",
                "tickets": []
            }

        if total_selected == size:
            # É apenas 1 jogo simples
            single = LotteryAnalyzer.analyze_game(lottery_id, s_nums)
            return {
                "total_selected": total_selected,
                "ticket_size": size,
                "total_tickets": 1,
                "guarantee": "Aposta individual direta",
                "tickets": [single]
            }

        # Seleção combinatória distribuída
        # Algoritmo de cobertura gulosa para maximizar cobertura de pares
        all_possible_pairs = set(combinations(s_nums, min(3, size)))
        uncovered = set(all_possible_pairs)
        chosen_tickets: List[List[int]] = []

        # Amostragem combinatória inteligente
        all_candidate_combs = list(combinations(s_nums, size))
        random.shuffle(all_candidate_combs)

        for comb in all_candidate_combs:
            comb_set = set(comb)
            comb_pairs = set(combinations(comb, min(3, size)))
            covers_new = len(uncovered.intersection(comb_pairs))
            
            if covers_new > 0 or len(chosen_tickets) < 3:
                chosen_tickets.append(list(comb))
                uncovered -= comb_pairs
                if len(chosen_tickets) >= max_tickets:
                    break

        # Se sobraram poucos, completa até a cota solicitada
        if len(chosen_tickets) < max_tickets and len(all_candidate_combs) > len(chosen_tickets):
            for comb in all_candidate_combs:
                if list(comb) not in chosen_tickets:
                    chosen_tickets.append(list(comb))
                    if len(chosen_tickets) >= max_tickets:
                        break

        analyzed_tickets = [LotteryAnalyzer.analyze_game(lottery_id, t) for t in chosen_tickets]

        # Mensagem de garantia teórica
        guarantee_text = f"Fechamento de {total_selected} dezenas em {len(analyzed_tickets)} jogos de {size} números."

        return {
            "lottery_id": lottery_id,
            "total_selected": total_selected,
            "ticket_size": size,
            "total_tickets": len(analyzed_tickets),
            "guarantee": guarantee_text,
            "coverage_percentage": round(100.0 * (1.0 - (len(uncovered) / max(1, len(all_possible_pairs)))), 1),
            "tickets": analyzed_tickets
        }


class LotteryChecker:
    """Conferência de apostas contra resultados oficiais."""

    @classmethod
    def check_ticket(
        cls,
        lottery_id: str,
        ticket_numbers: List[int],
        drawn_numbers: List[int],
        ticket_extras: Optional[Dict[str, Any]] = None,
        drawn_extras: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Calcula dezenas acertadas, taxa de acerto e faixa de premiação atingida."""
        cfg = LOTTERIES_CONFIG.get(lottery_id, LOTTERIES_CONFIG["megasena"])
        
        # Conversão para inteiros se forem strings
        t_nums = [int(n) for n in ticket_numbers]
        d_nums = [int(n) for n in drawn_numbers]

        if cfg.get("special_type") == "columns_matrix":
            # No Super Sete compara coluna por coluna
            acertos_colunas = sum(1 for i in range(min(len(t_nums), len(d_nums))) if t_nums[i] == d_nums[i])
            acertos = acertos_colunas
            hits_list = [t_nums[i] for i in range(min(len(t_nums), len(d_nums))) if t_nums[i] == d_nums[i]]
        else:
            s_ticket = set(t_nums)
            s_drawn = set(d_nums)
            hits_set = s_ticket.intersection(s_drawn)
            acertos = len(hits_set)
            hits_list = sorted(list(hits_set))

        # Determina a premiação
        prize_tiers = cfg.get("prize_tiers", [])
        premiado = False
        faixa_ganha = "Não premiado"

        for tier in prize_tiers:
            hits_req = tier.get("hits")
            if isinstance(hits_req, int) and acertos == hits_req:
                faixa_ganha = tier["tier"]
                premiado = True
                break
            elif isinstance(hits_req, tuple) and lottery_id == "maismilionaria":
                # (dezenas, trevos)
                req_num, req_clover = hits_req
                clover_hits = 0
                if ticket_extras and drawn_extras:
                    t_clov = set(ticket_extras.get("trevos", []))
                    d_clov = set(drawn_extras.get("trevos", []))
                    clover_hits = len(t_clov.intersection(d_clov))
                if acertos == req_num and clover_hits >= req_clover:
                    faixa_ganha = tier["tier"]
                    premiado = True
                    break

        return {
            "lottery_id": lottery_id,
            "acertos": acertos,
            "dezenas_acertadas": hits_list,
            "premiado": premiado,
            "faixa": faixa_ganha
        }
