"""
Servidor Web Local e Dashboard do Caixa Loterias Expert Hub
Autor: Caixa Loterias Expert
Sem dependências externas - utiliza apenas a biblioteca padrão do Python.
"""

import sys
import os
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List

from lottery_rules import LOTTERIES_CONFIG
from lottery_engine import LotteryAnalyzer, LotteryGenerator, LotteryClosings, LotteryChecker
from caixa_api import CaixaLoteriasAPI

# HTML / CSS / JS embutido completo e responsivo
HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caixa Loterias Expert - Todas as Loterias Oficiais</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #0a0e17;
            --bg-card: #121826;
            --bg-card-hover: #182236;
            --border: #202b42;
            --primary: #209869;
            --primary-glow: rgba(32, 152, 105, 0.25);
            --accent: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
            --gold: #fbbf24;
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
            padding-bottom: 70px;
        }

        header {
            background: linear-gradient(180deg, #172138 0%, rgba(10, 14, 23, 0) 100%);
            padding: 24px 20px 16px 20px;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }

        .brand-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
            color: #38bdf8;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.subtitle {
            color: var(--text-muted);
            margin-top: 6px;
            font-size: 1rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Seletor de Loterias Caixa */
        .lottery-selector {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 12px;
            margin-bottom: 24px;
            scrollbar-width: thin;
        }

        .lottery-btn {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 10px 18px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .lottery-btn:hover {
            color: #fff;
            transform: translateY(-2px);
        }

        .lottery-btn.active {
            color: #fff;
            border-color: currentColor;
            box-shadow: 0 4px 18px var(--primary-glow);
        }

        .lottery-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: currentColor;
        }

        /* Banner de Status da Loteria & Resultado Oficial */
        .lottery-banner {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-left: 6px solid var(--primary);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 25px;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 20px;
            align-items: center;
        }

        .banner-info h2 {
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .banner-info p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .banner-result {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 18px;
            text-align: right;
            min-width: 300px;
        }

        .result-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--text-muted);
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .result-contest {
            font-size: 1.15rem;
            font-weight: 700;
            color: #38bdf8;
            margin: 2px 0 8px 0;
        }

        .result-balls {
            display: flex;
            gap: 6px;
            justify-content: flex-end;
            flex-wrap: wrap;
            margin-bottom: 6px;
        }

        .result-ball {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--primary);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        }

        .result-ball.clover {
            background: #10b981;
            border: 2px solid #34d399;
        }

        .refresh-api-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 0.8rem;
            cursor: pointer;
            text-decoration: underline;
            margin-top: 4px;
        }

        .refresh-api-btn:hover {
            color: #fff;
        }

        /* Abas de Ação */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px 18px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .tab-btn:hover {
            color: #fff;
            background: rgba(255,255,255,0.04);
        }

        .tab-btn.active {
            color: #fff;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-bottom: 3px solid var(--primary);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Layout Grid */
        .grid-layout {
            display: grid;
            grid-template-columns: 380px 1fr;
            gap: 25px;
        }

        @media (max-width: 900px) {
            .grid-layout {
                grid-template-columns: 1fr;
            }
            .lottery-banner {
                grid-template-columns: 1fr;
            }
            .banner-result {
                text-align: left;
            }
            .result-balls {
                justify-content: flex-start;
            }
        }

        .panel-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px;
        }

        .panel-card h3 {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .form-group {
            margin-bottom: 18px;
        }

        .form-group label {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .form-control {
            width: 100%;
            background: #090d15;
            border: 1px solid var(--border);
            color: #fff;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
        }

        .form-control:focus {
            border-color: var(--primary);
        }

        /* Volante Interativo */
        .volante-container {
            margin-top: 15px;
        }

        .volante-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        .volante-grid {
            display: grid;
            gap: 6px;
            background: #090d15;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid var(--border);
            max-height: 380px;
            overflow-y: auto;
        }

        .num-btn {
            background: #141c2c;
            border: 1px solid #233152;
            color: #e2e8f0;
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            user-select: none;
        }

        .num-btn:hover {
            border-color: var(--primary);
            color: #fff;
        }

        .num-btn.fixed {
            background: #059669 !important;
            border-color: #34d399 !important;
            color: #fff !important;
        }

        .num-btn.excluded {
            background: #dc2626 !important;
            border-color: #f87171 !important;
            color: #fff !important;
            opacity: 0.6;
        }

        .num-btn.selected {
            background: var(--primary) !important;
            border-color: #fff !important;
            color: #fff !important;
            transform: scale(1.05);
        }

        .volante-legend {
            display: flex;
            gap: 14px;
            font-size: 0.75rem;
            margin-top: 8px;
            color: var(--text-muted);
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .legend-box {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        /* Super Sete - Matriz Vertical */
        .supersete-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 8px;
        }

        .col-supersete {
            display: flex;
            flex-direction: column;
            gap: 4px;
            text-align: center;
        }

        .col-title {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 700;
        }

        /* Botões de Ação */
        .btn-primary {
            width: 100%;
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 14px 20px;
            border-radius: 10px;
            font-size: 1.05rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 15px var(--primary-glow);
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 15px;
        }

        .btn-primary:hover {
            filter: brightness(1.15);
            transform: translateY(-2px);
        }

        /* Cards de Palpites Gerados */
        .games-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }

        .game-card {
            background: #0e1422;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 15px;
            transition: all 0.2s;
        }

        .game-card:hover {
            border-color: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .card-number {
            font-weight: 800;
            font-size: 1rem;
            color: #fff;
        }

        .score-pill {
            font-size: 0.75rem;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 999px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .balls-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }

        .ball {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #172138;
            border: 1px solid var(--border);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.95rem;
            font-weight: 700;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }

        .ball.hit {
            background: #eab308 !important;
            border-color: #fef08a !important;
            color: #000 !important;
            font-weight: 900 !important;
            box-shadow: 0 0 10px rgba(234, 179, 8, 0.6) !important;
        }

        .card-stats {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 8px;
        }

        .stat-badge {
            background: rgba(255,255,255,0.04);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .extras-badge {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 8px;
            display: inline-block;
        }

        /* Auditor */
        .audit-result-box {
            background: #090d15;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }

        .score-circle {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            border: 4px solid var(--primary);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto 15px auto;
        }

        .score-value {
            font-size: 1.8rem;
            font-weight: 800;
        }

        .score-lbl {
            font-size: 0.65rem;
            text-transform: uppercase;
            color: var(--text-muted);
        }

        .bullet-list {
            list-style: none;
            margin-top: 12px;
            font-size: 0.9rem;
        }

        .bullet-list li {
            padding: 6px 0;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }

        .bullet-list li.alert {
            color: #f87171;
        }

        .bullet-list li.praise {
            color: #4ade80;
        }

        /* Fechamento Info */
        .closing-badge {
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }

        /* Export Bar */
        .export-actions {
            display: flex;
            gap: 10px;
        }

        .btn-secondary {
            background: #172138;
            color: #fff;
            border: 1px solid var(--border);
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .btn-secondary:hover {
            background: #233152;
        }

        .empty-placeholder {
            text-align: center;
            padding: 50px 20px;
            color: var(--text-muted);
        }

        .empty-icon {
            font-size: 3rem;
            margin-bottom: 10px;
            opacity: 0.5;
        }
    </style>
</head>
<body>

    <header>
        <div class="brand-badge">Caixa Loterias Expert Hub</div>
        <h1>Especialista em Loterias da Caixa</h1>
        <p class="subtitle">Análise Estatística Avançada, Palpites Calibrados, Fechamentos Matemáticos e Auditor de Volantes</p>
    </header>

    <div class="container">
        <!-- Barra de Seleção de Loterias -->
        <div class="lottery-selector" id="lotterySelector"></div>

        <!-- Banner com a Loteria Ativa e Último Resultado Oficial -->
        <div class="lottery-banner" id="lotteryBanner">
            <div class="banner-info">
                <h2 id="bannerTitle">Carregando...</h2>
                <p id="bannerSlogan"></p>
                <p id="bannerRules" style="font-size: 0.85rem; color: #38bdf8; margin-top: 6px;"></p>
            </div>
            <div class="banner-result">
                <div class="result-title">Último Concurso Oficial Caixa</div>
                <div class="result-contest" id="resContest">Concurso ---</div>
                <div class="result-balls" id="resBalls"></div>
                <div id="resExtras"></div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #4ade80; margin-top: 4px;" id="resPrize"></div>
                <button class="refresh-api-btn" onclick="fetchLatestResult(true)">🔄 Atualizar Resultado da Caixa</button>
            </div>
        </div>

        <!-- Abas do Módulo -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('generator')">🎲 Gerador de Palpites</button>
            <button class="tab-btn" onclick="switchTab('closings')">🔒 Fechamentos Reduzidos</button>
            <button class="tab-btn" onclick="switchTab('auditor')">🩺 Raio-X & Auditor</button>
            <button class="tab-btn" onclick="switchTab('checker')">🏆 Conferidor de Apostas</button>
        </div>

        <!-- TAB 1: GERADOR EXPERT -->
        <div class="tab-content active" id="tab-generator">
            <div class="grid-layout">
                <div class="panel-card">
                    <h3>⚙️ Configuração do Jogo</h3>
                    
                    <div class="form-group">
                        <label>Quantidade de Palpites:</label>
                        <select class="form-control" id="genCount">
                            <option value="1">1 Jogo Otimizado</option>
                            <option value="3">3 Jogos Otimizados</option>
                            <option value="5" selected>5 Jogos Otimizados</option>
                            <option value="10">10 Jogos Otimizados</option>
                            <option value="15">15 Jogos Otimizados</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Dezenas por Cartão:</label>
                        <select class="form-control" id="genPickSize"></select>
                    </div>

                    <div class="volante-container">
                        <div class="volante-label">
                            <span>Volante Estratégico (Opcional):</span>
                            <span id="volanteCounter" style="color: #38bdf8;">0 fixos / 0 excluídos</span>
                        </div>
                        <div class="volante-legend">
                            <div class="legend-item"><div class="legend-box" style="background: #059669;"></div> Fixo (1 clique)</div>
                            <div class="legend-item"><div class="legend-box" style="background: #dc2626;"></div> Excluído (2 cliques)</div>
                            <div class="legend-item"><div class="legend-box" style="background: #141c2c;"></div> Livre (3 cliques)</div>
                        </div>
                        <div class="volante-grid" id="genVolante"></div>
                    </div>

                    <button class="btn-primary" onclick="generateGames()">
                        <span>✨ Gerar Palpites Certeiros</span>
                    </button>
                </div>

                <div class="panel-card">
                    <div class="games-header">
                        <h3>📋 Palpites Calibrados (<span id="gamesCountBadge">0</span>)</h3>
                        <div class="export-actions" id="exportActions" style="display: none;">
                            <button class="btn-secondary" onclick="copyGames()">📋 Copiar</button>
                            <button class="btn-secondary" onclick="downloadTxt()">💾 Baixar TXT</button>
                        </div>
                    </div>

                    <div id="gamesContainer">
                        <div class="empty-placeholder">
                            <div class="empty-icon">🎯</div>
                            <p>Configure seus filtros à esquerda e clique em <b>Gerar Palpites Certeiros</b> para receber jogos balanceados com o algoritmo da Caixa Loterias Expert.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: FECHAMENTOS INTELIGENTES -->
        <div class="tab-content" id="tab-closings">
            <div class="grid-layout">
                <div class="panel-card">
                    <h3>📐 Montar Fechamento</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
                        Selecione as dezenas que você deseja combinar no volante abaixo. O motor calculará uma matriz reduzida de alta cobertura.
                    </p>
                    
                    <div class="volante-label">
                        <span>Dezenas Selecionadas:</span>
                        <span id="closingSelectedCount" style="color: #38bdf8; font-weight: 700;">0 dezenas</span>
                    </div>
                    <div class="volante-grid" id="closingVolante"></div>

                    <button class="btn-primary" onclick="generateClosing()">
                        <span>🔒 Calcular Desdobramento</span>
                    </button>
                </div>

                <div class="panel-card">
                    <div class="games-header">
                        <h3>Matriz de Fechamento</h3>
                        <div class="export-actions" id="closingExportActions" style="display: none;">
                            <button class="btn-secondary" onclick="copyClosingGames()">📋 Copiar</button>
                        </div>
                    </div>
                    <div id="closingInfoBadge"></div>
                    <div id="closingGamesContainer">
                        <div class="empty-placeholder">
                            <div class="empty-icon">📐</div>
                            <p>Selecione um grupo de dezenas no volante e calcule um fechamento para obter a maior probabilidade com menor custo de apostas.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: AUDITOR (RAIO-X) -->
        <div class="tab-content" id="tab-auditor">
            <div class="grid-layout">
                <div class="panel-card">
                    <h3>🩺 Teste seu Próprio Jogo</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
                        Marque as dezenas no volante para receber a nota do seu jogo (0 a 100) baseada nos padrões históricos de sorteio da Caixa.
                    </p>

                    <div class="volante-label">
                        <span>Dezenas Marcadas:</span>
                        <span id="auditSelectedCount" style="color: #38bdf8; font-weight: 700;">0 marcadas</span>
                    </div>
                    <div class="volante-grid" id="auditVolante"></div>

                    <button class="btn-primary" onclick="auditManualGame()">
                        <span>🔍 Auditar Volante</span>
                    </button>
                </div>

                <div class="panel-card">
                    <h3>Raio-X Estatístico</h3>
                    <div id="auditResultContainer">
                        <div class="empty-placeholder">
                            <div class="empty-icon">📊</div>
                            <p>Marque as dezenas da sua aposta para verificar se você está jogando com alta probabilidade ou cometendo erros clássicos (como excesso de pares, números seguidos ou somas improváveis).</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: CONFERIDOR DE APOSTAS -->
        <div class="tab-content" id="tab-checker">
            <div class="panel-card">
                <h3>🏆 Conferência de Jogos contra Concurso Oficial</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 20px;">
                    Confira instantaneamente os palpites gerados ou fechamentos contra as dezenas sorteadas pela Caixa Econômica Federal.
                </p>

                <div style="margin-bottom: 20px;">
                    <button class="btn-primary" style="max-width: 300px;" onclick="checkAllGeneratedGames()">
                        <span>⚡ Conferir Meus Palpites Agora</span>
                    </button>
                </div>

                <div id="checkerResultsContainer">
                    <div class="empty-placeholder">
                        <div class="empty-icon">🥇</div>
                        <p>Gere palpites ou fechamentos na aba do Gerador e clique em <b>Conferir Meus Palpites Agora</b> para ver quantos acertos cada bilhete teria feito no concurso oficial!</p>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        let lotteriesConfig = {};
        let currentLotteryId = "megasena";
        let currentLottery = null;
        let latestResult = null;

        // Estado do Gerador
        let fixedNumbers = new Set();
        let excludedNumbers = new Set();
        let generatedGames = [];

        // Estado do Fechamento
        let closingSelected = new Set();
        let closingGames = [];

        // Estado do Auditor
        let auditSelected = new Set();

        async function init() {
            try {
                const res = await fetch('/api/lotteries');
                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}`);
                }
                lotteriesConfig = await res.json();
                renderLotterySelector();
                selectLottery('megasena');
            } catch (e) {
                console.error("Erro ao carregar loterias:", e);
                document.getElementById('bannerTitle').innerText = "Erro ao Carregar";
                document.getElementById('bannerSlogan').innerText = "Falha ao obter lista de loterias: " + e.message;
            }
        }

        function renderLotterySelector() {
            const container = document.getElementById('lotterySelector');
            container.innerHTML = '';
            for (const [id, cfg] of Object.entries(lotteriesConfig)) {
                const btn = document.createElement('button');
                btn.className = `lottery-btn ${id === currentLotteryId ? 'active' : ''}`;
                btn.id = `btn-lottery-${id}`;
                btn.style.setProperty('--primary-glow', cfg.color_primary + '40');
                btn.innerHTML = `<span class="lottery-dot" style="color: ${cfg.color_primary};"></span> ${cfg.name}`;
                btn.onclick = () => selectLottery(id);
                container.appendChild(btn);
            }
        }

        function selectLottery(id) {
            currentLotteryId = id;
            currentLottery = lotteriesConfig[id];

            // Atualiza botões
            document.querySelectorAll('.lottery-btn').forEach(b => b.classList.remove('active'));
            const activeBtn = document.getElementById(`btn-lottery-${id}`);
            if (activeBtn) activeBtn.classList.add('active');

            // Aplica cor primária
            document.documentElement.style.setProperty('--primary', currentLottery.color_primary);
            document.documentElement.style.setProperty('--primary-glow', currentLottery.color_primary + '40');

            // Atualiza banner
            document.getElementById('bannerTitle').innerText = currentLottery.name;
            document.getElementById('bannerSlogan').innerText = currentLottery.slogan;
            document.getElementById('bannerRules').innerText = `Aposta padrão: ${currentLottery.default_pick} números (mínimo ${currentLottery.min_pick}, máximo ${currentLottery.max_pick}). Faixa: ${currentLottery.min_number} a ${currentLottery.max_number}.`;

            // Atualiza opções de Dezenas por Cartão
            const pickSelect = document.getElementById('genPickSize');
            pickSelect.innerHTML = '';
            for (let i = currentLottery.min_pick; i <= currentLottery.max_pick; i++) {
                const opt = document.createElement('option');
                opt.value = i;
                opt.innerText = `${i} dezenas ${i === currentLottery.default_pick ? '(Padrão)' : ''}`;
                if (i === currentLottery.default_pick) opt.selected = true;
                pickSelect.appendChild(opt);
            }

            // Reseta seleções
            fixedNumbers.clear();
            excludedNumbers.clear();
            closingSelected.clear();
            auditSelected.clear();
            generatedGames = [];
            closingGames = [];

            updateVolanteCounters();
            renderVolantes();
            renderGamesList();

            // Busca resultado oficial
            fetchLatestResult(false);
        }

        async function fetchLatestResult(forceRefresh = false) {
            const ballsContainer = document.getElementById('resBalls');
            ballsContainer.innerHTML = '<span style="font-size:0.8rem;color:#94a3b8;">Buscando...</span>';

            try {
                const res = await fetch(`/api/latest-result?lottery=${currentLotteryId}&refresh=${forceRefresh}`);
                latestResult = await res.json();

                document.getElementById('resContest').innerText = `Concurso ${latestResult.numero || '---'} (${latestResult.dataApuracao || ''})`;
                
                ballsContainer.innerHTML = '';
                const dezenas = latestResult.listaDezenas || [];
                dezenas.forEach(d => {
                    const b = document.createElement('div');
                    b.className = 'result-ball';
                    b.innerText = d;
                    ballsContainer.appendChild(b);
                });

                // Trevos se for +Milionária
                const extrasContainer = document.getElementById('resExtras');
                extrasContainer.innerHTML = '';
                if (latestResult.trevosSorteados) {
                    const trevosHtml = latestResult.trevosSorteados.map(t => `<span class="result-ball clover">🍀${t}</span>`).join(' ');
                    extrasContainer.innerHTML = `<div style="display:flex;gap:4px;justify-content:flex-end;margin-top:4px;">${trevosHtml}</div>`;
                } else if (latestResult.nomeMesSorte) {
                    extrasContainer.innerHTML = `<span style="font-size:0.8rem;color:#f59e0b;">Mês: ${latestResult.nomeMesSorte}</span>`;
                } else if (latestResult.nomeTimeCoracaoMesSorte) {
                    extrasContainer.innerHTML = `<span style="font-size:0.8rem;color:#4ade80;">Time: ${latestResult.nomeTimeCoracaoMesSorte}</span>`;
                }

                // Prêmio estimado
                const estimativa = latestResult.valorEstimadoProximoConcurso;
                if (estimativa && estimativa > 0) {
                    const fmt = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(estimativa);
                    document.getElementById('resPrize').innerText = (latestResult.acumulado ? 'Acumulou! Estimativa: ' : 'Estimativa: ') + fmt;
                } else {
                    document.getElementById('resPrize').innerText = '';
                }

            } catch (e) {
                console.error("Erro na API da Caixa:", e);
                ballsContainer.innerHTML = '<span style="color:#f87171;font-size:0.8rem;">Modo Offline</span>';
            }
        }

        function renderVolantes() {
            renderGenVolante();
            renderClosingVolante();
            renderAuditVolante();
        }

        function renderGenVolante() {
            const container = document.getElementById('genVolante');
            container.innerHTML = '';
            
            const minN = currentLottery.min_number;
            const maxN = currentLottery.max_number;
            const cols = currentLottery.layout_cols || 10;
            container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

            for (let n = minN; n <= maxN; n++) {
                const btn = document.createElement('div');
                btn.className = 'num-btn';
                const formatted = (minN === 0 && n < 10) ? `0${n}` : (n < 10 ? `0${n}` : `${n}`);
                btn.innerText = formatted;

                if (fixedNumbers.has(n)) btn.classList.add('fixed');
                if (excludedNumbers.has(n)) btn.classList.add('excluded');

                btn.onclick = () => {
                    if (!fixedNumbers.has(n) && !excludedNumbers.has(n)) {
                        fixedNumbers.add(n);
                    } else if (fixedNumbers.has(n)) {
                        fixedNumbers.delete(n);
                        excludedNumbers.add(n);
                    } else {
                        excludedNumbers.delete(n);
                    }
                    updateVolanteCounters();
                    renderGenVolante();
                };

                container.appendChild(btn);
            }
        }

        function renderClosingVolante() {
            const container = document.getElementById('closingVolante');
            container.innerHTML = '';
            
            const minN = currentLottery.min_number;
            const maxN = currentLottery.max_number;
            const cols = currentLottery.layout_cols || 10;
            container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

            for (let n = minN; n <= maxN; n++) {
                const btn = document.createElement('div');
                btn.className = 'num-btn';
                const formatted = (minN === 0 && n < 10) ? `0${n}` : (n < 10 ? `0${n}` : `${n}`);
                btn.innerText = formatted;

                if (closingSelected.has(n)) btn.classList.add('selected');

                btn.onclick = () => {
                    if (closingSelected.has(n)) {
                        closingSelected.delete(n);
                    } else {
                        closingSelected.add(n);
                    }
                    document.getElementById('closingSelectedCount').innerText = `${closingSelected.size} dezenas selecionadas`;
                    renderClosingVolante();
                };

                container.appendChild(btn);
            }
        }

        function renderAuditVolante() {
            const container = document.getElementById('auditVolante');
            container.innerHTML = '';
            
            const minN = currentLottery.min_number;
            const maxN = currentLottery.max_number;
            const cols = currentLottery.layout_cols || 10;
            container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

            for (let n = minN; n <= maxN; n++) {
                const btn = document.createElement('div');
                btn.className = 'num-btn';
                const formatted = (minN === 0 && n < 10) ? `0${n}` : (n < 10 ? `0${n}` : `${n}`);
                btn.innerText = formatted;

                if (auditSelected.has(n)) btn.classList.add('selected');

                btn.onclick = () => {
                    if (auditSelected.has(n)) {
                        auditSelected.delete(n);
                    } else {
                        auditSelected.add(n);
                    }
                    document.getElementById('auditSelectedCount').innerText = `${auditSelected.size} marcadas`;
                    renderAuditVolante();
                };

                container.appendChild(btn);
            }
        }

        function updateVolanteCounters() {
            document.getElementById('volanteCounter').innerText = `${fixedNumbers.size} fixos / ${excludedNumbers.size} excluídos`;
        }

        async function generateGames() {
            const count = parseInt(document.getElementById('genCount').value);
            const pickSize = parseInt(document.getElementById('genPickSize').value);

            const payload = {
                lottery_id: currentLotteryId,
                count: count,
                pick_size: pickSize,
                fixed_numbers: Array.from(fixedNumbers),
                excluded_numbers: Array.from(excludedNumbers),
                min_score: 75
            };

            try {
                const res = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                generatedGames = await res.json();
                renderGamesList();
            } catch (e) {
                alert("Erro ao gerar palpites: " + e);
            }
        }

        function renderGamesList() {
            const container = document.getElementById('gamesContainer');
            const countBadge = document.getElementById('gamesCountBadge');
            const exportActions = document.getElementById('exportActions');

            countBadge.innerText = generatedGames.length;

            if (generatedGames.length === 0) {
                exportActions.style.display = 'none';
                container.innerHTML = `
                    <div class="empty-placeholder">
                        <div class="empty-icon">🎯</div>
                        <p>Configure seus filtros à esquerda e clique em <b>Gerar Palpites Certeiros</b> para receber jogos balanceados com o algoritmo da Caixa Loterias Expert.</p>
                    </div>`;
                return;
            }

            exportActions.style.display = 'flex';
            container.innerHTML = '';

            generatedGames.forEach((game, idx) => {
                const card = document.createElement('div');
                card.className = 'game-card';

                const ballsHtml = game.numbers.map(n => {
                    const formatted = (n < 10 && currentLottery.min_number === 0) ? `0${n}` : (n < 10 ? `0${n}` : `${n}`);
                    return `<div class="ball">${formatted}</div>`;
                }).join('');

                let extrasHtml = '';
                if (game.extras) {
                    if (game.extras.trevos) {
                        extrasHtml = `<div class="extras-badge">🍀 Trevos: ${game.extras.trevos.join(' e ')}</div>`;
                    } else if (game.extras.mes_da_sorte) {
                        extrasHtml = `<div class="extras-badge">📅 Mês: ${game.extras.mes_da_sorte}</div>`;
                    } else if (game.extras.time_do_coracao) {
                        extrasHtml = `<div class="extras-badge">⚽ Time: ${game.extras.time_do_coracao}</div>`;
                    }
                }

                card.innerHTML = `
                    <div class="card-top">
                        <div class="card-number">Jogo #${idx + 1}</div>
                        <div class="score-pill" style="background: ${game.level_color}25; color: ${game.level_color}; border: 1px solid ${game.level_color};">
                            Score ${game.score}% • ${game.level}
                        </div>
                    </div>
                    <div class="balls-row">${ballsHtml}</div>
                    ${extrasHtml}
                    <div class="card-stats">
                        <span class="stat-badge">Soma: ${game.soma}</span>
                        <span class="stat-badge">Pares: ${game.pares} | Ímpares: ${game.impares}</span>
                        <span class="stat-badge">Primos: ${game.primos}</span>
                        <span class="stat-badge">Max Seq: ${game.max_consecutive}</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        async function generateClosing() {
            if (closingSelected.size < currentLottery.default_pick) {
                alert(`Para desdobrar na ${currentLottery.name}, selecione no mínimo ${currentLottery.default_pick} dezenas no volante.`);
                return;
            }

            const payload = {
                lottery_id: currentLotteryId,
                selected_numbers: Array.from(closingSelected),
                ticket_size: currentLottery.default_pick,
                max_tickets: 10
            };

            try {
                const res = await fetch('/api/closing', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                closingGames = data.tickets || [];

                document.getElementById('closingInfoBadge').innerHTML = `
                    <div class="closing-badge">
                        ✨ <b>${data.guarantee}</b> | Cobertura estimada: <b>${data.coverage_percentage}%</b>
                    </div>
                `;
                document.getElementById('closingExportActions').style.display = 'flex';

                const container = document.getElementById('closingGamesContainer');
                container.innerHTML = '';

                closingGames.forEach((game, idx) => {
                    const card = document.createElement('div');
                    card.className = 'game-card';
                    const ballsHtml = game.numbers.map(n => `<div class="ball">${n < 10 ? '0' + n : n}</div>`).join('');
                    card.innerHTML = `
                        <div class="card-top">
                            <div class="card-number">Volante #${idx + 1}</div>
                            <div class="score-pill" style="background: ${game.level_color}25; color: ${game.level_color};">Score ${game.score}%</div>
                        </div>
                        <div class="balls-row">${ballsHtml}</div>
                    `;
                    container.appendChild(card);
                });

            } catch (e) {
                alert("Erro ao gerar fechamento: " + e);
            }
        }

        async function auditManualGame() {
            if (auditSelected.size === 0) {
                alert("Selecione os números do seu jogo no volante para auditar.");
                return;
            }

            const payload = {
                lottery_id: currentLotteryId,
                numbers: Array.from(auditSelected)
            };

            try {
                const res = await fetch('/api/audit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const analysis = await res.json();
                renderAuditResult(analysis);
            } catch (e) {
                alert("Erro ao auditar jogo: " + e);
            }
        }

        function renderAuditResult(analysis) {
            const container = document.getElementById('auditResultContainer');
            
            const alertsHtml = (analysis.alerts || []).map(a => `<li class="alert">⚠️ ${a}</li>`).join('');
            const praisesHtml = (analysis.praises || []).map(p => `<li class="praise">✅ ${p}</li>`).join('');

            container.innerHTML = `
                <div class="audit-result-box">
                    <div class="score-circle" style="border-color: ${analysis.level_color};">
                        <div class="score-value" style="color: ${analysis.level_color};">${analysis.score}</div>
                        <div class="score-lbl">Pontos</div>
                    </div>
                    <div style="text-align: center; font-weight: 800; font-size: 1.1rem; color: ${analysis.level_color}; margin-bottom: 12px;">
                        ${analysis.level}
                    </div>
                    <div class="card-stats" style="justify-content: center; margin-bottom: 15px;">
                        <span class="stat-badge">Total Dezenas: ${analysis.total_numbers}</span>
                        <span class="stat-badge">Soma: ${analysis.soma}</span>
                        <span class="stat-badge">Pares: ${analysis.pares} | Ímpares: ${analysis.impares}</span>
                        <span class="stat-badge">Primos: ${analysis.primos}</span>
                    </div>
                    <ul class="bullet-list">
                        ${praisesHtml}
                        ${alertsHtml}
                    </ul>
                </div>
            `;
        }

        async function checkAllGeneratedGames() {
            if (!latestResult || !latestResult.listaDezenas || latestResult.listaDezenas.length === 0) {
                alert("Aguarde o carregamento do resultado oficial ou atualize o concurso.");
                return;
            }

            const gamesToCheck = generatedGames.length > 0 ? generatedGames : closingGames;
            if (gamesToCheck.length === 0) {
                alert("Nenhum palpite gerado ainda! Gere jogos na aba Gerador antes de conferir.");
                return;
            }

            const container = document.getElementById('checkerResultsContainer');
            container.innerHTML = '<p style="color: #38bdf8;">Conferindo apostas contra o concurso oficial...</p>';

            const drawnNumbers = latestResult.listaDezenas.map(d => parseInt(d));
            const results = [];

            for (const g of gamesToCheck) {
                const res = await fetch('/api/check-ticket', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        lottery_id: currentLotteryId,
                        ticket_numbers: g.numbers,
                        drawn_numbers: drawnNumbers,
                        ticket_extras: g.extras,
                        drawn_extras: latestResult
                    })
                });
                const checkData = await res.json();
                results.push({ game: g, check: checkData });
            }

            container.innerHTML = '';
            results.forEach((item, idx) => {
                const g = item.game;
                const c = item.check;

                const card = document.createElement('div');
                card.className = 'game-card';
                if (c.premiado) {
                    card.style.borderColor = '#fbbf24';
                    card.style.background = 'rgba(251, 191, 36, 0.05)';
                }

                const ballsHtml = g.numbers.map(n => {
                    const isHit = c.dezenas_acertadas.includes(n);
                    const formatted = (n < 10) ? `0${n}` : `${n}`;
                    return `<div class="ball ${isHit ? 'hit' : ''}">${formatted}</div>`;
                }).join('');

                const badgeColor = c.premiado ? '#fbbf24' : '#94a3b8';
                card.innerHTML = `
                    <div class="card-top">
                        <div class="card-number">Bilhete #${idx + 1}</div>
                        <div class="score-pill" style="background: ${badgeColor}20; color: ${badgeColor}; border: 1px solid ${badgeColor};">
                            ${c.acertos} Acertos • ${c.faixa}
                        </div>
                    </div>
                    <div class="balls-row">${ballsHtml}</div>
                `;
                container.appendChild(card);
            });
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(`tab-${tabId}`).classList.add('active');
        }

        function copyGames() {
            if (generatedGames.length === 0) return;
            const text = generatedGames.map((g, i) => `Jogo ${i+1}: ` + g.numbers.map(n => n < 10 ? '0' + n : n).join(' - ')).join('\\n');
            navigator.clipboard.writeText(text);
            alert("Jogos copiados para a área de transferência!");
        }

        function copyClosingGames() {
            if (closingGames.length === 0) return;
            const text = closingGames.map((g, i) => `Volante ${i+1}: ` + g.numbers.map(n => n < 10 ? '0' + n : n).join(' - ')).join('\\n');
            navigator.clipboard.writeText(text);
            alert("Fechamento copiado para a área de transferência!");
        }

        function downloadTxt() {
            if (generatedGames.length === 0) return;
            let content = `=== CAIXA LOTERIAS EXPERT ===\\n`;
            content += `Modalidade: ${currentLottery.name}\\n`;
            content += `Total de Jogos: ${generatedGames.length}\\n\\n`;
            generatedGames.forEach((g, i) => {
                content += `Jogo ${i+1} [Score: ${g.score}%]: ` + g.numbers.map(n => n < 10 ? '0' + n : n).join(' ') + `\\n`;
            });
            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = `palpites_${currentLotteryId}.txt`;
            a.click();
        }

        window.onload = init;
    </script>
</body>
</html>
"""

class LotteryRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type="application/json", status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ["/", "/index.html"]:
            self._set_headers(content_type="text/html; charset=utf-8")
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
            return

        elif path == "/api/lotteries":
            self._set_headers()
            def json_safe_helper(o):
                if isinstance(o, (set, tuple)):
                    return list(o)
                return str(o)
            self.wfile.write(json.dumps(LOTTERIES_CONFIG, default=json_safe_helper, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/latest-result":
            lottery_id = query.get("lottery", ["megasena"])[0]
            force = query.get("refresh", ["false"])[0].lower() == "true"
            data = CaixaLoteriasAPI.get_latest_result(lottery_id, force_refresh=force)
            self._set_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        self._set_headers(status=404)
        self.wfile.write(b'{"error": "Not found"}')

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        if path == "/api/generate":
            lottery_id = payload.get("lottery_id", "megasena")
            count = int(payload.get("count", 5))
            pick_size = payload.get("pick_size")
            fixed = payload.get("fixed_numbers", [])
            excluded = payload.get("excluded_numbers", [])
            min_score = int(payload.get("min_score", 75))

            games = LotteryGenerator.generate_batch(
                lottery_id=lottery_id,
                count=count,
                pick_size=pick_size,
                fixed_numbers=fixed,
                excluded_numbers=excluded,
                min_score=min_score
            )
            self._set_headers()
            self.wfile.write(json.dumps(games, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/closing":
            lottery_id = payload.get("lottery_id", "megasena")
            selected = payload.get("selected_numbers", [])
            size = payload.get("ticket_size")
            max_tickets = int(payload.get("max_tickets", 10))

            closing = LotteryClosings.generate_closing(
                lottery_id=lottery_id,
                selected_numbers=selected,
                ticket_size=size,
                max_tickets=max_tickets
            )
            self._set_headers()
            self.wfile.write(json.dumps(closing, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/audit":
            lottery_id = payload.get("lottery_id", "megasena")
            numbers = payload.get("numbers", [])
            analysis = LotteryAnalyzer.analyze_game(lottery_id, numbers)
            self._set_headers()
            self.wfile.write(json.dumps(analysis, ensure_ascii=False).encode("utf-8"))
            return

        elif path == "/api/check-ticket":
            lottery_id = payload.get("lottery_id", "megasena")
            t_nums = payload.get("ticket_numbers", [])
            d_nums = payload.get("drawn_numbers", [])
            t_extras = payload.get("ticket_extras")
            d_extras = payload.get("drawn_extras")

            result = LotteryChecker.check_ticket(
                lottery_id=lottery_id,
                ticket_numbers=t_nums,
                drawn_numbers=d_nums,
                ticket_extras=t_extras,
                drawn_extras=d_extras
            )
            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            return

        self._set_headers(status=404)
        self.wfile.write(b'{"error": "Not found"}')


def run_server(port=5050, open_browser=True):
    env_port = os.environ.get("PORT")
    is_cloud = env_port is not None
    effective_port = int(env_port) if is_cloud else port

    server_address = ("0.0.0.0", effective_port)
    httpd = HTTPServer(server_address, LotteryRequestHandler)
    print(f"============================================================")
    print(f"  CAIXA LOTERIAS EXPERT HUB")
    print(f"  Mega-Sena, Lotofácil, Quina, Lotomania, Dupla Sena,")
    print(f"  Dia de Sorte, Timemania, +Milionária e Super Sete")
    print(f"============================================================")
    print(f"  Servidor rodando em: http://0.0.0.0:{effective_port}")
    if is_cloud:
        print(f"  Modo Nuvem (Render / Web Service) ativo na porta {effective_port}")
    else:
        print(f"  Acesse no navegador: http://localhost:{effective_port}")
    print(f"  Pressione Ctrl+C para encerrar o servidor.")
    print(f"============================================================")

    if open_browser and not is_cloud:
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{effective_port}")).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    run_server()
