"""
Catálogo Completo de Regras, Parâmetros Estatísticos e Identidade Visual
das 9 Principais Loterias Oficiais da Caixa Econômica Federal.
"""

from typing import Dict, Any, List, Set

LOTTERIES_CONFIG: Dict[str, Dict[str, Any]] = {
    "megasena": {
        "id": "megasena",
        "name": "Mega-Sena",
        "slogan": "A maior loteria do Brasil com prêmios milionários",
        "color_primary": "#209869",
        "color_dark": "#135d40",
        "color_light": "#2ecc71",
        "min_number": 1,
        "max_number": 60,
        "default_pick": 6,
        "min_pick": 6,
        "max_pick": 20,
        "layout_cols": 10,
        "layout_rows": 6,
        "special_type": "standard", # apenas dezenas
        "stat_filters": {
            "sum_range": (140, 220), # Média ~183
            "even_odd_ratio": [(3, 3), (4, 2), (2, 4)], # Mais de 80% dos concursos
            "primes_ideal": (1, 3), # Primos: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59 (17 primos)
            "max_consecutive": 2, # Quase nunca saem 3 seguidos
            "quadrant_balance": True
        },
        "prize_tiers": [
            {"tier": "Sena (6 acertos)", "hits": 6},
            {"tier": "Quina (5 acertos)", "hits": 5},
            {"tier": "Quadra (4 acertos)", "hits": 4}
        ]
    },
    "lotofacil": {
        "id": "lotofacil",
        "name": "Lotofácil",
        "slogan": "A loteria mais fácil de apostar e ganhar",
        "color_primary": "#930089",
        "color_dark": "#5e0057",
        "color_light": "#bd10e0",
        "min_number": 1,
        "max_number": 25,
        "default_pick": 15,
        "min_pick": 15,
        "max_pick": 20,
        "layout_cols": 5,
        "layout_rows": 5,
        "special_type": "standard",
        "frame_numbers": [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25], # 16 na moldura
        "core_numbers": [7, 8, 9, 12, 13, 14, 17, 18, 19], # 9 no miolo
        "stat_filters": {
            "sum_range": (175, 215), # Média ~195
            "even_odd_ratio": [(8, 7), (7, 8), (9, 6), (6, 9)],
            "frame_ideal": (9, 11), # Moldura 9 a 11
            "primes_ideal": (5, 7), # Primos: 2, 3, 5, 7, 11, 13, 17, 19, 23
            "fibonacci_ideal": (3, 5), # 1, 2, 3, 5, 8, 13, 21
            "max_consecutive": 4
        },
        "prize_tiers": [
            {"tier": "15 acertos", "hits": 15},
            {"tier": "14 acertos", "hits": 14},
            {"tier": "13 acertos", "hits": 13},
            {"tier": "12 acertos", "hits": 12},
            {"tier": "11 acertos", "hits": 11}
        ]
    },
    "quina": {
        "id": "quina",
        "name": "Quina",
        "slogan": "Sorteios de segunda a sábado com grandes prêmios",
        "color_primary": "#260085",
        "color_dark": "#170054",
        "color_light": "#4a15d6",
        "min_number": 1,
        "max_number": 80,
        "default_pick": 5,
        "min_pick": 5,
        "max_pick": 15,
        "layout_cols": 10,
        "layout_rows": 8,
        "special_type": "standard",
        "stat_filters": {
            "sum_range": (150, 250), # Média ~202.5
            "even_odd_ratio": [(3, 2), (2, 3), (4, 1), (1, 4)],
            "primes_ideal": (1, 2), # 22 primos até 80
            "max_consecutive": 2
        },
        "prize_tiers": [
            {"tier": "Quina (5 acertos)", "hits": 5},
            {"tier": "Quadra (4 acertos)", "hits": 4},
            {"tier": "Terno (3 acertos)", "hits": 3},
            {"tier": "Duque (2 acertos)", "hits": 2}
        ]
    },
    "lotomania": {
        "id": "lotomania",
        "name": "Lotomania",
        "slogan": "Fácil de jogar e fácil de ganhar com 50 números",
        "color_primary": "#f78100",
        "color_dark": "#a35500",
        "color_light": "#ff9f38",
        "min_number": 0, # De 00 a 99
        "max_number": 99,
        "default_pick": 50,
        "min_pick": 50,
        "max_pick": 50,
        "layout_cols": 10,
        "layout_rows": 10,
        "special_type": "zero_indexed", # 00 até 99
        "stat_filters": {
            "sum_range": (2300, 2650), # Média teórica 2475
            "even_odd_ratio": [(25, 25), (26, 24), (24, 26), (27, 23), (23, 27)],
            "max_consecutive": 4
        },
        "prize_tiers": [
            {"tier": "20 acertos", "hits": 20},
            {"tier": "19 acertos", "hits": 19},
            {"tier": "18 acertos", "hits": 18},
            {"tier": "17 acertos", "hits": 17},
            {"tier": "16 acertos", "hits": 16},
            {"tier": "15 acertos", "hits": 15},
            {"tier": "0 acertos", "hits": 0}
        ]
    },
    "duplasena": {
        "id": "duplasena",
        "name": "Dupla Sena",
        "slogan": "Com apenas um bilhete você tem o dobro de chances",
        "color_primary": "#a61324",
        "color_dark": "#690a16",
        "color_light": "#d4253a",
        "min_number": 1,
        "max_number": 50,
        "default_pick": 6,
        "min_pick": 6,
        "max_pick": 15,
        "layout_cols": 10,
        "layout_rows": 5,
        "special_type": "standard",
        "has_two_draws": True,
        "stat_filters": {
            "sum_range": (120, 190), # Média ~153
            "even_odd_ratio": [(3, 3), (4, 2), (2, 4)],
            "primes_ideal": (1, 3), # 15 primos até 50
            "max_consecutive": 2
        },
        "prize_tiers": [
            {"tier": "Sena (6 acertos) 1º ou 2º sorteio", "hits": 6},
            {"tier": "Quina (5 acertos) 1º ou 2º sorteio", "hits": 5},
            {"tier": "Quadra (4 acertos) 1º ou 2º sorteio", "hits": 4},
            {"tier": "Terno (3 acertos) 1º ou 2º sorteio", "hits": 3}
        ]
    },
    "diadesorte": {
        "id": "diadesorte",
        "name": "Dia de Sorte",
        "slogan": "A loteria dos seus dias e meses da sorte",
        "color_primary": "#cb852c",
        "color_dark": "#825318",
        "color_light": "#e09f4b",
        "min_number": 1,
        "max_number": 31,
        "default_pick": 7,
        "min_pick": 7,
        "max_pick": 15,
        "layout_cols": 7,
        "layout_rows": 5,
        "special_type": "month_extra", # Tem Mês de Sorte (1 a 12)
        "months": [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ],
        "stat_filters": {
            "sum_range": (90, 135), # Média ~112
            "even_odd_ratio": [(4, 3), (3, 4), (5, 2), (2, 5)],
            "primes_ideal": (2, 4), # 11 primos até 31
            "max_consecutive": 3
        },
        "prize_tiers": [
            {"tier": "7 acertos", "hits": 7},
            {"tier": "6 acertos", "hits": 6},
            {"tier": "5 acertos", "hits": 5},
            {"tier": "4 acertos", "hits": 4},
            {"tier": "Mês da Sorte", "hits": "month"}
        ]
    },
    "timemania": {
        "id": "timemania",
        "name": "Timemania",
        "slogan": "Aposte e ajude seu time do coração a vencer",
        "color_primary": "#00ff1e",
        "color_dark": "#057012",
        "color_light": "#00c418",
        "min_number": 1,
        "max_number": 80,
        "default_pick": 10, # São sorteadas 7 dezenas dentre 80
        "drawn_count": 7,
        "min_pick": 10,
        "max_pick": 10,
        "layout_cols": 10,
        "layout_rows": 8,
        "special_type": "team_extra", # Tem Time do Coração
        "teams_sample": [
            "Flamengo / RJ", "Corinthians / SP", "Santos / SP", "Palmeiras / SP",
            "São Paulo / SP", "Grêmio / RS", "Internacional / RS", "Vasco da Gama / RJ",
            "Atlético / MG", "Cruzeiro / MG", "Fluminense / RJ", "Botafogo / RJ",
            "Bahia / BA", "Vitória / BA", "Sport / PE", "Fortaleza / CE",
            "Ceará / CE", "Athletico / PR", "Coritiba / PR", "Goiás / GO"
        ],
        "stat_filters": {
            "sum_range": (240, 360),
            "even_odd_ratio": [(5, 5), (6, 4), (4, 6)],
            "primes_ideal": (2, 4),
            "max_consecutive": 2
        },
        "prize_tiers": [
            {"tier": "7 acertos", "hits": 7},
            {"tier": "6 acertos", "hits": 6},
            {"tier": "5 acertos", "hits": 5},
            {"tier": "4 acertos", "hits": 4},
            {"tier": "3 acertos", "hits": 3},
            {"tier": "Time do Coração", "hits": "team"}
        ]
    },
    "maismilionaria": {
        "id": "maismilionaria",
        "name": "+Milionária",
        "slogan": "Prêmio principal mínimo de R$ 10 Milhões",
        "color_primary": "#1f3b6c",
        "color_dark": "#0f203d",
        "color_light": "#3b68b3",
        "min_number": 1,
        "max_number": 50,
        "default_pick": 6,
        "min_pick": 6,
        "max_pick": 12,
        "clover_total": 6, # 6 trevos numerados de 1 a 6
        "clover_pick": 2,  # Escolhe 2 trevos
        "min_clovers": 2,
        "max_clovers": 6,
        "layout_cols": 10,
        "layout_rows": 5,
        "special_type": "clovers_extra",
        "stat_filters": {
            "sum_range": (120, 190),
            "even_odd_ratio": [(3, 3), (4, 2), (2, 4)],
            "primes_ideal": (1, 3),
            "max_consecutive": 2
        },
        "prize_tiers": [
            {"tier": "Faixa 1: 6 dezenas + 2 trevos", "hits": (6, 2)},
            {"tier": "Faixa 2: 6 dezenas + 1 ou 0 trevo", "hits": (6, 1)},
            {"tier": "Faixa 3: 5 dezenas + 2 trevos", "hits": (5, 2)},
            {"tier": "Faixa 4: 5 dezenas + 1 ou 0 trevo", "hits": (5, 1)},
            {"tier": "Faixa 5: 4 dezenas + 2 trevos", "hits": (4, 2)},
            {"tier": "Faixa 6: 4 dezenas + 1 ou 0 trevo", "hits": (4, 1)},
            {"tier": "Faixa 7: 3 dezenas + 2 trevos", "hits": (3, 2)},
            {"tier": "Faixa 8: 3 dezenas + 1 trevo", "hits": (3, 1)},
            {"tier": "Faixa 9: 2 dezenas + 2 trevos", "hits": (2, 2)},
            {"tier": "Faixa 10: 2 dezenas + 1 trevo", "hits": (2, 1)}
        ]
    },
    "supersete": {
        "id": "supersete",
        "name": "Super Sete",
        "slogan": "A loteria em colunas com dinâmica única",
        "color_primary": "#98b922",
        "color_dark": "#5e7510",
        "color_light": "#b9de38",
        "min_number": 0,
        "max_number": 9,
        "columns_count": 7, # 7 colunas
        "default_pick": 7,  # 1 número por coluna
        "min_pick": 7,
        "max_pick": 21, # Até 3 por coluna
        "special_type": "columns_matrix",
        "stat_filters": {
            "sum_range": (24, 38), # Média 7 * 4.5 = 31.5
            "even_odd_ratio": [(4, 3), (3, 4)],
            "distinct_numbers": (4, 7) # Evita marcar tudo o mesmo dígito
        },
        "prize_tiers": [
            {"tier": "7 colunas certas", "hits": 7},
            {"tier": "6 colunas certas", "hits": 6},
            {"tier": "5 colunas certas", "hits": 5},
            {"tier": "4 colunas certas", "hits": 4},
            {"tier": "3 colunas certas", "hits": 3}
        ]
    }
}

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

ALL_PRIMES_UP_TO_100: Set[int] = {n for n in range(2, 101) if is_prime(n)}
FIBONACCI_NUMBERS: Set[int] = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
