"""
Interface de Linha de Comando (CLI) - Especialista Lotofácil
Autor: Especialista Lotofácil
"""

import sys
import os
from lotofacil_engine import LotofacilStats, LotofacilGenerator

# Cores para terminal ANSI
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def format_numbers(numbers):
    return " ".join(f"[{n:02d}]" for n in sorted(numbers))

def print_banner():
    print(f"""{CYAN}{BOLD}
========================================================================
    L O T O F A C I L   E X P E R T   -   P A L P I T E S   &   A N A L I S E
    Engenharia Estatistica e Probabilidade Aplicada
========================================================================{RESET}""")

def parse_numbers_input(prompt_text):
    raw = input(prompt_text).strip()
    if not raw:
        return []
    cleaned = raw.replace(",", " ").replace(";", " ").replace("-", " ")
    parts = cleaned.split()
    nums = []
    for p in parts:
        try:
            n = int(p)
            if 1 <= n <= 25:
                if n not in nums:
                    nums.append(n)
            else:
                print(f"{RED}Aviso: {n} ignorado (deve ser entre 1 e 25).{RESET}")
        except ValueError:
            pass
    return sorted(nums)

def display_analysis(analysis, title="ANALISE DO JOGO"):
    print(f"\n{BOLD}{'='*60}")
    print(f" {title} | NOTA DE QUALIDADE: {analysis['score']}/100 ")
    print(f"{'='*60}{RESET}")
    print(f"{GREEN}{BOLD}Dezenas ({len(analysis['numeros'])}): {format_numbers(analysis['numeros'])}{RESET}\n")
    
    print(f"{CYAN}--- RADIOGRAFIA ESTATISTICA ---{RESET}")
    print(f"• Pares / Impares:    {analysis['pares']} pares  |  {analysis['impares']} impares")
    print(f"• Moldura / Miolo:    {analysis['moldura']} na moldura  |  {analysis['miolo']} no miolo")
    print(f"• Numeros Primos:     {analysis['primos']} primos")
    print(f"• Fibonacci:          {analysis['fibonacci']} dezenas")
    print(f"• Multiplos de 3:     {analysis['multiplos_3']} dezenas")
    print(f"• Soma Total:         {analysis['soma']} (Faixa ideal: 175-210)")
    print(f"• Maior Sequencia:    {analysis['max_consecutivos']} seguidos")
    if analysis['repetidas_ultimo'] is not None:
        print(f"• Repetidas do Ultimo:{analysis['repetidas_ultimo']} dezenas (Media historica: 9)")
        
    print(f"\n{YELLOW}--- PARECER DO ESPECIALISTA ---{RESET}")
    for tipo, msg in analysis['feedbacks']:
        cor = GREEN if tipo == "Excelente" else (YELLOW if tipo == "Bom" else RED)
        print(f"[{cor}{tipo.upper()}{RESET}] {msg}")
    print(f"{'='*60}\n")

def menu_gerar_palpites():
    print(f"\n{BOLD}{CYAN}>>> GERADOR DE PALPITES CALIBRADOS <<<{RESET}")
    try:
        qtd = int(input("Quantos palpites deseja gerar? (Ex: 3): ").strip() or "3")
    except ValueError:
        qtd = 3

    print(f"\n{YELLOW}Opcoes avancadas (pressione Enter para pular):{RESET}")
    fixed = parse_numbers_input("Dezenas FIXAS que quer no jogo (ex: 05 13): ")
    excluded = parse_numbers_input("Dezenas EXCLUIDAS que NAO quer no jogo (ex: 04 22): ")
    last = parse_numbers_input("Resultado do ULTIMO concurso (15 numeros para medir repetencia): ")

    if len(last) not in (0, 15):
        print(f"{YELLOW}Aviso: Ultimo concurso incompleto ({len(last)} dezenas). Ignorando filtro de repetencia.{RESET}")
        last = None

    print(f"\n{CYAN}Calculando combinacoes e aplicando 8 filtros de ouro...{RESET}")
    try:
        palpites = LotofacilGenerator.generate_palpites(
            qtd=qtd,
            fixed=fixed,
            excluded=excluded,
            last_contest=last
        )

        for idx, p in enumerate(palpites, 1):
            display_analysis(p, title=f"PALPITE #{idx}")

        salvar = input("Deseja salvar estes palpites em um arquivo .TXT? (S/N): ").strip().upper()
        if salvar == 'S':
            nome_arquivo = "palpites_lotofacil.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write("=== PALPITES LOTOFACIL EXPERT ===\n\n")
                for i, p in enumerate(palpites, 1):
                    f.write(f"Jogo #{i} [Nota: {p['score']}/100]:\n")
                    f.write(" ".join(f"{n:02d}" for n in p['numeros']) + "\n")
                    f.write(f"Pares/Impares: {p['pares']}/{p['impares']} | Moldura: {p['moldura']} | Primos: {p['primos']} | Soma: {p['soma']}\n\n")
            print(f"{GREEN}Sucesso! Arquivo '{nome_arquivo}' salvo com sucesso!{RESET}")

    except Exception as e:
        print(f"{RED}Erro ao gerar palpites: {e}{RESET}")

