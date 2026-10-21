"""
Motor de Análise Estatística e Geração de Palpites Inteligentes da Lotofácil
Autor: Especialista Lotofácil
"""

import random
from itertools import combinations
from typing import List, Dict, Any, Tuple, Optional, Set

# Constantes Fundamentais da Lotofácil
TOTAL_NUMBERS = 25
GAME_SIZE = 15

MOLDURA = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25} # 16 dezenas
MIOLO = {7, 8, 9, 12, 13, 14, 17, 18, 19}                             # 9 dezenas
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}                              # 9 dezenas
FIBONACCI = {1, 2, 3, 5, 8, 13, 21}                                    # 7 dezenas
MULTIPLOS_3 = {3, 6, 9, 12, 15, 18, 21, 24}                           # 8 dezenas
PARES = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24}                  # 12 dezenas
IMPARES = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25}             # 13 dezenas

# Linhas e Colunas do Volante
LINHAS = [
    {1, 2, 3, 4, 5},
    {6, 7, 8, 9, 10},
    {11, 12, 13, 14, 15},
    {16, 17, 18, 19, 20},
    {21, 22, 23, 24, 25}
]

COLUNAS = [
    {1, 6, 11, 16, 21},
    {2, 7, 12, 17, 22},
    {3, 8, 13, 18, 23},
    {4, 9, 14, 19, 24},
    {5, 10, 15, 20, 25}
]

