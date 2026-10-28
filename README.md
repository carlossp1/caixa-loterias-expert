# 🎯 Caixa Loterias Expert Hub - Suíte Completa das Loterias Oficiais

Sistema inteligente de análise estatística, probabilidade aplicada, geração de palpites calibrados, fechamentos reduzidos e conferência de resultados para **todas as 9 loterias oficiais da Caixa Econômica Federal**:

1. 🟢 **Mega-Sena** (6 a 20 dezenas de 1 a 60)
2. 🟣 **Lotofácil** (15 a 20 dezenas de 1 a 25)
3. 🔵 **Quina** (5 a 15 dezenas de 1 a 80)
4. 🟠 **Lotomania** (50 dezenas de 00 a 99)
5. 🔴 **Dupla Sena** (6 a 15 dezenas de 1 a 50 com 2 sorteios)
6. 🟡 **Dia de Sorte** (7 a 15 dezenas de 1 a 31 + Mês de Sorte)
7. 🟢 **Timemania** (10 dezenas de 1 a 80 + Time do Coração)
8. 🔷 **+Milionária** (6 a 12 dezenas de 1 a 50 + 2 a 6 trevos)
9. 🍏 **Super Sete** (7 colunas com números de 0 a 9)

---

## 🚀 Como Iniciar

### 1. Painel Web Gráfico Moderno (Recomendado)
Dê um duplo clique no arquivo:
👉 `iniciar_painel_web.bat`

Ou pelo terminal dentro da pasta:
```powershell
py web_app.py
```
*O sistema abrirá automaticamente o navegador em `http://localhost:5050` com interface escura Glassmorphism, volantes interativos adaptáveis para cada jogo, cards estatísticos com Score de 0 a 100%, conferidor automático e exportador TXT.*

### 2. Linha de Comando (Terminal CLI)
Dê um duplo clique no arquivo:
👉 `iniciar_terminal.bat`

Ou pelo terminal:
```powershell
py cli.py
```

---

## 🧠 Recursos do Sistema

- **Gerador de Palpites Otimizados:** Gera de 1 a 20 palpites balanceados pela curva de probabilidade histórica (soma teórica, proporção par/ímpar, números primos, controle de sequências consecutivas e quadrantes). Permite fixar dezenas favoritas e excluir dezenas indesejadas no volante visual.
- **Fechamentos / Desdobramentos Matemáticos:** Selecione um pool ampliado de números e gere uma matriz reduzida com garantia de acertos e cobertura de pares.
- **Raio-X e Auditor de Volantes:** Avalie qualquer bilhete manual e receba uma nota de 0 a 100 com alertas de riscos estatísticos (somas descalibradas, sequências longas, aberrações de paridade).
- **Conferidor Automático com API da Caixa:** Busca o último resultado oficial do concurso, destaca acertos em dourado brilhante e indica se o bilhete foi premiado.
- **Funcionamento Offline Resiliente:** Cache local em JSON para resultados e algoritmos combinatórios nativos que funcionam sem depender de internet.
- **Zero Dependências Pesadas:** Desenvolvido em Python puro com bibliotecas nativas, sem necessidade de Node.js ou compilações externas.
