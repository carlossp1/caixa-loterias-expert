"""
Interface de Linha de Comando (CLI) - Caixa Loterias Expert Hub
Suporte completo às 9 Loterias Oficiais da Caixa Econômica Federal.
"""

import sys
import os
from lottery_rules import LOTTERIES_CONFIG
from lottery_engine import LotteryAnalyzer, LotteryGenerator, LotteryClosings, LotteryChecker
from caixa_api import CaixaLoteriasAPI

# Cores ANSI
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_banner():
    print(f"""{CYAN}{BOLD}
========================================================================
     C A I X A   L O T E R I A S   E X P E R T   H U B
     Mega-Sena • Lotofácil • Quina • Lotomania • Dupla Sena
     Dia de Sorte • Timemania • +Milionária • Super Sete
========================================================================{RESET}""")

def select_lottery_menu() -> str:
    print(f"\n{YELLOW}{BOLD}Selecione a Modalidade de Loteria:{RESET}")
    items = list(LOTTERIES_CONFIG.items())
    for idx, (lid, cfg) in enumerate(items, 1):
        print(f"  {idx}. {cfg['name']} ({cfg['slogan']})")
    print("  0. Sair")

    while True:
        try:
            choice = input(f"\n{BOLD}Escolha uma opção (1-{len(items)}): {RESET}").strip()
            if choice == "0":
                sys.exit(0)
            c = int(choice)
            if 1 <= c <= len(items):
                return items[c - 1][0]
            print(f"{RED}Opção inválida!{RESET}")
        except ValueError:
            print(f"{RED}Por favor, digite um número.{RESET}")

def parse_numbers_input(prompt_text: str, min_n: int, max_n: int):
    raw = input(prompt_text).strip()
    if not raw:
        return []
    cleaned = raw.replace(",", " ").replace(";", " ").replace("-", " ")
    parts = cleaned.split()
    nums = []
    for p in parts:
        try:
            n = int(p)
            if min_n <= n <= max_n:
                if n not in nums:
                    nums.append(n)
            else:
                print(f"{RED}Aviso: {n} ignorado (deve ser entre {min_n} e {max_n}).{RESET}")
        except ValueError:
            pass
    return sorted(nums)

def display_analysis(analysis: dict):
    lottery_id = analysis.get("lottery_id", "megasena")
    cfg = LOTTERIES_CONFIG.get(lottery_id, {})
    name = cfg.get("name", "Loteria")
    
    print(f"\n{BOLD}{'='*65}")
    print(f" {name.upper()} | NOTA DE QUALIDADE: {analysis['score']}/100 [{analysis['level']}] ")
    print(f"{'='*65}{RESET}")
    
    formatted_nums = " ".join(f"[{n:02d}]" for n in analysis["numbers"])
    print(f"{GREEN}{BOLD}Dezenas ({analysis['total_numbers']}): {formatted_nums}{RESET}\n")

    if "extras" in analysis and analysis["extras"]:
        print(f"{MAGENTA}Informações Extras: {analysis['extras']}{RESET}")

    print(f"{CYAN}--- RADIOGRAFIA ESTATÍSTICA ---{RESET}")
    print(f"• Pares / Ímpares:    {analysis.get('pares', 0)} pares | {analysis.get('impares', 0)} ímpares")
    print(f"• Números Primos:     {analysis.get('primos', 0)} primos")
    print(f"• Fibonacci:          {analysis.get('fibonacci', 0)} dezenas")
    print(f"• Soma Total:         {analysis.get('soma', 0)}")
    print(f"• Maior Sequência:    {analysis.get('max_consecutive', 1)} seguidas")

    if analysis.get("praises"):
        print(f"\n{GREEN}--- PONTOS FORTES ---{RESET}")
        for p in analysis["praises"]:
            print(f"  ✓ {p}")

    if analysis.get("alerts"):
        print(f"\n{YELLOW}--- ALERTAS ESTRATÉGICOS ---{RESET}")
        for a in analysis["alerts"]:
            print(f"  ! {a}")

