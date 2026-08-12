import streamlit as st
from groq import Groq
from datetime import datetime, date
import json
import random

st.set_page_config(page_title="CONEXA IA", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FAFAFA; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background-color: #FFF0F5 !important;
        color: #1A1A2E !important;
        border: 1px solid #FFB6C1 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #FF69B4, #FF85A1) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(255,105,180,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #E05590, #FF69B4) !important; transform: translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color: white !important; }

    .stApp h1, .stApp h2, .stApp h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }

    .card { background:linear-gradient(135deg,#FFF5F7,#FFF0F5); padding:22px; border-radius:16px; border:1px solid #FFD1DC; margin-bottom:15px; white-space:pre-wrap; box-shadow:0 2px 12px rgba(255,105,180,0.08); }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#2D0A1A,#1A0010); padding:22px; border-radius:16px; border:1px solid #FF69B4; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong, .stApp .card-dark em { color:#FFD1DC !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:22px; border-radius:16px; border:1px solid #86EFAC; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div, .stApp .card-green strong { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:22px; border-radius:16px; border:1px solid #93C5FD; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:22px; border-radius:16px; border:2px solid #FECACA; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:pre-wrap; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .painel-conexa { background:linear-gradient(135deg,#2D0A1A,#1A0010); border:2px solid #FF69B4; border-radius:20px; padding:24px; margin-bottom:20px; }
    .stApp .painel-conexa, .stApp .painel-conexa p, .stApp .painel-conexa span, .stApp .painel-conexa div, .stApp .painel-conexa strong { color:#FFD1DC !important; }

    .faixa-box { border-radius:14px; padding:18px 20px; margin-bottom:10px; }
    .stApp .faixa-box, .stApp .faixa-box p, .stApp .faixa-box span, .stApp .faixa-box div, .stApp .faixa-box strong { color:#1A1A2E !important; }

    .chat-user { background:#FFF0F5; border:1px solid #FFB6C1; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#FFF5F7; border:1px solid #FFD1DC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #FFB6C1; border-radius:16px; padding:20px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div, .stApp .avaliacao-box strong { color:#1A1A2E !important; }

    .carta-box { background:linear-gradient(135deg,#FFF0F5,#FFE8F0); border:2px solid #FF69B4; border-radius:16px; padding:18px 20px; margin-bottom:12px; }
    .stApp .carta-box, .stApp .carta-box p, .stApp .carta-box span, .stApp .carta-box div, .stApp .carta-box strong { color:#1A1A2E !important; }

    .stat-box { background:#FFF0F5; border-radius:12px; padding:18px; text-align:center; border:1px solid #FFD1DC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#FF69B4 !important; font-family:'Playfair Display',serif; }

    .hist-item { background:#FFF8FA; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #FFB6C1; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .conquista-item { background:#FFFBEB; border:1px solid #FCD34D; border-radius:10px; padding:12px 16px; margin-bottom:8px; text-align:center; }
    .stApp .conquista-item, .stApp .conquista-item p, .stApp .conquista-item span, .stApp .conquista-item div { color:#78350F !important; }

    .badge { background:#FF69B4; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#D97706; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#7C3AED; color:white !important; padding:4px 14px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .perfil-btn>button { background:linear-gradient(135deg,#FF69B4,#FF85A1) !important; color:white !important; font-weight:700 !important; border-radius:12px !important; height:3em !important; }
    .perfil-btn>button, .perfil-btn>button p, .perfil-btn>button span { color:white !important; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#FFB6C1,transparent); margin:20px 0; }

    .radar-verde { background:#F0FDF4; border-left:4px solid #22C55E; border-radius:0 10px 10px 0; padding:12px 16px; margin-bottom:8px; }
    .stApp .radar-verde, .stApp .radar-verde p, .stApp .radar-verde span, .stApp .radar-verde div { color:#14532D !important; }
    .radar-amarelo { background:#FFFBEB; border-left:4px solid #F59E0B; border-radius:0 10px 10px 0; padding:12px 16px; margin-bottom:8px; }
    .stApp .radar-amarelo, .stApp .radar-amarelo p, .stApp .radar-amarelo span, .stApp .radar-amarelo div { color:#78350F !important; }
    .radar-vermelho { background:#FFF5F5; border-left:4px solid #EF4444; border-radius:0 10px 10px 0; padding:12px 16px; margin-bottom:8px; }
    .stApp .radar-vermelho, .stApp .radar-vermelho p, .stApp .radar-vermelho span, .stApp .radar-vermelho div { color:#7F1D1D !important; }
    </style>
""", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache():
    return {"perfis": {}}
_cache = get_cache()

# ─── FAIXAS DA ARTE DA LÁBIA ───
FAIXAS = [
    (1, "⚪ Faixa Branca",  "🌱 O Invisível",    "Recebe ajuda direta. Personagem facilitador."),
    (2, "🟡 Faixa Amarela", "🟢 O Quebra-Gelo",  "Aprende a captar ganchos. Ajuda reduzida."),
    (3, "🟠 Faixa Laranja", "🟡 O Interessante", "Lida com silêncio e improvisação. Sem ajuda direta."),
    (4, "🟢 Faixa Verde",   "🟠 O Inabalável",   "Provocações e pressão social."),
    (5, "🔵 Faixa Azul",    "🔴 O Desafiador",   "Respostas frias e pouca reciprocidade."),
    (6, "🟤 Faixa Marrom",  "⚫ O Sedutor",       "Oscilação e imprevisibilidade."),
    (7, "⚫ Faixa Preta",   "👑 Don Juan",        "Conversa livre. Zero rede de proteção."),
]

CONQUISTAS_DEF = [
    ("primeira_analise",   "🔍 Primeira Análise",        "Realizou sua primeira análise de conversa"),
    ("primeiro_treino",    "🎭 Primeiro Treino",          "Completou o primeiro roleplay"),
    ("cinco_analises",     "📊 5 Conversas",              "5 conversas analisadas"),
    ("dez_mensagens",      "✨ 10 Mensagens",             "10 mensagens aprimoradas"),
    ("primeira_carta",     "🃏 Primeira Carta",           "Usou a Carta na Manga pela primeira vez"),
    ("cinco_cartas",       "🎴 5 Cartas",                 "5 Cartas na Manga utilizadas"),
    ("plano_7dias",        "🗓️ Plano 7 Dias",            "Concluiu o plano de 7 dias"),
    ("primeiro_passo",     "🌱 Primeiro Passo",           "Concluiu a primeira conversa na Arte da Lábia"),
    ("cacador_ganchos",    "🧩 Caçador de Ganchos",      "Aproveitou 10 ganchos em conversas"),
    ("resposta_relampago", "⚡ Resposta Relâmpago",       "Respondeu 10 situações dentro do tempo"),
    ("sem_roteiro",        "🧠 Sem Roteiro",              "Completou uma conversa sem ajuda"),
    ("inabalavel",         "🛡️ Inabalável",              "Superou 5 provocações com naturalidade"),
    ("resgatador",         "🔥 Resgatador",               "Recuperou 5 conversas esfriando"),
    ("camaleao",           "🦎 Camaleão",                 "Adaptou-se a 10 personalidades diferentes"),
    ("don_juan",           "👑 Don Juan",                 "Concluiu o Nível 7 — Don Juan"),
]

CHAVES_SALVAR = [
    'usuario', 'historico', 'biblioteca', 'resumo_semanal',
    'plano_conquista', 'plano_pessoa',
    'conversas_analisadas', 'mensagens_aprimoradas', 'analises_realizadas',
    'cartas_usadas', 'treinos_realizados', 'favoritos_total',
    'clareza', 'naturalidade', 'reciprocidade', 'confianca', 'escuta',
    'conquistas', 'faixa_atual', 'historico_personagens',
    'labia_nivel', 'labia_chat', 'labia_personagem', 'labia_falha_anterior',
    'objetivos_usuario',
]

def gerar_json():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_cache(u):
    return _cache["perfis"].get(u)

def salvar_historico(tipo, tema, conteudo):
    st.session_state.historico.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'tema': tema, 'conteudo': conteudo,
    })

def verificar_conquistas():
    c = st.session_state.get('conquistas', [])
    novas = []
    checks = [
        ("primeira_analise",   st.session_state.analises_realizadas >= 1),
        ("primeiro_treino",    st.session_state.treinos_realizados >= 1),
        ("cinco_analises",     st.session_state.conversas_analisadas >= 5),
        ("dez_mensagens",      st.session_state.mensagens_aprimoradas >= 10),
        ("primeira_carta",     st.session_state.cartas_usadas >= 1),
        ("cinco_cartas",       st.session_state.cartas_usadas >= 5),
    ]
    for chave, cond in checks:
        if cond and chave not in c:
            c.append(chave); novas.append(chave)
    st.session_state['conquistas'] = c
    return novas

defaults = {
    'etapa': 'Login', 'usuario': '', 'api_key': '', 'pagina': 'Home',
    'historico': [], 'biblioteca': [], 'resumo_semanal': '',
    'plano_conquista': '', 'plano_pessoa': '',
    'conversas_analisadas': 0, 'mensagens_aprimoradas': 0,
    'analises_realizadas': 0, 'cartas_usadas': 0,
    'treinos_realizados': 0, 'favoritos_total': 0,
    'clareza': 0, 'naturalidade': 0, 'reciprocidade': 0,
    'confianca': 0, 'escuta': 0,
    'conquistas': [], 'faixa_atual': 1,
    'historico_personagens': [],
    'labia_nivel': 1, 'labia_chat': [], 'labia_personagem': None,
    'labia_falha_anterior': None, 'objetivos_usuario': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── IA ───
def conexa_ia(prompt, system_extra=""):
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = (
            "Você é o CONEXA IA — sistema de inteligência para comunicação e conexões humanas. "
            "Você ajuda pessoas a entender conversas, melhorar mensagens e desenvolver habilidades sociais. "
            "NUNCA afirme intenções ou sentimentos que não podem ser conhecidos. "
            "Trabalhe apenas com padrões observáveis. "
            "Seja direto, prático e baseado no contexto fornecido. "
            "Português do Brasil. " + system_extra
        )
        resp = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="llama-3.3-70b-versatile",
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def barra_salvar():
    salvar_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    faixa_info = FAIXAS[min(st.session_state.faixa_atual-1, 6)]
    col_i, col_b = st.columns([4,2])
    with col_i:
        st.markdown(
            f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#FF69B4;font-size:0.88em;'>"
            f"{faixa_info[0]} {faixa_info[2]} · "
            f"{st.session_state.conversas_analisadas} análises · "
            f"{st.session_state.cartas_usadas} cartas usadas"
            f"</span></div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("💾 SALVAR DADOS (.json)", data=gerar_json(),
            file_name=f"conexa_{nome_u}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🧠 CONEXA IA")
        st.markdown("**Inteligência para conversas, comunicação e conexões.**")
        st.markdown("*Entenda melhor. Comunique-se melhor. Saiba o que fazer a seguir.*")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""<div style="background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
        padding:12px 16px;margin-bottom:16px;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href='https://quizcompremios.com.br/' target='_blank'
        style='color:#FF69B4;font-weight:600;text-decoration:none;'>quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        perfis = perfis_salvos()
        if perfis:
            chave_r = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for np in perfis:
                dp = carregar_cache(np)
                faixa_p = dp.get('faixa_atual', 1) if dp else 1
                fi = FAIXAS[min(faixa_p-1, 6)]
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(f"🧠 {np}  ·  {fi[0]} {fi[2]}", key=f"perfil_{np}", use_container_width=True):
                    if not chave_r.strip():
                        st.warning("Cole sua chave API acima.")
                    else:
                        st.session_state.usuario = np
                        st.session_state.api_key = chave_r
                        carregar_json(dp)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # PRIMEIRA EXPERIÊNCIA
        if not perfis:
            st.markdown("#### Vamos configurar seu Conexa")
            st.markdown("*Como você quer melhorar sua comunicação?*")
            objetivos = st.multiselect("Escolha seus objetivos:", [
                "☐ Fazer novas amizades",
                "☐ Conversar com mais confiança",
                "☐ Melhorar minha comunicação",
                "☐ Treinar conversas",
                "☐ Aprender a interpretar contextos",
            ])
            st.session_state.objetivos_usuario = objetivos

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            arq = st.file_uploader("Restaurar dados (.json):", type=["json"], key="upload_login")
        else:
            arq = None

        dados_login = None
        if arq is not None:
            try:
                dados_login = json.load(arq)
                st.success(f"✅ Dados de **{dados_login.get('usuario','')}** reconhecidos!")
            except Exception:
                st.error("Arquivo inválido.")

        if st.button("🧠 ENTRAR NO CONEXA"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")
        st.markdown("🔑 Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#FF69B4;'>console.groq.com/keys</a>", unsafe_allow_html=True)


# ============================================================
# APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    # NAVBAR linha 1
    cols1 = st.columns(7)
    nav1 = [("🏠","Home"),("⚡","Rapida"),("🃏","Carta"),("💬","Turbinar"),("🧠","Analisar"),("🎭","Roleplay"),("🎭2","Labia")]
    lb1 = {"Home":"Dashboard","Rapida":"Resposta Rápida","Carta":"Carta na Manga",
           "Turbinar":"Turbinar Mensagem","Analisar":"Raio-X da Conversa",
           "Roleplay":"Simulador de Conversa","Labia":"🎭 A Arte da Lábia"}
    for i,(ic,pg) in enumerate(nav1):
        ch = list(lb1.keys())[i]
        if cols1[i].button(ic, key=f"nav1_{ch}", help=lb1[ch]):
            st.session_state.pagina = ch; st.rerun()

    # NAVBAR linha 2
    cols2 = st.columns(7)
    nav2 = [("📚","Biblioteca"),("📸","Perfil"),("⚔️","Comparar"),("🗓️","Plano"),("📈","Progresso"),("📋","Resumo"),("🏆","Conquistas")]
    lb2 = {"Biblioteca":"Biblioteca Inteligente","Perfil":"Leitor de Perfil",
           "Comparar":"Comparar Conversas","Plano":"Plano 7 Dias",
           "Progresso":"Minha Evolução","Resumo":"Relatório Semanal","Conquistas":"Conquistas"}
    for i,(ic,pg) in enumerate(nav2):
        ch = list(lb2.keys())[i]
        if cols2[i].button(ic, key=f"nav2_{ch}", help=lb2[ch]):
            st.session_state.pagina = ch; st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # HOME — DASHBOARD
    # ──────────────────────────────────────────
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🧠 Olá, {st.session_state.usuario}!")
            faixa = FAIXAS[min(st.session_state.faixa_atual-1, 6)]
            st.markdown(f"<span class='badge-roxo'>{faixa[0]} {faixa[2]}</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()): del st.session_state[k]
                st.rerun()

        if not st.session_state.historico and not st.session_state.conversas_analisadas:
            arq_h = st.file_uploader("Restaurar dados (.json):", type=["json"], key="upload_home")
            if arq_h:
                try:
                    d = json.load(arq_h); carregar_json(d); salvar_cache(st.session_state.usuario)
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")

        # PAINEL PRINCIPAL
        st.markdown(f"""
        <div class='painel-conexa'>
            <div style='font-size:0.82em;opacity:0.7;letter-spacing:2px;margin-bottom:12px;'>🧠 CONEXA IA — PAINEL DE INTELIGÊNCIA</div>
            <div style='font-size:1.1em;opacity:0.6;margin-bottom:16px;'>A IA que ajuda você a entender a conversa — e saber o próximo passo.</div>
            <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>⚡ NÍVEL ATUAL</div>
                    <div style='font-size:1.3em;font-weight:700;'>{faixa[2]}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>💬 CONVERSAS</div>
                    <div style='font-size:1.6em;font-weight:700;'>{st.session_state.conversas_analisadas}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>🃏 CARTAS USADAS</div>
                    <div style='font-size:1.6em;font-weight:700;'>{st.session_state.cartas_usadas}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # DASHBOARD MÉTRICAS
        st.markdown("### 📊 Seu Desempenho")
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.conversas_analisadas}</div><div>Conversas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.mensagens_aprimoradas}</div><div>Turbinadas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.analises_realizadas}</div><div>Análises</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.cartas_usadas}</div><div>Cartas</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.treinos_realizados}</div><div>Treinos</div></div>", unsafe_allow_html=True)
        c6.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.favoritos_total}</div><div>Favoritos</div></div>", unsafe_allow_html=True)

        # EVOLUÇÃO
        st.markdown("### 📈 Evolução")
        metricas = [
            ("Clareza", st.session_state.clareza),
            ("Naturalidade", st.session_state.naturalidade),
            ("Reciprocidade", st.session_state.reciprocidade),
            ("Confiança", st.session_state.confianca),
            ("Escuta", st.session_state.escuta),
        ]
        for nome_m, val in metricas:
            cor = "#22C55E" if val >= 7 else ("#F59E0B" if val >= 4 else "#EF4444")
            st.markdown(f"""
            <div style='margin-bottom:10px;'>
                <div style='display:flex;justify-content:space-between;font-size:0.88em;font-weight:600;color:#1A1A2E;'>
                    <span>{nome_m}</span><span style='color:{cor};'>{val}/10</span>
                </div>
                <div style='background:#F1F5F9;border-radius:999px;height:8px;overflow:hidden;margin-top:4px;'>
                    <div style='height:100%;border-radius:999px;background:{cor};width:{val*10}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # GUIA DE ABAS
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "⚡ Resposta Rápida": "Cole uma mensagem e receba 3 opções de resposta com estratégia",
            "🃏 Carta na Manga": "Quando você não sabe o que dizer — a IA encontra uma nova possibilidade",
            "💬 Turbinar": "Melhore qualquer mensagem — clareza, tom e naturalidade",
            "🧠 Raio-X": "Análise completa de uma conversa — fluidez, reciprocidade e oportunidades",
            "🎭 Roleplay": "Simule conversas e receba avaliação detalhada",
            "🎭 Arte da Lábia": "Treinamento adaptativo em 7 faixas — do iniciante ao Don Juan",
            "📚 Biblioteca": "Suas melhores respostas organizadas por categoria",
            "📸 Leitor de Perfil": "Analisa informações públicas e sugere assuntos de conversa",
            "⚔️ Comparar": "Compare duas conversas e descubra qual tem melhor dinâmica",
            "🗓️ Plano 7 Dias": "Plano de desenvolvimento de comunicação personalizado",
            "📈 Progresso": "Sua evolução ao longo do tempo em todas as métricas",
            "📋 Relatório": "Resumo semanal gerado automaticamente pela IA",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — <span style='color:#4B5563;'>{desc}</span>", unsafe_allow_html=True)

        if st.session_state.historico:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Atividades")
            for item in reversed(st.session_state.historico[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['tema'][:80]}</small></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # RESPOSTA RÁPIDA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Rapida":
        st.header("⚡ Resposta Inteligente")
        st.markdown("Cole a mensagem recebida e receba 3 opções estratégicas de resposta.")

        msg_recebida = st.text_area("💬 Mensagem recebida:", height=100, placeholder="Cole a mensagem aqui...")
        col1, col2 = st.columns(2)
        with col1:
            quem = st.selectbox("Quem é essa pessoa?", ["Colega","Amigo","Pessoa nova","Interesse romântico","Familiar","Outro"])
        with col2:
            objetivo = st.selectbox("O que você quer fazer?", ["Continuar a conversa","Responder de forma natural","Esclarecer algo","Iniciar um assunto novo","Dar um passo à frente"])

        contexto_extra = st.text_input("Contexto adicional (opcional):", placeholder="ex: acabamos de nos conhecer, faz 2 dias que não falamos...")

        if st.button("⚡ ANALISAR E RESPONDER"):
            if msg_recebida.strip():
                with st.spinner("Analisando o contexto..."):
                    prompt = (
                        f"Analise esta mensagem e gere 3 opções estratégicas de resposta.\n"
                        f"Mensagem recebida: '{msg_recebida}'\n"
                        f"Quem enviou: {quem}. Objetivo: {objetivo}. Contexto: {contexto_extra or 'não informado'}.\n\n"
                        f"REGRAS:\n"
                        f"- NÃO afirme intenções ou sentimentos que não podem ser conhecidos\n"
                        f"- Trabalhe apenas com padrões observáveis na mensagem\n"
                        f"- Respostas devem soar naturais, não robóticas\n\n"
                        f"FORMATO:\n\n"
                        f"📊 LEITURA DO CONTEXTO:\n[O que é observável nessa mensagem — tom, abertura, oportunidades]\n\n"
                        f"💬 OPÇÃO 1 — NATURAL\n[resposta]\nPor quê: [explicação curta]\n\n"
                        f"💡 OPÇÃO 2 — INTERESSANTE\n[resposta]\nPor quê: [explicação curta]\n\n"
                        f"🎯 OPÇÃO 3 — DIRETA\n[resposta]\nPor quê: [explicação curta]\n\n"
                        f"⭐ RECOMENDAÇÃO:\n[qual das 3 é mais adequada para esse contexto e por quê]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.analises_realizadas += 1
                    st.session_state.conversas_analisadas += 1
                    verificar_conquistas()
                    salvar_historico("Resposta Rápida", msg_recebida[:60], res)
                    st.session_state['rapida_temp'] = res
            else:
                st.warning("Cole a mensagem antes de analisar.")

        if st.session_state.get('rapida_temp'):
            st.markdown(f"<div class='card'>{st.session_state['rapida_temp']}</div>", unsafe_allow_html=True)
            col_cp, col_fv, col_sv = st.columns(3)
            with col_cp:
                st.download_button("📋 Copiar (.txt)", data=st.session_state['rapida_temp'], file_name="resposta.txt", mime="text/plain", use_container_width=True)
            with col_fv:
                if st.button("⭐ Favoritar", key="fav_rapida", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Respostas','conteudo':st.session_state['rapida_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1
                    st.success("⭐ Salvo na biblioteca!")
            with col_sv:
                if st.button("🃏 Carta na Manga", key="carta_rapida", use_container_width=True):
                    st.session_state.pagina = "Carta"; st.rerun()

    # ──────────────────────────────────────────
    # CARTA NA MANGA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Carta":
        st.header("🃏 Carta na Manga")
        st.markdown("Quando você não sabe mais o que dizer — a IA encontra uma nova possibilidade.")

        conversa_carta = st.text_area("💬 Cole a conversa completa:", height=180, placeholder="Cole aqui toda a conversa...")
        contexto_carta = st.text_input("Contexto (opcional):", placeholder="ex: amigo, interesse romântico, colega de trabalho...")

        if st.button("🃏 GERAR CARTAS NA MANGA"):
            if conversa_carta.strip():
                with st.spinner("A IA está procurando novas possibilidades..."):
                    prompt = (
                        f"Analise esta conversa e gere 5 cartas na manga — novas possibilidades de interação.\n"
                        f"Conversa:\n{conversa_carta}\n"
                        f"Contexto: {contexto_carta or 'não informado'}\n\n"
                        f"REGRAS:\n"
                        f"- Trabalhe APENAS com o que está na conversa\n"
                        f"- NÃO fabrique fatos, interesses ou sentimentos\n"
                        f"- Cada carta deve ser genuinamente diferente das outras\n\n"
                        f"FORMATO:\n\n"
                        f"🃏 CARTA #01 — RESGATAR UM ASSUNTO\n"
                        f"[mensagem sugerida]\n"
                        f"Por que essa carta: [explicação]\n\n"
                        f"🃏 CARTA #02 — MUDAR O RUMO\n"
                        f"[mensagem sugerida]\n"
                        f"Por que essa carta: [explicação]\n\n"
                        f"🃏 CARTA #03 — PERGUNTA-CHAVE\n"
                        f"[pergunta aberta]\n"
                        f"Por que essa carta: [explicação]\n\n"
                        f"🃏 CARTA #04 — LEVEZA\n"
                        f"[abordagem descontraída]\n"
                        f"Por que essa carta: [explicação]\n\n"
                        f"🛡️ CARTA #05 — DAR ESPAÇO\n"
                        f"[avaliação de quando não insistir é o melhor caminho]\n\n"
                        f"⭐ CARTA RECOMENDADA: [número e por quê é a melhor agora]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.cartas_usadas += 1
                    verificar_conquistas()
                    salvar_historico("Carta na Manga", conversa_carta[:60], res)
                    st.session_state['carta_temp'] = res
            else:
                st.warning("Cole a conversa antes de gerar.")

        if st.session_state.get('carta_temp'):
            st.markdown(f"<div class='carta-box'>{st.session_state['carta_temp']}</div>", unsafe_allow_html=True)
            col_cp, col_fv = st.columns(2)
            with col_cp:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['carta_temp'], file_name="carta_manga.txt", mime="text/plain", use_container_width=True)
            with col_fv:
                if st.button("⭐ Favoritar cartas", key="fav_carta", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Cartas na Manga','conteudo':st.session_state['carta_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1
                    st.success("⭐ Salvo!")

    # ──────────────────────────────────────────
    # TURBINAR
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Turbinar":
        st.header("💬 Turbinar Mensagem")
        st.markdown("Cole sua mensagem e a IA a aprimora — clareza, tom e naturalidade.")

        msg_orig = st.text_area("✍️ Sua mensagem:", height=100, placeholder="Cole sua mensagem aqui...")
        col1, col2 = st.columns(2)
        with col1:
            estilo = st.selectbox("Estilo desejado:", ["Natural","Leve","Confiante","Divertido","Direto","Empático"])
        with col2:
            contexto_turb = st.text_input("Contexto:", placeholder="ex: primeira mensagem, resposta após sumiço...")

        if st.button("💬 TURBINAR MENSAGEM"):
            if msg_orig.strip():
                with st.spinner("Aprimorando..."):
                    prompt = (
                        f"Avalie e melhore esta mensagem.\n"
                        f"Mensagem original: '{msg_orig}'\n"
                        f"Estilo desejado: {estilo}. Contexto: {contexto_turb or 'não informado'}.\n\n"
                        f"FORMATO:\n\n"
                        f"📊 AVALIAÇÃO DA MENSAGEM ORIGINAL:\n"
                        f"• Clareza: [nota]/10\n"
                        f"• Naturalidade: [nota]/10\n"
                        f"• Tom: [análise]\n"
                        f"• Reciprocidade: [abre espaço para o outro?]\n"
                        f"• Pressão: [há pressão excessiva?]\n\n"
                        f"❌ ANTES:\n{msg_orig}\n\n"
                        f"✅ DEPOIS — ESTILO {estilo.upper()}:\n[mensagem aprimorada]\n\n"
                        f"🧠 POR QUE MELHOROU:\n[explicação objetiva das mudanças]\n\n"
                        f"💡 VARIAÇÃO ALTERNATIVA:\n[outra versão em estilo diferente]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.mensagens_aprimoradas += 1
                    verificar_conquistas()
                    salvar_historico("Turbinar", msg_orig[:60], res)
                    st.session_state['turb_temp'] = res
            else:
                st.warning("Cole a mensagem antes de turbinar.")

        if st.session_state.get('turb_temp'):
            st.markdown(f"<div class='card'>{st.session_state['turb_temp']}</div>", unsafe_allow_html=True)
            if st.button("⭐ Favoritar", key="fav_turb"):
                st.session_state.biblioteca.append({'categoria':'Mensagens Turbinadas','conteudo':st.session_state['turb_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                st.session_state.favoritos_total += 1
                st.success("⭐ Salvo!")

    # ──────────────────────────────────────────
    # RAIO-X DA CONVERSA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Analisar":
        st.header("🧠 Raio-X da Conversa")
        st.markdown("Análise completa — fluidez, reciprocidade, qualidade e oportunidades.")

        conversa_rx = st.text_area("💬 Cole a conversa completa:", height=200, placeholder="Cole a conversa aqui...")

        if st.button("🧠 ANALISAR CONVERSA"):
            if conversa_rx.strip():
                with st.spinner("Fazendo o raio-X..."):
                    prompt = (
                        f"Faça uma análise completa desta conversa.\n\n"
                        f"IMPORTANTE: NÃO afirme sentimentos ou intenções. Apresente APENAS padrões observáveis.\n\n"
                        f"Conversa:\n{conversa_rx}\n\n"
                        f"FORMATO:\n\n"
                        f"📊 01 — FLUIDEZ\n"
                        f"Status: [🟢 Fluindo / 🟡 Perdendo ritmo / 🔴 Travada]\n"
                        f"[análise observável]\n\n"
                        f"🤝 02 — RECIPROCIDADE\n"
                        f"[Quem inicia, tamanho das respostas, perguntas feitas, equilíbrio — sem afirmar sentimentos]\n\n"
                        f"💬 03 — QUALIDADE DA COMUNICAÇÃO\n"
                        f"• Clareza: [nota]/10\n• Naturalidade: [nota]/10\n• Escuta: [nota]/10\n"
                        f"• Perguntas: [quantidade e qualidade]\n• Pressão: [há?]\n\n"
                        f"🎯 04 — ASSUNTOS\n"
                        f"✅ Que funcionaram: [lista]\n"
                        f"💡 Que podem ser explorados: [lista]\n"
                        f"📉 Que perderam força: [lista]\n\n"
                        f"🚦 05 — RADAR\n"
                        f"[🟢 / 🟡 / 🔴 com justificativa baseada em padrões observáveis]\n\n"
                        f"🎯 06 — PRÓXIMO PASSO RECOMENDADO:\n[ação concreta]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.analises_realizadas += 1
                    st.session_state.conversas_analisadas += 1
                    verificar_conquistas()
                    salvar_historico("Raio-X", conversa_rx[:60], res)
                    st.session_state['rx_temp'] = res
            else:
                st.warning("Cole a conversa antes de analisar.")

        if st.session_state.get('rx_temp'):
            st.markdown(f"<div class='card'>{st.session_state['rx_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_fv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['rx_temp'], file_name="raio_x.txt", mime="text/plain", use_container_width=True)
            with col_fv:
                if st.button("⭐ Favoritar", key="fav_rx", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Análises','conteudo':st.session_state['rx_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1; st.success("⭐ Salvo!")

    # ──────────────────────────────────────────
    # ROLEPLAY
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Roleplay":
        st.header("🎭 Simulador de Conversa")
        st.markdown("Treine antes de enviar. A IA simula uma pessoa real em um cenário.")

        if 'roleplay_chat' not in st.session_state:
            st.session_state.roleplay_chat = []
        if 'roleplay_ativo' not in st.session_state:
            st.session_state.roleplay_ativo = False
        if 'roleplay_key' not in st.session_state:
            st.session_state.roleplay_key = 0

        if not st.session_state.roleplay_ativo:
            cenario = st.selectbox("Escolha o cenário:", [
                "🤝 Conhecer alguém novo","👥 Fazer amizade","🏫 Conversar com colega",
                "💼 Networking","🗣️ Conversa difícil","😬 Situação que causa nervosismo"])
            nivel_role = st.selectbox("Dificuldade:", ["Fácil — pessoa receptiva","Médio — pessoa neutra","Difícil — pessoa reservada"])

            if st.button("🎭 INICIAR SIMULAÇÃO"):
                with st.spinner("Criando o cenário..."):
                    system_role = (
                        f"Você é uma pessoa num simulador de conversa para treino de comunicação. "
                        f"Cenário: {cenario}. Dificuldade: {nivel_role}. "
                        f"Seja realista — não force perguntas, não salve a conversa artificialmente. "
                        f"Mantenha personalidade consistente. Responda como essa pessoa responderia, "
                        f"não como um assistente. Primeira mensagem: apresente o cenário brevemente e comece a interação."
                    )
                    resp = conexa_ia("Inicie o cenário com uma fala natural da personagem.", system_role)
                    st.session_state.roleplay_chat = [{"role":"assistant","content":resp,"system":system_role}]
                    st.session_state.roleplay_ativo = True
                    st.session_state.roleplay_cenario = cenario
                    st.session_state.roleplay_system = system_role
                    st.rerun()
        else:
            st.markdown(f"**Cenário:** {st.session_state.get('roleplay_cenario','')}")
            for msg in st.session_state.roleplay_chat:
                if msg['role'] == 'user':
                    st.markdown(f"<div class='chat-user'><b style='color:#FF69B4;'>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-persona'><b style='color:#1D4ED8;'>🎭 Personagem:</b> {msg['content']}</div>", unsafe_allow_html=True)

            msg_role = st.text_input("Sua resposta:", key=f"role_input_{st.session_state.roleplay_key}", placeholder="O que você diria?")

            col_e, col_f = st.columns([4,1])
            with col_e:
                if st.button("📤 ENVIAR"):
                    if msg_role.strip():
                        historico_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.roleplay_chat]
                        with st.spinner("..."):
                            try:
                                client = Groq(api_key=st.session_state.api_key)
                                msgs = [{"role":"system","content":st.session_state.roleplay_system}] + historico_msgs + [{"role":"user","content":msg_role}]
                                resp = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile")
                                resp_txt = resp.choices[0].message.content
                            except Exception as e:
                                resp_txt = f"⚠️ Erro: {e}"
                        st.session_state.roleplay_chat.append({"role":"user","content":msg_role})
                        st.session_state.roleplay_chat.append({"role":"assistant","content":resp_txt})
                        st.session_state.roleplay_key += 1
                        st.rerun()
            with col_f:
                if st.button("🏁 Finalizar"):
                    with st.spinner("Avaliando sua performance..."):
                        hist_txt = "\n".join(f"{'Usuário' if m['role']=='user' else 'Personagem'}: {m['content']}" for m in st.session_state.roleplay_chat)
                        prompt_aval = (
                            f"Avalie a performance deste usuário na simulação de conversa.\n"
                            f"Cenário: {st.session_state.get('roleplay_cenario','')}\n\n"
                            f"Conversa:\n{hist_txt}\n\n"
                            f"FORMATO:\n\n"
                            f"🏆 AVALIAÇÃO DA SIMULAÇÃO\n\n"
                            f"| Competência | Nota |\n|---|---|\n"
                            f"| 🗣️ Naturalidade | [X]/10 |\n"
                            f"| 👂 Escuta | [X]/10 |\n"
                            f"| ❓ Qualidade das perguntas | [X]/10 |\n"
                            f"| 🔄 Adaptação | [X]/10 |\n"
                            f"| 🤝 Reciprocidade | [X]/10 |\n\n"
                            f"⭐ NOTA GERAL: [X]/10\n\n"
                            f"🟢 O QUE VOCÊ FEZ BEM:\n[feedback específico]\n\n"
                            f"🟡 O QUE PODE MELHORAR:\n[feedback específico]\n\n"
                            f"🎯 PRÓXIMO DESAFIO:\n[o que trabalhar na próxima simulação]"
                        )
                        aval = conexa_ia(prompt_aval)
                        st.session_state.treinos_realizados += 1
                        verificar_conquistas()
                        salvar_historico("Roleplay", st.session_state.get('roleplay_cenario',''), aval)
                        st.session_state['role_aval'] = aval
                        st.session_state.roleplay_ativo = False
                        st.session_state.roleplay_chat = []
                        st.rerun()

        if st.session_state.get('role_aval'):
            st.markdown(f"<div class='avaliacao-box'>{st.session_state['role_aval']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar avaliação (.txt)", data=st.session_state['role_aval'], file_name="avaliacao_roleplay.txt", mime="text/plain")


    # ──────────────────────────────────────────
    # A ARTE DA LÁBIA — SISTEMA COMPLETO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Labia":
        st.header("🎭 A Arte da Lábia")
        st.markdown("*Aprenda a conversar sem travar, encantar sem esforço e seduzir com confiança.*")
        st.markdown("*Aqui você não responde perguntas. Você conhece pessoas.*")

        nivel = st.session_state.labia_nivel
        faixa_atual = FAIXAS[min(nivel-1, 6)]

        # Tabs internas
        tab_j, tab_t, tab_h = st.tabs(["🥋 Sua Jornada","💬 Treinar Agora","📜 Histórico"])

        with tab_j:
            st.markdown("### 🥋 Sua Jornada nas Faixas")
            for i, (n, faixa, titulo, desc) in enumerate(FAIXAS):
                desbloqueada = n <= nivel
                cor = "#FF69B4" if n == nivel else ("#22C55E" if n < nivel else "#E5E7EB")
                status = "✅ Concluída" if n < nivel else ("🔥 Atual" if n == nivel else "🔒 Bloqueada")
                st.markdown(f"""
                <div style='background:#FFFFFF;border:2px solid {cor};border-radius:14px;
                padding:14px 18px;margin-bottom:10px;'>
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div>
                            <span style='font-weight:700;color:#1A1A2E;font-size:1em;'>{faixa} {titulo}</span><br>
                            <span style='font-size:0.85em;color:#4B5563;'>{desc}</span>
                        </div>
                        <span style='font-size:0.82em;font-weight:600;color:{cor};'>{status}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""<div class='card-blue'>
            👑 <strong>Don Juan não significa conquistar qualquer pessoa.</strong><br>
            Significa dominar a própria comunicação. Saber iniciar. Saber ouvir. Saber improvisar.
            Saber quando continuar — e quando deixar ir.
            </div>""", unsafe_allow_html=True)

        with tab_t:
            st.markdown(f"### {faixa_atual[0]} {faixa_atual[2]} — Nível {nivel}")
            st.markdown(f"*{faixa_atual[3]}*")

            # Configurações do desafio por nível
            configs_nivel = {
                1: {"ajuda":"TOTAL — dicas e respostas sugeridas","dificuldade":"Facilitador","turnos_min":5,"tempo":None},
                2: {"ajuda":"PISTA — sem resposta direta","dificuldade":"Acessível","turnos_min":7,"tempo":None},
                3: {"ajuda":"NENHUMA — silêncio real","dificuldade":"Neutro","turnos_min":8,"tempo":12},
                4: {"ajuda":"NENHUMA — provocações","dificuldade":"Testador","turnos_min":8,"tempo":8},
                5: {"ajuda":"NENHUMA — respostas frias","dificuldade":"Reservado","turnos_min":10,"tempo":8},
                6: {"ajuda":"NENHUMA — imprevisível","dificuldade":"Oscilante","turnos_min":10,"tempo":7},
                7: {"ajuda":"ZERO — sem proteção","dificuldade":"Extremamente seletivo","turnos_min":12,"tempo":6},
            }
            cfg = configs_nivel[nivel]

            if not st.session_state.labia_personagem:
                # Gerar novo personagem
                hist_p = st.session_state.get('historico_personagens', [])
                hist_txt = ", ".join(hist_p[-5:]) if hist_p else "nenhum"

                col_c, col_g = st.columns([3,1])
                with col_c:
                    st.markdown(f"**Ajuda disponível:** {cfg['ajuda']}")
                    st.markdown(f"**Tipo de personagem:** {cfg['dificuldade']}")

                    # Mostrar erro anterior se houver
                    if st.session_state.labia_falha_anterior:
                        st.markdown(f"<div class='card-yellow'>⚠️ <strong>No desafio anterior você falhou em:</strong> {st.session_state.labia_falha_anterior}<br>O próximo personagem vai testar exatamente essa habilidade.</div>", unsafe_allow_html=True)

                with col_g:
                    if st.button("🎲 GERAR PERSONAGEM", use_container_width=True):
                        with st.spinner("Criando personagem..."):
                            falha_txt = f"O usuário falhou anteriormente em: {st.session_state.labia_falha_anterior}. Crie situações que testem especificamente essa habilidade." if st.session_state.labia_falha_anterior else ""

                            prompt_persona = (
                                f"Crie um personagem fictício adulto para simulação de conversa no nível {nivel}/7.\n"
                                f"Dificuldade: {cfg['dificuldade']}. {falha_txt}\n"
                                f"Personagens já usados: {hist_txt}. NÃO repita nome, profissão ou cenário.\n\n"
                                f"NÍVEL {nivel} — características:\n"
                                + {
                                    1: "Personagem aberto, receptivo, facilita a conversa naturalmente. Cenário casual simples.",
                                    2: "Personagem acessível mas não carrega a conversa. Fornece ganchos mas não os reforça.",
                                    3: "Personagem neutro. Pode ficar em silêncio após respostas curtas do usuário.",
                                    4: "Personagem que faz provocações leves e plausíveis. Testa segurança e humor.",
                                    5: "Personagem reservado. Respostas curtas. Pouca reciprocidade. Não oferece ganchos.",
                                    6: "Personagem imprevisível — pode estar aberto e fechar de repente. Ironia e mudanças de energia.",
                                    7: "Personagem extremamente seletivo, sociável, recebe muita atenção. Pouco tempo de paciência.",
                                }[nivel] + "\n\n"
                                f"RETORNE UM JSON com:\n"
                                f'{{"nome":"","idade_aprox":"","profissao":"","cenario":"","personalidade":"","interesses":[],"estilo_fala":"","nivel_abertura":"","primeira_fala":""}}'
                            )
                            persona_txt = conexa_ia(prompt_persona)
                            # Extrai JSON
                            try:
                                import re as re_mod
                                json_match = re_mod.search(r'\{[^{}]+\}', persona_txt, re_mod.DOTALL)
                                persona = json.loads(json_match.group(0)) if json_match else {"nome":"Alex","cenario":"Numa cafeteria","primeira_fala":"Oi, desculpa o barulho aqui hoje.","personalidade":"Reservado","interesses":["música"],"estilo_fala":"Direto","nivel_abertura":"Baixo","profissao":"Designer","idade_aprox":"28"}
                            except:
                                persona = {"nome":"Alex","cenario":"Numa cafeteria","primeira_fala":"Oi, desculpa o barulho aqui hoje.","personalidade":"Reservado","interesses":["música"],"estilo_fala":"Direto","nivel_abertura":"Baixo","profissao":"Designer","idade_aprox":"28"}

                            st.session_state.labia_personagem = persona
                            st.session_state.labia_chat = []
                            # Registra no histórico anti-repetição
                            hist_p.append(f"{persona.get('nome','')} / {persona.get('profissao','')} / {persona.get('cenario','')}")
                            st.session_state['historico_personagens'] = hist_p
                            st.rerun()

            else:
                persona = st.session_state.labia_personagem
                chat = st.session_state.labia_chat

                # Info do personagem (sem revelar a ficha completa)
                st.markdown(f"""
                <div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:12px;padding:12px 18px;margin-bottom:16px;'>
                    <strong style='color:#1A1A2E;'>📍 {persona.get('cenario','')}</strong><br>
                    <span style='font-size:0.85em;color:#4B5563;'>Você está prestes a iniciar uma conversa. O personagem possui personalidade própria — descubra conversando.</span>
                </div>
                """, unsafe_allow_html=True)

                # Iniciar conversa se chat vazio
                if not chat:
                    primeira_fala = persona.get('primeira_fala', 'Oi.')
                    chat.append({"role":"assistant","content":primeira_fala})
                    st.session_state.labia_chat = chat

                # Exibir chat
                turno_usuario = sum(1 for m in chat if m['role']=='user')
                for msg in chat:
                    if msg['role'] == 'user':
                        st.markdown(f"<div class='chat-user'><b style='color:#FF69B4;'>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-persona'><b style='color:#1D4ED8;'>🎭 {persona.get('nome','?')}:</b> {msg['content']}</div>", unsafe_allow_html=True)

                # Ajuda contextual por nível
                if nivel == 1 and turno_usuario == 0:
                    ultima_persona = [m['content'] for m in chat if m['role']=='assistant'][-1] if chat else ""
                    st.markdown(f"<div class='card-green'>💡 <strong>Dica (Nível 1):</strong> {persona.get('nome','Ela')} acabou de falar. Responda de forma natural — você pode comentar o que foi dito ou fazer uma pergunta relacionada.</div>", unsafe_allow_html=True)
                elif nivel == 2 and turno_usuario < 2:
                    st.markdown("<div class='card-yellow'>💡 <strong>Pista:</strong> Existe um detalhe na última fala que pode virar assunto.</div>", unsafe_allow_html=True)

                # Input e botões
                msg_labia = st.text_input("Sua resposta:", key=f"labia_input_{len(chat)}", placeholder="O que você diz?")

                col_e, col_fim, col_aband = st.columns([3,1,1])
                with col_e:
                    if st.button("📤 ENVIAR", key="labia_enviar"):
                        if msg_labia.strip():
                            # Sistema do personagem
                            system_labia = (
                                f"Você é {persona.get('nome','?')}, {persona.get('idade_aprox','adulto')}, {persona.get('profissao','')}. "
                                f"Personalidade: {persona.get('personalidade','')}. "
                                f"Interesses: {', '.join(persona.get('interesses',[]))}. "
                                f"Estilo de fala: {persona.get('estilo_fala','')}. "
                                f"Nível de abertura: {persona.get('nivel_abertura','')}. "
                                f"Cenário: {persona.get('cenario','')}.\n\n"
                                f"REGRAS ABSOLUTAS:\n"
                                f"- Responda como essa pessoa real responderia, não como assistente\n"
                                f"- NÃO termine toda fala com pergunta — pessoas reais não fazem isso\n"
                                f"- Mantenha personalidade CONSISTENTE com o nível {nivel}\n"
                                f"- Nível {nivel}: {cfg['dificuldade']} — {'facilite naturalmente' if nivel<=2 else 'não salve a conversa artificialmente'}\n"
                                f"- A conversa deve parecer real, não um script\n"
                                f"- Lembre de TODO o histórico da conversa"
                            )
                            historico_msgs = [{"role":m["role"],"content":m["content"]} for m in chat]
                            with st.spinner("..."):
                                try:
                                    client = Groq(api_key=st.session_state.api_key)
                                    msgs = [{"role":"system","content":system_labia}] + historico_msgs + [{"role":"user","content":msg_labia}]
                                    resp_l = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile")
                                    resp_txt_l = resp_l.choices[0].message.content
                                except Exception as e:
                                    resp_txt_l = f"⚠️ Erro: {e}"
                            chat.append({"role":"user","content":msg_labia})
                            chat.append({"role":"assistant","content":resp_txt_l})
                            st.session_state.labia_chat = chat
                            st.rerun()

                with col_fim:
                    if st.button("🏁 Finalizar", key="labia_fim"):
                        if len(chat) >= cfg['turnos_min'] * 2:
                            with st.spinner("Avaliando..."):
                                hist_labia_txt = "\n".join(f"{'Usuário' if m['role']=='user' else persona.get('nome','?')}: {m['content']}" for m in chat)
                                criterios_nivel = {
                                    1: "5+ turnos, sem respostas monossilábicas, iniciou 1 assunto, aproveitou 1 informação do personagem",
                                    2: "7+ turnos, aproveitou 2+ ganchos, 1 pergunta aberta, sem depender de ajuda",
                                    3: "8-10 turnos, 80% das respostas desenvolvidas, 3+ ganchos aproveitados, sem pedir dica",
                                    4: "8+ turnos, respondeu provocações com naturalidade, manteve humor, sem ficar defensivo",
                                    5: "10+ turnos, recuperou 3 momentos de baixa reciprocidade, soube quando não insistir",
                                    6: "10+ turnos, adaptou-se a mudanças de energia, não seguiu formato de entrevista",
                                    7: "12+ turnos, sustentou conversa interessante sem rede de proteção alguma",
                                }
                                prompt_aval_l = (
                                    f"Avalie a performance nesta simulação de Arte da Lábia.\n"
                                    f"Nível: {nivel}/7 — {faixa_atual[2]}.\n"
                                    f"Personagem: {persona.get('nome','')} — {persona.get('personalidade','')}.\n"
                                    f"Critérios de aprovação nível {nivel}: {criterios_nivel[nivel]}\n\n"
                                    f"Conversa:\n{hist_labia_txt}\n\n"
                                    f"FORMATO:\n\n"
                                    f"🏆 AVALIAÇÃO — NÍVEL {nivel}\n\n"
                                    f"| Competência | Nota |\n|---|---|\n"
                                    f"| 🗣️ Naturalidade | [X]/10 |\n"
                                    f"| 🧠 Raciocínio | [X]/10 |\n"
                                    f"| ⚡ Agilidade | [X]/10 |\n"
                                    f"| 👂 Escuta | [X]/10 |\n"
                                    f"| 🔄 Adaptação | [X]/10 |\n"
                                    f"| ❓ Qualidade das perguntas | [X]/10 |\n\n"
                                    f"⭐ NOTA GERAL: [X]/10\n\n"
                                    f"RESULTADO: [APROVADO ✅ / REPROVADO ❌]\n\n"
                                    f"🟢 O QUE VOCÊ FEZ MUITO BEM:\n[feedback específico]\n\n"
                                    f"🟡 O QUE PODE MELHORAR:\n[feedback específico]\n\n"
                                    f"🔴 SEU MAIOR ERRO:\n[o erro mais crítico — se houver]\n\n"
                                    f"HABILIDADE QUE PRECISA DESENVOLVER: [1 habilidade específica em 1 linha]\n\n"
                                    f"🎯 PRÓXIMO DESAFIO: [orientação para a próxima conversa]"
                                )
                                aval_l = conexa_ia(prompt_aval_l)

                                # Detecta aprovação
                                import re as re_mod2
                                aprovado = "APROVADO" in aval_l and "REPROVADO" not in aval_l.split("APROVADO")[0]
                                # Extrai habilidade a desenvolver
                                hab_match = re_mod2.search(r"HABILIDADE QUE PRECISA DESENVOLVER:\s*(.+)", aval_l)
                                hab = hab_match.group(1).strip() if hab_match else None

                                if aprovado:
                                    st.session_state.labia_nivel = min(nivel + 1, 7)
                                    st.session_state.labia_falha_anterior = None
                                    if nivel == 1 and "primeiro_passo" not in st.session_state.conquistas:
                                        st.session_state.conquistas.append("primeiro_passo")
                                    if nivel == 7 and "don_juan" not in st.session_state.conquistas:
                                        st.session_state.conquistas.append("don_juan")
                                else:
                                    st.session_state.labia_falha_anterior = hab

                                st.session_state.treinos_realizados += 1
                                salvar_historico("Arte da Lábia", f"Nível {nivel} — {'✅' if aprovado else '❌'}", aval_l)
                                st.session_state['labia_aval'] = (aval_l, aprovado)
                                st.session_state.labia_personagem = None
                                st.session_state.labia_chat = []
                                st.rerun()
                        else:
                            st.warning(f"Complete pelo menos {cfg['turnos_min']} turnos antes de finalizar. Você tem {turno_usuario} turnos.")

                with col_aband:
                    if st.button("🔄 Novo", key="labia_novo"):
                        st.session_state.labia_personagem = None
                        st.session_state.labia_chat = []
                        st.rerun()

        if st.session_state.get('labia_aval'):
            aval_txt, aprovado = st.session_state['labia_aval']
            cor_card = "card-green" if aprovado else "card-red"
            st.markdown(f"<div class='{cor_card}'>{aval_txt}</div>", unsafe_allow_html=True)
            if aprovado:
                prox = FAIXAS[min(st.session_state.labia_nivel-1, 6)]
                st.success(f"🏆 Aprovado! Próxima faixa: {prox[0]} {prox[2]}")
            else:
                st.info("❌ Não desta vez. Mas você ganhou um novo desafio com personagem diferente.")
            if st.button("▶️ Continuar", key="labia_continuar"):
                del st.session_state['labia_aval']; st.rerun()

        with tab_h:
            st.markdown("### 📜 Histórico de Personagens")
            hist_p = st.session_state.get('historico_personagens', [])
            if hist_p:
                for i, p in enumerate(reversed(hist_p)):
                    st.markdown(f"<div class='hist-item'><small style='color:#888;'>#{len(hist_p)-i}</small> {p}</div>", unsafe_allow_html=True)
            else:
                st.info("Nenhum personagem enfrentado ainda.")


    # ──────────────────────────────────────────
    # BIBLIOTECA
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca Inteligente")
        categorias = ["Todas","Respostas","Cartas na Manga","Mensagens Turbinadas","Análises","Primeiras conversas","Amizade","Networking","Perguntas"]
        filtro = st.selectbox("Filtrar:", categorias, key="filtro_bib")
        bib = st.session_state.biblioteca
        if filtro != "Todas":
            bib = [b for b in bib if b.get('categoria','') == filtro]
        if not bib:
            st.info("Nenhum item salvo nesta categoria ainda.")
        else:
            st.markdown(f"**{len(bib)} item(ns) encontrado(s)**")
            for i, item in enumerate(reversed(bib)):
                idx = len(st.session_state.biblioteca) - 1 - i
                with st.expander(f"[{item.get('categoria','')}] {item['conteudo'][:60]}... — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3,1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name="item_biblioteca.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️", key=f"del_bib_{i}"):
                            st.session_state.biblioteca.pop(idx); st.rerun()

    # ──────────────────────────────────────────
    # LEITOR DE PERFIL
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Perfil":
        st.header("📸 Leitor de Perfil")
        st.markdown("*Analisa informações públicas e sugere assuntos de conversa.*")
        st.markdown("""<div class='card-yellow'>⚠️ <strong>Limite ético:</strong> A IA trabalha APENAS com informações fornecidas por você.
        Não determina personalidade por aparência. Não afirma intenções. Não diagnostica.
        Use apenas informações públicas.</div>""", unsafe_allow_html=True)

        bio_perfil = st.text_area("📋 Informações do perfil (bio, posts, interesses):", height=150, placeholder="ex: 'Viajante apaixonada. Fotógrafa nas horas vagas. Amo trilhas e café ☕'")
        nome_perfil = st.text_input("Nome (opcional):", placeholder="ex: Marina")
        contexto_perfil = st.text_input("Como vocês se conheceram:", placeholder="ex: seguimos um ao outro, colega de trabalho, amigo em comum...")

        if st.button("📸 ANALISAR PERFIL"):
            if bio_perfil.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Analise as informações públicas deste perfil e sugira assuntos para conversa.\n"
                        f"Nome: {nome_perfil or 'não informado'}. Bio/informações: {bio_perfil}. Contexto: {contexto_perfil or 'não informado'}.\n\n"
                        f"REGRAS ABSOLUTAS:\n"
                        f"- NÃO determine personalidade por aparência\n- NÃO afirme intenções ou sentimentos\n"
                        f"- Trabalhe APENAS com informações fornecidas\n\n"
                        f"FORMATO:\n\n"
                        f"🎯 INTERESSES IDENTIFICADOS:\n[o que é explicitamente visível nas informações]\n\n"
                        f"💬 ASSUNTOS PARA CONVERSA:\n[lista de 5-7 assuntos com base nos interesses]\n\n"
                        f"❓ PERGUNTAS NATURAIS:\n[3-5 perguntas abertas relacionadas aos interesses]\n\n"
                        f"🧩 ELEMENTOS DA BIO QUE PODEM GERAR ASSUNTO:\n[análise dos elementos específicos]\n\n"
                        f"💡 COMO INICIAR A CONVERSA:\n[2-3 aberturas naturais baseadas no perfil]"
                    )
                    res = conexa_ia(prompt)
                    salvar_historico("Leitor de Perfil", bio_perfil[:60], res)
                    st.session_state['perfil_temp'] = res
            else:
                st.warning("Cole as informações do perfil.")

        if st.session_state.get('perfil_temp'):
            st.markdown(f"<div class='card'>{st.session_state['perfil_temp']}</div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # COMPARAR CONVERSAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Comparar":
        st.header("⚔️ Comparar Duas Conversas")
        col1, col2 = st.columns(2)
        with col1:
            conv_a = st.text_area("💬 Conversa A:", height=180, placeholder="Cole a primeira conversa...")
        with col2:
            conv_b = st.text_area("💬 Conversa B:", height=180, placeholder="Cole a segunda conversa...")

        if st.button("⚔️ COMPARAR"):
            if conv_a.strip() and conv_b.strip():
                with st.spinner("Comparando..."):
                    prompt = (
                        f"Compare estas duas conversas.\n\nConversa A:\n{conv_a}\n\nConversa B:\n{conv_b}\n\n"
                        f"FORMATO:\n\n"
                        f"🧠 COMPARAÇÃO\n\n"
                        f"| Critério | A | B |\n|---|---|---|\n"
                        f"| Clareza | [nota] | [nota] |\n"
                        f"| Naturalidade | [nota] | [nota] |\n"
                        f"| Reciprocidade | [nota] | [nota] |\n"
                        f"| Fluidez | [nota] | [nota] |\n"
                        f"| Qualidade das perguntas | [nota] | [nota] |\n\n"
                        f"🏆 MELHOR DINÂMICA:\n[qual e por quê — baseado em padrões observáveis]\n\n"
                        f"💡 O QUE A MELHOR CONVERSA FEZ DIFERENTE:\n[lições práticas]"
                    )
                    res = conexa_ia(prompt)
                    salvar_historico("Comparação", "Conversa A vs B", res)
                    st.session_state['comp_temp'] = res
            else:
                st.warning("Cole as duas conversas.")

        if st.session_state.get('comp_temp'):
            st.markdown(st.session_state['comp_temp'])

    # ──────────────────────────────────────────
    # PLANO 7 DIAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Plano":
        st.header("🗓️ Plano de Evolução — 7 Dias")

        foco_plano = st.text_input("Qual aspecto da comunicação você mais quer desenvolver?",
            placeholder="ex: fazer perguntas melhores, não travar no início da conversa, lidar com silêncio...")

        if st.button("🗓️ GERAR MEU PLANO"):
            with st.spinner("Criando seu plano personalizado..."):
                prompt = (
                    f"Crie um plano de desenvolvimento de comunicação de 7 dias.\n"
                    f"Foco principal: {foco_plano or 'desenvolvimento geral'}.\n\n"
                    f"Para cada dia:\n\n"
                    f"📅 DIA [N] — [TEMA]\n"
                    f"🎯 Objetivo do dia: [o que desenvolver]\n"
                    f"📖 Conceito: [explicação simples]\n"
                    f"💪 Exercício prático: [tarefa concreta que pode ser feita hoje]\n"
                    f"⭐ Critério de sucesso: [como saber se conseguiu]\n\n"
                    f"[repita para 7 dias]\n\n"
                    f"🏆 DIA 7 — DESAFIO FINAL:\n[simulação completa integrando tudo]"
                )
                res = conexa_ia(prompt)
                st.session_state.plano_conquista = res
                salvar_historico("Plano 7 Dias", foco_plano[:60] if foco_plano else "Geral", res)
                st.session_state['plano_temp'] = res

        if st.session_state.get('plano_temp'):
            st.markdown(f"<div class='card'>{st.session_state['plano_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar plano (.txt)", data=st.session_state['plano_temp'], file_name="plano_7dias.txt", mime="text/plain")

    # ──────────────────────────────────────────
    # PROGRESSO
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Progresso":
        st.header("📈 Minha Evolução")

        # Atualizar métricas manualmente
        st.markdown("### 📊 Atualizar Evolução")
        st.markdown("*Após cada sessão de treino, atualize suas métricas.*")
        col1, col2 = st.columns(2)
        with col1:
            nova_clareza = st.slider("Clareza:", 0, 10, st.session_state.clareza)
            nova_naturalidade = st.slider("Naturalidade:", 0, 10, st.session_state.naturalidade)
            nova_reciprocidade = st.slider("Reciprocidade:", 0, 10, st.session_state.reciprocidade)
        with col2:
            nova_confianca = st.slider("Confiança:", 0, 10, st.session_state.confianca)
            nova_escuta = st.slider("Escuta:", 0, 10, st.session_state.escuta)

        if st.button("💾 SALVAR EVOLUÇÃO"):
            st.session_state.clareza = nova_clareza
            st.session_state.naturalidade = nova_naturalidade
            st.session_state.reciprocidade = nova_reciprocidade
            st.session_state.confianca = nova_confianca
            st.session_state.escuta = nova_escuta
            salvar_cache(st.session_state.usuario)
            st.success("✅ Evolução salva!")

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 📊 Desempenho Geral")
        c1,c2,c3,c4,c5 = st.columns(5)
        for col, nome_m, val in [(c1,"Clareza",st.session_state.clareza),(c2,"Naturalidade",st.session_state.naturalidade),(c3,"Reciprocidade",st.session_state.reciprocidade),(c4,"Confiança",st.session_state.confianca),(c5,"Escuta",st.session_state.escuta)]:
            col.markdown(f"<div class='stat-box'><div class='stat-numero'>{val}</div><div>{nome_m}</div></div>", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.conversas_analisadas}</div><div>Conversas analisadas</div></div>", unsafe_allow_html=True)
        col_b.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.treinos_realizados}</div><div>Treinos realizados</div></div>", unsafe_allow_html=True)
        col_c.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.labia_nivel}</div><div>Nível Arte da Lábia</div></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # RESUMO SEMANAL
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Resumo":
        st.header("📋 Relatório Semanal")

        if st.button("📋 GERAR RELATÓRIO"):
            with st.spinner("Gerando relatório..."):
                prompt = (
                    f"Crie um relatório semanal de evolução em comunicação.\n"
                    f"Dados: {st.session_state.conversas_analisadas} conversas analisadas, "
                    f"{st.session_state.mensagens_aprimoradas} mensagens turbinadas, "
                    f"{st.session_state.treinos_realizados} treinos, "
                    f"{st.session_state.cartas_usadas} cartas usadas.\n"
                    f"Métricas: Clareza {st.session_state.clareza}/10, Naturalidade {st.session_state.naturalidade}/10, "
                    f"Reciprocidade {st.session_state.reciprocidade}/10, Confiança {st.session_state.confianca}/10, Escuta {st.session_state.escuta}/10.\n"
                    f"Nível Arte da Lábia: {st.session_state.labia_nivel}/7.\n\n"
                    f"FORMATO:\n\n"
                    f"📋 RELATÓRIO SEMANAL — {st.session_state.usuario.upper()}\n\n"
                    f"🧠 O QUE A IA PERCEBEU:\n"
                    f"Maior avanço: [gerado automaticamente]\n"
                    f"Ponto de atenção: [gerado automaticamente]\n"
                    f"Comportamento funcionando: [gerado automaticamente]\n"
                    f"Próximo desafio: [gerado automaticamente]\n\n"
                    f"💡 INSIGHT DA SEMANA:\n[frase personalizada baseada nos dados]\n\n"
                    f"🎯 OBJETIVOS PARA A PRÓXIMA SEMANA:\n[3 metas específicas]"
                )
                res = conexa_ia(prompt)
                st.session_state.resumo_semanal = res
                salvar_historico("Resumo Semanal", "Relatório automático", res)
                st.session_state['resumo_temp'] = res

        if st.session_state.get('resumo_temp') or st.session_state.resumo_semanal:
            txt = st.session_state.get('resumo_temp') or st.session_state.resumo_semanal
            st.markdown(f"<div class='card'>{txt}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar relatório (.txt)", data=txt, file_name="relatorio_semanal.txt", mime="text/plain")

    # ──────────────────────────────────────────
    # CONQUISTAS
    # ──────────────────────────────────────────
    elif st.session_state.pagina == "Conquistas":
        st.header("🏆 Conquistas")
        conquistadas = st.session_state.get('conquistas', [])
        total = len(CONQUISTAS_DEF)
        obtidas = len(conquistadas)
        st.markdown(f"**{obtidas} de {total} conquistas desbloqueadas**")
        st.progress(obtidas / total if total > 0 else 0)

        novas = verificar_conquistas()
        if novas:
            for nc in novas:
                nome_c = next((n for ch,n,_ in CONQUISTAS_DEF if ch==nc), nc)
                st.success(f"🏆 Nova conquista: {nome_c}!")

        st.markdown("<br>", unsafe_allow_html=True)
        cols_c = st.columns(3)
        for i, (chave, nome, desc) in enumerate(CONQUISTAS_DEF):
            obtida = chave in conquistadas
            estilo = "border:2px solid #FF69B4;" if obtida else "opacity:0.4;border:1px solid #E2E8F0;"
            icon = "🏆" if obtida else "🔒"
            with cols_c[i % 3]:
                st.markdown(f"<div class='conquista-item' style='{estilo}'>"
                    f"<div style='font-size:1.3em;'>{icon}</div>"
                    f"<div style='font-weight:700;font-size:0.88em;color:#1A1A2E;'>{nome}</div>"
                    f"<div style='font-size:0.75em;color:#6B7280;'>{desc}</div>"
                    f"</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 CONEXA IA — Inteligência para Conversas · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
