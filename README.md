# 🎯 Lotofácil Expert - Sistema de Análise e Palpites Certeiros

Sistema inteligente de análise estatística, probabilidade aplicada e geração de palpites calibrados para a **Lotofácil**. Desenvolvido com base nos padrões históricos que ocorrem em mais de 80% de todos os concursos já realizados pela Caixa Econômica Federal.

---

## 🚀 Como Iniciar

O projeto possui **duas formas de uso** no Windows:

### 1. Painel Web Gráfico (Recomendado)
Dê um duplo clique no arquivo:
👉 `iniciar_painel_web.bat`

Ou pelo terminal dentro da pasta do projeto:
```powershell
py web_app.py
```
*O sistema abrirá automaticamente seu navegador em `http://localhost:5050` com interface gráfica escura, volantes interativos clicáveis, cartões com dezenas estilizadas e exportador de jogos em TXT.*

### 2. Linha de Comando (Terminal CLI)
Dê um duplo clique no arquivo:
👉 `iniciar_terminal.bat`

Ou pelo terminal:
```powershell
py cli.py
```

---

## 🧠 Como Funciona o Motor Estatístico

Diferente de geradores aleatórios comuns, cada palpite gerado pelo **Lotofácil Expert** é testado contra **8 Filtros de Ouro da Matemática Combinatória**:

1. **Equilíbrio de Pares e Ímpares:**
   - Filtra apenas volantes com **8 ímpares / 7 pares** ou **7 ímpares / 8 pares** (padrão de ~57% dos resultados).
2. **Moldura vs. Miolo:**
   - 10 na moldura e 5 no miolo (ou 9/6), que cobrem a esmagadora maioria dos sorteios.
3. **Distribuição de Primos:**
   - Entre 5 e 6 números primos (do conjunto `02, 03, 05, 07, 11, 13, 17, 19, 23`).
4. **Série Fibonacci:**
   - Entre 3 e 5 dezenas do conjunto Fibonacci (`01, 02, 03, 05, 08, 13, 21`).
5. **Múltiplos de 3:**
   - Entre 4 e 6 dezenas múltiplas de 3.
6. **Soma Total das Dezenas:**
   - Mantida rigidamente na faixa normal de **175 a 210** (média teórica: 195).
7. **Controle de Sequências:**
   - Evita aberrações estatísticas (como sequências de 6 números seguidos).
8. **Repetência do Concurso Anterior (Opcional):**
   - Ao informar o concurso anterior, o sistema calibra para manter entre **8, 9 e 10 repetidas** (a média histórica é exatamente 9).

---

## 🛠️ Recursos do Sistema

- **Gerador de Palpites Otimizados:** Gere de 1 a 10 jogos prontos com Score de 0 a 100%. Permite fixar dezenas favoritas ou excluir dezenas frias.
- **Fechamento / Desdobramento Inteligente:** Selecione de 16 a 21 dezenas no volante interativo e o sistema gera o número ideal de volantes reduzidos, maximizando a cobertura matemática de pares e trios.
- **Auditor de Volantes:** Marque 15 dezenas no volante e receba instantaneamente a nota do seu jogo com alertas detalhados sobre possíveis desvios estatísticos.
- **Exportação para TXT:** Baixe seus palpites com um clique para levar à lotérica ou copiar direto para o aplicativo Loterias Caixa.

---

## 📁 Estrutura dos Arquivos

- `lotofacil_engine.py`: Motor matemático com regras, classes de auditoria e algoritmos de combinação e fechamento.
- `web_app.py`: Servidor HTTP nativo do Python e Dashboard HTML/CSS/JS moderno (zero dependências externas).
- `cli.py`: Interface de linha de comando com menus e cores ANSI.
- `iniciar_painel_web.bat`: Atalho executável para o painel web.
- `iniciar_terminal.bat`: Atalho executável para o menu do terminal.
