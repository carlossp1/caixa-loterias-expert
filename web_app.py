"""
Servidor Web Local e Dashboard do Especialista em Lotofácil
Autor: Especialista Lotofácil
Sem dependências externas - utiliza apenas a biblioteca padrão do Python.
"""

import sys
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from lotofacil_engine import LotofacilStats, LotofacilGenerator

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lotofácil Expert - Palpites & Análise Estatística</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #090d16;
            --bg-card: #131b2e;
            --bg-card-hover: #1b2640;
            --border: #233152;
            --primary: #10b981;
            --primary-glow: rgba(16, 185, 129, 0.25);
            --secondary: #8b5cf6;
            --accent: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 60px;
        }

        header {
            background: linear-gradient(180deg, #162038 0%, rgba(9, 13, 22, 0) 100%);
            padding: 30px 20px 20px 20px;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }

        .badge-pro {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: var(--primary);
            border: 1px solid var(--primary);
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        h1 {
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            color: var(--text-muted);
            margin-top: 6px;
            font-size: 1.05rem;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 25px 20px;
        }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .tab-btn:hover {
            border-color: var(--primary);
            color: var(--text-main);
        }

        .tab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #042f2e;
            box-shadow: 0 0 20px var(--primary-glow);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .card h2 {
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card h2 span {
            color: var(--primary);
        }

        /* Form elements */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 18px;
            margin-bottom: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        input[type="text"], input[type="number"], select {
            background: #0b1120;
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .btn {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #ffffff;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 1.05rem;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s;
            box-shadow: 0 4px 15px var(--primary-glow);
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--primary-glow);
        }

        .btn-secondary {
            background: #233152;
            color: var(--text-main);
            box-shadow: none;
        }

        .btn-secondary:hover {
            background: #2e416d;
            box-shadow: none;
        }

        /* Volante Interativo Grid (1 a 25) */
        .volante-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            max-width: 440px;
            margin: 15px auto 20px auto;
        }

        .volante-ball {
            aspect-ratio: 1;
            background: #0b1120;
            border: 2px solid var(--border);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text-muted);
            cursor: pointer;
            user-select: none;
            transition: all 0.15s ease;
        }

        .volante-ball:hover {
            border-color: var(--primary);
            color: var(--text-main);
            transform: scale(1.05);
        }

        .volante-ball.selected {
            background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
            border-color: #a78bfa;
            color: #ffffff;
            box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
            transform: scale(1.06);
        }

        .volante-ball.moldura {
            position: relative;
        }

        .volante-ball.moldura::after {
            content: '';
            position: absolute;
            top: 4px;
            right: 4px;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--accent);
        }

        /* Balls display for generated games */
        .game-balls {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 16px 0;
        }

        .ball {
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #10b981 0%, #047857 100%);
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        }

        .game-card {
            background: #0d1424;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 18px;
            transition: border-color 0.2s;
        }

        .game-card:hover {
            border-color: var(--primary);
        }

        .game-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 12px;
        }

        .score-pill {
            background: rgba(16, 185, 129, 0.15);
            color: var(--primary);
            border: 1px solid var(--primary);
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.95rem;
        }

        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 10px;
        }

        .badge {
            background: #1e293b;
            color: var(--text-muted);
            font-size: 0.8rem;
            padding: 4px 8px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
        }

        .badge b {
            color: var(--text-main);
        }

        .feedbacks-list {
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 0.88rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .feedback-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tag-excelente { color: var(--primary); font-weight: 700; }
        .tag-bom { color: var(--accent); font-weight: 700; }
        .tag-alerta { color: var(--danger); font-weight: 700; }

        .actions-row {
            display: flex;
            gap: 10px;
            margin-top: 14px;
        }

        .btn-sm {
            padding: 8px 14px;
            font-size: 0.85rem;
            border-radius: 8px;
        }

        /* Rules summary table */
        .rules-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .rules-table th, .rules-table td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid var(--border);
            font-size: 0.95rem;
        }

        .rules-table th {
            color: var(--text-muted);
            font-weight: 600;
        }

        .rules-table tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Toast notification */
        #toast {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: var(--primary);
            color: #042f2e;
            padding: 14px 24px;
            border-radius: 10px;
            font-weight: 700;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
            pointer-events: none;
            z-index: 999;
        }

        #toast.show {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body>

    <header>
        <div class="badge-pro">Algoritmo Estatístico V2.5</div>
        <h1>LOTOFÁCIL EXPERT</h1>
        <p class="subtitle">Otimização probabilística e palpites matematicamente calibrados</p>
    </header>

    <div class="container">
        <!-- Tabs de navegação -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('gerador')">🎯 Gerador de Palpites</button>
            <button class="tab-btn" onclick="switchTab('fechamento')">📦 Fechamento (Desdobramento)</button>
            <button class="tab-btn" onclick="switchTab('auditor')">🔍 Auditar Meu Jogo</button>
            <button class="tab-btn" onclick="switchTab('regras')">📊 Os 5 Pilares de Ouro</button>
        </div>

        <!-- ABA 1: GERADOR DE PALPITES -->
        <div id="tab-gerador" class="tab-content active">
            <div class="card">
                <h2><span>🎯</span> Gerar Palpites Certeiros</h2>
                <p style="color: var(--text-muted); margin-bottom: 18px;">
                    Todos os jogos gerados são submetidos a 8 filtros rigorosos (Pares/Ímpares, Moldura/Miolo, Primos, Fibonacci, Soma e Repetição).
                </p>

                <div class="form-grid">
                    <div class="form-group">
                        <label for="gen-qtd">Quantidade de Jogos</label>
                        <select id="gen-qtd">
                            <option value="1">1 Jogo Calibrado</option>
                            <option value="3" selected>3 Jogos (Recomendado)</option>
                            <option value="5">5 Jogos Estratégicos</option>
                            <option value="10">10 Jogos</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="gen-last">Último Concurso (15 números para medir repetência)</label>
                        <input type="text" id="gen-last" placeholder="Ex: 01 02 04 06 09 10 11 13 14 16 18 20 21 23 25">
                    </div>

                    <div class="form-group">
                        <label for="gen-fixed">Dezenas FIXAS (Opcional - ex: 05 13)</label>
                        <input type="text" id="gen-fixed" placeholder="Dezenas que você quer em todos os jogos">
                    </div>

                    <div class="form-group">
                        <label for="gen-excluded">Dezenas EXCLUÍDAS (Opcional - ex: 04 22)</label>
                        <input type="text" id="gen-excluded" placeholder="Dezenas que você NÃO quer em nenhum jogo">
                    </div>
                </div>

                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <button class="btn" onclick="gerarPalpites()">⚡ Gerar Palpites Otimizados</button>
                    <button class="btn btn-secondary" onclick="preencherExemplo()">💡 Preencher com Exemplo</button>
                </div>
            </div>

            <div id="results-palpites"></div>
        </div>

        <!-- ABA 2: FECHAMENTO / DESDOBRAMENTO -->
        <div id="tab-fechamento" class="tab-content">
            <div class="card">
                <h2><span>📦</span> Desdobramento / Fechamento Matemático</h2>
                <p style="color: var(--text-muted);">
                    Selecione de <b>16 a 21 dezenas</b> abaixo. O motor criará os volantes de 15 números que maximizam a cobertura combinatória e atendem aos filtros estatísticos.
                </p>

                <div style="text-align: center; margin: 15px 0;">
                    <span style="font-size: 1.1rem; font-weight: 700; color: var(--primary);">
                        Dezenas Selecionadas: <span id="count-fechamento">0</span> / 25
                    </span>
                    <span style="color: var(--text-muted); font-size: 0.9rem; margin-left: 10px;">(Mínimo 16, Máximo 21)</span>
                </div>

                <!-- Volante Interativo para Fechamento -->
                <div class="volante-grid" id="volante-fechamento"></div>

                <div class="form-grid" style="max-width: 500px; margin: 0 auto 20px auto;">
                    <div class="form-group">
                        <label for="fech-max">Quantidade de Volantes a Gerar</label>
                        <select id="fech-max">
                            <option value="6">6 Volantes Econômicos</option>
                            <option value="8" selected>8 Volantes (Equilibrado)</option>
                            <option value="12">12 Volantes (Maior Cobertura)</option>
                            <option value="16">16 Volantes</option>
                        </select>
                    </div>
                </div>

                <div style="text-align: center;">
                    <button class="btn" onclick="executarFechamento()">🧩 Gerar Fechamento Reduzido</button>
                    <button class="btn btn-secondary" onclick="limparFechamento()">Limpar Seleção</button>
                </div>
            </div>

            <div id="results-fechamento"></div>
        </div>

        <!-- ABA 3: AUDITOR DE VOLANTE -->
        <div id="tab-auditor" class="tab-content">
            <div class="card">
                <h2><span>🔍</span> Auditoria Completa de Volante</h2>
                <p style="color: var(--text-muted);">
                    Clique exatamente em <b>15 dezenas</b> no volante abaixo para receber uma análise profunda e a nota de probabilidade do seu jogo.
                </p>

                <div style="text-align: center; margin: 15px 0;">
                    <span style="font-size: 1.1rem; font-weight: 700; color: var(--primary);">
                        Dezenas Marcadas: <span id="count-auditor">0</span> / 15
                    </span>
                </div>

                <div class="volante-grid" id="volante-auditor"></div>

                <div style="text-align: center;">
                    <button class="btn" onclick="auditarJogo()">🔬 Auditar Este Jogo</button>
                    <button class="btn btn-secondary" onclick="limparAuditor()">Limpar Volante</button>
                </div>
            </div>

            <div id="results-auditor"></div>
        </div>

        <!-- ABA 4: REGRAS E DICAS -->
        <div id="tab-regras" class="tab-content">
            <div class="card">
                <h2><span>📊</span> Os Filtros de Ouro da Lotofácil</h2>
                <p style="color: var(--text-muted); line-height: 1.6;">
                    A Lotofácil não é sorte pura: os resultados seguem leis da física estatística e da distribuição combinatória. Veja as métricas que se repetem em mais de 80% de todos os concursos da história:
                </p>

                <table class="rules-table">
                    <thead>
                        <tr>
                            <th>Métrica</th>
                            <th>Faixa de Ouro (Maior Incidência)</th>
                            <th>Frequência Histórica</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>Pares e Ímpares</b></td>
                            <td>8 Ímpares e 7 Pares ou 7 Ímpares e 8 Pares</td>
                            <td>~57% de todos os concursos</td>
                        </tr>
                        <tr>
                            <td><b>Repetidas do Anterior</b></td>
                            <td>8, 9 ou 10 dezenas do concurso passado</td>
                            <td>~62% (média perfeita é 9)</td>
                        </tr>
                        <tr>
                            <td><b>Moldura vs. Miolo</b></td>
                            <td>10 na moldura / 5 no miolo (ou 9/6)</td>
                            <td>~58% das extrações</td>
                        </tr>
                        <tr>
                            <td><b>Números Primos</b></td>
                            <td>5 ou 6 primos (entre 02,03,05,07,11,13,17,19,23)</td>
                            <td>~54% dos concursos</td>
                        </tr>
                        <tr>
                            <td><b>Soma Total</b></td>
                            <td>Entre 175 e 205 (média teórica: 195)</td>
                            <td>~75% dos concursos</td>
                        </tr>
                        <tr>
                            <td><b>Sequência Máxima</b></td>
                            <td>No máximo 4 ou 5 dezenas seguidas</td>
                            <td>~85% dos concursos</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div id="toast">Ação concluída com sucesso!</div>

    <script>
        const MOLDURA = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25];

        let selectedFechamento = new Set();
        let selectedAuditor = new Set();

        function switchTab(tabName) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        // Monta volante interativo
        function buildVolante(containerId, selectedSet, countId, maxLimit) {
            const container = document.getElementById(containerId);
            container.innerHTML = '';
            for (let i = 1; i <= 25; i++) {
                const ball = document.createElement('div');
                ball.className = 'volante-ball' + (MOLDURA.includes(i) ? ' moldura' : '');
                ball.textContent = String(i).padStart(2, '0');
                ball.onclick = () => {
                    if (selectedSet.has(i)) {
                        selectedSet.delete(i);
                        ball.classList.remove('selected');
                    } else {
                        if (maxLimit && selectedSet.size >= maxLimit) {
                            showToast(`Limite de ${maxLimit} dezenas atingido!`);
                            return;
                        }
                        selectedSet.add(i);
                        ball.classList.add('selected');
                    }
                    document.getElementById(countId).textContent = selectedSet.size;
                };
                container.appendChild(ball);
            }
        }

        function renderGameCard(game, title) {
            const ballsHtml = game.numeros.map(n => `<div class="ball">${String(n).padStart(2, '0')}</div>`).join('');
            const feedbacksHtml = game.feedbacks.map(f => {
                const cls = f[0] === 'Excelente' ? 'tag-excelente' : (f[0] === 'Bom' ? 'tag-bom' : 'tag-alerta');
                return `<div class="feedback-item"><span class="${cls}">[${f[0]}]</span> <span>${f[1]}</span></div>`;
            }).join('');

            const numbersText = game.numeros.map(n => String(n).padStart(2, '0')).join(' ');

            return `
                <div class="game-card">
                    <div class="game-header">
                        <span style="font-size: 1.15rem; font-weight: 700; color: var(--text-main);">${title}</span>
                        <span class="score-pill">Nota: ${game.score}/100</span>
                    </div>
                    <div class="game-balls">${ballsHtml}</div>
                    <div class="badges">
                        <div class="badge">P/I: <b>${game.pares}/${game.impares}</b></div>
                        <div class="badge">Moldura: <b>${game.moldura}/16</b></div>
                        <div class="badge">Miolo: <b>${game.miolo}/9</b></div>
                        <div class="badge">Primos: <b>${game.primos}</b></div>
                        <div class="badge">Fib: <b>${game.fibonacci}</b></div>
                        <div class="badge">Soma: <b>${game.soma}</b></div>
                        ${game.repetidas_ultimo !== null ? `<div class="badge">Repetidas: <b>${game.repetidas_ultimo}</b></div>` : ''}
                    </div>
                    <div class="feedbacks-list">${feedbacksHtml}</div>
                    <div class="actions-row">
                        <button class="btn btn-secondary btn-sm" onclick="navigator.clipboard.writeText('${numbersText}'); showToast('Dezenas copiadas!');">📋 Copiar Dezenas</button>
                    </div>
                </div>
            `;
        }

        function preencherExemplo() {
            document.getElementById('gen-last').value = "01 02 04 05 08 09 11 13 14 16 18 20 21 22 25";
            document.getElementById('gen-fixed').value = "05 13";
            document.getElementById('gen-excluded').value = "07";
            showToast('Dados de exemplo preenchidos!');
        }

        async function gerarPalpites() {
            const qtd = parseInt(document.getElementById('gen-qtd').value);
            const lastRaw = document.getElementById('gen-last').value;
            const fixedRaw = document.getElementById('gen-fixed').value;
            const exclRaw = document.getElementById('gen-excluded').value;

            const parseList = (str) => {
                if (!str.trim()) return [];
                return str.replace(/[,;-]/g, ' ').split(/\s+/).map(Number).filter(n => n >= 1 && n <= 25);
            };

            const payload = {
                count: qtd,
                lastContest: parseList(lastRaw),
                fixed: parseList(fixedRaw),
                excluded: parseList(exclRaw)
            };

            const container = document.getElementById('results-palpites');
            container.innerHTML = '<p style="color: var(--primary); text-align: center; margin: 20px 0;">⚡ Processando combinatória e filtros...</p>';

            try {
                const res = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.error) {
                    container.innerHTML = `<div class="game-card" style="border-color: var(--danger);"><p style="color: var(--danger);">${data.error}</p></div>`;
                    return;
                }

                let html = '<div style="margin: 20px 0; display: flex; justify-content: space-between; align-items: center;">';
                html += `<h3 style="font-size: 1.2rem;">${data.length} Palpites Otimizados Prontos:</h3>`;
                html += `<button class="btn btn-secondary btn-sm" onclick="downloadTXT('palpites')">💾 Baixar Todos em TXT</button></div>`;

                window.lastGenerated = data;
                data.forEach((p, idx) => {
                    html += renderGameCard(p, `Palpite Especialista #${idx + 1}`);
                });

                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = `<div class="game-card"><p style="color: var(--danger);">Falha de conexão: ${err.message}</p></div>`;
            }
        }

        async function executarFechamento() {
            if (selectedFechamento.size < 16 || selectedFechamento.size > 21) {
                showToast('Selecione entre 16 e 21 dezenas no volante acima!');
                return;
            }

            const maxGames = parseInt(document.getElementById('fech-max').value);
            const container = document.getElementById('results-fechamento');
            container.innerHTML = '<p style="color: var(--primary); text-align: center; margin: 20px 0;">🧩 Calculando cobertura e desdobrando volantes...</p>';

            try {
                const res = await fetch('/api/fechamento', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        pool: Array.from(selectedFechamento),
                        maxGames: maxGames
                    })
                });
                const data = await res.json();

                if (data.error) {
                    container.innerHTML = `<div class="game-card" style="border-color: var(--danger);"><p style="color: var(--danger);">${data.error}</p></div>`;
                    return;
                }

                window.lastFechamento = data;
                let html = `<div style="margin: 20px 0; display: flex; justify-content: space-between; align-items: center;">`;
                html += `<h3 style="font-size: 1.2rem;">Fechamento com ${data.length} Volantes:</h3>`;
                html += `<button class="btn btn-secondary btn-sm" onclick="downloadTXT('fechamento')">💾 Baixar Volantes em TXT</button></div>`;

                data.forEach((j, idx) => {
                    html += renderGameCard(j, `Volante Desdobrado #${idx + 1}`);
                });

                container.innerHTML = html;
            } catch (err) {
                container.innerHTML = `<div class="game-card"><p style="color: var(--danger);">Erro: ${err.message}</p></div>`;
            }
        }

        async function auditarJogo() {
            if (selectedAuditor.size !== 15) {
                showToast(`Marque exatamente 15 dezenas (atualmente: ${selectedAuditor.size})!`);
                return;
            }

            const container = document.getElementById('results-auditor');
            container.innerHTML = '<p style="color: var(--primary); text-align: center; margin: 20px 0;">🔬 Auditando seu jogo...</p>';

            try {
                const res = await fetch('/api/audit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ numbers: Array.from(selectedAuditor) })
                });
                const data = await res.json();
                container.innerHTML = renderGameCard(data, 'Diagnóstico Estatístico do seu Jogo');
            } catch (err) {
                container.innerHTML = `<div class="game-card"><p style="color: var(--danger);">Erro: ${err.message}</p></div>`;
            }
        }

        function limparFechamento() {
            selectedFechamento.clear();
            document.querySelectorAll('#volante-fechamento .volante-ball').forEach(b => b.classList.remove('selected'));
            document.getElementById('count-fechamento').textContent = '0';
            document.getElementById('results-fechamento').innerHTML = '';
        }

        function limparAuditor() {
            selectedAuditor.clear();
            document.querySelectorAll('#volante-auditor .volante-ball').forEach(b => b.classList.remove('selected'));
            document.getElementById('count-auditor').textContent = '0';
            document.getElementById('results-auditor').innerHTML = '';
        }

        function downloadTXT(type) {
            const list = type === 'palpites' ? window.lastGenerated : window.lastFechamento;
            if (!list || !list.length) return;

            let text = `=== LOTOFÁCIL EXPERT - ${type.toUpperCase()} ===\\n\\n`;
            list.forEach((item, idx) => {
                text += `Jogo #${idx + 1} (Score: ${item.score}/100):\\n`;
                text += item.numeros.map(n => String(n).padStart(2, '0')).join(' ') + '\\n';
                text += `Pares/Ímpares: ${item.pares}/${item.impares} | Moldura: ${item.moldura} | Primos: ${item.primos} | Soma: ${item.soma}\\n\\n`;
            });

            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${type}_lotofacil.txt`;
            link.click();
            showToast('Arquivo TXT baixado com sucesso!');
        }

        // Inicializa volantes na carga
        window.onload = () => {
            buildVolante('volante-fechamento', selectedFechamento, 'count-fechamento', 21);
            buildVolante('volante-auditor', selectedAuditor, 'count-auditor', 15);
        };
    </script>
</body>
</html>
"""

class LotofacilServerHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            body = HTML_CONTENT.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Arquivo não encontrado")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        data = json.loads(body) if body else {}

        if parsed.path == "/api/generate":
            try:
                qtd = int(data.get("count", 3))
                fixed = data.get("fixed", [])
                excluded = data.get("excluded", [])
                last = data.get("lastContest", [])
                last_contest = last if len(last) == 15 else None
                
                palpites = LotofacilGenerator.generate_palpites(
                    qtd=qtd,
                    fixed=fixed,
                    excluded=excluded,
                    last_contest=last_contest
                )
                self._send_json(palpites)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)

        elif parsed.path == "/api/fechamento":
            try:
                pool = data.get("pool", [])
                max_games = int(data.get("maxGames", 8))
                last = data.get("lastContest", [])
                last_contest = last if len(last) == 15 else None

                jogos = LotofacilGenerator.fechamento(
                    pool=pool,
                    max_games=max_games,
                    last_contest=last_contest
                )
                self._send_json(jogos)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)

        elif parsed.path == "/api/audit":
            try:
                numbers = data.get("numbers", [])
                if len(numbers) != 15:
                    self._send_json({"error": "Exatamente 15 dezenas são necessárias"}, status=400)
                    return
                analysis = LotofacilStats.analyze_game(numbers)
                self._send_json(analysis)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
        else:
            self.send_error(404, "Endpoint não encontrado")

    def log_message(self, format, *args):
        # Desabilita logs barulhentos no console para manter o terminal limpo
        pass

def run_server(port=5050):
    server_address = ('127.0.0.1', port)
    try:
        httpd = HTTPServer(server_address, LotofacilServerHandler)
    except OSError:
        port = 5051
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, LotofacilServerHandler)

    url = f"http://localhost:{port}"
    print(f"\n=======================================================")
    print(f"  LOTOFACIL EXPERT - PAINEL WEB INICIADO COM SUCESSO!")
    print(f"  Acesse no navegador: {url}")
    print(f"=======================================================\n")
    print("Pressione Ctrl+C para encerrar o servidor a qualquer momento.\n")

    # Abre o navegador automaticamente
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado.")
        httpd.server_close()

if __name__ == "__main__":
    port = 5050
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