class LotofacilStats:
    """Classe para auditoria estatística completa de um jogo de 15 dezenas."""

    @staticmethod
    def max_consecutive(numbers: List[int]) -> int:
        """Calcula o maior número de dezenas consecutivas no jogo."""
        s = sorted(numbers)
        max_c = 1
        curr = 1
        for i in range(1, len(s)):
            if s[i] == s[i-1] + 1:
                curr += 1
                if curr > max_c:
                    max_c = curr
            else:
                curr = 1
        return max_c

    @classmethod
    def analyze_game(cls, numbers: List[int], last_contest: Optional[List[int]] = None) -> Dict[str, Any]:
        """Realiza a radiografia estatística completa do jogo."""
        s_nums = set(numbers)
        sorted_nums = sorted(numbers)
        
        impares_count = len(s_nums.intersection(IMPARES))
        pares_count = len(s_nums.intersection(PARES))
        moldura_count = len(s_nums.intersection(MOLDURA))
        miolo_count = len(s_nums.intersection(MIOLO))
        primos_count = len(s_nums.intersection(PRIMOS))
        fibonacci_count = len(s_nums.intersection(FIBONACCI))
        mult3_count = len(s_nums.intersection(MULTIPLOS_3))
        soma = sum(sorted_nums)
        max_seq = cls.max_consecutive(sorted_nums)
        
        linhas_dist = [len(s_nums.intersection(linha)) for linha in LINHAS]
        colunas_dist = [len(s_nums.intersection(col)) for col in COLUNAS]
        
        repetidas = None
        if last_contest:
            repetidas = len(s_nums.intersection(set(last_contest)))
            
        # Sistema de pontuação e conformidade (Score 0-100)
        score = 0
        feedbacks = []
        
        # 1. Pares e Ímpares (Peso 20): ideal 7-8 ou 8-7
        if (impares_count, pares_count) in [(8, 7), (7, 8)]:
            score += 20
            feedbacks.append(("Excelente", f"Pares/Ímpares perfeitos: {pares_count} pares e {impares_count} ímpares."))
        elif (impares_count, pares_count) in [(9, 6), (6, 9)]:
            score += 14
            feedbacks.append(("Bom", f"Pares/Ímpares aceitáveis: {pares_count} pares e {impares_count} ímpares."))
        else:
            score += 5
            feedbacks.append(("Alerta", f"Desbalanceado: {pares_count} pares e {impares_count} ímpares (raro de ocorrer)."))

        # 2. Moldura e Miolo (Peso 20): ideal 10 moldura / 5 miolo ou 9 moldura / 6 miolo
        if (moldura_count, miolo_count) in [(10, 5), (9, 6)]:
            score += 20
            feedbacks.append(("Excelente", f"Moldura/Miolo perfeito: {moldura_count} na moldura e {miolo_count} no miolo."))
        elif (moldura_count, miolo_count) in [(11, 4), (8, 7)]:
            score += 13
            feedbacks.append(("Bom", f"Moldura/Miolo razoável: {moldura_count} moldura / {miolo_count} miolo."))
        else:
            score += 4
            feedbacks.append(("Alerta", f"Distribuição atípica de moldura ({moldura_count}) e miolo ({miolo_count})."))

        # 3. Primos (Peso 15): ideal 5 ou 6
        if primos_count in [5, 6]:
            score += 15
            feedbacks.append(("Excelente", f"Primos no alvo: {primos_count} números primos."))
        elif primos_count in [4, 7]:
            score += 10
            feedbacks.append(("Bom", f"Primos aceitáveis: {primos_count} números primos."))
        else:
            score += 3
            feedbacks.append(("Alerta", f"Quantidade incomum de primos: {primos_count}."))

        # 4. Soma (Peso 15): ideal 170 a 210
        if 180 <= soma <= 205:
            score += 15
            feedbacks.append(("Excelente", f"Soma ideal: {soma} (média teórica é 195)."))
        elif 165 <= soma <= 215:
            score += 10
            feedbacks.append(("Bom", f"Soma aceitável: {soma}."))
        else:
            score += 2
            feedbacks.append(("Alerta", f"Soma fora da curva ({soma}). Jogos premiados raramente fogem de 165-215."))

        # 5. Sequência Consecutiva (Peso 10): ideal max 4 ou 5
        if max_seq in [3, 4, 5]:
            score += 10
            feedbacks.append(("Excelente", f"Sequência máxima equilibrada ({max_seq} seguidos)."))
        elif max_seq in [2, 6]:
            score += 6
            feedbacks.append(("Bom", f"Sequência máxima de {max_seq} seguidos."))
        else:
            score += 1
            feedbacks.append(("Alerta", f"Sequência aberrante de {max_seq} números seguidos."))

        # 6. Múltiplos de 3 e Fibonacci (Peso 10)
        if 4 <= mult3_count <= 6 and 3 <= fibonacci_count <= 5:
            score += 10
            feedbacks.append(("Excelente", f"Fibonacci ({fibonacci_count}) e Múltiplos de 3 ({mult3_count}) perfeitamente alinhados."))
        elif 3 <= mult3_count <= 7 and 2 <= fibonacci_count <= 6:
            score += 6
            feedbacks.append(("Bom", f"Fibonacci ({fibonacci_count}) e Múltiplos de 3 ({mult3_count}) dentro dos limites."))
        else:
            score += 2
            feedbacks.append(("Alerta", f"Proporções anômalas de Fibonacci ({fibonacci_count}) ou Múltiplos de 3 ({mult3_count})."))

        # 7. Linhas e Colunas (Peso 10): nenhuma linha/coluna zerada ou com 5 dezenas completas
        if all(1 <= l <= 4 for l in linhas_dist) and all(1 <= c <= 4 for c in colunas_dist):
            score += 10
            feedbacks.append(("Excelente", "Distribuição harmônica pelas 5 linhas e 5 colunas."))
        elif all(l <= 5 for l in linhas_dist) and (0 not in linhas_dist):
            score += 6
            feedbacks.append(("Bom", "Distribuição aceitável em linhas e colunas."))
        else:
            score += 2
            feedbacks.append(("Alerta", "Linha ou coluna vazia/saturada."))

        # Se houver concurso anterior
        if repetidas is not None:
            if repetidas in [8, 9, 10]:
                feedbacks.append(("Excelente", f"Repetiu {repetidas} dezenas do concurso anterior (faixa de maior incidência)."))
            elif repetidas in [7, 11]:
                feedbacks.append(("Bom", f"Repetiu {repetidas} dezenas do concurso anterior."))
            else:
                feedbacks.append(("Alerta", f"Repetiu {repetidas} dezenas do concurso anterior (anomalia estatística)."))

        return {
            "numeros": sorted_nums,
            "score": score,
            "pares": pares_count,
            "impares": impares_count,
            "moldura": moldura_count,
            "miolo": miolo_count,
            "primos": primos_count,
            "fibonacci": fibonacci_count,
            "multiplos_3": mult3_count,
            "soma": soma,
            "max_consecutivos": max_seq,
            "linhas": linhas_dist,
            "colunas": colunas_dist,
            "repetidas_ultimo": repetidas,
            "feedbacks": feedbacks
        }

