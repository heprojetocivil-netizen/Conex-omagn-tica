import streamlit as st
from groq import Groq
from datetime import datetime, date
import json
import random

st.set_page_config(page_title="CONEXA IA", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
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
    # Mestre da Lábia
    'lj_fase': 1, 'lj_personagem_sel': 'Rafaela',
    'lj_ativo': False, 'lj_chat': [], 'lj_conexo': 100,
    'lj_atributos': {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20},
    'lj_inicio': 0, 'lj_duracao': 300,
    'lj_missao': '', 'lj_missao_cumprida': False,
    'lj_aval': None, 'lj_arranques': [],
    'lj_historico_cenarios': [], 'lj_historico_aberturas': [],
    'lj_ts_persona': 0, 'lj_ts_usuario': 0,
    'lj_combo': 0,
    'lj_fases_concluidas': 0,
    'lj_titulo': 'Paquerador',
    'lj_personagens_desbloqueadas': ['Rafaela'],
    'lj_perfil_estilo': None,
    'lj_historico_partidas': [],
    'lj_desbloqueado': False,
    'lj_ficha': {}, 'lj_ficha_resumo': '',
    'lj_nome_persona': '', 'lj_dados_persona': {},
    'lj_cenario': '', 'lj_cenario_label': '',
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
            model="openai/gpt-oss-120b",
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
        st.download_button("💾 SALVAR DADOS (.json)", data=gerar_json(),
            file_name=f"conexa_{nome_u}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================
# ── CONSTANTES GLOBAIS ──
FASES_DEF_G = [
    # (num, nome,             mins, titulo,          min_conexao, min_natural, min_interesse)
    (1, "ATRACAO",           5,  "Paquerador",      70, 60, 65),
    (2, "CONEXAO EMOCIONAL", 7,  "Galanteador",     75, 70, 65),
    (3, "SEDUCAO",           10, "Mestre da Labia", 80, 75, 70),
]
# Índices: [0]=num [1]=nome [2]=mins [3]=titulo [4]=min_conexao [5]=min_natural [6]=min_interesse

def estado_conexo_g(val):
    if val >= 80: return "CONEXAO FORTE", "#DC2626"
    if val >= 60: return "BOA QUIMICA", "#F59E0B"
    if val >= 40: return "NEUTRO", "#64748B"
    if val >= 20: return "INTERESSE CAINDO", "#EA580C"
    if val >= 1:  return "ULTIMA CHANCE", "#7F1D1D"
    return "ELIMINADA", "#000000"

PERSONAGENS = {
    "Rafaela": {
        "emoji": "😊", "dificuldade": 2, "estrelas": "⭐⭐",
        "desc": "Simpática, inteligente, bem-humorada. Conversa naturalmente mas não demonstra interesse imediatamente.",
        "personalidade": "simpatica, inteligente, bem-humorada, curiosa, fala de forma leve e natural",
        "humor": 80, "receptividade": 70, "provocacao": 30, "exigencia": 40, "bloqueada": False,
    },
    "Camila": {
        "emoji": "😏", "dificuldade": 4, "estrelas": "⭐⭐⭐⭐",
        "desc": "Segura, provocadora, responde com ironia e testa a confiança do usuário.",
        "personalidade": "segura, ironica, provocadora, testa confianca, nao facilita",
        "humor": 70, "receptividade": 45, "provocacao": 80, "exigencia": 70, "bloqueada": True,
    },
    "Helena": {
        "emoji": "🧐", "dificuldade": 5, "estrelas": "⭐⭐⭐⭐⭐",
        "desc": "Sofisticada, seletiva, difícil de impressionar. Exige conversa mais inteligente.",
        "personalidade": "sofisticada, seletiva, intelectual, dificil de impressionar, exige profundidade",
        "humor": 55, "receptividade": 30, "provocacao": 60, "exigencia": 90, "bloqueada": True,
    },
}

MISSOES_POR_FASE = {
    1: ["Fazer ela fazer uma pergunta espontânea sobre você","Conseguir que ela demonstre curiosidade","Criar um momento de humor","Fazer ela contar algo pessoal"],
    2: ["Fazer ela lembrar algo que você disse antes","Conseguir que ela compartilhe um sonho","Criar um momento de empatia genuína","Fazer ela admitir algo que normalmente não diria"],
    3: ["Criar um momento de flerte natural","Fazer ela brincar com você","Criar uma brincadeira interna entre vocês","Fazer ela perguntar algo pessoal espontaneamente"],
}

CENARIOS_TODOS = [
    "cafeteria","parque","livraria","fila de evento","shopping","feira",
    "exposicao de arte","aeroporto","praca","academia","show de musica",
    "festa de aniversario","mercado","galeria","coworking","food court",
    "banca de jornal","pet shop","sebo de livros","farmacia","bancada de bar",
    "fila de banco","salao de beleza","loja de discos","jardim botanico",
    "estacao de metro","calcadao","praia","aluguel de bicicletas","museu"
]

PERFIS_ESTILO = {
    "O Confiante":     "Fala com segurança, mas às vezes avança rápido demais.",
    "O Estrategista":  "Faz boas perguntas e lê bem os sinais.",
    "O Divertido":     "Usa humor para criar conexão.",
    "O Conquistador":  "Cria conexão emocional rapidamente.",
    "O Reservado":     "Tem boas respostas, mas demonstra pouco interesse.",
}

if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🧠 CONEXA IA")
        st.markdown("**Inteligência para conversas, comunicação e conexões.**")
        st.markdown("*Entenda melhor. Comunique-se melhor. Saiba o que fazer a seguir.*")

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
                faixa_p = dp.get("faixa_atual", 1) if dp else 1
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
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        if not perfis:
            st.markdown("#### Vamos configurar seu Conexa")

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")
        arq = st.file_uploader("Restaurar dados (.json):", type=["json"], key="upload_login")

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

elif st.session_state.etapa == "App":
    faixa = FAIXAS[min(st.session_state.faixa_atual-1, 6)]
    em_partida = st.session_state.get('pagina') == 'Dialogo'

    if not em_partida:
        barra_salvar()
        # ── NAVBAR ──
        cols1 = st.columns(7)
        nav1 = [("🏠","Home"),("⚡","Rapida"),("🃏","Carta"),("💬","Turbinar"),("🧠","Analisar"),("🎭","Roleplay"),("💋","Labia")]
        lb1 = {"Home":"Dashboard","Rapida":"Resposta Rápida","Carta":"Carta na Manga",
               "Turbinar":"Turbinar Mensagem","Analisar":"Raio-X da Conversa",
               "Roleplay":"Simulador de Conversa","Labia":"💋 Mestre da Lábia ⭐"}
        for i,(ic,pg) in enumerate(nav1):
            ch = list(lb1.keys())[i]
            if cols1[i].button(ic, key=f"nav1_{ch}", help=lb1[ch]):
                st.session_state.pagina = ch; st.rerun()
        st.markdown("""
        <style>@keyframes pisca{0%{opacity:1}50%{opacity:.5}100%{opacity:1}}
        .labia-hint{text-align:right;font-size:.7em;font-weight:700;color:#C2185B;
        animation:pisca 2s ease-in-out infinite;margin-top:-4px;}
        </style><div class='labia-hint'>💋 ← Mestre da Lábia ⭐</div>
        """, unsafe_allow_html=True)
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

    # ── ROTEAMENTO ──
    if st.session_state.pagina == "Dialogo":
        import time as _t, json as _j, re as _r

        # Esconde header do Streamlit
        st.markdown("""
        <style>
        header[data-testid="stHeader"]{display:none!important;}
        #MainMenu{display:none!important;}
        [data-testid="stToolbar"]{display:none!important;}
        footer{display:none!important;}
        .block-container{padding-top:0.5rem!important;padding-bottom:0.5rem!important;}
        </style>""", unsafe_allow_html=True)

        # Redireciona se não há partida ativa
        if not st.session_state.get('lj_ativo') or not st.session_state.get('lj_nome_persona') or st.session_state.get('lj_inicio',0)==0:
            st.session_state.pagina="Labia"; st.rerun()

        chat     = st.session_state.lj_chat
        conexo   = st.session_state.lj_conexo
        fase_n   = st.session_state.lj_fase
        nome_p   = st.session_state.lj_nome_persona
        dados_p  = st.session_state.lj_dados_persona
        cenario  = st.session_state.lj_cenario
        ficha    = st.session_state.lj_ficha
        atribs   = st.session_state.lj_atributos

        FASES_D  = {1:(5,70,60,65,"🥉 Paquerador"),2:(7,75,70,65,"🥈 Galanteador"),3:(10,80,75,70,"👑 Mestre da Lábia")}
        fi       = FASES_D[fase_n]
        duracao  = fi[0]*60
        inicio   = st.session_state.lj_inicio
        decorrido= _t.time() - inicio
        restante = max(0, duracao - decorrido)
        mins_r   = int(restante//60); segs_r = int(restante%60)
        pct_t    = max(0.0, 1-decorrido/duracao)
        cor_t    = "#22C55E" if pct_t>0.5 else ("#B45309" if pct_t>0.2 else "#B91C1C")
        cor_c    = "#22C55E" if conexo>60 else ("#F59E0B" if conexo>30 else "#EF4444")

        # Estado
        def estado(v):
            if v>=80: return "🔥 CONEXÃO FORTE"
            if v>=60: return "❤️ BOA QUÍMICA"
            if v>=40: return "😐 NEUTRO"
            if v>=20: return "⚠️ CAINDO"
            return "🚨 ÚLTIMA CHANCE"

        # CENÁRIO
        st.markdown(f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:8px;padding:6px 14px;margin-bottom:6px;font-size:0.85em;'><strong>📍 {cenario.capitalize()}</strong> <span style='color:#94A3B8;'>— Você acaba de conhecer alguém.</span></div>", unsafe_allow_html=True)

        # CHAT com scroll
        chat_html = "<div class='chat-scroll-container' id='chat-c'>"
        for msg in chat:
            if msg['role']=='user':
                chat_html += f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>"
            else:
                arr = msg.get('arranque','')
                if arr: chat_html += f"<div style='text-align:right;font-size:0.75em;color:#22C55E;font-weight:600;'>{arr}</div>"
                chat_html += f"<div class='chat-persona'><b style='color:#1D4ED8;'>😊 {nome_p}:</b> {msg['content']}</div>"
        chat_html += "<div id='cb'></div></div>"
        chat_html += "<script>setTimeout(()=>{var c=document.getElementById('chat-c');if(c)c.scrollTop=c.scrollHeight;},80);</script>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # Dica fase 1
        turno_u = sum(1 for m in chat if m['role']=='user')
        if fase_n==1 and turno_u==0:
            st.markdown(f"<div style='font-size:0.75em;color:#94A3B8;padding:2px 10px;border-left:2px solid #FFB6C1;margin:4px 0;'>💡 Comente o que {nome_p} disse.</div>", unsafe_allow_html=True)

        # Alertas
        if 0 < conexo <= 20:
            st.markdown("<div style='font-size:0.8em;color:#B91C1C;font-weight:600;text-align:center;'>🚨 ÚLTIMA CHANCE</div>", unsafe_allow_html=True)
        if st.session_state.lj_missao_cumprida:
            st.markdown("<div style='font-size:0.75em;color:#22C55E;font-weight:600;text-align:center;'>🎯 MISSÃO CUMPRIDA!</div>", unsafe_allow_html=True)

        # Inatividade
        ts_p = st.session_state.lj_ts_persona; ts_u = st.session_state.lj_ts_usuario
        INAT = {1:60,2:50,3:40}; QINAT = {1:3,2:6,3:10}
        if ts_p>0 and ts_u<ts_p:
            inat = _t.time()-ts_p
            if inat > INAT.get(fase_n,60):
                queda = min(int(inat/INAT.get(fase_n,60))*QINAT.get(fase_n,5),15)
                novo_c = max(0,conexo-queda)
                if novo_c!=conexo: st.session_state.lj_conexo=novo_c

        # CONEXÔMETRO + TIMER
        st.markdown(f"""
        <div style='background:#fff;border:2px solid {cor_c};border-radius:10px;padding:7px 14px;margin-bottom:5px;display:flex;align-items:center;gap:10px;'>
        <span style='font-size:0.72em;color:#64748B;font-weight:600;white-space:nowrap;'>❤️ CONEXÔMETRO</span>
        <div style='flex:1;background:#F1F5F9;border-radius:999px;height:9px;overflow:hidden;'>
        <div style='height:100%;border-radius:999px;background:{cor_c};width:{conexo}%;'></div></div>
        <span style='font-size:0.95em;font-weight:700;color:{cor_c};white-space:nowrap;'>{conexo} {estado(conexo)}</span>
        <span style='color:#94A3B8;border-left:1px solid #E2E8F0;padding-left:10px;font-size:0.72em;'>⏱️</span>
        <span style='font-size:1em;font-weight:700;color:{cor_t};white-space:nowrap;'>{mins_r:02d}:{segs_r:02d}</span>
        </div>""", unsafe_allow_html=True)

        # FIM
        if restante<=0 or conexo<=0:
            hist_txt = "\n".join(f"{'Você' if m['role']=='user' else nome_p}: {m['content']}" for m in chat)
            n_arr = len(st.session_state.lj_arranques)
            mc,mn,mi,_ ,titulo_fase = fi[1],fi[2],fi[3],fi[0],fi[4]
            passou = (conexo>=mc and atribs.get('naturalidade',0)>=mn and atribs.get('interesse',0)>=mi and turno_u>=4 and restante<=0)

            prompt_av = (
                f"Avalie conversa de treinamento — Fase {fase_n}.\n"
                f"Personagem:{nome_p}. Conexao:{conexo}. Arranques:{n_arr}. Turnos:{turno_u}.\n"
                f"Missao:'{st.session_state.lj_missao}' — cumprida:{st.session_state.lj_missao_cumprida}\n"
                f"Conversa:\n{hist_txt}\n\n"
                f"JSON sem markdown:\n"
                + '{"aprovado":false,"ponto_forte":"1 frase","melhorar":"1 frase","perfil":"O Confiante","missao_ok":false}'
            )
            with st.spinner("Avaliando..."):
                try:
                    av_txt = conexa_ia(prompt_av)
                    jm = _r.search(r'\{.*\}',av_txt,_r.DOTALL)
                    av_d = _j.loads(jm.group(0)) if jm else {}
                except: av_d = {}

            aprovado = passou and av_d.get('aprovado',passou)
            if aprovado:
                st.session_state.lj_fases_ok = max(st.session_state.lj_fases_ok, fase_n)
                nomes_pers = ["Rafaela","Camila","Helena"]
                for i in range(min(fase_n,3)):
                    if nomes_pers[i] not in st.session_state.lj_personagens_ok:
                        st.session_state.lj_personagens_ok.append(nomes_pers[i])
                TITULOS = {1:"🥉 Paquerador",2:"🥈 Galanteador",3:"👑 Mestre da Lábia"}
                st.session_state.lj_titulo = TITULOS[fase_n]

            st.session_state.lj_aval = {
                'aprovado':aprovado,
                'titulo': f"FASE {fase_n} CONCLUÍDA! 🎉" if aprovado else "CONEXÃO PERDIDA 💥",
                'conexo_final':conexo,'n_arranques':n_arr,
                'missao_cumprida':av_d.get('missao_ok',False),
                'ponto_forte':av_d.get('ponto_forte','—'),
                'melhorar':av_d.get('melhorar','—'),
            }
            st.session_state.lj_hist_partidas.append({
                'fase':fase_n,'personagem':nome_p,'conexo_final':conexo,
                'aprovado':aprovado,'data':datetime.now().strftime('%d/%m %H:%M'),
                'ficha_resumo':st.session_state.get('lj_ficha_resumo',''),
            })
            st.session_state.lj_ativo=False; st.session_state.lj_chat=[]
            st.session_state.pagina="Labia"; st.rerun()

        else:
            # INPUT
            msg_in = st.text_input("",key=f"lj_in_{len(chat)}",placeholder="O que você diz?",label_visibility="collapsed")
            col_e,col_s = st.columns([4,1])
            with col_e:
                if st.button("📤 ENVIAR",key="lj_env",use_container_width=True):
                    if msg_in.strip():
                        st.session_state.lj_ts_usuario = _t.time()

                        # System do personagem
                        f2 = ficha
                        aviso_pes = ""
                        kws = ['aniversario','cidade','mora','trabalha','profissao','musica','hobby','medo','sonho']
                        if any(k in msg_in.lower() for k in kws):
                            aviso_pes = f"\nAVISO PESSOAL: Aniversario={f2.get('aniversario','?')}, Cidade={f2.get('cidade','?')}, Profissao={f2.get('profissao','?')}."

                        ultima = chat[-1]['content'] if chat else ''
                        sys_p = (
                            f"Você é {nome_p}, {f2.get('profissao','')}, {f2.get('cidade','')}.\n"
                            f"Personalidade: {dados_p.get('personalidade','')}.\n"
                            f"Cenário: {cenario}. Hoje: {f2.get('hoje','')}.\n"
                            f"Aniversário: {f2.get('aniversario','?')} — não esqueça.\n\n"
                            f"TURNO ATUAL: Você disse '{ultima}', pessoa respondeu '{msg_in}'.\n"
                            f"Reaja a ISSO especificamente.\n\n"
                            f"REGRAS:\n"
                            f"- Máximo 10 palavras. Estilo WhatsApp.\n"
                            f"- Reaja ao que foi dito agora — não continue assuntos antigos.\n"
                            f"- Se mudar de assunto, acompanhe.\n"
                            f"- Sem filosofia. Sem explicação. Só reaja.\n"
                            f"- NUNCA revele que é IA."
                            + aviso_pes
                        )

                        hist = [{"role":m["role"],"content":m["content"]} for m in chat[-6:]]
                        with st.spinner(""):
                            try:
                                client_l = Groq(api_key=st.session_state.api_key)
                                msgs_l = [{"role":"system","content":sys_p.encode("utf-8","ignore").decode("utf-8")}]+hist+[{"role":"user","content":msg_in}]
                                resp_l = client_l.chat.completions.create(messages=msgs_l,model="openai/gpt-oss-120b",max_tokens=25)
                                resp_bruto = resp_l.choices[0].message.content.strip().split('\n')[0]
                                import re as _re2
                                mc2 = _re2.search(r'[.!?]',resp_bruto)
                                resp_txt = resp_bruto[:mc2.end()].strip() if mc2 else ' '.join(resp_bruto.split()[:10])
                            except Exception as e:
                                resp_txt = "É mesmo?"

                        # Avaliador
                        CRIT = {
                            1:"Fase 1 ATRACAO: avalie curiosidade,humor,originalidade,confianca,reciprocidade. Generoso. Excelente+15a+25 Bom+5a+14 Neutro-2a+4 Ruim-5a-12",
                            2:"Fase 2 CONEXAO: avalie escuta,empatia,profundidade,reciprocidade. Penalize ignorar abertura emocional. Excelente+12a+22 Bom+4a+11 Neutro-3a+3 Ruim-6a-14",
                            3:"Fase 3 SEDUCAO: avalie timing,sinais,tensao,confianca. Exigente. Excelente+15a+25 Bom+5a+14 Neutro-4a+4 Ruim-7a-16",
                        }
                        ARR = {
                            1:["CURIOSIDADE","HUMOR","ORIGINALIDADE","CONFIANCA","GANCHO"],
                            2:["CONEXAO","ESCUTA","PROFUNDIDADE","RECIPROCIDADE","MOMENTO"],
                            3:["TENSAO","FLERTE","TIMING","LEITURA","MESTRE"],
                        }
                        prompt_ev = (
                            f"Avaliador invisivel. Fase {fase_n}.\n"
                            f"Ela disse:'{ultima}' Usuario:'{msg_in}'\n"
                            f"{CRIT.get(fase_n,CRIT[1])}\n"
                            f"Missao:'{st.session_state.lj_missao}'\n"
                            f"JSON sem markdown:\n"
                            + '{"delta":0,"interesse":50,"atracao":50,"conexao":50,"confianca":50,"naturalidade":50,"curiosidade":50,"tensao":20,"arranque":"","missao_cumprida":false}\n'
                            + "arranque: se delta>=12 escreva '+DELTA NOME'. Senao vazio."
                        )
                        with st.spinner(""):
                            try:
                                ev_txt = conexa_ia(prompt_ev.encode("utf-8","ignore").decode("utf-8"))
                                jm2 = _r.search(r'\{.*\}',ev_txt,_r.DOTALL)
                                ev_d = _j.loads(jm2.group(0)) if jm2 else {}
                            except: ev_d = {}

                        delta = ev_d.get('delta',0)
                        arranque = f"🚀 {ev_d['arranque']}" if ev_d.get('arranque') else ""
                        for k in ['interesse','atracao','conexao','confianca','naturalidade','curiosidade','tensao']:
                            if k in ev_d: atribs[k]=max(0,min(100,ev_d[k]))
                            st.session_state.lj_atributos = atribs
                        st.session_state.lj_conexo = max(0,min(100,conexo+delta))
                        if ev_d.get('missao_cumprida'): st.session_state.lj_missao_cumprida=True
                        st.session_state.lj_combo = st.session_state.lj_combo+1 if delta>5 else 0
                        if arranque: st.session_state.lj_arranques.append(arranque)

                        # Efeito digitação
                        ph = st.empty()
                        palavras = resp_txt.split()
                        txt_ac = ""
                        for p_w in palavras:
                            txt_ac += ("" if txt_ac=="" else " ")+p_w
                            ph.markdown(f"<div class='chat-persona'><b style='color:#1D4ED8;'>😊 {nome_p}:</b> {txt_ac}▌</div>",unsafe_allow_html=True)
                            _t.sleep(0.07)
                        ph.empty()

                        chat.append({"role":"user","content":msg_in,"ts":_t.time()})
                        chat.append({"role":"assistant","content":resp_txt,"ts":_t.time(),"arranque":arranque})
                        st.session_state.lj_chat=chat
                        st.session_state.lj_ts_persona=_t.time()
                        st.rerun()

            with col_s:
                if st.button("🚩 Sair",key="lj_sair",use_container_width=True):
                    st.session_state.lj_ativo=False; st.session_state.lj_chat=[]
                    st.session_state.pagina="Labia"; st.rerun()

            _t.sleep(0.8); st.rerun()


        st.stop()

        st.stop()

        st.stop()

    elif st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🧠 Olá, {st.session_state.usuario}!")
            st.markdown(f"<span class='badge-roxo'>{faixa[0]} {faixa[2]}</span>", unsafe_allow_html=True)
        with col_r:
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
                            resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
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
        import time as _t, json as _j, re as _r, random as _rand

        # ── DEFAULTS ──────────────────────────────────────────────────
        for _k,_v in [
            ('lj_fase',1),('lj_ativo',False),('lj_chat',[]),('lj_conexo',100),
            ('lj_atributos',{'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20}),
            ('lj_inicio',0),('lj_duracao',300),('lj_missao',''),('lj_missao_cumprida',False),
            ('lj_arranques',[]),('lj_combo',0),('lj_ts_persona',0),('lj_ts_usuario',0),
            ('lj_hist_cenarios',[]),('lj_hist_aberturas',[]),('lj_hist_partidas',[]),
            ('lj_nome_persona',''),('lj_dados_persona',{}),('lj_cenario',''),
            ('lj_ficha',{}),('lj_ficha_resumo',''),('lj_aval',None),
            ('lj_desbloqueado',False),('lj_personagem_sel','Rafaela'),
            ('lj_personagens_ok',['Rafaela']),('lj_fases_ok',0),('lj_titulo','🥉 Paquerador'),
        ]:
            if _k not in st.session_state: st.session_state[_k] = _v

        # ── TELA INICIAL ──────────────────────────────────────────────
        if not st.session_state.lj_ativo:
            st.markdown("## 👑 Mestre da Lábia")
            st.markdown("*Você consegue conquistar uma conversa sem usar frases prontas?*")

            # Senha
            with st.expander("🔑 Acesso especial"):
                s = st.text_input("Senha:", type="password", key="lj_senha")
                if st.button("Desbloquear", key="lj_btn_senha"):
                    if s == "123":
                        st.session_state.lj_desbloqueado = True
                        st.session_state.lj_personagens_ok = ["Rafaela","Camila","Helena"]
                        st.success("✅ Tudo desbloqueado!"); st.rerun()
                    else: st.error("Senha incorreta.")

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # Fases
            st.markdown("### 🗺️ Jornada")
            c1,c2,c3 = st.columns(3)
            for col,(fn,emoji,nome,mins,titulo,mc,mn,mi) in zip(
                [c1,c2,c3],
                [(1,"🟢","ATRAÇÃO",5,"🥉 Paquerador",70,60,65),
                 (2,"🟡","CONEXÃO",7,"🥈 Galanteador",75,70,65),
                 (3,"🔴","SEDUÇÃO",10,"👑 Mestre da Lábia",80,75,70)]
            ):
                concluida = st.session_state.lj_fases_ok >= fn
                atual     = st.session_state.lj_fases_ok == fn-1
                cor = "#22C55E" if concluida else ("#C2185B" if atual else "#E5E7EB")
                with col:
                    st.markdown(f"""
                    <div style='text-align:center;background:#fff;border:2px solid {cor};border-radius:12px;padding:12px 6px;'>
                    <div style='font-size:1.4em;'>{emoji}</div>
                    <div style='font-size:0.75em;font-weight:700;color:#1A1A2E;'>FASE {fn} — {nome}</div>
                    <div style='font-size:0.68em;color:#888;'>⏱️ {mins} min · {titulo}</div>
                    <div style='margin-top:4px;'>{"✅" if concluida else ("🔓" if atual else "🔒")}</div>
                    </div>""", unsafe_allow_html=True)

            # Resultado anterior
            if st.session_state.lj_aval:
                av = st.session_state.lj_aval
                cor_av = "#059669" if av.get('aprovado') else "#B91C1C"
                bg_av  = "#F0FDF4" if av.get('aprovado') else "#FFF5F5"
                bd_av  = "#86EFAC" if av.get('aprovado') else "#FECACA"
                st.markdown(f"""
                <div style='background:{bg_av};border:2px solid {bd_av};border-radius:12px;
                padding:12px 16px;margin:12px 0;'>
                <strong style='color:{cor_av};'>{"🎉 " if av.get("aprovado") else "💥 "}{av.get("titulo","Resultado")}</strong><br>
                <small style='color:#1A1A2E;'>❤️ {av.get("conexo_final",0)} · 🚀 {av.get("n_arranques",0)} arranques
                {" · 🎯 Missão cumprida!" if av.get("missao_cumprida") else ""}</small><br>
                <small style='color:#555;'>✅ {av.get("ponto_forte","—")} &nbsp;|&nbsp; ⚠️ {av.get("melhorar","—")}</small>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            # Personagens
            st.markdown("### 👩 Escolha a Personagem")
            pa,pb,pc = st.columns(3)
            for col,nome_p,estrelas,desc_p in [
                (pa,"Rafaela","⭐⭐","Simpática e bem-humorada. Não demonstra interesse imediatamente."),
                (pb,"Camila","⭐⭐⭐⭐","Segura e provocadora. Testa sua confiança com ironia."),
                (pc,"Helena","⭐⭐⭐⭐⭐","Sofisticada e seletiva. Difícil de impressionar."),
            ]:
                ok = nome_p in st.session_state.lj_personagens_ok or st.session_state.lj_desbloqueado
                sel = st.session_state.lj_personagem_sel == nome_p
                cor_p = "#C2185B" if sel else ("#1A1A2E" if ok else "#E5E7EB")
                with col:
                    if ok and st.button(f"{'✓ ' if sel else ''}{nome_p} {estrelas}", key=f"sel_{nome_p}", use_container_width=True):
                        st.session_state.lj_personagem_sel = nome_p; st.rerun()
                    st.markdown(f"<div style='font-size:0.75em;color:{'#1A1A2E' if ok else '#9CA3AF'};padding:4px;'>{desc_p if ok else '🔒 Bloqueada'}</div>", unsafe_allow_html=True)

            # Fase
            fase_max = min(st.session_state.lj_fases_ok + 1, 3)
            if st.session_state.lj_desbloqueado:
                fi = st.selectbox("Fase:", ["Fase 1 — Atração","Fase 2 — Conexão","Fase 3 — Sedução"], index=fase_max-1, key="lj_fase_sel")
                fase_jog = int(fi.split()[1])
            else:
                fase_jog = fase_max

            FASES = [(1,"🟢","ATRACAO",5,"🥉 Paquerador",70,60,65),
                     (2,"🟡","CONEXAO",7,"🥈 Galanteador",75,70,65),
                     (3,"🔴","SEDUCAO",10,"👑 Mestre da Lábia",80,75,70)]
            fi_sel = FASES[fase_jog-1]
            st.markdown(f"**Jogando:** Fase {fi_sel[0]} — {fi_sel[2]} · ⏱️ {fi_sel[3]} min · {fi_sel[4]}")

            if st.button("▶ COMEÇAR DESAFIO", use_container_width=True):
                nome_sel  = st.session_state.lj_personagem_sel
                PERS_DEF  = {
                    "Rafaela":{"personalidade":"simpatica, bem-humorada, curiosa, receptiva","humor":80,"receptividade":70,"provocacao":30,"exigencia":40},
                    "Camila": {"personalidade":"segura, ironica, provocadora, nao facilita","humor":70,"receptividade":45,"provocacao":80,"exigencia":70},
                    "Helena": {"personalidade":"sofisticada, seletiva, exige profundidade","humor":55,"receptividade":30,"provocacao":60,"exigencia":90},
                }
                dados_sel = PERS_DEF[nome_sel]

                CENARIOS = ["cafeteria","parque","livraria","shopping","feira","exposição de arte",
                            "aeroporto","praça","academia","banca de jornal","pet shop","museu",
                            "food court","jardim botânico","loja de discos","sebo de livros",
                            "calçadão","praia","estação de metrô","galeria"]
                usados_c = st.session_state.lj_hist_cenarios[-8:]
                disponiveis = [x for x in CENARIOS if x not in usados_c] or CENARIOS
                cenario = _rand.choice(disponiveis)

                MISSOES = {
                    1:["Fazer ela perguntar algo sobre você","Criar um momento de humor","Fazer ela contar algo pessoal","Conseguir que ela demonstre curiosidade"],
                    2:["Fazer ela lembrar algo que você disse","Conseguir que ela compartilhe um sonho","Criar um momento de empatia genuína"],
                    3:["Criar um momento de flerte natural","Fazer ela brincar com você","Criar uma brincadeira interna entre vocês"],
                }
                missao = _rand.choice(MISSOES.get(fase_jog,[MISSOES[1][0]]))

                # Ficha única por partida
                profissoes = ["designer","professora","nutricionista","jornalista","médica","fotógrafa","chef","publicitária","advogada","veterinária"]
                cidades    = ["São Paulo","Rio de Janeiro","Belo Horizonte","Florianópolis","Curitiba","Porto Alegre","Fortaleza","Recife"]
                musicas    = ["MPB","rock alternativo","pop","jazz","funk","sertanejo","indie","eletrônica"]
                hobbies    = ["fotografia","culinária","corrida","yoga","leitura","viagens","séries","pintura","academia"]
                hoje_lst   = ["derramei café na blusa","perdi o ônibus","achei R$20 no bolso","queimei o almoço","recebi uma proposta de emprego","meu gato fugiu e voltou","choveu quando saí sem guarda-chuva","encontrei um livro perdido"]
                meses_br   = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]

                ficha = {
                    "profissao": _rand.choice(profissoes),
                    "cidade":    _rand.choice(cidades),
                    "musica":    _rand.choice(musicas),
                    "hobby1":    _rand.choice(hobbies),
                    "hobby2":    _rand.choice([h for h in hobbies]),
                    "hoje":      _rand.choice(hoje_lst),
                    "aniversario": f"{_rand.randint(1,28)} de {_rand.choice(meses_br)}",
                }

                usados_ab = st.session_state.lj_hist_aberturas[-5:]
                hist_fichas = [p.get('ficha_resumo','') for p in st.session_state.lj_hist_partidas[-6:]]

                with st.spinner("Preparando a conversa..."):
                    prompt_ab = (
                        f"Você é {nome_sel}, {ficha['profissao']}, {ficha['cidade']}.\n"
                        f"Personalidade: {dados_sel['personalidade']}.\n"
                        f"Hoje aconteceu com você: {ficha['hoje']}.\n"
                        f"Cenário: {cenario}.\n"
                        f"NÃO repita estas aberturas anteriores: {' | '.join(usados_ab)}\n"
                        f"NÃO repita estes contextos anteriores: {' | '.join(hist_fichas)}\n\n"
                        f"Gere UMA primeira fala sua — 1 frase curta (máx 10 palavras), natural e contextual.\n"
                        f"Pode mencionar algo que aconteceu com você hoje ou algo do cenário.\n"
                        f"NÃO comece com 'Oi tudo bem'. Retorne APENAS a fala."
                    )
                    primeira_fala = conexa_ia(prompt_ab).strip().strip('"').strip("'").split('\n')[0]

                st.session_state.lj_hist_cenarios.append(cenario)
                st.session_state.lj_hist_aberturas.append(primeira_fala[:50])
                st.session_state.lj_ativo        = True
                st.session_state.lj_fase         = fase_jog
                st.session_state.lj_chat         = [{"role":"assistant","content":primeira_fala,"ts":_t.time()}]
                st.session_state.lj_conexo       = 100
                st.session_state.lj_atributos    = {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20}
                st.session_state.lj_inicio       = _t.time()
                st.session_state.lj_duracao      = fi_sel[3] * 60
                st.session_state.lj_missao       = missao
                st.session_state.lj_missao_cumprida = False
                st.session_state.lj_arranques    = []
                st.session_state.lj_combo        = 0
                st.session_state.lj_ts_persona   = _t.time()
                st.session_state.lj_ts_usuario   = 0
                st.session_state.lj_cenario      = cenario
                st.session_state.lj_nome_persona = nome_sel
                st.session_state.lj_dados_persona= dados_sel
                st.session_state.lj_ficha        = ficha
                st.session_state.lj_ficha_resumo = f"{ficha['profissao']}/{ficha['cidade']}/{ficha['hobby1']}/{ficha['hoje'][:20]}"
                st.session_state.lj_aval         = None
                st.session_state.pagina          = "Dialogo"
                st.rerun()

            # Histórico
            if st.session_state.lj_hist_partidas:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📈 Histórico")
                for h in reversed(st.session_state.lj_hist_partidas[-5:]):
                    taxa = h.get('conexo_final',0)
                    cor_h = "#059669" if taxa>=70 else ("#B45309" if taxa>=40 else "#B91C1C")
                    st.markdown(f"<div class='hist-item'><span class='badge'>{h.get('personagem','?')}</span> Fase {h.get('fase','?')} · <small style='color:#888;'>{h.get('data','')}</small> <strong style='color:{cor_h};float:right;'>❤️ {taxa}</strong></div>", unsafe_allow_html=True)

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

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 CONEXA IA — Inteligência para Conversas · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 CONEXA IA — Inteligência para Conversas · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 CONEXA IA — Inteligência para Conversas · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
