"""
Lotofácil Expert - Aplicativo Streamlit
Pronto para execução local e publicação no Streamlit Community Cloud (share.streamlit.io).
"""

import streamlit as st
from lotofacil_engine import LotofacilStats, LotofacilGenerator, MOLDURA, PRIMOS, FIBONACCI

# Configurações da página
st.set_page_config(
    page_title="Lotofácil Expert - Análise & Palpites",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada
st.markdown("""
<style>
    .ball-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 12px 0 16px 0;
    }
    .ball {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: monospace;
        font-size: 1.05rem;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
    }
    .score-badge {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        border: 1px solid #10b981;
        font-size: 0.95rem;
    }
    .badge-chip {
        display: inline-block;
        background: #1e293b;
        color: #94a3b8;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.82rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .feedback-box {
        padding: 10px;
        border-radius: 8px;
        background: #0d1424;
        border-left: 4px solid #10b981;
        margin-top: 8px;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

def render_balls(numbers):
    balls_html = "".join([f'<div class="ball">{n:02d}</div>' for n in sorted(numbers)])
    return f'<div class="ball-container">{balls_html}</div>'

# Cabeçalho Principal
st.title("🎯 Lotofácil Expert")
st.caption("Otimização estatística avançada e palpites calibrados com os 8 Filtros de Ouro da Matemática Combinatória.")

# Menu Lateral (Sidebar)
st.sidebar.image("https://images.unsplash.com/photo-1518609878373-06d740f60d8b?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.title("Navegação")
modulo = st.sidebar.radio(
    "Escolha o Módulo:",
    [
        "🎯 Gerador de Palpites",
        "📦 Fechamento / Desdobramento",
        "🔍 Auditar Volante",
        "📊 Os 5 Pilares de Ouro"
    ]
)

# -------------------------------------------------------------
# MÓDULO 1: GERADOR DE PALPITES
# -------------------------------------------------------------
if modulo == "🎯 Gerador de Palpites":
    st.subheader("Gerador de Palpites Estatisticamente Calibrados")
    st.write("Gere combinações de alta probabilidade que atendem a todos os critérios históricos da Lotofácil.")

    col1, col2 = st.columns([1, 1])

    with col1:
        qtd = st.slider("Quantidade de Palpites:", min_value=1, max_value=10, value=3)
        dezenas_fixas = st.multiselect(
            "Dezenas FIXAS (Opcional - estarão em todos os jogos):",
            options=list(range(1, 26)),
            format_func=lambda x: f"{x:02d}"
        )

    with col2:
        dezenas_excluidas = st.multiselect(
            "Dezenas EXCLUÍDAS (Opcional - não entrarão em nenhum jogo):",
            options=[n for n in range(1, 26) if n not in dezenas_fixas],
            format_func=lambda x: f"{x:02d}"
        )
        
        ultimo_concurso_raw = st.text_input(
            "Último Concurso (15 números separados por espaço - opcional):",
            placeholder="Ex: 01 02 04 05 08 09 11 13 14 16 18 20 21 22 25"
        )

    # Processamento do último concurso
    last_contest = None
    if ultimo_concurso_raw.strip():
        try:
            parsed = [int(x) for x in ultimo_concurso_raw.replace(',', ' ').split() if 1 <= int(x) <= 25]
            if len(parsed) == 15:
                last_contest = parsed
            else:
                st.warning(f"O último concurso informado contém {len(parsed)} dezenas. São necessárias exatamente 15 para ativar o filtro de repetência.")
        except ValueError:
            pass

    if st.button("⚡ Gerar Palpites Certeiros", type="primary"):
        with st.spinner("Calculando combinações e aplicando filtros rigorosos..."):
            try:
                palpites = LotofacilGenerator.generate_palpites(
                    qtd=qtd,
                    fixed=dezenas_fixas,
                    excluded=dezenas_excluidas,
                    last_contest=last_contest
                )

                st.success(f"{len(palpites)} Palpites Gerados com Sucesso!")

                txt_export = "=== LOTOFÁCIL EXPERT - PALPITES OTIMIZADOS ===\n\n"
                
                for idx, p in enumerate(palpites, 1):
                    with st.container():
                        st.markdown(f"### Palpite #{idx} &nbsp; <span class='score-badge'>Nota: {p['score']}/100</span>", unsafe_allow_html=True)
                        st.markdown(render_balls(p['numeros']), unsafe_allow_html=True)

                        # Chips de Métricas
                        chips_html = f"""
                        <div>
                            <span class='badge-chip'>Pares/Ímpares: <b>{p['pares']}/{p['impares']}</b></span>
                            <span class='badge-chip'>Moldura: <b>{p['moldura']}/16</b></span>
                            <span class='badge-chip'>Miolo: <b>{p['miolo']}/9</b></span>
                            <span class='badge-chip'>Primos: <b>{p['primos']}</b></span>
                            <span class='badge-chip'>Fibonacci: <b>{p['fibonacci']}</b></span>
                            <span class='badge-chip'>Soma: <b>{p['soma']}</b></span>
                            {f"<span class='badge-chip'>Repetidas do Anterior: <b>{p['repetidas_ultimo']}</b></span>" if p['repetidas_ultimo'] is not None else ""}
                        </div>
                        """
                        st.markdown(chips_html, unsafe_allow_html=True)

                        # Feedbacks do especialista
                        with st.expander("Ver radiografia e justificativa estatística"):
                            for status, msg in p['feedbacks']:
                                cor = "#10b981" if status == "Excelente" else ("#f59e0b" if status == "Bom" else "#ef4444")
                                st.markdown(f"<div style='color:{cor}; margin: 4px 0;'>• <b>[{status.upper()}]</b> {msg}</div>", unsafe_allow_html=True)

                        st.divider()

                        txt_export += f"Jogo #{idx} (Score: {p['score']}/100):\n"
                        txt_export += " ".join(f"{n:02d}" for n in p['numeros']) + "\n"
                        txt_export += f"Pares/Ímpares: {p['pares']}/{p['impares']} | Moldura: {p['moldura']} | Primos: {p['primos']} | Soma: {p['soma']}\n\n"

                st.download_button(
                    label="💾 Baixar Todos os Palpites em Arquivo TXT",
                    data=txt_export,
                    file_name="palpites_lotofacil.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Erro ao gerar palpites: {e}")

# -------------------------------------------------------------
# MÓDULO 2: FECHAMENTO / DESDOBRAMENTO
# -------------------------------------------------------------
elif modulo == "📦 Fechamento / Desdobramento":
    st.subheader("Desdobramento / Fechamento Inteligente")
    st.write("Selecione de **16 a 21 dezenas**. O motor gerará volantes enxutos de 15 números garantindo a maior dispersão combinatória e aprovação em todos os filtros.")

    pool_dezenas = st.multiselect(
        "Selecione suas dezenas (16 a 21 números):",
        options=list(range(1, 26)),
        default=[1, 2, 3, 5, 6, 8, 9, 10, 11, 13, 14, 16, 18, 20, 21, 23, 24, 25],
        format_func=lambda x: f"{x:02d}"
    )

    st.write(f"**Total de dezenas selecionadas:** `{len(pool_dezenas)}` dezenas.")

    max_games = st.select_slider(
        "Quantidade de volantes reduzidos a gerar:",
        options=[4, 6, 8, 10, 12, 16],
        value=8
    )

    if st.button("🧩 Gerar Fechamento Reduzido", type="primary"):
        if len(pool_dezenas) < 16 or len(pool_dezenas) > 23:
            st.error("Por favor, selecione entre 16 e 23 dezenas para o fechamento.")
        else:
            with st.spinner("Processando desdobramento com cobertura otimizada..."):
                try:
                    jogos = LotofacilGenerator.fechamento(pool_dezenas, max_games=max_games)
                    st.success(f"{len(jogos)} Volantes Otimizados Gerados!")

                    txt_fech = f"=== FECHAMENTO LOTOFÁCIL ({len(pool_dezenas)} DEZENAS) ===\n"
                    txt_fech += "Dezenas base: " + " ".join(f"{n:02d}" for n in sorted(pool_dezenas)) + "\n\n"

                    for idx, j in enumerate(jogos, 1):
                        st.markdown(f"#### Volante #{idx:02d} &nbsp; <span class='score-badge'>Nota: {j['score']}/100</span>", unsafe_allow_html=True)
                        st.markdown(render_balls(j['numeros']), unsafe_allow_html=True)
                        st.caption(f"P/I: {j['pares']}/{j['impares']} | Moldura: {j['moldura']} | Primos: {j['primos']} | Soma: {j['soma']}")
                        st.divider()

                        txt_fech += f"Volante #{idx:02d}: " + " ".join(f"{n:02d}" for n in j['numeros']) + f" [Score: {j['score']}]\n"

                    st.download_button(
                        label="💾 Baixar Fechamento em TXT",
                        data=txt_fech,
                        file_name="fechamento_lotofacil.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Erro no desdobramento: {e}")

# -------------------------------------------------------------
# MÓDULO 3: AUDITOR DE VOLANTE
# -------------------------------------------------------------
elif modulo == "🔍 Auditar Volante":
    st.subheader("Auditoria e Raio-X de Volante")
    st.write("Descubra se o seu jogo atende aos padrões de probabilidade ou se está desperdiçando chances estatísticas.")

    jogo_teste = st.multiselect(
        "Selecione as 15 dezenas do seu jogo:",
        options=list(range(1, 26)),
        format_func=lambda x: f"{x:02d}"
    )

    st.write(f"Dezenas marcadas: `{len(jogo_teste)}` / 15")

    if st.button("🔬 Analisar Jogo", type="primary"):
        if len(jogo_teste) != 15:
            st.error(f"Você marcou {len(jogo_teste)} dezenas. A Lotofácil exige exatamente 15!")
        else:
            analysis = LotofacilStats.analyze_game(jogo_teste)
            
            st.markdown(f"### Nota de Qualidade Estatística: <span class='score-badge'>{analysis['score']}/100</span>", unsafe_allow_html=True)
            st.markdown(render_balls(analysis['numeros']), unsafe_allow_html=True)

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Pares / Ímpares", f"{analysis['pares']}P / {analysis['impares']}I")
            m2.metric("Moldura / Miolo", f"{analysis['moldura']}M / {analysis['miolo']}C")
            m3.metric("Números Primos", f"{analysis['primos']}")
            m4.metric("Fibonacci", f"{analysis['fibonacci']}")
            m5.metric("Soma Total", f"{analysis['soma']}")

            st.write("#### Parecer Detalhado do Especialista:")
            for status, msg in analysis['feedbacks']:
                cor = "#10b981" if status == "Excelente" else ("#f59e0b" if status == "Bom" else "#ef4444")
                st.markdown(f"<div class='feedback-box' style='border-left-color: {cor};'><b>[{status.upper()}]</b> {msg}</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# MÓDULO 4: OS 5 PILARES DE OURO
# -------------------------------------------------------------
elif modulo == "📊 Os 5 Pilares de Ouro":
    st.subheader("Fundamentos Estatísticos da Lotofácil")
    st.markdown("""
    A Lotofácil obedece a distribuições de probabilidades combinatórias bem definidas. 
    Abaixo estão os padrões consolidados em mais de 3.000 sorteios oficiais:
    """)

    st.table({
        "Critério Estatístico": [
            "Pares e Ímpares",
            "Moldura vs. Miolo",
            "Números Primos",
            "Soma das Dezenas",
            "Repetição do Anterior",
            "Sequência Máxima"
        ],
        "Faixa de Maior Frequência": [
            "8 Ímpares e 7 Pares OU 7 Ímpares e 8 Pares",
            "10 na Moldura e 5 no Miolo (ou 9/6)",
            "5 ou 6 Primos",
            "Entre 175 e 205 (Média: 195)",
            "8, 9 ou 10 Dezenas Repetidas",
            "No máximo 4 ou 5 Números Consecutivos"
        ],
        "Frequência Histórica": [
            "~57% dos concursos",
            "~58% dos concursos",
            "~54% dos concursos",
            "~75% dos concursos",
            "~62% (Média exata: 9)",
            "~85% dos concursos"
        ]
    })
