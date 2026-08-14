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

    /* Container do chat com scroll — mostra sempre as últimas mensagens */
    .chat-scroll-container {
        max-height: 40vh;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        scroll-behavior: smooth;
        padding-bottom: 4px;
    }
    .chat-scroll-container > * { flex-shrink: 0; }

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

    # Só mostra navbar e barra quando NÃO está em partida ativa
    em_partida = (st.session_state.get('pagina') == 'Labia' and st.session_state.get('lj_ativo', False))

    if not em_partida:
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

    # DESTAQUE — Arte da Lábia (botão real do Streamlit)
    st.markdown("""
    <style>
    @keyframes pulsar {
        0%   { opacity: 1; transform: scale(1); }
        50%  { opacity: 0.85; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes brilhar {
        0%   { box-shadow: 0 0 8px rgba(194,24,91,0.4); }
        50%  { box-shadow: 0 0 22px rgba(194,24,91,0.9), 0 0 40px rgba(194,24,91,0.4); }
        100% { box-shadow: 0 0 8px rgba(194,24,91,0.4); }
    }
    div[data-testid="stButton"] button.labia-cta {
        animation: pulsar 2s ease-in-out infinite, brilhar 2s ease-in-out infinite;
        background: linear-gradient(135deg, #FF69B4, #C2185B) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1em !important;
        padding: 12px 20px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("🎭 TORNE-SE UM SEDUTOR IMPARÁVEL  ·  A Arte da Lábia  ·  ⭐ TOP  —  Clique aqui", key="btn_labia_cta", use_container_width=True):
        st.session_state.pagina = "Labia"; st.rerun()

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
        import random as _rand

        # ── CONSTANTES ──
        PERSONAGENS = {
            "Rafaela": {
                "emoji": "👩",
                "dificuldade": 2,
                "estrelas": "⭐⭐",
                "desc": "Simpática, inteligente, bem-humorada. Conversa naturalmente mas não demonstra interesse imediatamente.",
                "personalidade": "simpática, inteligente, bem-humorada, curiosa, fala de forma leve e natural",
                "humor": 80, "receptividade": 70, "provocacao": 30, "exigencia": 40,
                "bloqueada": False,
            },
            "Camila": {
                "emoji": "👩",
                "dificuldade": 4,
                "estrelas": "⭐⭐⭐⭐",
                "desc": "Segura, provocadora, responde com ironia e testa a confiança do usuário.",
                "personalidade": "segura, irônica, provocadora, testa confiança, não facilita",
                "humor": 70, "receptividade": 45, "provocacao": 80, "exigencia": 70,
                "bloqueada": True,
            },
            "Helena": {
                "emoji": "👩",
                "dificuldade": 5,
                "estrelas": "⭐⭐⭐⭐⭐",
                "desc": "Sofisticada, seletiva, difícil de impressionar. Exige conversa mais inteligente.",
                "personalidade": "sofisticada, seletiva, intelectual, difícil de impressionar, exige profundidade",
                "humor": 55, "receptividade": 30, "provocacao": 60, "exigencia": 90,
                "bloqueada": True,
            },
        }

        FASES_DEF = [
            (1, "🟢", "ATRAÇÃO",           "Despertar interesse",        5,  "🥉 Paquerador",      70, 60, 65),
            (2, "🟡", "CONEXÃO EMOCIONAL", "Criar vínculo",              7,  "🥈 Galanteador",     75, 70, 65),
            (3, "🔴", "SEDUÇÃO",           "Criar química e tensão",     10, "👑 Mestre da Lábia", 80, 75, 70),
        ]
        # (fase, cor, nome, objetivo, minutos, titulo, min_conexao, min_naturalidade, min_interesse)

        MISSOES_POR_FASE = {
            1: [
                "Fazer a personagem fazer uma pergunta espontânea sobre você",
                "Conseguir que ela demonstre curiosidade",
                "Criar um momento de humor",
                "Fazer ela contar algo pessoal",
            ],
            2: [
                "Fazer a personagem lembrar algo que você disse antes",
                "Conseguir que ela compartilhe um sonho ou plano",
                "Criar um momento de empatia genuína",
                "Fazer ela admitir algo que normalmente não diria",
            ],
            3: [
                "Criar um momento de flerte natural",
                "Fazer ela usar um emoji de coração ou 😏",
                "Criar uma brincadeira interna entre vocês",
                "Fazer ela perguntar algo pessoal de forma espontânea",
            ],
        }

        CENARIOS_TODOS = [
            "cafeteria","parque","livraria","fila de evento","shopping","feira",
            "exposição de arte","aeroporto","praça","academia","show de música",
            "festa de aniversário","mercado","galeria","coworking","food court",
            "banca de jornal","pet shop","sebo de livros","farmácia","bancada de bar",
            "fila de banco","salão de beleza","loja de discos","jardim botânico",
            "estação de metrô","calçadão","praia","aluguel de bicicletas","museu"
        ]

        PERFIS_ESTILO = {
            "O Confiante":     "Fala com segurança, mas às vezes avança rápido demais.",
            "O Estrategista":  "Faz boas perguntas e lê bem os sinais.",
            "O Divertido":     "Usa humor para criar conexão.",
            "O Conquistador":  "Cria conexão emocional rapidamente.",
            "O Reservado":     "Tem boas respostas, mas demonstra pouco interesse.",
        }

        # ── DEFAULTS ──
        defs_labia = {
            'lj_fase': 1, 'lj_personagem_sel': 'Rafaela',
            'lj_ativo': False, 'lj_chat': [], 'lj_conexo': 100,
            'lj_atributos': {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20},
            'lj_inicio': 0, 'lj_duracao': 300,
            'lj_missao': '', 'lj_missao_cumprida': False,
            'lj_aval': None, 'lj_tentativas': [],
            'lj_historico_cenarios': [], 'lj_historico_aberturas': [],
            'lj_ts_persona': 0, 'lj_ts_usuario': 0,
            'lj_combo': 0, 'lj_arranques': [],
            'lj_fases_concluidas': 0,
            'lj_titulo': '🥉 Paquerador',
            'lj_personagens_desbloqueadas': ['Rafaela'],
            'lj_perfil_estilo': None,
            'lj_historico_partidas': [],
            'lj_desbloqueado': False,
            'lj_ficha': {},
            'lj_ficha_resumo': '',
        }
        for k, v in defs_labia.items():
            if k not in st.session_state:
                st.session_state[k] = v

        def estado_conexo(val):
            if val >= 80: return "🔥 ALTA CONEXÃO", "#DC2626"
            if val >= 60: return "❤️ BOA QUÍMICA", "#F59E0B"
            if val >= 40: return "😐 NEUTRO", "#64748B"
            if val >= 20: return "⚠️ INTERESSE CAINDO", "#EA580C"
            if val >= 1:  return "🚨 ÚLTIMA CHANCE", "#7F1D1D"
            return "💥 ELIMINADA", "#000000"

        # ══════════════════════════════════════
        # TELA INICIAL — SEM PARTIDA ATIVA
        # ══════════════════════════════════════
        if not st.session_state.lj_ativo:

            st.markdown("## 👑 Mestre da Lábia")
            st.markdown("*Você consegue conquistar uma conversa sem usar frases prontas?*")

            # Senha de desbloqueio
            with st.expander("🔑 Acesso especial"):
                senha_inp = st.text_input("Senha:", type="password", key="lj_senha")
                if st.button("Desbloquear tudo", key="lj_btn_senha"):
                    if senha_inp == "123":
                        st.session_state.lj_desbloqueado = True
                        st.session_state.lj_personagens_desbloqueadas = list(PERSONAGENS.keys())
                        st.success("✅ Todas as personagens e fases desbloqueadas!")
                        st.rerun()
                    else:
                        st.error("Senha incorreta.")

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # JORNADA
            st.markdown("### 🗺️ Sua Jornada")
            cols_fases = st.columns(3)
            for i, (fn, cor_f, nome_f, obj_f, mins_f, titulo_f, *_) in enumerate(FASES_DEF):
                concluida = st.session_state.lj_fases_concluidas >= fn
                atual     = st.session_state.lj_fases_concluidas == fn - 1
                bloqueada = not concluida and not atual
                cor = "#22C55E" if concluida else ("#C2185B" if atual else "#E5E7EB")
                with cols_fases[i]:
                    st.markdown(f"""
                    <div style='text-align:center;background:#FFFFFF;border:2px solid {cor};
                    border-radius:14px;padding:14px 8px;'>
                        <div style='font-size:1.3em;'>{cor_f}</div>
                        <div style='font-size:0.8em;font-weight:700;color:#1A1A2E;margin-top:4px;'>FASE {fn}</div>
                        <div style='font-size:0.75em;color:#C2185B;font-weight:700;'>{nome_f}</div>
                        <div style='font-size:0.7em;color:#4B5563;'>{obj_f}</div>
                        <div style='font-size:0.7em;color:#888;margin-top:4px;'>⏱️ {mins_f} min</div>
                        <div style='margin-top:6px;'>{"✅" if concluida else ("🔓" if atual else "🔒")}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Nível atual
            st.markdown(f"""
            <div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:10px;
            padding:10px 16px;margin:12px 0;text-align:center;'>
                <span style='font-size:0.82em;color:#64748B;'>Seu nível atual</span><br>
                <span style='font-size:1.3em;font-weight:700;color:#C2185B;'>{st.session_state.lj_titulo}</span>
            </div>
            """, unsafe_allow_html=True)

            # Resultado da última partida
            if st.session_state.lj_aval:
                aval = st.session_state.lj_aval
                aprovado = aval.get('aprovado', False)
                cor_res = "#14532D" if aprovado else "#7F1D1D"
                bg_res  = "#F0FDF4" if aprovado else "#FFF5F5"
                bd_res  = "#86EFAC" if aprovado else "#FECACA"
                st.markdown(f"""
                <div style='background:{bg_res};border:2px solid {bd_res};border-radius:12px;padding:14px 18px;margin-bottom:12px;'>
                    <div style='font-weight:700;color:{cor_res};'>{"🎉 " if aprovado else "💥 "}{aval.get("titulo","Resultado")}</div>
                    <div style='font-size:0.88em;color:#1A1A2E;margin-top:6px;'>
                        ❤️ Conexão final: <strong>{aval.get("conexo_final",0)}</strong> &nbsp;·&nbsp;
                        🚀 Arranques: <strong>{aval.get("n_arranques",0)}</strong>
                        {" &nbsp;·&nbsp; 🎯 Missão cumprida!" if aval.get("missao_cumprida") else ""}
                    </div>
                    <div style='font-size:0.85em;color:#1A1A2E;margin-top:4px;'>
                        ✅ <em>{aval.get("ponto_forte","—")}</em><br>
                        ⚠️ <em>{aval.get("melhorar","—")}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # ESCOLHA DA PERSONAGEM
            st.markdown("### 👩 Escolha a Personagem")
            cols_p = st.columns(3)
            for i, (nome_p, dados_p) in enumerate(PERSONAGENS.items()):
                desbloqueada = nome_p in st.session_state.lj_personagens_desbloqueadas or st.session_state.lj_desbloqueado
                selecionada  = st.session_state.lj_personagem_sel == nome_p
                cor_p = "#C2185B" if selecionada else ("#1A1A2E" if desbloqueada else "#E5E7EB")
                with cols_p[i]:
                    if desbloqueada:
                        if st.button(f"{dados_p['emoji']} {nome_p}\n{dados_p['estrelas']}", key=f"sel_p_{nome_p}", use_container_width=True):
                            st.session_state.lj_personagem_sel = nome_p; st.rerun()
                    st.markdown(f"""
                    <div style='background:#{"FFF0F5" if selecionada else "FFFFFF"};border:2px solid {cor_p};
                    border-radius:12px;padding:10px;font-size:0.78em;color:{"#1A1A2E" if desbloqueada else "#9CA3AF"};'>
                        {"🔒 Bloqueada" if not desbloqueada else dados_p["desc"]}
                    </div>
                    """, unsafe_allow_html=True)

            # Fase a jogar
            fase_atual = min(st.session_state.lj_fases_concluidas + 1, 3)
            if st.session_state.lj_desbloqueado:
                fase_sel_idx = st.selectbox("Fase:", [f"Fase {f[0]} — {f[2]}" for f in FASES_DEF],
                    index=fase_atual-1, key="lj_fase_sel_idx")
                fase_atual = int(fase_sel_idx.split()[1])

            fase_info = FASES_DEF[fase_atual - 1]
            st.markdown(f"**Jogando:** Fase {fase_info[0]} — {fase_info[2]} · {fase_info[1]} · ⏱️ {fase_info[4]} min")

            if st.button("▶ COMEÇAR DESAFIO", use_container_width=True):
                nome_sel = st.session_state.lj_personagem_sel
                dados_sel = PERSONAGENS[nome_sel]

                # Cenário anti-repetição
                hist_c = st.session_state.lj_historico_cenarios
                disponiveis = [x for x in CENARIOS_TODOS if x not in hist_c[-8:]]
                if not disponiveis: disponiveis = CENARIOS_TODOS
                cenario = _rand.choice(disponiveis)

                # Missão secreta
                missoes_fase = MISSOES_POR_FASE.get(fase_atual, MISSOES_POR_FASE[1])
                missao = _rand.choice(missoes_fase)

                # Histórico de aberturas e fichas anteriores para anti-repetição
                hist_ab = st.session_state.lj_historico_aberturas
                hist_ab_txt = " | ".join(hist_ab[-5:]) if hist_ab else "nenhuma"

                # Histórico de fichas para evitar repetição de assuntos/contextos
                hist_fichas = [p.get('ficha_resumo','') for p in st.session_state.lj_historico_partidas[-6:]]
                hist_fichas_txt = " | ".join(hist_fichas) if hist_fichas else "nenhuma"

                # Listas de variação para gerar fichas únicas
                profissoes_f   = ["designer","professora","nutricionista","arquiteta","jornalista","médica","advogada","engenheira","fotógrafa","chef de cozinha","publicitária","veterinária","terapeuta","psicóloga","empreendedora"]
                profissoes_m   = ["arquiteto","professor","médico","engenheiro","jornalista","fotógrafo","chef","publicitário","advogado","veterinário","empreendedor","designer","músico","psicólogo","produtor"]
                cidades_br     = ["São Paulo","Rio de Janeiro","Belo Horizonte","Florianópolis","Curitiba","Porto Alegre","Fortaleza","Salvador","Recife","Manaus","Goiânia","Brasília","Natal","Belém","Campinas"]
                musicas        = ["MPB","rock alternativo","pop","jazz","funk","sertanejo","indie","eletrônica","clássica","R&B","samba","reggae","bossa nova","trap","folk"]
                hobbies        = ["fotografia","culinária","corrida","yoga","leitura","viagens","séries","pintura","dança","academia","escalada","natação","jardinagem","teatro","meditação"]
                algo_hoje_lst  = ["derramei café na blusa","perdi o ônibus","achei R$20 no bolso da calça","minha bike furou","esqueci o carregador em casa","meu gato fugiu e voltou","queimei o almoço","recebi uma proposta de emprego","ganhei um elogio aleatório","vi um arco-íris","me perdi no GPS","minha reunião foi cancelada","encontrei um livro perdido","meu café da manhã ficou perfeito","choveu quando saí sem guarda-chuva"]
                sonhos         = ["morar um ano fora do Brasil","abrir meu próprio negócio","aprender a surfar","escrever um livro","viajar pela América do Sul de carro","aprender outro idioma","correr uma maratona","ter uma horta em casa","fazer um retiro de meditação","tocar um instrumento","fazer intercâmbio","voltar a estudar","adotar um cachorro","conhecer a Patagônia","aprender a cozinhar culinária asiática"]
                medos          = ["altura","falar em público","avião","perder pessoas importantes","fracassar","ficar sozinha para sempre","barata","dirigir na chuva","médico","dentista","escuro","se arrepender de decisões","perder o emprego","envelhecer","ser esquecida"]
                assuntos_ama   = ["viagens","gastronomia","filmes","música","psicologia","esportes","livros","moda","tecnologia","natureza","animais","arte","história","ciência","arquitetura"]
                assuntos_odeia = ["política partidária","fofoca","trânsito","segunda-feira","reuniões longas","fila","spam","spoiler","mansplaining","burocracia","barulho alto","fake news","pessoas que chegam atrasadas","preguiça","reclamação excessiva"]

                # Gera variações aleatórias únicas
                profissao_rand = _rand.choice(profissoes_f if nome_sel != "none" else profissoes_m)
                cidade_rand    = _rand.choice(cidades_br)
                musica_rand    = _rand.choice(musicas)
                hobby1, hobby2 = _rand.sample(hobbies, 2)
                algo_hoje      = _rand.choice(algo_hoje_lst)
                sonho_rand     = _rand.choice(sonhos)
                medo_rand      = _rand.choice(medos)
                assunto_ama    = _rand.choice(assuntos_ama)
                assunto_odeia  = _rand.choice(assuntos_odeia)

                # Gera data de aniversário única
                meses_br = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
                aniversario = f"{_rand.randint(1,28)} de {_rand.choice(meses_br)}"

                # Resumo da ficha para anti-repetição futura
                ficha_resumo = f"{profissao_rand}/{cidade_rand}/{hobby1}/{algo_hoje[:30]}"

                with st.spinner("Preparando a conversa..."):
                    # Gera ficha completa + primeira fala de uma vez
                    prompt_ficha = (
                        f"Você é {nome_sel}, {dados_sel['personalidade']}.\n"
                        f"Profissão: {profissao_rand}. Cidade: {cidade_rand}.\n"
                        f"Aniversário: {aniversario}.\n"
                        f"Música favorita: {musica_rand}. Hobbies: {hobby1} e {hobby2}.\n"
                        f"O que aconteceu com você hoje: {algo_hoje}.\n"
                        f"Sonho: {sonho_rand}. Maior medo: {medo_rand}.\n"
                        f"Assunto que ama: {assunto_ama}. Assunto que odeia: {assunto_odeia}.\n\n"
                        f"Cenário: {cenario}.\n"
                        f"Fase: {fase_info[2]} — {fase_info[3]}.\n\n"
                        f"Aberturas já usadas — NÃO repita nenhuma delas: {hist_ab_txt}\n"
                        f"Contextos anteriores — crie algo TOTALMENTE diferente: {hist_fichas_txt}\n\n"
                        f"Gere UMA primeira fala sua — 1-2 frases, natural, contextual ao cenário.\n"
                        f"Pode surgir de: algo que aconteceu hoje, o ambiente, uma situação no cenário.\n"
                        f"NÃO comece com 'Oi tudo bem'. Seja original e surpreendente.\n"
                        f"Retorne APENAS a fala, sem aspas."
                    )
                    primeira_fala = conexa_ia(prompt_ficha)
                    primeira_fala = primeira_fala.strip().strip('"').strip("'")

                # Monta ficha completa para o system de cada turno
                ficha_completa = {
                    "nome": nome_sel,
                    "profissao": profissao_rand,
                    "cidade": cidade_rand,
                    "aniversario": aniversario,
                    "musica": musica_rand,
                    "hobbies": [hobby1, hobby2],
                    "algo_hoje": algo_hoje,
                    "sonho": sonho_rand,
                    "medo": medo_rand,
                    "assunto_ama": assunto_ama,
                    "assunto_odeia": assunto_odeia,
                }

                # Registra anti-repetição
                st.session_state.lj_historico_cenarios.append(cenario)
                st.session_state.lj_historico_aberturas.append(primeira_fala[:50])

                # Inicia partida
                st.session_state.lj_ativo       = True
                st.session_state.lj_fase        = fase_atual
                st.session_state.lj_chat        = [{"role":"assistant","content":primeira_fala,"ts":_time.time()}]
                st.session_state.lj_conexo      = 100
                st.session_state.lj_atributos   = {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20}
                st.session_state.lj_inicio      = _time.time()
                st.session_state.lj_duracao     = fase_info[4] * 60
                st.session_state.lj_missao      = missao
                st.session_state.lj_missao_cumprida = False
                st.session_state.lj_arranques   = []
                st.session_state.lj_combo       = 0
                st.session_state.lj_ts_persona  = _time.time()
                st.session_state.lj_ts_usuario  = 0
                st.session_state.lj_cenario     = cenario
                st.session_state.lj_nome_persona  = nome_sel
                st.session_state.lj_dados_persona = dados_sel
                st.session_state.lj_ficha       = ficha_completa
                st.session_state.lj_ficha_resumo = ficha_resumo
                st.rerun()

            # Histórico de partidas
            if st.session_state.lj_historico_partidas:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📈 Histórico de Partidas")
                for h in reversed(st.session_state.lj_historico_partidas[-5:]):
                    taxa = h.get('conexo_final', 0)
                    cor_h = "#059669" if taxa >= 70 else ("#B45309" if taxa >= 40 else "#B91C1C")
                    st.markdown(f"<div class='hist-item'><span class='badge'>{h.get('personagem','?')}</span> Fase {h.get('fase','?')} · <small style='color:#888;'>{h.get('data','')}</small> <strong style='color:{cor_h};float:right;'>❤️ {taxa}</strong></div>", unsafe_allow_html=True)

        # ══════════════════════════════════════
        # PARTIDA ATIVA — TELA LIMPA
        # ══════════════════════════════════════
        else:
            chat      = st.session_state.lj_chat
            conexo    = st.session_state.lj_conexo
            fase_n    = st.session_state.lj_fase
            fase_info = FASES_DEF[fase_n - 1]
            nome_p    = st.session_state.lj_nome_persona
            dados_p   = st.session_state.lj_dados_persona
            cenario   = st.session_state.lj_cenario
            atribs    = st.session_state.lj_atributos

            duracao   = st.session_state.lj_duracao
            decorrido = _time.time() - st.session_state.lj_inicio
            restante  = max(0, duracao - decorrido)
            mins_r    = int(restante // 60)
            segs_r    = int(restante % 60)
            pct_tempo = max(0.0, 1 - decorrido / duracao)
            cor_timer = "#22C55E" if pct_tempo > 0.5 else ("#B45309" if pct_tempo > 0.2 else "#B91C1C")
            estado_label, estado_cor = estado_conexo(conexo)

            # 1. CENÁRIO — linha única discreta
            st.markdown(
                f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:8px;"
                f"padding:6px 14px;margin-bottom:8px;font-size:0.85em;'>"
                f"<strong style='color:#1A1A2E;'>📍 {cenario.capitalize()}</strong>"
                f"<span style='color:#94A3B8;margin-left:8px;font-size:0.88em;'>Você acaba de conhecer alguém.</span>"
                f"</div>",
                unsafe_allow_html=True
            )

            # 2. CHAT — container com scroll interno, sempre mostra o fim
            chat_html = "<div class='chat-scroll-container' id='chat-container'>"
            for msg in chat:
                if msg['role'] == 'user':
                    chat_html += f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>"
                else:
                    arr = msg.get('arranque','')
                    if arr:
                        chat_html += f"<div style='text-align:right;font-size:0.75em;color:#22C55E;font-weight:600;margin-bottom:1px;'>{arr}</div>"
                    chat_html += f"<div class='chat-persona'><b style='color:#1D4ED8;'>😊 {nome_p}:</b> {msg['content']}</div>"
            chat_html += "<div id='chat-bottom'></div></div>"
            chat_html += """
            <script>
                setTimeout(function(){
                    var c = document.getElementById('chat-container');
                    if(c) c.scrollTop = c.scrollHeight;
                }, 100);
            </script>"""
            st.markdown(chat_html, unsafe_allow_html=True)

            # 3. DICA SUTIL — só na fase 1 no primeiro turno
            turno_u = sum(1 for m in chat if m['role']=='user')
            if fase_n == 1 and turno_u == 0:
                st.markdown(
                    f"<div style='font-size:0.78em;color:#94A3B8;margin:4px 0;padding:4px 10px;"
                    f"border-left:2px solid #FFB6C1;'>💡 Comente o que {nome_p} disse ou faça uma pergunta relacionada.</div>",
                    unsafe_allow_html=True
                )

            # Alertas de estado (mínimos, só quando crítico)
            if 0 < conexo <= 20:
                st.markdown("<div style='font-size:0.8em;color:#B91C1C;font-weight:600;text-align:center;margin:4px 0;'>🚨 ÚLTIMA CHANCE — A conexão está caindo.</div>", unsafe_allow_html=True)
            if st.session_state.lj_missao_cumprida:
                st.markdown("<div style='font-size:0.75em;color:#22C55E;font-weight:600;text-align:center;margin:2px 0;'>🎯 MISSÃO CUMPRIDA!</div>", unsafe_allow_html=True)
            if st.session_state.lj_combo >= 3:
                st.markdown(f"<div style='font-size:0.8em;color:#B45309;font-weight:600;text-align:center;margin:2px 0;'>🔥 COMBO x{st.session_state.lj_combo}</div>", unsafe_allow_html=True)

            # Inatividade por fase
            INATIVIDADE = {1:60,2:50,3:40}
            QUEDA_INAT  = {1:3, 2:6, 3:10}
            ts_p = st.session_state.lj_ts_persona
            ts_u = st.session_state.lj_ts_usuario
            if ts_p > 0 and ts_u < ts_p:
                inat = _time.time() - ts_p
                lim  = INATIVIDADE.get(fase_n, 60)
                if inat > lim:
                    ciclos = int(inat / lim)
                    queda  = min(ciclos * QUEDA_INAT.get(fase_n, 5), 15)
                    novo_c = max(0, conexo - queda)
                    if novo_c != conexo:
                        st.session_state.lj_conexo = novo_c

            # 4. CONEXÔMETRO + TIMER — barra única colada antes do input
            cor_con = "#22C55E" if conexo>60 else ("#F59E0B" if conexo>30 else "#EF4444")
            st.markdown(f"""
            <div style='background:#FFFFFF;border:2px solid {cor_con};border-radius:10px;
            padding:8px 16px;margin-bottom:6px;display:flex;align-items:center;gap:12px;'>
                <span style='font-size:0.75em;color:#64748B;font-weight:600;white-space:nowrap;'>❤️ CONEXÔMETRO</span>
                <div style='flex:1;background:#F1F5F9;border-radius:999px;height:10px;overflow:hidden;'>
                    <div style='height:100%;border-radius:999px;background:{cor_con};width:{conexo}%;'></div>
                </div>
                <span style='font-size:1em;font-weight:700;color:{cor_con};white-space:nowrap;'>{conexo} {estado_label}</span>
                <span style='font-size:0.75em;color:#64748B;border-left:1px solid #E2E8F0;padding-left:12px;white-space:nowrap;'>⏱️</span>
                <span style='font-size:1.1em;font-weight:700;color:{cor_timer};white-space:nowrap;'>{mins_r:02d}:{segs_r:02d}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── VERIFICAR FIM ──
            tempo_esgotado = restante <= 0
            conexo_zero    = conexo <= 0

            if tempo_esgotado or conexo_zero:
                motivo = "tempo" if tempo_esgotado else "conexao"
                hist_txt = "\n".join(f"{'Você' if m['role']=='user' else nome_p}: {m['content']}" for m in chat)
                n_arr = len(st.session_state.lj_arranques)
                turno_u = sum(1 for m in chat if m['role']=='user')

                # Verifica critérios de passagem
                _, _, _, _, _, titulo_fase, min_c, min_n, min_i = fase_info
                passou = (
                    conexo >= min_c and
                    atribs.get('naturalidade',0) >= min_n and
                    atribs.get('interesse',0) >= min_i and
                    turno_u >= 4 and
                    motivo == "tempo"
                )

                prompt_aval = (
                    f"Avalie esta conversa de treinamento social — {fase_info[2]}.\n"
                    f"Personagem: {nome_p} ({dados_p['personalidade']}).\n"
                    f"Motivo encerramento: {'tempo esgotado' if motivo=='tempo' else 'conexão zerou'}.\n"
                    f"Conexão final: {conexo}. Arranques: {n_arr}. Turnos do usuário: {turno_u}.\n"
                    f"Missão secreta: '{st.session_state.lj_missao}' — cumprida: {st.session_state.lj_missao_cumprida}\n\n"
                    f"Conversa:\n{hist_txt}\n\n"
                    f"RETORNE JSON (sem markdown):\n"
                    f'{{"aprovado":{"true" if passou else "true/false"},"nota_atracao":0,"nota_conexao":0,"nota_naturalidade":0,"nota_confianca":0,"nota_timing":0,"nota_leitura":0,"ponto_forte":"1 frase","melhorar":"1 frase","perfil_estilo":"um dos: O Confiante/O Estrategista/O Divertido/O Conquistador/O Reservado","missao_cumprida":true/false}}'
                )
                with st.spinner("Avaliando..."):
                    aval_txt = conexa_ia(prompt_aval)
                    try:
                        jm = _re.search(r'\{.*\}', aval_txt, _re.DOTALL)
                        aval_d = _json.loads(jm.group(0)) if jm else {}
                    except:
                        aval_d = {}

                aprovado = passou and aval_d.get('aprovado', passou)
                missao_ok = aval_d.get('missao_cumprida', False)
                perfil = aval_d.get('perfil_estilo', '')

                if aprovado:
                    novo_fases = min(st.session_state.lj_fases_concluidas + 1, 3)
                    st.session_state.lj_fases_concluidas = max(st.session_state.lj_fases_concluidas, fase_n)
                    # Desbloqueia personagem
                    if fase_n >= 1 and "Camila" not in st.session_state.lj_personagens_desbloqueadas:
                        st.session_state.lj_personagens_desbloqueadas.append("Camila")
                    if fase_n >= 2 and "Helena" not in st.session_state.lj_personagens_desbloqueadas:
                        st.session_state.lj_personagens_desbloqueadas.append("Helena")
                    # Título
                    _, _, _, _, _, titulo_fase, *_ = fase_info
                    st.session_state.lj_titulo = titulo_fase
                if perfil:
                    st.session_state.lj_perfil_estilo = perfil

                # Salva resultado
                st.session_state.lj_aval = {
                    'aprovado': aprovado,
                    'titulo': f"FASE {fase_n} CONCLUÍDA! 🎉" if aprovado else f"CONEXÃO PERDIDA 💥",
                    'conexo_final': conexo,
                    'n_arranques': n_arr,
                    'missao_cumprida': missao_ok,
                    'ponto_forte': aval_d.get('ponto_forte','—'),
                    'melhorar': aval_d.get('melhorar','—'),
                    'nota_atracao': aval_d.get('nota_atracao',0),
                    'nota_conexao': aval_d.get('nota_conexao',0),
                    'nota_naturalidade': aval_d.get('nota_naturalidade',0),
                    'nota_confianca': aval_d.get('nota_confianca',0),
                    'nota_timing': aval_d.get('nota_timing',0),
                    'nota_leitura': aval_d.get('nota_leitura',0),
                }
                st.session_state.lj_historico_partidas.append({
                    'fase': fase_n, 'personagem': nome_p,
                    'conexo_final': conexo, 'aprovado': aprovado,
                    'data': datetime.now().strftime('%d/%m %H:%M'),
                    'ficha_resumo': st.session_state.get('lj_ficha_resumo',''),
                })
                st.session_state.lj_ativo   = False
                st.session_state.lj_chat    = []
                st.rerun()

            elif conexo > 0:
                # ── INPUT ──
                msg_labia = st.text_input("", key=f"lj_input_{len(chat)}",
                    placeholder="O que você diz?", label_visibility="collapsed")

                col_e, col_ab = st.columns([4,1])
                with col_e:
                    if st.button("📤 ENVIAR", key="lj_enviar", use_container_width=True):
                        if msg_labia.strip():
                            ts_user = _time.time()
                            st.session_state.lj_ts_usuario = ts_user

                            # ── SYSTEM DO PERSONAGEM — usa ficha única da partida ──
                            ficha = st.session_state.get('lj_ficha', {})
                            aniv_p    = ficha.get('aniversario','data não definida')
                            prof_p    = ficha.get('profissao','')
                            cidade_p  = ficha.get('cidade','')
                            musica_p  = ficha.get('musica','')
                            hobbies_p = ', '.join(ficha.get('hobbies',[]))
                            hoje_p    = ficha.get('algo_hoje','')
                            sonho_p   = ficha.get('sonho','')
                            medo_p    = ficha.get('medo','')
                            ama_p     = ficha.get('assunto_ama','')
                            odeia_p   = ficha.get('assunto_odeia','')

                            # Detecta pergunta pessoal
                            kws_pes = ['aniversário','aniversario','cidade','mora','trabalha','profissão',
                                       'profissao','música','musica','hobby','hobbies','medo','sonho',
                                       'chama','nome']
                            aviso_pes = (
                                f"\n⚠️ PERGUNTA PESSOAL: responda conforme seus dados — "
                                f"Aniversário={aniv_p}, Cidade={cidade_p}, Profissão={prof_p}."
                            ) if any(k in msg_labia.lower() for k in kws_pes) else ""

                            lembrete = (
                                f"\n\nSEUS DADOS FIXOS (nunca mude nem contradiga):\n"
                                f"Nome: {nome_p} | Profissão: {prof_p} | Cidade: {cidade_p}\n"
                                f"Aniversário: {aniv_p}\n"
                                f"Música: {musica_p} | Hobbies: {hobbies_p}\n"
                                f"Hoje: {hoje_p}\n"
                                f"Sonho: {sonho_p} | Medo: {medo_p}\n"
                                f"Ama falar de: {ama_p} | Odeia: {odeia_p}"
                            )

                            system_p = (
                                f"Você é {nome_p}, {prof_p}, morando em {cidade_p}.\n"
                                f"Personalidade: {dados_p['personalidade']}.\n"
                                f"Aniversário: {aniv_p}. Hoje: {hoje_p}.\n"
                                f"Cenário: {cenario}.\n\n"
                                f"COMO RESPONDER:\n"
                                f"- Maximo 10 palavras. Estilo mensagem de WhatsApp.\n"
                                f"- Direta, humana, contextual ao que a pessoa disse\n"
                                f"- Pode ter emoji se fizer sentido\n"
                                f"- Nao explique. Nao filosofe. So reaja.\n"
                                f"- {'Seja receptiva' if fase_n==1 else 'Seja mais seletiva'}\n"
                                f"- NUNCA revele que e IA"
                                + lembrete + aviso_pes
                            )
                            # Última fala do personagem e última do usuário — foco no turno atual
                            ultima_fala_persona = next((m['content'] for m in reversed(chat) if m['role']=='assistant'), '')
                            penultima_user = [m['content'] for m in chat if m['role']=='user']
                            penultima_user = penultima_user[-1] if penultima_user else ''

                            # Só as últimas 6 mensagens — evita o modelo ficar preso em assuntos antigos
                            historico = [{"role":m["role"],"content":m["content"]} for m in chat[-6:]]

                            # Injeta lembrete de foco no final do system
                            foco_atual = (
                                f"\n\nTURNO ATUAL:\n"
                                f"Você acabou de dizer: \"{ultima_fala_persona}\"\n"
                                f"A pessoa respondeu: \"{msg_labia}\"\n"
                                f"Responda ESPECIFICAMENTE a isso. Ignore o histórico anterior se ele não for relevante.\n"
                                f"Se a resposta da pessoa for curta, vaga ou mudar de assunto — acompanhe naturalmente.\n"
                                f"Se tiver erro de digitação, reaja com humor ou ignore — nunca finja que entendeu algo que não foi dito."
                            )

                            system_p = (
                                f"Você é {nome_p}, {prof_p}, morando em {cidade_p}.\n"
                                f"Personalidade: {dados_p['personalidade']}.\n"
                                f"Aniversário: {aniv_p}. Hoje: {hoje_p}.\n"
                                f"Cenário: {cenario}.\n\n"
                                f"COMO VOCÊ CONVERSA:\n"
                                f"- Você reage ao que a pessoa acabou de dizer — não ao que você disse antes\n"
                                f"- Máximo 1-2 frases curtas e naturais (10 a 35 palavras)\n"
                                f"- Não explique seus pensamentos — reaja e pronto\n"
                                f"- Não termine sempre com pergunta\n"
                                f"- Se a pessoa mudar de assunto, mude também — sem resistência\n"
                                f"- Reaja como uma pessoa inteligente e presente reagiria: percebe o que está sendo dito, responde ao tom\n"
                                f"- Se receber 'está aí?', 'oi', 'ok', responda curto e humano — 'Estou sim 😄' ou 'Aqui 😊'\n"
                                f"- Se receber erro de digitação óbvio, brinque levemente ou pergunte o que quis dizer\n"
                                f"- {'Seja aberta e receptiva' if fase_n==1 else 'Seja mais seletiva'}\n"
                                f"- NUNCA revele que é IA"
                                + lembrete + aviso_pes + foco_atual
                            )
                            with st.spinner(""):
                                try:
                                    msgs_p = [{"role":"system","content":system_p}] + historico + [{"role":"user","content":msg_labia}]
                                    msgs_p_safe = [{"role":m["role"],"content":m["content"].encode("utf-8","ignore").decode("utf-8")} for m in msgs_p]
                                    resp = client.chat.completions.create(messages=msgs_p_safe, model="llama-3.3-70b-versatile", max_tokens=30)
                                    resp_txt = resp.choices[0].message.content.strip()
                                    # Remove frases explicativas longas que o modelo adiciona
                                    resp_txt = resp_txt.split('\n')[0].strip()
                                except:
                                    resp_txt = "É mesmo?"

                            # ── AVALIADOR INVISÍVEL ──
                            # Critérios específicos por fase
                            tempo_resp = int(_time.time() - st.session_state.lj_ts_persona)
                            ultima_fala_av = chat[-1]['content'] if chat else ''

                            criterios_fase = {
                                1: (
                                    "FASE 1 — ATRAÇÃO. Avalie:\n"
                                    "CURIOSIDADE (+): despertou vontade de saber mais sobre ele?\n"
                                    "HUMOR (+): criou leveza ou momento divertido?\n"
                                    "ORIGINALIDADE (+): evitou perguntas previsíveis?\n"
                                    "CONFIANCA (+): falou com segurança sem forçar?\n"
                                    "RECIPROCIDADE (+): demonstrou interesse nela?\n"
                                    "PENALIZE: monossílabos, sequência de perguntas, tentar impressionar.\n"
                                    "Excelente: +15 a +25 | Bom: +5 a +14 | Neutro: -2 a +4 | Ruim: -5 a -12 | Péssimo: -13 a -25\n"
                                    "SEJA GENEROSO — iniciantes merecem crédito por tentativas sinceras."
                                ),
                                2: (
                                    "FASE 2 — CONEXÃO EMOCIONAL. Avalie:\n"
                                    "ESCUTA (+): reagiu ao que ela disse ou ignorou?\n"
                                    "EMPATIA (+): demonstrou compreensão antes de falar de si?\n"
                                    "PROFUNDIDADE (+): foi além do superficial?\n"
                                    "RECIPROCIDADE (+): compartilhou algo pessoal depois dela se abrir?\n"
                                    "PENALIZE FORTE: ignorar abertura emocional, resolver o problema dela, falar de si quando ela se abriu.\n"
                                    "Excelente: +12 a +22 | Bom: +4 a +11 | Neutro: -3 a +3 | Ruim: -6 a -14 | Péssimo: -15 a -28\n"
                                    "SEJA MODERADO — mais exigente que fase 1."
                                ),
                                3: (
                                    "FASE 3 — SEDUÇÃO. Avalie:\n"
                                    "TIMING (+): respondeu no momento certo?\n"
                                    "LEITURA DE SINAIS (+): percebeu o estado emocional e reagiu?\n"
                                    "TENSAO (+): criou flerte leve sem ser vulgar?\n"
                                    "CONFIANCA (+): respondeu provocações com segurança e humor?\n"
                                    "PENALIZE FORTE: insistência após recuo, vulgaridade, tentar impressionar, perder o fio.\n"
                                    f"Tempo: {tempo_resp}s — acima de 20s penaliza levemente.\n"
                                    "Excepcional: +15 a +25 | Bom: +5 a +14 | Neutro: -4 a +4 | Ruim: -7 a -16 | Péssimo: -17 a -30\n"
                                    "SEJA EXIGENTE — só respostas realmente boas sobem."
                                ),
                            }

                            arranques_fase = {
                                1: ["🧲 CURIOSIDADE DESPERTADA","😄 MOMENTO DE HUMOR","✨ ORIGINALIDADE","💪 CONFIANÇA NATURAL","🎯 GANCHO PERFEITO","🚀 ARRANQUE!"],
                                2: ["❤️ CONEXÃO CRIADA","👂 ESCUTA GENUÍNA","🧠 PROFUNDIDADE","🔄 RECIPROCIDADE","💎 MOMENTO ESPECIAL","🚀 ARRANQUE!"],
                                3: ["🔥 TENSÃO CRIADA","😏 FLERTE NATURAL","⚡ TIMING PERFEITO","👀 LEITURA CORRETA","👑 MOVIMENTO MESTRE","🚀 ARRANQUE!"],
                            }
                            arr_disp = arranques_fase.get(fase_n, arranques_fase[1])

                            prompt_eval = (
                                f"Você é o avaliador invisível do Mestre da Lábia. Analise com precisão.\n\n"
                                f"PERSONAGEM: {nome_p} — {dados_p['personalidade']}\n"
                                f"CENÁRIO: {cenario}\n"
                                f"ATRIBUTOS ATUAIS: {atribs}\n\n"
                                f"ELA DISSE: \"{ultima_fala_av}\"\n"
                                f"USUÁRIO RESPONDEU: \"{msg_labia}\"\n"
                                f"TEMPO: {tempo_resp}s\n\n"
                                f"{criterios_fase.get(fase_n, criterios_fase[1])}\n\n"
                                f"MISSÃO SECRETA: '{st.session_state.lj_missao}'\n\n"
                                f"RETORNE APENAS JSON sem markdown:\n"
                                + '{"delta":0,"interesse":50,"atracao":50,"conexao":50,"confianca":50,"naturalidade":50,"curiosidade":50,"tensao":20,"arranque":"","missao_cumprida":false}' + "\n\n"
                                f"arranque: se delta>=12 escolha um de {arr_disp} e formate 'EMOJI +DELTA NOME'. Senão vazio.\n"
                                f"missao_cumprida: true SOMENTE se esta mensagem cumpriu a missão."
                            )

                            with st.spinner(""):
                                try:
                                    eval_txt = conexa_ia(prompt_eval.encode("utf-8", errors="ignore").decode("utf-8"))
                                    jm2 = _re.search(r'\{.*\}', eval_txt, _re.DOTALL)
                                    eval_d = _json.loads(jm2.group(0)) if jm2 else {}
                                except:
                                    eval_d = {}

                            delta = eval_d.get('delta', 0)
                            arranque = eval_d.get('arranque', '')

                            # Atualiza atributos
                            for k in ['interesse','atracao','conexao','confianca','naturalidade','curiosidade','tensao']:
                                if k in eval_d:
                                    atribs[k] = max(0, min(100, eval_d[k]))
                            st.session_state.lj_atributos = atribs

                            # Conexômetro
                            novo_conexo = max(0, min(100, conexo + delta))
                            st.session_state.lj_conexo = novo_conexo

                            # Missão
                            if eval_d.get('missao_cumprida'):
                                st.session_state.lj_missao_cumprida = True

                            # Combo e arranques
                            if delta > 5:
                                st.session_state.lj_combo += 1
                            else:
                                st.session_state.lj_combo = 0
                            if arranque:
                                st.session_state.lj_arranques.append(arranque)

                            # Efeito de digitação
                            placeholder_dig = st.empty()
                            palavras_resp = resp_txt.split()
                            texto_acum = ""
                            for palavra in palavras_resp:
                                texto_acum += ("" if texto_acum=="" else " ") + palavra
                                placeholder_dig.markdown(
                                    f"<div class='chat-persona'><b style='color:#1D4ED8;'>👩 {nome_p}:</b> {texto_acum}▌</div>",
                                    unsafe_allow_html=True
                                )
                                _time.sleep(0.06)
                            placeholder_dig.empty()

                            chat.append({"role":"user","content":msg_labia,"ts":ts_user,"delta":delta})
                            chat.append({"role":"assistant","content":resp_txt,"ts":_time.time(),"arranque":arranque})
                            st.session_state.lj_chat = chat
                            st.session_state.lj_ts_persona = _time.time()
                            st.rerun()

                with col_ab:
                    if st.button("🚩 Sair", key="lj_sair", use_container_width=True):
                        st.session_state.lj_ativo = False
                        st.session_state.lj_chat  = []
                        st.rerun()

                # Auto-refresh
                _time.sleep(0.8)
                st.rerun()

        # ── RESULTADO ──
        if st.session_state.lj_aval and not st.session_state.lj_ativo:
            aval = st.session_state.lj_aval
            aprovado = aval.get('aprovado', False)
            cor_card = "card-green" if aprovado else "card-red"

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            if aprovado:
                _, _, _, _, _, titulo_f, *_ = FASES_DEF[st.session_state.lj_fases_concluidas-1] if st.session_state.lj_fases_concluidas > 0 else FASES_DEF[0]
                st.markdown(f"<div class='card-green' style='text-align:center;'><div style='font-size:1.5em;font-weight:700;color:#14532D;'>🎉 {aval['titulo']}</div><div style='color:#14532D;margin-top:4px;'>Você ganhou o título: <strong>{st.session_state.lj_titulo}</strong></div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='card-red' style='text-align:center;'><div style='font-size:1.3em;font-weight:700;color:#7F1D1D;'>💥 {aval['titulo']}</div></div>", unsafe_allow_html=True)

            # Notas por critério
            notas = [
                ("🧲 Atração", aval.get('nota_atracao',0)),
                ("❤️ Conexão", aval.get('nota_conexao',0)),
                ("🗣️ Naturalidade", aval.get('nota_naturalidade',0)),
                ("💪 Confiança", aval.get('nota_confianca',0)),
                ("⏱️ Timing", aval.get('nota_timing',0)),
                ("👀 Leitura", aval.get('nota_leitura',0)),
            ]
            cols_n = st.columns(6)
            for i, (label, nota) in enumerate(notas):
                cor_n = "#22C55E" if nota>=70 else ("#F59E0B" if nota>=50 else "#EF4444")
                with cols_n[i]:
                    st.markdown(f"<div style='text-align:center;'><div style='font-size:0.7em;color:#64748B;'>{label}</div><div style='font-size:1.3em;font-weight:700;color:{cor_n};'>{nota}</div></div>", unsafe_allow_html=True)

            st.markdown(f"<div style='margin-top:10px;font-size:0.88em;color:#1A1A2E;'>✅ {aval.get('ponto_forte','')}<br>⚠️ {aval.get('melhorar','')}</div>", unsafe_allow_html=True)

            if aval.get('missao_cumprida'):
                st.markdown(f"<div class='card-yellow' style='padding:8px 14px;font-size:0.85em;'>🎯 <strong>MISSÃO SECRETA CUMPRIDA!</strong></div>", unsafe_allow_html=True)

            if st.session_state.lj_perfil_estilo:
                perfil = st.session_state.lj_perfil_estilo
                st.markdown(f"<div class='card-blue' style='padding:10px 14px;'><strong>🧠 Seu perfil: {perfil}</strong><br><small>{PERFIS_ESTILO.get(perfil,'')}</small></div>", unsafe_allow_html=True)

            if st.button("▶ CONTINUAR", key="lj_continuar", use_container_width=True):
                st.session_state.lj_aval = None; st.rerun()

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
