import streamlit as st
from groq import Groq
from datetime import datetime, timedelta
import re
import os
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AGENTE MAGNÉTICO", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #FFF0F5 !important;
        color: #000000 !important;
        border: 1px solid #FFB6C1 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background-color: #FFB6C1 !important; color: #000000 !important;
        font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(255,105,180,0.2);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #FF85A1 !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #000000 !important; }
    p, span, label, div { color: #000000 !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #FFF5F7 0%, #FFF0F5 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FFD1DC; margin-bottom: 15px;
        color: #000000; box-shadow: 0 2px 12px rgba(255,105,180,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #2D0A1A 0%, #1A0010 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #FF69B4; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #FFD1DC !important; }

    .card-vermelho {
        background: linear-gradient(135deg, #FFF0F0 0%, #FFE8E8 100%);
        padding: 22px; border-radius: 16px;
        border: 2px solid #F44336; margin-bottom: 15px;
        white-space: pre-wrap;
    }

    .badge         { background: #FF69B4; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde   { background: #4CAF50; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-amarelo { background: #FFC107; color: #000  !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-vermelho{ background: #F44336; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #FFF0F5; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #FFD1DC; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #FF69B4 !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #FFF8FA; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #FFB6C1; }

    .salvar-box {
        background: linear-gradient(135deg, #FFF0F5, #FFE4EE);
        border: 2px solid #FF69B4; border-radius: 14px;
        padding: 16px 20px; margin-bottom: 16px;
        font-size: 0.9em; line-height: 1.7; color: #000;
    }

    .divider-rosa { border: none; height: 1px; background: linear-gradient(to right, transparent, #FFB6C1, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTÊNCIA LOCAL (JSON) ---
def gerar_json_sessao() -> str:
    """Serializa historico + biblioteca em JSON para download."""
    dados = {
        'usuario': st.session_state.usuario,
        'historico': st.session_state.historico,
        'biblioteca': st.session_state.biblioteca,
        'resumo_semanal': st.session_state.resumo_semanal,
        'resumo_gerado_em': st.session_state.resumo_gerado_em,
        'plano_conquista': st.session_state.plano_conquista,
        'plano_pessoa': st.session_state.plano_pessoa,
        'salvo_em': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    """Restaura sessão a partir do JSON carregado."""
    st.session_state.historico       = dados.get('historico', [])
    st.session_state.biblioteca      = dados.get('biblioteca', [])
    st.session_state.resumo_semanal  = dados.get('resumo_semanal', '')
    st.session_state.resumo_gerado_em= dados.get('resumo_gerado_em', None)
    st.session_state.plano_conquista = dados.get('plano_conquista', '')
    st.session_state.plano_pessoa    = dados.get('plano_pessoa', '')

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login",
    'usuario': "", 'api_key': "",
    'pagina': "Home",
    'modo_confianca': False,
    'modo_dark': False,
    'historico': [],
    'biblioteca': [],
    'roleplay_hist': [],
    'roleplay_ativo': False,
    'roleplay_perfil': '',
    'roleplay_situacao': '',
    'resumo_semanal': "",
    'resumo_gerado_em': None,
    'plano_conquista': "",
    'plano_pessoa': "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def mentor_milhao(prompt_usuario, sistema_extra="", historico_msgs=None):
    try:
        client = Groq(api_key=st.session_state.api_key)
        confianca = (
            "MODO CONFIANÇA ATIVADO: Respostas curtas, firmes, sem insegurança, mais diretas e dominantes."
            if st.session_state.modo_confianca
            else "Estilo natural, carismático e leve."
        )
        system_base = f"""Você é o Mentor do Agente Magnético. O usuário se chama {st.session_state.usuario}.
{confianca}
{sistema_extra}
Sempre que analisar ou gerar mensagens, siga esta estrutura:
1. 📊 LEITURA INVISÍVEL: Interesse (0-10), Energia (Fria/Quente), Posição (Passivo/Dominante).
2. 🎯 DIAGNÓSTICO: Curto e direto sobre o erro ou acerto.
3. 💬 RESPOSTA IDEAL: A sugestão pronta para copiar.
4. 🧠 MICRO-ENSINO: Por que isso funciona?
Sempre termine com: "👉 Quer que eu ajuste pro seu estilo?"
"""
        messages = [{"role": "system", "content": system_base}]
        if historico_msgs:
            messages.extend(historico_msgs)
        messages.append({"role": "user", "content": prompt_usuario})
        response = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na conexão: Verifique sua chave API. ({e})"

def extrair_interesse(texto_ia: str) -> int:
    matches = re.findall(r'Interesse[:\s]+(\d+)', texto_ia, re.IGNORECASE)
    return min(int(matches[0]), 10) if matches else 5

def salvar_historico(tipo: str, entrada: str, saida: str):
    st.session_state.historico.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo,
        'entrada': entrada[:80] + ('...' if len(entrada) > 80 else ''),
        'saida': saida,
        'nivel_interesse': extrair_interesse(saida),
        'favoritado': False,
    })

def calcular_stats():
    h = st.session_state.historico
    total = len(h)
    if total == 0:
        return 0, 0, 0
    media = sum(x['nivel_interesse'] for x in h) / total
    quentes = sum(1 for x in h if x['nivel_interesse'] >= 7)
    return total, round(media, 1), round((quentes / total) * 100)

def exportar_historico_txt() -> str:
    linhas = [f"AGENTE MAGNÉTICO — Histórico de {st.session_state.usuario}\n{'='*50}\n"]
    for item in st.session_state.historico:
        linhas.append(f"[{item['data']}] {item['tipo']} | Interesse: {item['nivel_interesse']}/10")
        linhas.append(f"Entrada: {item['entrada']}\nAnálise:\n{item['saida']}\n" + "-"*40)
    return "\n".join(linhas)

def banner_manual():
    manual_txt = """AGENTE MAGNÉTICO — Manual Completo de Funcionalidades
Versão Milhão 2026
======================================================

🏠 HOME — Painel Principal
Tela inicial com estatísticas em tempo real.

⚡ RESPOSTA RÁPIDA
Gera 3 opções de resposta imediata para qualquer mensagem recebida.

💬 TURBINAR MENSAGEM
A IA reescreve sua mensagem com gatilhos poderosos.

🧠 ANALISAR CONVERSA
Diagnóstico completo de uma conversa inteira.

🎭 ROLEPLAY — TREINE ANTES DE ENVIAR
Simule uma conversa com a pessoa antes de falar de verdade.

📚 BIBLIOTECA DE ABERTURAS
Banco pessoal de mensagens de abertura salvas.

📸 ANÁLISE DE PERFIL E BIO
Leitura de personalidade + abordagem ideal.

⚔️ COMPARAR DUAS CONVERSAS
Analise duas conversas lado a lado.

🗓️ PLANO DE CONQUISTA — 7 DIAS
Roteiro personalizado de ações para os próximos 7 dias.

🚩 DETECTOR DE RED FLAGS
Identifica sinais de desinteresse ou comportamento problemático.

📈 PROGRESSO
Histórico completo com filtros, favoritos e exportação.

📋 RESUMO SEMANAL
Relatório gerado por IA com análise da sua evolução.

© 2026 Agente Magnético — Treinador Social de Elite
"""
    st.download_button(
        label="📖 Baixar Manual Completo do Agente Magnético",
        data=manual_txt.encode("utf-8"),
        file_name="manual_agente_magnetico.txt",
        mime="text/plain",
        use_container_width=False
    )

# ── BARRA LATERAL DE SALVAR/CARREGAR ─────────────────────────
def barra_salvar():
    """Botão discreto para salvar dados no computador — aparece no topo do app."""
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    json_dados = gerar_json_sessao()
    total, media, _ = calcular_stats()

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#000;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador</strong> — assim você não perde nada se o servidor reiniciar.<br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises registradas · interesse médio {media}/10</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=json_dados,
            file_name=f"agente_magnetico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("<hr class='divider-rosa'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("💎 AGENTE MAGNÉTICO")
        st.markdown("**Seu Treinador Social de Elite com Inteligência Artificial**")
        st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#000;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A ASSOCIADOS DO QUIZ MAIS PRÊMIOS</strong><br>
        🔗 <a href="https://www.quizmaispremios.com.br" target="_blank"
        style="color:#FF69B4;font-weight:600;text-decoration:none;">www.quizmaispremios.com.br</a>
        </div>""", unsafe_allow_html=True)
        nome = st.text_input("Seu Nome:")
        chave = st.text_input("Sua Chave API da Groq:", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── UPLOADER: carrega dados se o servidor tiver zerado ──
        tem_dados = len(st.session_state.get('historico', [])) > 0 or len(st.session_state.get('biblioteca', [])) > 0
        if not tem_dados:
            st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#000;line-height:1.7;margin-bottom:10px;">
            📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None
            st.markdown(f"""<div style="background:#F0FFF4;border:1px solid #86EFAC;border-radius:10px;
            padding:10px 14px;font-size:0.84em;color:#000;margin-bottom:10px;">
            ✅ <strong>Seus dados estão no servidor.</strong> É só entrar normalmente.
            </div>""", unsafe_allow_html=True)

        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                nome_login = dados_login.get('usuario', '')
                st.success(f"✅ Dados de **{nome_login}** reconhecidos! Clique em Desbloquear para entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None
                arq_login = None
        else:
            dados_login = None

        if st.button("✨ DESBLOQUEAR ACESSO"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#FF69B4;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    # DARK MODE
    if st.session_state.modo_dark:
        st.markdown("""<style>
        .stApp { background-color: #1A0010 !important; }
        h1,h2,h3 { color: #FFD1DC !important; }
        p, span, label, div { color: #FFD1DC !important; }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #2D0A1A !important; color: #FFD1DC !important; }
        .stat-box { background: #2D0A1A !important; border-color: #FF69B4 !important; }
        </style>""", unsafe_allow_html=True)

    # BANNER DO MANUAL
    banner_manual()

    # ── BARRA DE SALVAR — SEMPRE VISÍVEL ─────────────────────
    barra_salvar()

    # NAVBAR
    cols = st.columns(12)
    paginas = [
        ("🏠", "Home"), ("⚡", "Rapida"), ("💬", "Turbinar"), ("🧠", "Analisar"),
        ("🎭", "Roleplay"), ("📚", "Biblioteca"), ("📸", "Perfil"), ("⚔️", "Comparar"),
        ("🗓️", "Plano"), ("🚩", "RedFlags"), ("📈", "Progresso"), ("📋", "Resumo"),
    ]
    nomes_paginas = {
        "Home": "Home", "Rapida": "Resposta Rápida", "Turbinar": "Turbinar Msg",
        "Analisar": "Analisar", "Roleplay": "Roleplay", "Biblioteca": "Biblioteca",
        "Perfil": "Análise de Perfil", "Comparar": "Comparar", "Plano": "Plano 7 Dias",
        "RedFlags": "Red Flags", "Progresso": "Progresso", "Resumo": "Resumo Semanal",
    }
    for i, (icone, pagina) in enumerate(paginas):
        if cols[i].button(icone, key=f"nav_{pagina}", help=nomes_paginas[pagina]):
            st.session_state.pagina = pagina
            st.rerun()

    st.markdown("<hr class='divider-rosa'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_m, col_d, col_r = st.columns([2, 1, 1, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 💫")
            st.markdown("<span class='badge'>Nível: MAGNÉTICO</span>", unsafe_allow_html=True)
        with col_m:
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.modo_confianca = st.toggle("🔥 Confiança", value=st.session_state.modo_confianca)
        with col_d:
            st.markdown("<br>", unsafe_allow_html=True)
            st.session_state.modo_dark = st.toggle("🌙 Dark", value=st.session_state.modo_dark)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        total, media, taxa = calcular_stats()
        favs = sum(1 for x in st.session_state.historico if x.get('favoritado'))

        # ── AVISO SE DADOS SUMIRAM — uploader direto na Home ──
        if total == 0 and len(st.session_state.biblioteca) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:14px 18px;margin-bottom:8px;color:#000;font-size:0.9em;line-height:1.7;">
            ⚠️ <strong>Seus dados não estão carregados.</strong><br>
            O servidor reiniciou e a memória foi apagada — isso é normal.<br>
            Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes e tudo volta como era. 👇
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader(
                "📥 Carregar meus dados salvos (.json):",
                type=["json"],
                key="upload_home"
            )
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    st.success("✅ Dados recuperados com sucesso! Sua sessão está completa.")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido. Use o .json gerado pelo Agente Magnético.")
            st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        dados_stats = [
            (total, "Análises feitas"), (media, "Interesse médio"),
            (f"{taxa}%", "Conversas quentes"), (len(st.session_state.biblioteca), "Aberturas salvas"),
            (favs, "Favoritos"),
        ]
        for col, (val, label) in zip([c1,c2,c3,c4,c5], dados_stats):
            col.markdown(f"<div class='stat-box'><div class='stat-numero'>{val}</div><div>{label}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Enquanto a maioria tenta adivinhar o que dizer... você vai saber exatamente como agir.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "⚡ Rápida": "Gera 3 respostas imediatas para qualquer mensagem recebida",
            "💬 Turbinar": "Melhora sua mensagem para a pessoa que você está conquistando",
            "🧠 Analisar": "Diagnóstico completo de uma conversa inteira",
            "🎭 Roleplay": "Simula a pessoa e você treina antes de enviar",
            "📚 Biblioteca": "Banco de aberturas salvas por vibe/situação",
            "📸 Perfil": "Lê a personalidade pelo perfil/bio/fotos",
            "⚔️ Comparar": "Analisa duas conversas lado a lado",
            "🗓️ Plano": "Roteiro de 7 dias personalizado para conquistar alguém",
            "🚩 Red Flags": "Detecta sinais de desinteresse ou comportamento problemático",
            "📈 Progresso": "Histórico completo com filtros, favoritos e exportação",
            "📋 Resumo": "Relatório semanal com análise da sua evolução",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico:
            st.markdown("### 🕐 Últimas Análises")
            for item in reversed(st.session_state.historico[-5:]):
                cor = "badge-verde" if item['nivel_interesse'] >= 7 else ("badge-amarelo" if item['nivel_interesse'] >= 4 else "badge-vermelho")
                fav = "⭐ " if item.get('favoritado') else ""
                st.markdown(
                    f"<div class='hist-item'><span class='{cor}'>{item['tipo']}</span> "
                    f"<span class='badge-amarelo'>Interesse: {item['nivel_interesse']}/10</span> "
                    f"{fav}<small style='color:#999'>{item['data']}</small><br>"
                    f"<small>{item['entrada']}</small></div>", unsafe_allow_html=True)

    # ========================
    # RESPOSTA RÁPIDA
    # ========================
    elif st.session_state.pagina == "Rapida":
        st.header("⚡ Resposta Rápida")
        st.markdown("Gera 3 opções de resposta imediata para qualquer mensagem recebida.")

        situacao = st.selectbox("📍 Qual é a situação?", [
            "Primeiro contato", "Depois de um tempo sem falar",
            "Após uma briga ou esfriamento", "Marcando um encontro",
            "Flerte avançado", "Ela/ele deixou no visto", "Resposta curta/seca",
        ])
        sinais_extras = st.text_input("🔍 Sinais fora do chat (opcional):",
            placeholder="ex: viu meu story, demorou 3h pra responder, curtiu foto antiga...")
        recebida = st.text_area("📩 O que ela/ele te mandou?", height=120)

        if st.button("⚡ GERAR 3 OPÇÕES IMEDIATAS"):
            if recebida.strip():
                with st.spinner("Lendo subtexto..."):
                    sinais = f"\nSinais fora do chat: {sinais_extras}" if sinais_extras.strip() else ""
                    prompt = (
                        f"Situação: {situacao}.{sinais}\n"
                        f"Mensagem recebida: '{recebida}'\n"
                        f"Gere 3 opções de resposta rápida, cada uma com vibe diferente (divertida, provocante, direta). "
                        f"Para cada opção: mostre a resposta pronta e em 1 linha o efeito que causa."
                    )
                    res = mentor_milhao(prompt)
                    salvar_historico("⚡ Rápida", recebida, res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole a mensagem recebida antes de continuar.")

    # ========================
    # TURBINAR MENSAGEM
    # ========================
    elif st.session_state.pagina == "Turbinar":
        st.header("💬 Turbinar Mensagem")
        st.markdown("Você tem uma ideia do que quer dizer — a IA reescreve com gatilhos poderosos.")

        nome_destino = st.text_input("👤 Para quem é a mensagem?",
            placeholder="ex: Ana, o cara do app, a menina do gym...")
        contexto_destino = st.text_input("📌 O que você sabe sobre essa pessoa? (opcional)",
            placeholder="ex: extrovertida, gosta de humor, responde rápido...")
        situacao = st.selectbox("📍 Situação:", [
            "Primeiro contato", "Depois de um tempo sem falar",
            "Após uma briga ou esfriamento", "Marcando um encontro", "Flerte avançado",
        ])
        vibe = st.select_slider("Qual vibe você quer criar?",
            options=["Divertida", "Leve", "Provocante", "Profunda", "Dominante"])
        minha_msg = st.text_area("✏️ Sua ideia inicial (o que você quer dizer):", height=120)
        salvar_bib = st.checkbox("📚 Salvar resultado na Biblioteca de Aberturas")

        if st.button("🚀 TURBINAR PARA O MODO MILHÃO"):
            if minha_msg.strip():
                with st.spinner("Aplicando gatilhos..."):
                    contexto_pessoa = f" Contexto sobre {nome_destino}: {contexto_destino}." if contexto_destino.strip() else ""
                    prompt = (
                        f"Situação: {situacao}.\n"
                        f"Destinatário da mensagem: {nome_destino or 'a pessoa de interesse'}.{contexto_pessoa}\n"
                        f"O usuário quer dizer para essa pessoa: '{minha_msg}'\n"
                        f"Turbine essa mensagem para a vibe '{vibe}', levando em conta quem é o destinatário.\n"
                        f"Mostre: 1) O PROBLEMA da versão original. 2) A NOVA VERSÃO turbinada (pronta pra enviar). "
                        f"3) Por que a nova versão funciona melhor com essa pessoa nessa situação."
                    )
                    res = mentor_milhao(prompt)
                    salvar_historico("💬 Turbinar", minha_msg, res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                    if salvar_bib:
                        st.session_state.biblioteca.append({
                            'vibe': vibe, 'situacao': situacao,
                            'texto': minha_msg, 'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")
            else:
                st.warning("Escreva sua mensagem antes de continuar.")

    # ========================
    # ANALISAR CONVERSA
    # ========================
    elif st.session_state.pagina == "Analisar":
        st.header("🧠 Análise Social Profissional")

        situacao = st.selectbox("📍 Contexto da conversa:", [
            "Primeiro contato", "Conversa em andamento",
            "Depois de um tempo sem falar", "Pós-encontro",
            "Após uma briga", "Flerte avançado",
        ])
        sinais_extras = st.text_area("🔍 Sinais fora do chat (opcional):",
            placeholder="ex: ela viu meu story mas não respondeu, curtiu uma foto antiga...", height=80)
        chat_log = st.text_area("💬 Cole os últimos balões da conversa:", height=200)

        if st.button("🔬 DIAGNÓSTICO COMPLETO"):
            if chat_log.strip():
                with st.spinner("Analisando interesse e energia..."):
                    sinais = f"\nSinais fora do chat: {sinais_extras}" if sinais_extras.strip() else ""
                    prompt = (
                        f"Situação: {situacao}.{sinais}\n"
                        f"Conversa:\n{chat_log}\n\n"
                        f"Análise completa: nível de interesse real, energia emocional, "
                        f"o que a pessoa está sinalizando e qual o próximo movimento ideal."
                    )
                    res = mentor_milhao(prompt)
                    salvar_historico("🧠 Análise", chat_log[:80], res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole a conversa antes de continuar.")

    # ========================
    # ROLEPLAY
    # ========================
    elif st.session_state.pagina == "Roleplay":
        st.header("🎭 Roleplay — Treine Antes de Enviar")
        st.markdown("A IA simula a **pessoa que você quer conquistar**. Treine aqui antes de falar de verdade.")

        if not st.session_state.roleplay_ativo:
            st.markdown("#### Configure a simulação")
            col_a, col_b = st.columns(2)
            with col_a:
                nome_simulado = st.text_input("Nome ou apelido da pessoa:",
                    placeholder="ex: Ana, Pedro, A menina do gym...")
            with col_b:
                situacao_rp = st.selectbox("Situação inicial:", [
                    "Primeiro contato no Direct",
                    "Retomando conversa após tempo sem falar",
                    "Pós-match no app de relacionamento",
                    "Após se conhecerem pessoalmente",
                    "Pós-primeiro encontro",
                ])
            perfil = st.text_area(
                "Descreva o perfil e a personalidade dessa pessoa:",
                placeholder="ex: mulher de 28 anos, independente, irônica, gosta de viagens...",
                height=120,
            )
            st.info("💡 Dica: descreva como essa pessoa costuma se comunicar, o que ela gosta, como ela reage.")

            if st.button("🎬 INICIAR SIMULAÇÃO"):
                if perfil.strip():
                    st.session_state.roleplay_perfil = perfil
                    st.session_state.roleplay_nome = nome_simulado or "a pessoa"
                    st.session_state.roleplay_situacao = situacao_rp
                    st.session_state.roleplay_hist = []
                    st.session_state.roleplay_ativo = True
                    st.rerun()
                else:
                    st.warning("Descreva a personalidade da pessoa antes de começar.")
        else:
            nome_sim = st.session_state.get('roleplay_nome', 'a pessoa')
            st.markdown(
                f"<div class='card'><b>🎭 Simulando:</b> {nome_sim}<br>"
                f"<small>Situação: {st.session_state.get('roleplay_situacao','')}</small><br>"
                f"<small>Perfil: {st.session_state.get('roleplay_perfil','')[:120]}...</small></div>",
                unsafe_allow_html=True
            )

            for msg in st.session_state.roleplay_hist:
                if msg['role'] == 'user':
                    st.markdown(f"**Você:** {msg['content']}")
                else:
                    st.markdown(f"<div class='card'><b>{nome_sim}:</b> {msg['content']}</div>", unsafe_allow_html=True)

            user_msg = st.text_input(
                "Sua mensagem:",
                placeholder="Digite o que você enviaria de verdade...",
                key=f"rp_input_{len(st.session_state.roleplay_hist)}"
            )
            col_env, col_fim, col_reset = st.columns([3, 1, 1])

            with col_env:
                if st.button("📤 ENVIAR"):
                    if user_msg.strip():
                        st.session_state.roleplay_hist.append({"role": "user", "content": user_msg})
                        with st.spinner(f"{nome_sim} digitando..."):
                            system_rp = (
                                f"Você está interpretando {nome_sim} em uma simulação de conversa para treinamento social. "
                                f"Perfil detalhado: {st.session_state.roleplay_perfil}. "
                                f"Situação: {st.session_state.roleplay_situacao}. "
                                f"REGRAS: Responda APENAS como {nome_sim} responderia, de forma realista. "
                                f"Nunca quebre o personagem. Nunca dê conselhos."
                            )
                            try:
                                client = Groq(api_key=st.session_state.api_key)
                                msgs = [{"role": "system", "content": system_rp}]
                                msgs.extend(st.session_state.roleplay_hist)
                                resp = client.chat.completions.create(
                                    messages=msgs, model="llama-3.3-70b-versatile",
                                ).choices[0].message.content
                            except Exception as e:
                                resp = f"Erro: {e}"
                            st.session_state.roleplay_hist.append({"role": "assistant", "content": resp})
                            st.rerun()
                    else:
                        st.warning("Digite sua mensagem.")

            with col_fim:
                if st.button("🏁 AVALIAR"):
                    if len(st.session_state.roleplay_hist) >= 2:
                        with st.spinner("Avaliando sua performance..."):
                            conversa_texto = "\n".join(
                                f"{'Você' if m['role']=='user' else nome_sim}: {m['content']}"
                                for m in st.session_state.roleplay_hist
                            )
                            avaliacao = mentor_milhao(
                                f"Avalie a performance do usuário nesta simulação com {nome_sim}:\n{conversa_texto}\n\n"
                                f"Perfil da pessoa simulada: {st.session_state.roleplay_perfil}\n\n"
                                f"Dê: nota geral (0-10), 3 acertos, 3 erros e o que fazer diferente.",
                                sistema_extra="Avalie um treino de roleplay social. Seja honesto e construtivo."
                            )
                            st.markdown(f"<div class='card-dark'>{avaliacao}</div>", unsafe_allow_html=True)
                            st.session_state.roleplay_ativo = False
                    else:
                        st.warning("Troque pelo menos 1 mensagem antes de avaliar.")

            with col_reset:
                if st.button("🔄 NOVA SIM"):
                    st.session_state.roleplay_ativo = False
                    st.session_state.roleplay_hist = []
                    st.rerun()

    # ========================
    # BIBLIOTECA DE ABERTURAS
    # ========================
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca de Aberturas")
        st.markdown("Gere e salve suas melhores aberturas por vibe e situação.")

        col_g, col_v = st.columns(2)
        with col_g:
            vibe_bib = st.selectbox("Vibe:", ["Divertida", "Misteriosa", "Direta", "Curiosa", "Provocante"])
        with col_v:
            sit_bib = st.selectbox("Situação:", ["Primeiro contato", "Retomada", "Pós-encontro", "Match novo"])

        if st.button("✨ GERAR 5 ABERTURAS"):
            with st.spinner("Criando arsenal..."):
                prompt = (
                    f"Gere 5 mensagens de abertura para '{sit_bib}' com vibe '{vibe_bib}'. "
                    f"Cada abertura deve ser curta (máx 2 linhas), original e magnética. "
                    f"Numere de 1 a 5. Só as aberturas e uma palavra sobre o efeito de cada."
                )
                res = mentor_milhao(prompt, sistema_extra="Especialista em primeiros contatos sociais magnéticos.")
                st.session_state['bib_temp'] = {'vibe': vibe_bib, 'situacao': sit_bib, 'texto': res}
                st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

        if 'bib_temp' in st.session_state and st.session_state['bib_temp']:
            if st.button("💾 SALVAR NA BIBLIOTECA"):
                item = st.session_state['bib_temp'].copy()
                item['data'] = datetime.now().strftime('%d/%m %H:%M')
                st.session_state.biblioteca.append(item)
                st.session_state['bib_temp'] = None
                st.success("✅ Salvo!")
                st.rerun()

        if st.session_state.biblioteca:
            st.markdown("---")
            st.markdown("### 📖 Suas Aberturas Salvas")
            for i, item in enumerate(reversed(st.session_state.biblioteca)):
                with st.expander(f"[{item['vibe']}] {item['situacao']} — {item['data']}"):
                    st.markdown(item['texto'])
                    if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                        st.session_state.biblioteca.pop(len(st.session_state.biblioteca) - 1 - i)
                        st.rerun()
        else:
            st.info("Biblioteca vazia. Gere aberturas acima e salve as melhores!")

    # ========================
    # ANÁLISE DE PERFIL/BIO
    # ========================
    elif st.session_state.pagina == "Perfil":
        st.header("📸 Análise de Perfil e Bio")
        st.markdown("Descreva o perfil e a IA faz leitura de personalidade + abordagem ideal.")

        nome_pessoa = st.text_input("Nome ou apelido (opcional):", placeholder="ex: Ana, O cara do gym...")
        bio = st.text_area("📝 Bio/descrição do perfil:",
            placeholder="ex: 'Vivendo um capítulo de cada vez ✈️🍷' | Médica | SP", height=80)
        fotos = st.text_area("📷 Descrição das fotos/posts recentes:",
            placeholder="ex: foto viajando sozinha, selfie academia, legenda filosófica...", height=100)
        comportamento = st.text_area("👁️ Comportamentos observados (opcional):",
            placeholder="ex: posta stories toda noite, segue poucos perfis...", height=80)

        if st.button("🔍 ANALISAR PERFIL COMPLETO"):
            if bio.strip() or fotos.strip():
                with st.spinner("Fazendo leitura invisível..."):
                    prompt = (
                        f"Analise o perfil desta pessoa{(' (' + nome_pessoa + ')') if nome_pessoa else ''}:\n"
                        f"Bio: {bio}\nFotos/posts: {fotos}\nComportamentos: {comportamento}\n\n"
                        f"Forneça:\n1. 🧬 PERFIL DE PERSONALIDADE\n2. ⚡ GATILHOS que funcionam\n"
                        f"3. 🚫 O QUE EVITAR\n4. 💬 ABERTURA IDEAL personalizada\n5. 🎯 ESTRATÉGIA DE CONQUISTA"
                    )
                    res = mentor_milhao(prompt, sistema_extra="Especialista em leitura de perfis sociais.")
                    salvar_historico("📸 Perfil", bio[:60], res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha pelo menos a bio ou descrição das fotos.")

    # ========================
    # COMPARAR DUAS CONVERSAS
    # ========================
    elif st.session_state.pagina == "Comparar":
        st.header("⚔️ Comparar Duas Conversas")
        st.markdown("Cole duas conversas e veja qual tem mais potencial — e o que fazer em cada uma.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Conversa A")
            nome_a = st.text_input("Nome/apelido (A):", placeholder="ex: Ana", key="nome_a")
            conversa_a = st.text_area("Cole a Conversa A:", height=200, key="conv_a")
        with col_b:
            st.markdown("### Conversa B")
            nome_b = st.text_input("Nome/apelido (B):", placeholder="ex: Carol", key="nome_b")
            conversa_b = st.text_area("Cole a Conversa B:", height=200, key="conv_b")

        if st.button("⚔️ COMPARAR AGORA"):
            if conversa_a.strip() and conversa_b.strip():
                with st.spinner("Analisando as duas conversas..."):
                    prompt = (
                        f"Compare estas duas conversas:\n\n"
                        f"CONVERSA A ({nome_a or 'Pessoa A'}):\n{conversa_a}\n\n"
                        f"CONVERSA B ({nome_b or 'Pessoa B'}):\n{conversa_b}\n\n"
                        f"Para cada conversa: nível de interesse (0-10), energia emocional, próximo movimento ideal.\n"
                        f"Ao final: qual das duas tem mais potencial e por quê."
                    )
                    res = mentor_milhao(prompt, sistema_extra="Analista especializado em dinâmicas de relacionamento.")
                    salvar_historico("⚔️ Comparar", f"{nome_a or 'A'} vs {nome_b or 'B'}", res)
                    st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole as duas conversas antes de comparar.")

    # ========================
    # PLANO DE CONQUISTA 7 DIAS
    # ========================
    elif st.session_state.pagina == "Plano":
        st.header("🗓️ Plano de Conquista — 7 Dias")
        st.markdown("Roteiro personalizado de ações para os próximos 7 dias.")

        nome_alvo = st.text_input("Nome ou apelido da pessoa:", placeholder="ex: Ana")
        contexto_alvo = st.text_area("O que você sabe sobre ela/ele e o contexto?",
            placeholder="ex: se conheceram na academia, já trocaram mensagens...", height=100)
        estagio = st.selectbox("Em que estágio vocês estão?", [
            "Nunca conversamos — vou abordar pela primeira vez",
            "Já conversamos pouco, mas a conversa esfriou",
            "Estamos em contato, mas não avança",
            "Já nos vimos pessoalmente uma vez",
            "Temos conexão mas falta dar o próximo passo",
        ])

        if st.button("🗓️ GERAR PLANO DE 7 DIAS"):
            if contexto_alvo.strip():
                with st.spinner("Montando seu roteiro personalizado..."):
                    prompt = (
                        f"Monte um plano de conquista de 7 dias para {st.session_state.usuario}.\n"
                        f"Pessoa: {nome_alvo or 'pessoa de interesse'}. Contexto: {contexto_alvo}. Estágio: {estagio}\n\n"
                        f"Para cada dia (Dia 1 ao 7):\n"
                        f"- 🎯 OBJETIVO DO DIA\n- 📲 AÇÃO ESPECÍFICA\n- ⏰ MELHOR HORÁRIO\n- ⚠️ O QUE EVITAR\n\n"
                        f"Seja prático. Ações concretas, nada de teoria."
                    )
                    res = mentor_milhao(prompt, sistema_extra="Coach especializado em estratégias de relacionamento.")
                    st.session_state.plano_conquista = res
                    st.session_state.plano_pessoa = nome_alvo or "Pessoa de interesse"
                    st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva o contexto antes de gerar o plano.")

        if st.session_state.plano_conquista:
            txt = f"PLANO DE CONQUISTA — {st.session_state.plano_pessoa}\n{'='*40}\n{st.session_state.plano_conquista}"
            st.download_button("⬇️ BAIXAR PLANO EM TXT", data=txt,
                file_name=f"plano_{st.session_state.plano_pessoa.lower().replace(' ','_')}.txt", mime="text/plain")

    # ========================
    # DETECTOR DE RED FLAGS
    # ========================
    elif st.session_state.pagina == "RedFlags":
        st.header("🚩 Detector de Red Flags")
        st.markdown("A IA identifica sinais de desinteresse, jogo mental ou comportamento problemático.")

        chat_rf = st.text_area("💬 Cole a conversa aqui:", height=220)
        comportamentos_rf = st.text_area("👁️ Comportamentos fora do chat (opcional):",
            placeholder="ex: some por dias, responde só quando quer...", height=80)

        if st.button("🚩 ANALISAR RED FLAGS"):
            if chat_rf.strip():
                with st.spinner("Vasculhando sinais de alerta..."):
                    prompt = (
                        f"Analise em busca de red flags:\nConversa:\n{chat_rf}\n"
                        f"Comportamentos externos: {comportamentos_rf}\n\n"
                        f"Identifique:\n1. 🚩 RED FLAGS (cite trechos)\n2. 🟡 SINAIS AMBÍGUOS\n"
                        f"3. ✅ SINAIS POSITIVOS\n4. 🧠 DIAGNÓSTICO GERAL\n5. 💡 RECOMENDAÇÃO\n\n"
                        f"Seja honesto mesmo que difícil de ouvir."
                    )
                    res = mentor_milhao(prompt, sistema_extra="Analista de padrões de comportamento. Seja direto e honesto.")
                    salvar_historico("🚩 Red Flags", chat_rf[:80], res)
                    tem_flags = "red flag" in res.lower() or "🚩" in res
                    card = "card-vermelho" if tem_flags else "card"
                    st.markdown(f"<div class='{card}'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Cole a conversa antes de analisar.")

    # ========================
    # PROGRESSO
    # ========================
    elif st.session_state.pagina == "Progresso":
        st.header("📈 Seu Progresso Real")

        total, media, taxa = calcular_stats()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Total de análises</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-box'><div class='stat-numero'>{media}/10</div><div>Interesse médio</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Conversas quentes</div></div>", unsafe_allow_html=True)

        if st.session_state.historico:
            st.markdown("<br>", unsafe_allow_html=True)
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos", "⚡ Rápida", "💬 Turbinar", "🧠 Análise",
                    "📸 Perfil", "⚔️ Comparar", "🚩 Red Flags", "⭐ Favoritos"])
            with col_ex:
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button("⬇️ Exportar TXT", data=exportar_historico_txt(),
                    file_name="historico_agente_magnetico.txt", mime="text/plain")

            for i, item in enumerate(reversed(st.session_state.historico)):
                if filtro == "⭐ Favoritos" and not item.get('favoritado'):
                    continue
                if filtro not in ["Todos", "⭐ Favoritos"] and item['tipo'] != filtro:
                    continue
                idx_real = len(st.session_state.historico) - 1 - i
                fav_label = "★ Desfavoritar" if item.get('favoritado') else "☆ Favoritar"
                with st.expander(f"{'⭐' if item.get('favoritado') else ''} {item['tipo']} — {item['data']} | Interesse: {item['nivel_interesse']}/10"):
                    st.markdown(f"**Entrada:** {item['entrada']}")
                    st.markdown(f"<div class='card'>{item['saida']}</div>", unsafe_allow_html=True)
                    col_fav, col_del = st.columns([3, 1])
                    with col_fav:
                        if st.button(fav_label, key=f"fav_{i}"):
                            st.session_state.historico[idx_real]['favoritado'] = not item.get('favoritado', False)
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico.pop(idx_real)
                            st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico = []
                st.rerun()
        else:
            st.info("Nenhuma análise ainda. Use as ferramentas para começar a construir seu histórico!")

    # ========================
    # RESUMO SEMANAL
    # ========================
    elif st.session_state.pagina == "Resumo":
        st.header("📋 Resumo Semanal Inteligente")

        total, media, taxa = calcular_stats()
        if total == 0:
            st.info("Você ainda não tem análises suficientes. Use as ferramentas primeiro!")
        else:
            st.markdown(f"<div class='card'>📊 Baseado em <b>{total} análises</b> | Interesse médio: <b>{media}/10</b> | Conversas quentes: <b>{taxa}%</b></div>", unsafe_allow_html=True)

            hoje = datetime.now().strftime('%d/%m/%Y')
            ja_gerou = st.session_state.resumo_semanal and st.session_state.resumo_gerado_em == hoje

            if ja_gerou:
                st.markdown("### 📄 Seu Resumo de Hoje")
                st.markdown(f"<div class='card-dark'>{st.session_state.resumo_semanal}</div>", unsafe_allow_html=True)
                st.download_button("⬇️ Baixar Resumo TXT",
                    data=f"RESUMO SEMANAL — {st.session_state.usuario}\n{hoje}\n\n{st.session_state.resumo_semanal}",
                    file_name="resumo_semanal.txt", mime="text/plain")
                if st.button("🔄 Gerar Novo Resumo"):
                    st.session_state.resumo_semanal = ""
                    st.rerun()
            else:
                if st.button("✨ GERAR RESUMO SEMANAL"):
                    with st.spinner("Analisando sua evolução..."):
                        tipos = [x['tipo'] for x in st.session_state.historico]
                        prompt = (
                            f"Resumo semanal para {st.session_state.usuario}:\n"
                            f"- Análises: {total} | Tipos: {', '.join(set(tipos))}\n"
                            f"- Interesse médio: {media}/10 | Conversas quentes: {taxa}%\n\n"
                            f"1. 🏆 CONQUISTAS DA SEMANA\n2. ⚠️ PADRÃO DE ERRO MAIS COMUM\n"
                            f"3. 📈 EVOLUÇÃO vs semana anterior\n4. 🎯 FOCO PARA A PRÓXIMA SEMANA\n5. 💡 DICA PERSONALIZADA"
                        )
                        resumo = mentor_milhao(prompt, sistema_extra="Coach de habilidades sociais. Seja encorajador mas honesto.")
                        st.session_state.resumo_semanal = resumo
                        st.session_state.resumo_gerado_em = hoje
                        st.markdown(f"<div class='card-dark'>{resumo}</div>", unsafe_allow_html=True)
                        st.download_button("⬇️ Baixar Resumo TXT",
                            data=f"RESUMO SEMANAL — {st.session_state.usuario}\n{hoje}\n\n{resumo}",
                            file_name="resumo_semanal.txt", mime="text/plain")

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Agente Magnético — Treinador Social de Elite"
    "</div>", unsafe_allow_html=True
)