def menu_fechamento():
    print(f"\n{BOLD}{CYAN}>>> FECHAMENTO / DESDOBRAMENTO INTELIGENTE <<<{RESET}")
    print("Escolha entre 16 e 21 dezenas para desdobrar em volantes enxutos.")
    pool = parse_numbers_input("Digite suas dezenas selecionadas (ex: 1 2 3 5 7 8 10 11 13 15 17 19 20 22 23 24 25): ")
    
    if len(pool) < 16 or len(pool) > 23:
        print(f"{RED}Erro: Voce digitou {len(pool)} dezenas. O fechamento precisa de 16 a 23 dezenas.{RESET}")
        return

    try:
        max_games = int(input("Quantos volantes economicos deseja gerar? (Ex: 6 a 12): ").strip() or "8")
    except ValueError:
        max_games = 8

    last = parse_numbers_input("Resultado do ULTIMO concurso (opcional, para filtro de repetidas): ")
    if len(last) != 15:
        last = None

    print(f"\n{CYAN}Calculando cobertura combinatoria e filtrando melhores volantes...{RESET}")
    try:
        jogos = LotofacilGenerator.fechamento(pool, max_games=max_games, last_contest=last)
        print(f"\n{GREEN}Foram gerados {len(jogos)} volantes de alta eficiencia estatistica:{RESET}\n")
        for idx, j in enumerate(jogos, 1):
            print(f"{BOLD}Volante #{idx:02d} (Nota: {j['score']}/100):{RESET} {format_numbers(j['numeros'])}")
            print(f"   P/I: {j['pares']}/{j['impares']} | Moldura: {j['moldura']}/16 | Primos: {j['primos']} | Soma: {j['soma']}")

        salvar = input("\nDeseja salvar o fechamento em arquivo TXT? (S/N): ").strip().upper()
        if salvar == 'S':
            with open("fechamento_lotofacil.txt", "w", encoding="utf-8") as f:
                f.write(f"=== FECHAMENTO LOTOFACIL ({len(pool)} DEZENAS) ===\n")
                f.write(f"Dezenas base: {' '.join(f'{n:02d}' for n in pool)}\n\n")
                for i, j in enumerate(jogos, 1):
                    f.write(f"Jogo #{i:02d}: " + " ".join(f"{n:02d}" for n in j['numeros']) + f" [Score: {j['score']}]\n")
            print(f"{GREEN}Fechamento salvo em 'fechamento_lotofacil.txt'!{RESET}")

    except Exception as e:
        print(f"{RED}Erro no fechamento: {e}{RESET}")

def menu_auditar():
    print(f"\n{BOLD}{CYAN}>>> AUDITORIA E ANALISE DE JOGO <<<{RESET}")
    numbers = parse_numbers_input("Digite as 15 dezenas do seu jogo (ex: 01 03 04 05 08 10 11 13 15 17 18 20 21 22 24): ")
    if len(numbers) != 15:
        print(f"{RED}Erro: Um jogo da Lotofacil precisa de exatamente 15 dezenas (voce digitou {len(numbers)}).{RESET}")
        return

    last = parse_numbers_input("Dezenas do ultimo concurso (opcional, para testar repetencia): ")
    if len(last) != 15:
        last = None

    analysis = LotofacilStats.analyze_game(numbers, last_contest=last)
    display_analysis(analysis, title="DIAGNOSTICO COMPLETO DO SEU JOGO")

def main():
    while True:
        print_banner()
        print("1. Gerar Palpites Certeiros (Filtros de Ouro da Matematica)")
        print("2. Fazer Fechamento / Desdobramento (16 a 23 dezenas)")
        print("3. Auditar Meu Jogo (Diagnostico de 0 a 100 com alertas)")
        print("4. Iniciar Dashboard Web (Interface Grafica no Navegador)")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opcao (1-5): ").strip()
        
        if opcao == "1":
            menu_gerar_palpites()
        elif opcao == "2":
            menu_fechamento()
        elif opcao == "3":
            menu_auditar()
        elif opcao == "4":
            print(f"\n{GREEN}Iniciando servidor web local...{RESET}")
            os.system(f"py web_app.py")
        elif opcao == "5":
            print(f"\n{CYAN}Boa sorte nos jogos! A estatistica esta a seu favor.{RESET}\n")
            sys.exit(0)
        else:
            print(f"{RED}Opcao invalida!{RESET}")
            
        input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    main()