class LotofacilGenerator:
    """Motor de geração de palpites de alta precisão probabilística."""

    @classmethod
    def filter_game(cls, numbers: List[int], last_contest: Optional[List[int]] = None, strictness: str = "high") -> bool:
        """Verifica se o jogo atende a todos os critérios estatísticos fundamentais."""
        s_nums = set(numbers)
        
        impares = len(s_nums.intersection(IMPARES))
        pares = 15 - impares
        moldura = len(s_nums.intersection(MOLDURA))
        miolo = 15 - moldura
        primos = len(s_nums.intersection(PRIMOS))
        fib = len(s_nums.intersection(FIBONACCI))
        mult3 = len(s_nums.intersection(MULTIPLOS_3))
        soma = sum(numbers)
        max_seq = LotofacilStats.max_consecutive(numbers)
        
        # Critérios de acordo com o rigor
        if strictness == "high":
            # Alta precisão: foca exclusivamente no miolo da curva normal
            if (impares, pares) not in [(8, 7), (7, 8)]:
                return False
            if (moldura, miolo) not in [(10, 5), (9, 6), (11, 4)]:
                return False
            if primos not in [5, 6]:
                return False
            if fib not in [3, 4, 5]:
                return False
            if mult3 not in [4, 5, 6]:
                return False
            if not (175 <= soma <= 210):
                return False
            if max_seq > 5:
                return False
            if last_contest:
                rep = len(s_nums.intersection(set(last_contest)))
                if rep not in [8, 9, 10]:
                    return False
        else:
            # Rigor médio: aceita faixas secundárias
            if (impares, pares) not in [(8, 7), (7, 8), (9, 6), (6, 9)]:
                return False
            if (moldura, miolo) not in [(10, 5), (9, 6), (11, 4), (8, 7)]:
                return False
            if primos not in [4, 5, 6, 7]:
                return False
            if fib not in [3, 4, 5, 6]:
                return False
            if mult3 not in [3, 4, 5, 6, 7]:
                return False
            if not (165 <= soma <= 215):
                return False
            if max_seq > 5:
                return False
            if last_contest:
                rep = len(s_nums.intersection(set(last_contest)))
                if rep not in [7, 8, 9, 10, 11]:
                    return False

        # Verifica linhas e colunas (nenhuma zerada)
        for l in LINHAS:
            if len(s_nums.intersection(l)) == 0 or len(s_nums.intersection(l)) == 5:
                return False
        for c in COLUNAS:
            if len(s_nums.intersection(c)) == 0 or len(s_nums.intersection(c)) == 5:
                return False

        return True

    @classmethod
    def generate_palpites(
        cls, 
        qtd: int = 3, 
        fixed: Optional[List[int]] = None, 
        excluded: Optional[List[int]] = None, 
        last_contest: Optional[List[int]] = None,
        strictness: str = "high"
    ) -> List[Dict[str, Any]]:
        """Gera 'qtd' palpites aprovados em 100% dos filtros estatísticos."""
        fixed = set(fixed) if fixed else set()
        excluded = set(excluded) if excluded else set()
        
        available = [n for n in range(1, 26) if n not in fixed and n not in excluded]
        needed = 15 - len(fixed)
        
        if needed < 0:
            raise ValueError("Você selecionou mais de 15 dezenas fixas!")
        if len(available) < needed:
            raise ValueError("Muitas dezenas excluídas, não há números suficientes para completar 15.")

        palpites = []
        max_attempts = 30000
        attempts = 0
        seen_games = set()

        while len(palpites) < qtd and attempts < max_attempts:
            attempts += 1
            chosen = sorted(list(fixed) + random.sample(available, needed))
            game_tuple = tuple(chosen)
            
            if game_tuple in seen_games:
                continue
                
            if cls.filter_game(chosen, last_contest, strictness=strictness):
                seen_games.add(game_tuple)
                analysis = LotofacilStats.analyze_game(chosen, last_contest)
                palpites.append(analysis)

        # Se não atingiu a quantidade por rigidez estrita, tenta com rigor médio
        if len(palpites) < qtd and strictness == "high":
            additional = cls.generate_palpites(
                qtd=qtd - len(palpites),
                fixed=list(fixed),
                excluded=list(excluded),
                last_contest=last_contest,
                strictness="medium"
            )
            for p in additional:
                if tuple(p["numeros"]) not in seen_games:
                    seen_games.add(tuple(p["numeros"]))
                    palpites.append(p)

        return palpites

    @classmethod
    def fechamento(
        cls, 
        pool: List[int], 
        guarantee: int = 14, 
        condition: int = 15, 
        max_games: int = 10,
        last_contest: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Gera um desdobramento/fechamento reduzido inteligente.
        Ex: Jogar com 18 dezenas, selecionando os melhores volantes que maximizam cobertura.
        """
        pool = sorted(list(set(pool)))
        if len(pool) < 16 or len(pool) > 23:
            raise ValueError("O fechamento requer entre 16 e 23 dezenas selecionadas.")

        # Gerar todas as combinações de 15 a partir do pool
        all_combs = list(combinations(pool, 15))
        
        # Filtrar apenas as combinações com alta nota estatística
        valid_combs = [
            c for c in all_combs 
            if cls.filter_game(list(c), last_contest, strictness="medium")
        ]
        
        if not valid_combs:
            # Fallback caso os filtros fiquem muito restritos
            valid_combs = all_combs

        # Selecionar os volantes com maior dispersão/cobertura combinatória
        selected_games = []
        covered_pairs: Set[Tuple[int, int]] = set()

        # Ordenar combinações pelo score estatístico
        scored = []
        for c in valid_combs:
            analysis = LotofacilStats.analyze_game(list(c), last_contest)
            scored.append((analysis["score"], list(c), analysis))
            
        scored.sort(key=lambda x: x[0], reverse=True)

        for score, game, analysis in scored:
            # Calcula quantos novos pares de números essa combinação cobre
            pairs = set(combinations(game, 2))
            new_pairs = len(pairs - covered_pairs)
            
            if new_pairs > 0 or len(selected_games) < 3:
                selected_games.append(analysis)
                covered_pairs.update(pairs)
                
            if len(selected_games) >= max_games:
                break

        return selected_games