def main():
    os.system("color" if os.name == "nt" else "")
    print_banner()

    while True:
        lottery_id = select_lottery_menu()
        cfg = LOTTERIES_CONFIG[lottery_id]

        print(f"\n{GREEN}{BOLD}Modalidade Ativa: {cfg['name']}{RESET}")

        print("\nO que você deseja fazer?")
        print("  1. Gerar Palpites Certeiros (Filtros de Ouro)")
        print("  2. Fechamento / Desdobramento Inteligente")
        print("  3. Auditar Jogo Próprio (Raio-X)")
        print("  4. Consultar Último Concurso Oficial Caixa")
        print("  5. Trocar de Loteria")
        print("  0. Sair")

        sub = input(f"\n{BOLD}Escolha (1-5): {RESET}").strip()

        if sub == "1":
            try:
                qtd = int(input("Quantos palpites gerar? (1 a 10): ").strip() or "5")
            except ValueError:
                qtd = 5

            print(f"\n(Opcional) Fixar ou excluir dezenas entre {cfg['min_number']} e {cfg['max_number']}:")
            fix = parse_numbers_input("Dezenas Fixas (Enter para nenhuma): ", cfg['min_number'], cfg['max_number'])
            exc = parse_numbers_input("Dezenas Excluídas (Enter para nenhuma): ", cfg['min_number'], cfg['max_number'])

            games = LotteryGenerator.generate_batch(
                lottery_id=lottery_id,
                count=qtd,
                fixed_numbers=fix,
                excluded_numbers=exc,
                min_score=75
            )

            print(f"\n{YELLOW}{BOLD}=== {len(games)} PALPITES GERADOS PARA {cfg['name'].upper()} ==={RESET}")
            for idx, g in enumerate(games, 1):
                display_analysis(g)
            input("\nPressione Enter para continuar...")

        elif sub == "2":
            min_need = cfg["default_pick"]
            print(f"\nDigite o conjunto de dezenas para desdobrar (mínimo de {min_need} números):")
            pool = parse_numbers_input("Dezenas: ", cfg['min_number'], cfg['max_number'])
            if len(pool) < min_need:
                print(f"{RED}Você precisa digitar ao menos {min_need} dezenas.{RESET}")
            else:
                closing = LotteryClosings.generate_closing(lottery_id, pool, max_tickets=8)
                print(f"\n{GREEN}{BOLD}Fechamento Gerado: {closing['total_tickets']} jogos! Cobertura: {closing['coverage_percentage']}%{RESET}")
                for idx, t in enumerate(closing["tickets"], 1):
                    print(f"Volante #{idx}: " + " ".join(f"{n:02d}" for n in t["numbers"]))
            input("\nPressione Enter para continuar...")

        elif sub == "3":
            print(f"\nDigite as dezenas do seu jogo na {cfg['name']}:")
            user_nums = parse_numbers_input("Dezenas: ", cfg['min_number'], cfg['max_number'])
            if not user_nums:
                print(f"{RED}Nenhuma dezena digitada.{RESET}")
            else:
                analysis = LotteryAnalyzer.analyze_game(lottery_id, user_nums)
                display_analysis(analysis)
            input("\nPressione Enter para continuar...")

        elif sub == "4":
            print(f"\n{CYAN}Buscando dados oficiais da Caixa...{RESET}")
            res = CaixaLoteriasAPI.get_latest_result(lottery_id, force_refresh=True)
            print(f"\n{GREEN}{BOLD}Concurso {res.get('numero')} ({res.get('dataApuracao')}){RESET}")
            print(f"Dezenas Sorteadas: {res.get('listaDezenas')}")
            if "trevosSorteados" in res:
                print(f"Trevos: {res.get('trevosSorteados')}")
            if "nomeMesSorte" in res:
                print(f"Mês da Sorte: {res.get('nomeMesSorte')}")
            if "nomeTimeCoracaoMesSorte" in res:
                print(f"Time do Coração: {res.get('nomeTimeCoracaoMesSorte')}")
            if res.get("valorEstimadoProximoConcurso"):
                print(f"Estimativa Próximo Concurso: R$ {res.get('valorEstimadoProximoConcurso'):,.2f}")
            input("\nPressione Enter para continuar...")

        elif sub == "0":
            sys.exit(0)

if __name__ == "__main__":
    main()
