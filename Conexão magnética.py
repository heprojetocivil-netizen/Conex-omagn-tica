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

    .card { background:linear-gradient(135deg,#FFF5F7,#FFF0F5); padding:22px; border-radius:16px; border:1px solid #FFD1DC; margin-bottom:15px; white-space:normal; word-wrap:break-word; box-shadow:0 2px 12px rgba(255,105,180,0.08); }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#2D0A1A,#1A0010); padding:22px; border-radius:16px; border:1px solid #FF69B4; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong, .stApp .card-dark em { color:#FFD1DC !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:22px; border-radius:16px; border:1px solid #86EFAC; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div, .stApp .card-green strong { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:22px; border-radius:16px; border:1px solid #93C5FD; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:22px; border-radius:16px; border:2px solid #FECACA; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:22px; border-radius:16px; border:1px solid #FCD34D; margin-bottom:15px; white-space:normal; word-wrap:break-word; }
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
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#C2185B !important; font-family:'Playfair Display',serif; }

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
    'labia_inicio': 0, 'labia_duracao': 180, 'labia_encerrado': False,
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
            f"<span style='color:#C2185B;font-size:0.88em;'>"
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
        style='color:#C2185B;font-weight:600;text-decoration:none;'>quizcompremios.com.br</a>
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
        st.markdown("🔑 Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#C2185B;'>console.groq.com/keys</a>", unsafe_allow_html=True)


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
           "Roleplay":"Simulador de Conversa","Labia":"🎭 A Arte da Lábia — EXCLUSIVO"}
    for i,(ic,pg) in enumerate(nav1):
        ch = list(lb1.keys())[i]
        if cols1[i].button(ic, key=f"nav1_{ch}", help=lb1[ch]):
            st.session_state.pagina = ch; st.rerun()

    # DESTAQUE — Arte da Lábia
    st.markdown("""
    <style>
    @keyframes pulsar {
        0%   { opacity: 1; transform: scale(1); }
        50%  { opacity: 0.7; transform: scale(1.03); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes brilhar {
        0%   { box-shadow: 0 0 8px rgba(255,105,180,0.4); }
        50%  { box-shadow: 0 0 22px rgba(255,105,180,0.9), 0 0 40px rgba(255,105,180,0.4); }
        100% { box-shadow: 0 0 8px rgba(255,105,180,0.4); }
    }
    .labia-destaque {
        animation: pulsar 2s ease-in-out infinite, brilhar 2s ease-in-out infinite;
        background: linear-gradient(135deg, #FF69B4, #C2185B);
        border-radius: 12px;
        padding: 10px 16px;
        text-align: center;
        cursor: pointer;
        margin-bottom: 4px;
    }
    .stApp .labia-destaque, .stApp .labia-destaque p,
    .stApp .labia-destaque span, .stApp .labia-destaque div { color: white !important; }
    </style>
    <div class='labia-destaque' onclick="window.location.reload()">
        🎭 <strong>TORNE-SE UM SEDUTOR IMPARÁVEL</strong> &nbsp;·&nbsp; A Arte da Lábia &nbsp;·&nbsp; ⭐ TOP &nbsp;&nbsp;👆 Clique em 🎭 acima
    </div>
    """, unsafe_allow_html=True)

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
            cor = "#22C55E" if val >= 7 else ("#B45309" if val >= 4 else "#B91C1C")
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
                    st.markdown(f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
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
        import time as _time
        import json as _json
        import re as _re

        # ── FASES / PERSONAGENS ──
        FASES_LABIA = [
            (1, "🌱", "A Modesta",          "Receptiva, acolhedora, facilita a conversa.",          "Começar e manter uma conversa."),
            (2, "😈", "A Atrevida",          "Brincalhona, irônica, testa espontaneidade.",          "Improviso e humor."),
            (3, "💋", "A Deusa do Bairro",   "Segura, sabe que chama atenção, difícil impressionar.","Autoconfiança."),
            (4, "👑", "A Inalcançável",      "Seletiva, pouca validação, percebe quem força.",       "Criar interesse sem forçar."),
            (5, "🔥", "A Perigosa",          "Imprevisível, muda de humor, oscila entre aberta e fria.","Adaptação."),
            (6, "💎", "A Raridade",          "Socialmente experiente, detecta artificialidade.",     "Profundidade e presença."),
            (7, "👑", "A Lenda",             "Extremamente segura, zero necessidade, exige naturalidade.","Domínio total da conversa."),
        ]

        DURACAO_FASES = {1:300,2:300,3:300,4:300,5:300,6:300,7:300}  # 5 min cada

        # Rostos por personalidade (feminino / masculino)
        ROSTOS_F = {
            1: "🙂",   # Modesta — tímida, discreta
            2: "😏",   # Atrevida — confiante, provocadora
            3: "😎",   # Deusa do Bairro — segura, estilosa
            4: "🧐",   # Inalcançável — analítica, seletiva
            5: "😈",   # Perigosa — imprevisível
            6: "🤨",   # Raridade — perspicaz, observadora
            7: "👑",   # Lenda — suprema confiança
        }
        ROSTOS_M = {
            1: "🙂",   # Modesto
            2: "😏",   # Atrevido
            3: "😎",   # O Popular
            4: "🧐",   # O Seletivo
            5: "😈",   # O Imprevisível
            6: "🤨",   # O Perspicaz
            7: "👑",   # O Lendário
        }

        # Regras de inatividade por fase (segundos sem digitar → queda no Conexômetro)
        # Mais generoso nas fases iniciais, mais rigoroso nas avançadas
        INATIVIDADE_REGRAS = {
            1: {"limite": 60, "queda": 3,  "msg": ""},           # 1 min → -3 (quase não penaliza)
            2: {"limite": 50, "queda": 5,  "msg": ""},
            3: {"limite": 40, "queda": 8,  "msg": "⚠️ Ela está esperando..."},
            4: {"limite": 35, "queda": 10, "msg": "⚠️ Ela está perdendo o interesse."},
            5: {"limite": 30, "queda": 12, "msg": "⚠️ A conversa está esfriando."},
            6: {"limite": 25, "queda": 15, "msg": "⚠️ Ela está olhando para outro lado."},
            7: {"limite": 20, "queda": 18, "msg": "⚠️ Ela já está pensando em ir embora."},
        }

        # Mínimos de turnos para aprovação por fase
        TURNOS_MIN_APROVACAO = {1:4, 2:5, 3:6, 4:6, 5:7, 6:7, 7:8}

        ESTADOS_CONEXO = [
            (80,  "🔥 CONEXÃO FORTE",    "#DC2626"),
            (60,  "❤️ BOA QUÍMICA",      "#B45309"),
            (40,  "😐 NEUTRO",           "#64748B"),
            (20,  "⚠️ INTERESSE CAINDO", "#EA580C"),
            (1,   "🚨 ÚLTIMA CHANCE",    "#7F1D1D"),
            (0,   "💥 ELIMINADO",        "#000000"),
        ]

        def estado_conexo(val):
            for minimo, label, cor in ESTADOS_CONEXO:
                if val >= minimo:
                    return label, cor
            return "💥 ELIMINADO", "#000000"

        # Defaults do jogo
        if 'lj_fase'     not in st.session_state: st.session_state.lj_fase     = 1
        if 'lj_persona'  not in st.session_state: st.session_state.lj_persona  = None
        if 'lj_chat'     not in st.session_state: st.session_state.lj_chat     = []
        if 'lj_conexo'   not in st.session_state: st.session_state.lj_conexo   = 100
        if 'lj_inicio'   not in st.session_state: st.session_state.lj_inicio   = 0
        if 'lj_ativo'    not in st.session_state: st.session_state.lj_ativo    = False
        if 'lj_arranques' not in st.session_state: st.session_state.lj_arranques = []
        if 'lj_ganchos'  not in st.session_state: st.session_state.lj_ganchos  = {"total":0,"usados":0}
        if 'lj_combo'    not in st.session_state: st.session_state.lj_combo    = 0
        if 'lj_aval'     not in st.session_state: st.session_state.lj_aval     = None
        if 'lj_hist'     not in st.session_state: st.session_state.lj_hist     = []
        if 'lj_fraqueza' not in st.session_state: st.session_state.lj_fraqueza = None
        if 'lj_usados'   not in st.session_state: st.session_state.lj_usados   = []
        if 'lj_contextos' not in st.session_state: st.session_state.lj_contextos = []
        if 'lj_ts_persona' not in st.session_state: st.session_state.lj_ts_persona = 0
        if 'lj_ts_usuario' not in st.session_state: st.session_state.lj_ts_usuario = 0
        if 'lj_recordes' not in st.session_state: st.session_state.lj_recordes = {"melhor_conexo":0,"maior_seq":0,"mais_arranques":0,"fases":0}

        fase_idx = st.session_state.lj_fase - 1
        fase_info = FASES_LABIA[min(fase_idx, 6)]

        # ══════════════════════════════════════
        # TELA INICIAL — SEM PARTIDA ATIVA
        # ══════════════════════════════════════
        if not st.session_state.lj_ativo:

            st.markdown("## 🎭 A Arte da Lábia")
            st.markdown("*Aprenda a conversar sem travar, criar conexão e dominar qualquer conversa.*")

            # ── CAMPO DE SENHA PARA DESBLOQUEIO TOTAL ──
            with st.expander("🔑 Acesso especial"):
                senha_input = st.text_input("Senha:", type="password", key="lj_senha_input")
                if st.button("Desbloquear", key="lj_btn_senha"):
                    if senha_input == "123":
                        st.session_state.lj_desbloqueado = True
                        st.success("✅ Todas as fases desbloqueadas!")
                        st.rerun()
                    else:
                        st.error("Senha incorreta.")

            if 'lj_desbloqueado' not in st.session_state:
                st.session_state.lj_desbloqueado = False

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # PROGRESSÃO
            st.markdown("### 🏆 Sua Progressão")
            cols_fases = st.columns(7)
            for i, (n, emoji, nome, _, _hab) in enumerate(FASES_LABIA):
                desbloqueada = n <= st.session_state.lj_fase or st.session_state.lj_desbloqueado
                concluida    = n <  st.session_state.lj_fase
                cor = "#22C55E" if concluida else ("#C2185B" if desbloqueada else "#E5E7EB")
                lock = "✅" if concluida else ("🔓" if desbloqueada else "🔒")
                with cols_fases[i]:
                    st.markdown(f"""
                    <div style='text-align:center;background:#FFFFFF;border:2px solid {cor};
                    border-radius:12px;padding:10px 4px;'>
                        <div style='font-size:1.4em;'>{emoji}</div>
                        <div style='font-size:0.65em;font-weight:700;color:#1A1A2E;line-height:1.2;'>{nome}</div>
                        <div style='font-size:0.8em;margin-top:4px;'>{lock}</div>
                    </div>
                    """, unsafe_allow_html=True)

            rec = st.session_state.lj_recordes
            st.markdown(f"""
            <div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
            padding:12px 16px;margin-top:12px;font-size:0.88em;color:#1A1A2E;'>
            🏅 Melhor Conexão: <strong>{rec['melhor_conexo']}</strong> &nbsp;·&nbsp;
            🔥 Maior sequência: <strong>{rec['maior_seq']}</strong> &nbsp;·&nbsp;
            🚀 Mais arranques: <strong>{rec['mais_arranques']}</strong> &nbsp;·&nbsp;
            🏆 Fases concluídas: <strong>{rec['fases']}</strong>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # Resultado da última partida
            if st.session_state.lj_aval:
                aval = st.session_state.lj_aval
                aprovado = aval.get('aprovado', False)
                cor_res = "#14532D" if aprovado else "#7F1D1D"
                bg_res  = "#F0FDF4" if aprovado else "#FFF5F5"
                bd_res  = "#86EFAC" if aprovado else "#FECACA"
                icon_res = "🎉" if aprovado else "💥"

                st.markdown(f"""
                <div style='background:{bg_res};border:2px solid {bd_res};border-radius:14px;padding:18px 22px;margin-bottom:16px;'>
                    <div style='font-size:1.1em;font-weight:700;color:{cor_res};'>{icon_res} {aval.get('titulo','Resultado')}</div>
                    <div style='display:flex;gap:20px;margin:10px 0;flex-wrap:wrap;'>
                        <span style='color:#1A1A2E;'>❤️ Conexão final: <strong>{aval.get('conexo_final',0)}</strong></span>
                        <span style='color:#1A1A2E;'>🚀 Arranques: <strong>{aval.get('n_arranques',0)}</strong></span>
                        <span style='color:#1A1A2E;'>🎯 Ganchos: <strong>{aval.get('ganchos_usados',0)}/{aval.get('ganchos_total',0)}</strong></span>
                    </div>
                    <div style='color:#1A1A2E;font-size:0.9em;margin-top:6px;'>
                        🟢 <strong>Acertou:</strong> {aval.get('acertou','—')}<br>
                        🟡 <strong>Pode melhorar:</strong> {aval.get('melhorar','—')}<br>
                        🔴 <strong>Principal erro:</strong> {aval.get('erro','—')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # INICIAR
            st.markdown(f"### {fase_info[1]} {fase_info[2]} — Fase {fase_info[0]}")
            st.markdown(f"*{fase_info[3]}*")
            st.markdown(f"🎯 **Habilidade:** {fase_info[4]}")

            col_g, col_f, col_i = st.columns([2,2,1])
            with col_g:
                genero_sel = st.radio("Conversar com:", ["Mulher","Homem"], horizontal=True, key="lj_genero")
            with col_f:
                if st.session_state.lj_desbloqueado:
                    fase_escolhida = st.selectbox("Escolher fase:",
                        [f"Fase {n} — {nome}" for n,emoji,nome,_,_ in FASES_LABIA],
                        index=st.session_state.lj_fase-1, key="lj_fase_sel")
                    st.session_state.lj_fase = int(fase_escolhida.split()[1])
                    fase_idx = st.session_state.lj_fase - 1
                    fase_info = FASES_LABIA[min(fase_idx, 6)]
            with col_i:
                st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🎲 INICIAR DESAFIO", use_container_width=True):
                fase_n = st.session_state.lj_fase
                genero_str = "feminino" if genero_sel == "Mulher" else "masculino"

                # Características por fase
                carac = {
                    1:"Aberta, receptiva, facilita a conversa, oferece muitos ganchos, tolera respostas medianas.",
                    2:"Brincalhona, usa ironia, provoca levemente, gosta de humor e espontaneidade.",
                    3:"Segura, sabe que chama atenção, não fica impressionada facilmente, não precisa de esforço.",
                    4:"Muito seletiva, oferece pouca validação, percebe quando alguém tenta impressioná-la.",
                    5:"Imprevisível — pode estar aberta e fechar de repente, muda de humor, oscila.",
                    6:"Socialmente experiente, detecta perguntas artificiais, insegurança e conversa superficial.",
                    7:"Extremamente segura, muitas opções sociais, não facilita, não precisa da conversa.",
                }[fase_n]

                fraqueza_txt = f"O usuário falhou em: {st.session_state.lj_fraqueza}. Crie situações que testem isso." if st.session_state.lj_fraqueza else ""
                usados_txt = ", ".join(st.session_state.lj_usados[-8:]) if st.session_state.lj_usados else "nenhum"

                # Monta histórico detalhado para anti-repetição
                ctx_hist = st.session_state.get("lj_contextos", [])
                cenarios_usados = [x.get("cenario","") for x in ctx_hist]
                profissoes_usadas = [x.get("profissao","") for x in ctx_hist]
                interesses_usados = [i for x in ctx_hist for i in x.get("interesses",[])]
                assuntos_usados = [x.get("assunto_ama","") for x in ctx_hist if x.get("assunto_ama")]
                cidades_usadas = [x.get("cidade","") for x in ctx_hist if x.get("cidade")]
                aberturas_usadas = [x.get("primeira_fala","")[:40] for x in ctx_hist if x.get("primeira_fala")]
                hoje_usados = [x.get("algo_hoje","") for x in ctx_hist if x.get("algo_hoje")]

                anti_rep = (
                    f"EVITE COMPLETAMENTE estas combinações já usadas:\n"
                    f"- Cenários: {', '.join(set(cenarios_usados)) or 'nenhum'}\n"
                    f"- Profissões: {', '.join(set(profissoes_usadas)) or 'nenhuma'}\n"
                    f"- Interesses: {', '.join(set(interesses_usados)[:10]) or 'nenhum'}\n"
                    f"- Assuntos principais: {', '.join(set(assuntos_usados)) or 'nenhum'}\n"
                    f"- Cidades: {', '.join(set(cidades_usadas)) or 'nenhuma'}\n"
                    f"- Aberturas similares a: {' | '.join(aberturas_usadas[-3:]) or 'nenhuma'}\n"
                    f"- Situações do dia similares a: {' | '.join(hoje_usados[-3:]) or 'nenhuma'}\n"
                    f"Seja CRIATIVO e surpreendente — cada personagem deve abrir a conversa de forma única."
                )

                cenarios_todos = [
                    "cafeteria","parque","livraria","fila de evento","shopping","feira",
                    "exposição de arte","aeroporto","praça","academia","show de música",
                    "festa de aniversário","mercado","galeria","coworking","food court",
                    "banca de jornal","pet shop","sebo de livros","farmácia","bancada de bar",
                    "fila de banco","salão de beleza","loja de discos","jardim botânico",
                    "estação de metrô","calçadão","praia","aluguel de bicicletas","museu"
                ]
                # Remove cenários já usados para garantir variedade
                cenarios_disponiveis = [x for x in cenarios_todos if x not in cenarios_usados]
                if not cenarios_disponiveis:
                    cenarios_disponiveis = cenarios_todos  # reset se usou todos
                cenario = _random.choice(cenarios_disponiveis)
                import random as _random
                cenario = _random.choice(cenarios)

                # Gera data de aniversário aleatória para o personagem
                import random as _r2
                meses = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
                mes_aniv = _r2.choice(meses)
                dia_aniv = _r2.randint(1, 28)

                prompt_p = (
                    f"Crie um personagem fictício adulto de gênero {genero_str} para simulação social.\n"
                    f"Fase {fase_n}/7: {carac}\n"
                    f"Cenário: {cenario}.\n"
                    f"Não repita combinações já usadas: {usados_txt}. {fraqueza_txt}\n"
                    f"{anti_rep}\n\n"
                    f"O personagem deve parecer uma PESSOA REAL com vida própria, não um NPC de jogo.\n\n"
                    f"RETORNE APENAS JSON válido (sem markdown, sem explicações fora do JSON):\n"
                    f'{{\n'
                    f'  "nome": "",\n'
                    f'  "genero": "{genero_str}",\n'
                    f'  "idade": 0,\n'
                    f'  "profissao": "",\n'
                    f'  "cidade": "",\n'
                    f'  "aniversario": "{dia_aniv} de {mes_aniv}",\n'
                    f'  "personalidade": {{"extroversao":0,"humor":0,"curiosidade":0,"paciencia":0,"confianca":0,"seletividade":0}},\n'
                    f'  "interesses": [],\n'
                    f'  "musica": "",\n'
                    f'  "esporte": "",\n'
                    f'  "comida_favorita": "",\n'
                    f'  "serie_favorita": "",\n'
                    f'  "filme_favorito": "",\n'
                    f'  "livro_favorito": "",\n'
                    f'  "viagem_sonho": "",\n'
                    f'  "maior_medo": "",\n'
                    f'  "maior_paixao": "",\n'
                    f'  "jeito_de_falar": "",\n'
                    f'  "expressoes_proprias": [],\n'
                    f'  "reacao_elogio": "",\n'
                    f'  "reacao_piada": "",\n'
                    f'  "reacao_provocacao": "",\n'
                    f'  "assunto_que_ama": "",\n'
                    f'  "assunto_que_odeia": "",\n'
                    f'  "algo_que_aconteceu_hoje": "",\n'
                    f'  "contexto_vida_atual": "",\n'
                    f'  "estilo_fala": "",\n'
                    f'  "nivel_dificuldade": {fase_n},\n'
                    f'  "cenario": "{cenario}",\n'
                    f'  "primeira_fala": ""\n'
                    f'}}\n\n'
                    f"INSTRUÇÕES IMPORTANTES:\n"
                    f"- expressoes_proprias: 3-5 expressões que só essa pessoa usa (ex: 'cara demais', 'sério?!', 'olha só')\n"
                    f"- algo_que_aconteceu_hoje: algo pequeno e real do dia dela (ex: 'derramei café na blusa', 'atrasou o ônibus')\n"
                    f"- contexto_vida_atual: o que está acontecendo na vida dela agora (ex: 'mudando de emprego', 'planejando viagem')\n"
                    f"- reacao_elogio/piada/provocacao: como ela reage emocionalmente (ex: 'fica levemente corada', 'ri alto', 'ergue sobrancelha')\n"
                    f"- primeira_fala: 1-2 frases humanas e contextuais. Pode incluir algo do 'algo_que_aconteceu_hoje'."
                )
                with st.spinner("Criando personagem..."):
                    p_txt = conexa_ia(prompt_p)
                    try:
                        jm = _re.search(r'\{.*\}', p_txt, _re.DOTALL)
                        persona = _json.loads(jm.group(0)) if jm else {}
                    except:
                        persona = {}

                if not persona.get('nome'):
                    defaults_f = {
                        "feminino": {"nome":"Ana","genero":"feminino","idade":27,"profissao":"Designer","cidade":"BH","personalidade":{"extroversao":7,"humor":7,"curiosidade":8,"paciencia":7,"confianca":7,"seletividade":fase_n*14},"interesses":["música","viagens"],"musica":"MPB","esporte":"yoga","estilo_fala":"casual","nivel_dificuldade":fase_n,"cenario":cenario,"primeira_fala":"Esse lugar sempre fica cheio assim?"},
                        "masculino": {"nome":"Bruno","genero":"masculino","idade":29,"profissao":"Arquiteto","cidade":"SP","personalidade":{"extroversao":6,"humor":7,"curiosidade":7,"paciencia":7,"confianca":7,"seletividade":fase_n*14},"interesses":["cinema","esporte"],"musica":"rock","esporte":"futebol","estilo_fala":"casual","nivel_dificuldade":fase_n,"cenario":cenario,"primeira_fala":"Você sabe se a fila anda logo?"},
                    }
                    persona = defaults_f[genero_str]

                # Registra anti-repetição — granular
                registro = f"{persona.get('nome','')} / {persona.get('profissao','')} / {cenario}"
                st.session_state.lj_usados.append(registro)

                # Salva contexto detalhado para impedir repetição de assuntos/abertura
                ctx_salvo = {
                    "cenario": cenario,
                    "profissao": persona.get("profissao",""),
                    "interesses": persona.get("interesses",[]),
                    "assunto_ama": persona.get("assunto_que_ama",""),
                    "algo_hoje": persona.get("algo_que_aconteceu_hoje",""),
                    "primeira_fala": persona.get("primeira_fala",""),
                    "musica": persona.get("musica",""),
                    "cidade": persona.get("cidade",""),
                }
                st.session_state.lj_contextos.append(ctx_salvo)
                # Mantém só os últimos 10
                if len(st.session_state.lj_contextos) > 10:
                    st.session_state.lj_contextos = st.session_state.lj_contextos[-10:]

                # Inicia partida
                st.session_state.lj_persona   = persona
                st.session_state.lj_chat      = [{"role":"assistant","content":persona.get('primeira_fala','Oi.'),"ts":_time.time()}]
                st.session_state.lj_conexo    = 100
                st.session_state.lj_inicio    = _time.time()
                st.session_state.lj_ativo     = True
                st.session_state.lj_arranques = []
                st.session_state.lj_ganchos   = {"total":0,"usados":0}
                st.session_state.lj_combo     = 0
                st.session_state.lj_aval      = None
                st.session_state.lj_ts_persona = _time.time()
                st.session_state.lj_ts_usuario = 0
                st.rerun()

        # ══════════════════════════════════════
        # PARTIDA ATIVA
        # ══════════════════════════════════════
        else:
            persona   = st.session_state.lj_persona
            chat      = st.session_state.lj_chat
            conexo    = st.session_state.lj_conexo
            fase_n    = st.session_state.lj_fase
            duracao   = DURACAO_FASES[min(fase_n, 7)]
            decorrido = _time.time() - st.session_state.lj_inicio
            restante  = max(0, duracao - decorrido)
            mins_r    = int(restante // 60)
            segs_r    = int(restante % 60)
            pct_tempo = max(0.0, 1 - decorrido / duracao)
            cor_timer = "#22C55E" if pct_tempo > 0.5 else ("#B45309" if pct_tempo > 0.2 else "#B91C1C")

            estado_label, estado_cor = estado_conexo(conexo)

            # ── HEADER: SÓ CENÁRIO ──
            st.markdown(f"""
            <div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;padding:10px 14px;margin-bottom:12px;'>
                <strong style='color:#1A1A2E;'>📍 {persona.get('cenario','').capitalize()}</strong>
                <span style='font-size:0.82em;color:#4B5563;margin-left:8px;'>Você acaba de conhecer alguém.</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── CHAT ──
            genero_p = persona.get('genero','feminino')
            rosto = ROSTOS_F.get(fase_n,"🙂") if genero_p == 'feminino' else ROSTOS_M.get(fase_n,"🙂")

            for msg in chat:
                if msg['role'] == 'user':
                    st.markdown(f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    arr = msg.get('arranque')
                    if arr:
                        st.markdown(f"<div style='text-align:right;font-size:0.8em;color:#22C55E;font-weight:600;margin-bottom:2px;'>{arr}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='chat-persona'><b style='color:#1D4ED8;'>{rosto} {persona.get('nome','?')}:</b> {msg['content']}</div>", unsafe_allow_html=True)

            # ── QUEDA POR INATIVIDADE ──
            regra_inat = INATIVIDADE_REGRAS[min(fase_n, 7)]
            ts_u = st.session_state.lj_ts_usuario
            ts_p = st.session_state.lj_ts_persona
            # Só aplica se o personagem já falou (ts_p > 0) e o usuário não respondeu ainda
            if ts_p > 0 and ts_u < ts_p:
                inatividade_seg = _time.time() - ts_p
                if inatividade_seg > regra_inat["limite"]:
                    # Aplica queda proporcional — a cada ciclo de "limite" segundos
                    ciclos = int(inatividade_seg / regra_inat["limite"])
                    queda_total = min(ciclos * regra_inat["queda"], 20)  # máx -20 por ciclo
                    novo_conexo = max(0, conexo - queda_total)
                    if novo_conexo != conexo:
                        st.session_state.lj_conexo = novo_conexo
                        if regra_inat["msg"]:
                            st.markdown(f"<div class='card-yellow' style='padding:8px 14px;font-size:0.83em;'>{regra_inat['msg']}</div>", unsafe_allow_html=True)

            # Alerta última chance
            if 0 < st.session_state.lj_conexo <= 20:
                st.markdown("<div class='card-red' style='padding:10px 14px;font-size:0.88em;'>🚨 <strong>ÚLTIMA CHANCE</strong> — A conversa está esfriando. Mude de rota.</div>", unsafe_allow_html=True)

            # Dica nível 1 e 2
            turno_u = sum(1 for m in chat if m['role']=='user')
            if fase_n == 1 and turno_u == 0:
                st.markdown(f"<div class='card-green' style='padding:10px 14px;font-size:0.85em;'>💡 Comente o que {persona.get('nome','ela')} disse ou faça uma pergunta relacionada.</div>", unsafe_allow_html=True)
            elif fase_n == 2 and turno_u < 2:
                st.markdown("<div class='card-yellow' style='padding:10px 14px;font-size:0.85em;'>💡 Há um detalhe na última fala que pode render assunto.</div>", unsafe_allow_html=True)

            # Combo
            if st.session_state.lj_combo >= 3:
                st.markdown(f"<div style='text-align:center;font-size:0.9em;font-weight:700;color:#B45309;'>🔥 COMBO x{st.session_state.lj_combo}</div>", unsafe_allow_html=True)

            # ── VERIFICAR FIM ──
            tempo_esgotado = restante <= 0
            conexo_zero = conexo <= 0

            if tempo_esgotado or conexo_zero:
                # ENCERRAR PARTIDA
                motivo = "tempo" if tempo_esgotado else "conexao"
                hist_txt = "\n".join(f"{'Você' if m['role']=='user' else persona.get('nome','?')}: {m['content']}" for m in chat)
                fa_info = FASES_LABIA[min(fase_n-1,6)]
                n_arr = len(st.session_state.lj_arranques)
                g = st.session_state.lj_ganchos

                prompt_aval = (
                    f"Avalie esta conversa de treinamento social. Fase {fase_n}/7 — {fa_info[2]}.\n"
                    f"Personagem: {persona.get('nome','')} ({persona.get('profissao','')}, fase {fase_n}).\n"
                    f"Motivo do encerramento: {'tempo esgotado' if motivo=='tempo' else 'conexão chegou a zero'}.\n"
                    f"Conexão final: {conexo}.\n\n"
                    f"Conversa:\n{hist_txt}\n\n"
                    f"RESPONDA EM JSON (sem markdown):\n"
                    f'{{"aprovado":true/false,"nota_natural":0,"nota_escuta":0,"nota_humor":0,"nota_adaptacao":0,'
                    f'"nota_ganchos":0,"acertou":"1-2 frases","melhorar":"1-2 frases","erro_principal":"1-2 frases",'
                    f'"proximo_treino":"1 linha","fraqueza_detectada":"1 habilidade específica"}}'
                )
                with st.spinner("Calculando resultado..."):
                    aval_txt = conexa_ia(prompt_aval)
                    try:
                        jm2 = _re.search(r'\{.*\}', aval_txt, _re.DOTALL)
                        aval_d = _json.loads(jm2.group(0)) if jm2 else {}
                    except:
                        aval_d = {}

                aprovado = (conexo > 0 and aval_d.get('aprovado', conexo >= 50)
                            and turno_u >= TURNOS_MIN_APROVACAO.get(fase_n, 4))

                # Atualizar recordes
                rec = st.session_state.lj_recordes
                if conexo > rec['melhor_conexo']:       rec['melhor_conexo'] = conexo
                if n_arr > rec['mais_arranques']:        rec['mais_arranques'] = n_arr
                if aprovado:
                    rec['fases'] = max(rec['fases'], fase_n)
                    st.session_state.lj_fase = min(fase_n + 1, 7)
                    st.session_state.lj_fraqueza = None
                else:
                    st.session_state.lj_fraqueza = aval_d.get('fraqueza_detectada')

                st.session_state.lj_recordes = rec
                st.session_state.lj_hist.append({
                    "fase": fase_n, "persona": persona.get('nome',''),
                    "conexo": conexo, "aprovado": aprovado,
                    "data": datetime.now().strftime('%d/%m %H:%M'),
                })

                # Monta objeto de avaliação
                st.session_state.lj_aval = {
                    "aprovado": aprovado,
                    "titulo": "FASE CONCLUÍDA! 🎉" if aprovado else "CONEXÃO PERDIDA 💥",
                    "conexo_final": conexo,
                    "n_arranques": n_arr,
                    "ganchos_usados": g.get("usados",0),
                    "ganchos_total": g.get("total",0),
                    "acertou": aval_d.get("acertou","—"),
                    "melhorar": aval_d.get("melhorar","—"),
                    "erro": aval_d.get("erro_principal","—"),
                }
                st.session_state.lj_ativo   = False
                st.session_state.lj_persona = None
                st.session_state.lj_chat    = []
                st.rerun()

            else:
                # ── CONEXÔMETRO + TIMER — sempre visível perto do input ──
                pct_con2 = conexo / 100
                cor_con2 = "#22C55E" if conexo > 60 else ("#B45309" if conexo > 30 else "#B91C1C")
                estado_label2, _ = estado_conexo(conexo)
                st.markdown(f"""
                <div style='background:#FFFFFF;border:2px solid {cor_con2};border-radius:10px;
                padding:8px 16px;margin-bottom:6px;display:flex;align-items:center;gap:12px;'>
                    <span style='font-size:0.78em;color:#64748B;font-weight:600;white-space:nowrap;'>❤️ CONEXÔMETRO</span>
                    <div style='flex:1;background:#F1F5F9;border-radius:999px;height:10px;overflow:hidden;'>
                        <div style='height:100%;border-radius:999px;background:{cor_con2};width:{conexo}%;'></div>
                    </div>
                    <span style='font-size:1em;font-weight:700;color:{cor_con2};white-space:nowrap;'>{conexo} &nbsp;{estado_label2}</span>
                    <span style='font-size:0.75em;color:#64748B;white-space:nowrap;border-left:1px solid #E2E8F0;padding-left:12px;'>⏱️</span>
                    <span style='font-size:1.1em;font-weight:700;color:{cor_timer};white-space:nowrap;font-family:"Playfair Display",serif;'>{mins_r:02d}:{segs_r:02d}</span>
                </div>
                """, unsafe_allow_html=True)

                # ── INPUT ──
                msg_labia = st.text_input("", key=f"lj_input_{len(chat)}", placeholder="O que você diz?", label_visibility="collapsed")

                col_e, col_ab = st.columns([4,1])
                with col_e:
                    if st.button("📤 ENVIAR", key="lj_enviar", use_container_width=True):
                        if msg_labia.strip():
                            ts_user = _time.time()
                            tempo_resposta = ts_user - st.session_state.lj_ts_persona

                            # System do personagem
                            pers = persona.get('personalidade',{})
                            aniv_p     = persona.get('aniversario','data não definida')
                            nome_p2    = persona.get('nome','?')
                            prof_p     = persona.get('profissao','')
                            cidade_p   = persona.get('cidade','')
                            musica_p   = persona.get('musica','')
                            comida_p   = persona.get('comida_favorita','')
                            serie_p    = persona.get('serie_favorita','')
                            inter_p    = ', '.join(persona.get('interesses',[]))

                            # Fatos fixos repetidos no final do system — o modelo não esquece
                            lembrete = (
                                f"\n\nSEUS DADOS FIXOS (nunca mude nem contradiga):\n"
                                f"Nome: {nome_p2} | Profissão: {prof_p} | Cidade: {cidade_p}\n"
                                f"Aniversário: {aniv_p}\n"
                                f"Música: {musica_p} | Comida: {comida_p} | Série: {serie_p}\n"
                                f"Interesses: {inter_p}"
                            )

                            # Detecta pergunta pessoal → injeta aviso extra
                            kws_pessoal = ['aniversário','aniversario','nasce','cidade','mora',
                                           'música','musica','série','serie','comida','come',
                                           'trabalha','profissão','profissao','chama']
                            eh_pessoal = any(k in msg_labia.lower() for k in kws_pessoal)
                            aviso_pessoal = (
                                f"\n⚠️ ATENÇÃO: pergunta pessoal detectada. "
                                f"Responda EXATAMENTE conforme seus dados: "
                                f"Aniversário={aniv_p}, Cidade={cidade_p}, Profissão={prof_p}."
                            ) if eh_pessoal else ""

                            system_p = (
                                f"Você é {nome_p2}, {persona.get('idade',25)} anos.\n"
                                f"NUNCA quebre o personagem. Nunca mencione IA, jogo ou treinamento.\n\n"
                                f"=== SUA IDENTIDADE COMPLETA (MEMORIZE TUDO) ===\n"
                                f"Nome: {nome_p2} | Gênero: {genero_persona} | Idade: {persona.get('idade',25)}\n"
                                f"Profissão: {prof_p} | Cidade: {cidade_p}\n"
                                f"Aniversário: {aniv_p}\n"
                                f"Música: {musica_p} | Esporte: {persona.get('esporte','')}\n"
                                f"Comida favorita: {comida_p} | Série: {serie_p}\n"
                                f"Filme favorito: {persona.get('filme_favorito','')}\n"
                                f"Livro favorito: {persona.get('livro_favorito','')}\n"
                                f"Viagem dos sonhos: {persona.get('viagem_sonho','')}\n"
                                f"Maior paixão: {persona.get('maior_paixao','')}\n"
                                f"Maior medo: {persona.get('maior_medo','')}\n"
                                f"Assunto que ama: {persona.get('assunto_que_ama','')}\n"
                                f"Assunto que odeia: {persona.get('assunto_que_odeia','')}\n"
                                f"Interesses: {inter_p}\n"
                                f"O que aconteceu com você hoje: {persona.get('algo_que_aconteceu_hoje','')}\n"
                                f"Contexto de vida atual: {persona.get('contexto_vida_atual','')}\n\n"
                                f"=== SEU JEITO DE SER ===\n"
                                f"Estilo: {persona.get('jeito_de_falar','')}\n"
                                f"Expressões que você usa: {', '.join(persona.get('expressoes_proprias',[]))}\n"
                                f"Quando te elogiam: {persona.get('reacao_elogio','')}\n"
                                f"Quando fazem piada: {persona.get('reacao_piada','')}\n"
                                f"Quando te provocam: {persona.get('reacao_provocacao','')}\n"
                                f"Fase de dificuldade: {fase_n}/7 — {FASES_LABIA[min(fase_n-1,6)][2]}\n\n"
                                f"=== COMO VOCÊ CONVERSA ===\n"
                                f"- Você É essa pessoa. Vive no cenário: {persona.get('cenario','')}\n"
                                f"- Respostas CURTAS — 1 a 2 frases, no máximo 40 palavras\n"
                                f"- Use suas expressões próprias naturalmente\n"
                                f"- Reaja emocionalmente quando fizer sentido: surpresa, risada, discordância\n"
                                f"- Pessoas reais NÃO terminam toda fala com pergunta\n"
                                f"- Você pode: comentar, discordar, brincar, contar algo, provocar, ignorar, mudar de assunto\n"
                                f"- Se te perguntarem algo pessoal, responda conforme sua identidade acima\n"
                                f"- Se a pessoa fizer 3+ perguntas seguidas, reaja: 'Isso é entrevista de emprego? 😂'\n"
                                f"- Mostre personalidade: você tem opiniões, preferências, histórias\n"
                                f"- {'Seja aberta e receptiva, facilite um pouco a conversa' if fase_n<=2 else 'Não facilite — deixe a pessoa trabalhar para manter a conversa'}\n"
                                f"- Às vezes reaja com emoção visível: 'Nossa, sério?!' / 'Que coincidência!' / 'Isso me lembra...'\n"
                                f"- Lembre de TUDO que foi dito anteriormente — não repita perguntas já feitas"
                                + aviso_pessoal
                            )
                            historico = [{"role":m["role"],"content":m["content"]} for m in chat]
                            with st.spinner(""):
                                try:
                                    client = Groq(api_key=st.session_state.api_key)
                                    msgs = [{"role":"system","content":system_p}] + historico + [{"role":"user","content":msg_labia}]
                                    resp = client.chat.completions.create(messages=msgs, model="llama-3.3-70b-versatile", max_tokens=80)
                                    resp_txt = resp.choices[0].message.content.strip()
                                except Exception as e:
                                    resp_txt = "Interessante."

                                                        # Efeito de digitação — exibe palavra por palavra
                            nome_p = persona.get('nome','?')
                            rosto_p = ROSTOS_F.get(fase_n,"🙂") if genero_persona=='feminino' else ROSTOS_M.get(fase_n,"🙂")
                            placeholder_dig = st.empty()
                            palavras_resp = resp_txt.split()
                            texto_acumulado = ""
                            for palavra in palavras_resp:
                                texto_acumulado += ("" if texto_acumulado=="" else " ") + palavra
                                placeholder_dig.markdown(
                                    f"<div class='chat-persona'><b style='color:#1D4ED8;'>{rosto_p} {nome_p}:</b> {texto_acumulado}▌</div>",
                                    unsafe_allow_html=True
                                )
                                _time.sleep(0.06)
                            placeholder_dig.empty()  # limpa — o chat vai rerender com st.rerun()

                            # ── AVALIAR RESPOSTA E ATUALIZAR CONEXÔMETRO ──
                            # Generosidade crescente por fase
                            gen = {1:"MUITO GENEROSO: fase iniciante, qualquer resposta sincera merece +3 a +15. Só penalize erros graves.",
                                   2:"GENEROSO: credito ao esforco, penalize so entrevista de perguntas.",
                                   3:"MODERADO: exija naturalidade.",
                                   4:"EXIGENTE: naturalidade e confianca obrigatorias.",
                                   5:"RIGOROSO: adaptacao essencial.",
                                   6:"MUITO RIGOROSO: profundidade e sem artificialidade.",
                                   7:"MAXIMO: so respostas excepcionais ganham pontos."}[min(fase_n,7)]

                            prompt_eval = (
                                f"Avalie a ultima resposta do usuario em conversa de treinamento social.\n"
                                f"Fase {fase_n}/7. Criterio: {gen}\n"
                                f"Personagem: {FASES_LABIA[min(fase_n-1,6)][2]}.\n"
                                f"Tempo resposta: {tempo_resposta:.1f}s.\n"
                                f"Personagem disse: {chat[-1]['content'] if chat else ''}\n"
                                f"Usuario respondeu: {msg_labia}\n\n"
                                f"RETORNE JSON sem markdown:\n"
                                f'{{"delta":0,"arranque":"","tipo_arranque":""}}\n\n'
                                f"delta: -30 a +25. Fase 1 tende positivo (+3 a +15) para respostas razoaveis.\n"
                                f"arranque: se delta>8 gere string curta ex '🎯 +12 GANCHO PERFEITO', senao vazio.\n"
                                f"Penalizar: monossílabos repetidos, sequencia de perguntas, ignorar contexto."
                            )
                            with st.spinner(""):
                                try:
                                    eval_txt = conexa_ia(prompt_eval)
                                    jm3 = _re.search(r'\{.*\}', eval_txt, _re.DOTALL)
                                    eval_d = _json.loads(jm3.group(0)) if jm3 else {}
                                except:
                                    eval_d = {}

                            delta = eval_d.get('delta', 0)
                            arranque = eval_d.get('arranque', '')

                            novo_conexo = max(0, min(100, conexo + delta))

                            # Combo
                            if delta > 5:
                                st.session_state.lj_combo += 1
                            else:
                                st.session_state.lj_combo = 0

                            # Registra arranque
                            if arranque:
                                st.session_state.lj_arranques.append(arranque)

                            # Ganchos (heurística simples)
                            if any(w in msg_labia.lower() for w in [p.lower() for p in persona.get('interesses',[])]):
                                st.session_state.lj_ganchos['usados'] += 1
                            st.session_state.lj_ganchos['total'] = max(1, turno_u + 1)

                            # Atualiza estado
                            st.session_state.lj_conexo = novo_conexo
                            st.session_state.lj_ts_persona = _time.time()

                            chat.append({"role":"user","content":msg_labia,"ts":ts_user,"delta":delta})
                            chat.append({"role":"assistant","content":resp_txt,"ts":_time.time(),"arranque":arranque})
                            st.session_state.lj_chat = chat
                            st.session_state.lj_ts_usuario = ts_user  # registra último envio
                            st.rerun()

                with col_ab:
                    if st.button("🚩 Sair", key="lj_sair", use_container_width=True):
                        st.session_state.lj_ativo   = False
                        st.session_state.lj_persona = None
                        st.session_state.lj_chat    = []
                        st.rerun()

                # Auto-refresh a cada segundo
                _time.sleep(0.8)
                st.rerun()

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
