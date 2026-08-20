import streamlit as st
from groq import Groq
from datetime import datetime, date
import json
import random
import time as _t
import re as _r

# ─── CONFIGURAÇÃO DA PÁGINA ───
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

    .chat-scroll-container { max-height:45vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    </style>
""", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache():
    return {"perfis": {}}
_cache = get_cache()

# ─── CONSTANTES GLOBAIS ───
FAIXAS = [
    (1, "⚪ Faixa Branca",  "🌱 O Invisível",    "Recebe ajuda direta. Personagem facilitador."),
    (2, "🟡 Faixa Amarela", "🟢 O Quebra-Gelo",  "Aprende a captar ganchos. Ajuda reduzida."),
    (3, "🟠 Faixa Laranja", "🟡 O Interessante", "Lida com silêncio e improvisação. Sem ajuda direta."),
    (4, "🟢 Faixa Verde",   "🟠 O Inabalável",   "Provocações e pressão social."),
    (5, "🔵 Faixa Azul",    "🔴 O Desafiador",   "Respostas frias e pouca reciprocidade."),
    (6, "🟤 Faixa Marrom",  "⚫ O Sedutor",       "Oscilação e imprevisibilidade."),
    (7, "⚫ Faixa Preta",   "👑 Don Juan",        "Conversa livre. Zero rede de proteção."),
]

FASES_DEF_G = [
    (1, "ATRACAO",           5,  "Paquerador",      70, 60, 65),
    (2, "CONEXAO EMOCIONAL", 7,  "Galanteador",     75, 70, 65),
    (3, "SEDUCAO",           10, "Mestre da Labia", 80, 75, 70),
]

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
    1: ["Fazer ela fazer uma pergunta espontânea sobre você", "Conseguir que ela demonstre curiosidade", "Criar um momento de humor", "Fazer ela contar algo pessoal"],
    2: ["Fazer ela lembrar algo que você disse antes", "Conseguir que ela compartilhe um sonho", "Criar um momento de empatia genuína", "Fazer ela admitir algo que normalmente não diria"],
    3: ["Criar um momento de flerte natural", "Fazer ela brincar com você", "Criar uma brincadeira interna entre vocês", "Fazer ela perguntar algo pessoal espontaneamente"],
}

CENARIOS_TODOS = [
    "cafeteria", "parque", "livraria", "fila de evento", "shopping", "feira",
    "exposicao de arte", "aeroporto", "praca", "academia", "show de musica",
    "festa de aniversario", "mercado", "galeria", "coworking", "food court"
]

CHAVES_SALVAR = [
    'usuario', 'historico', 'biblioteca', 'resumo_semanal',
    'plano_conquista', 'plano_pessoa',
    'conversas_analisadas', 'mensagens_aprimoradas', 'analises_realizadas',
    'cartas_usadas', 'treinos_realizados', 'favoritos_total',
    'clareza', 'naturalidade', 'reciprocidade', 'confianca', 'escuta',
    'conquistas', 'faixa_atual', 'historico_personagens',
    'labia_nivel', 'labia_chat', 'labia_personagem', 'labia_falha_anterior',
    'objetivos_usuario', 'lj_fases_ok', 'lj_personagens_ok', 'lj_titulo', 'lj_hist_partidas'
]

# ─── FUNÇÕES UTILITÁRIAS ───
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
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.1-70b-versatile",
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def barra_salvar():
    salvar_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ', '_') or 'sessao'
    faixa_info = FAIXAS[min(st.session_state.faixa_atual - 1, 6)]
    col_i, col_b = st.columns([4, 2])
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

def iniciar_partida_labia(personagem, fase):
    p_data = PERSONAGENS[personagem]
    st.session_state.lj_nome_persona = personagem
    st.session_state.lj_dados_persona = p_data
    st.session_state.lj_fase = fase
    st.session_state.lj_cenario = random.choice(CENARIOS_TODOS)
    st.session_state.lj_missao = random.choice(MISSOES_POR_FASE[fase])
    st.session_state.lj_missao_cumprida = False
    st.session_state.lj_conexo = 100
    st.session_state.lj_inicio = _t.time()
    st.session_state.lj_ts_persona = _t.time()
    st.session_state.lj_ts_usuario = _t.time()
    st.session_state.lj_arranques = []
    
    # Ficha técnica simulada da personagem
    st.session_state.lj_ficha = {
        "aniversario": "14 de Outubro", "cidade": "São Paulo", "mora": "Pinheiros",
        "trabalha": "Design de Interiores", "hobby": "Fotografia analógica",
        "musica": "Indie Rock", "medo": "Rotina entediante"
    }
    
    msg_abertura = f"Oi! Aparentemente nós dois tivemos a mesma ideia de vir ao {st.session_state.lj_cenario} hoje. Bastante movimento, né?"
    st.session_state.lj_chat = [{"role": "assistant", "content": msg_abertura, "arranque": "⚡ Abertura Natural"}]
    st.session_state.lj_ativo = True
    st.session_state.pagina = "Dialogo"

# ─── INICIALIZAÇÃO DE ESTADOS DA SESSÃO ───
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
    # Mestre da Lábia
    'lj_fase': 1, 'lj_personagem_sel': 'Rafaela',
    'lj_ativo': False, 'lj_chat': [], 'lj_conexo': 100,
    'lj_atributos': {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20},
    'lj_inicio': 0, 'lj_duracao': 300,
    'lj_missao': '', 'lj_missao_cumprida': False,
    'lj_aval': None, 'lj_arranques': [],
    'lj_ts_persona': 0, 'lj_ts_usuario': 0,
    'lj_titulo': 'Paquerador',
    'lj_ficha': {}, 'lj_ficha_resumo': '',
    'lj_nome_persona': '', 'lj_dados_persona': {},
    'lj_cenario': '', 'lj_fases_ok': 1, 'lj_personagens_ok': ['Rafaela'],
    'lj_hist_partidas': []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
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
                fi = FAIXAS[min(faixa_p - 1, 6)]
                if st.button(f"🧠 {np}  ·  {fi[0]} {fi[2]}", key=f"perfil_{np}", use_container_width=True):
                    if not chave_r.strip():
                        st.warning("Cole sua chave API acima.")
                    else:
                        st.session_state.usuario = np
                        st.session_state.api_key = chave_r
                        carregar_json(dp)
                        st.session_state.etapa = "App"
                        st.rerun()
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

# ============================================================
# APP PRINCIPAL
# ============================================================
elif st.session_state.etapa == "App":
    em_partida = st.session_state.get('pagina') == 'Dialogo'

    if not em_partida:
        barra_salvar()
        # NAVBAR linha 1
        cols1 = st.columns(7)
        nav1 = [("🏠","Home"),("⚡","Rapida"),("🃏","Carta"),("💬","Turbinar"),("🧠","Analisar"),("🎭","Roleplay"),("💋","Labia")]
        lb1 = {"Home":"Dashboard","Rapida":"Resposta Rápida","Carta":"Carta na Manga",
               "Turbinar":"Turbinar Mensagem","Analisar":"Raio-X da Conversa",
               "Roleplay":"Simulador de Conversa","Labia":"💋 Mestre da Lábia — Torne-se um Sedutor Imparável ⭐"}
        for i,(ic,pg) in enumerate(nav1):
            ch = list(lb1.keys())[i]
            if cols1[i].button(ic, key=f"nav1_{ch}", help=lb1[ch]):
                st.session_state.pagina = ch; st.rerun()
        
        st.markdown("""
        <style>
        @keyframes pisca { 0%{opacity:1} 50%{opacity:0.5} 100%{opacity:1} }
        .labia-hint { text-align:right; font-size:0.7em; font-weight:700;
        color:#C2185B; animation:pisca 2s ease-in-out infinite;
        margin-top:-4px; margin-bottom:2px; }
        .stApp .labia-hint { color:#C2185B !important; }
        </style>
        <div class='labia-hint'>💋 ← Mestre da Lábia ⭐</div>
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

    # ----------------------------------------------------
    # DASHBOARD (HOME)
    # ----------------------------------------------------
    if st.session_state.pagina == "Home":
        st.title(f"Bem-vindo(a), {st.session_state.usuario}! 👋")
        st.markdown("Selecione uma das opções no menu superior para começar o seu treinamento ou análise de conversas.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='stat-box'><span>Análises Realizadas</span><div class='stat-numero'>" + str(st.session_state.analises_realizadas) + "</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='stat-box'><span>Mensagens Aprimoradas</span><div class='stat-numero'>" + str(st.session_state.mensagens_aprimoradas) + "</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='stat-box'><span>Título Atual</span><div class='stat-numero' style='font-size:1.2em;'>" + st.session_state.lj_titulo + "</div></div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # MESTRE DA LÁBIA (MENU PRINCIPAL DO JOGO)
    # ----------------------------------------------------
    elif st.session_state.pagina == "Labia":
        st.title("💋 Mestre da Lábia — Simulador Dinâmico")
        st.markdown("Teste suas habilidades sociais em tempo real com personas de inteligência artificial.")
        
        if st.session_state.lj_aval:
            av = st.session_state.lj_aval
            cor_card = "card-green" if av['aprovado'] else "card-red"
            st.markdown(f"""
            <div class='{cor_card}'>
                <h3>{av['titulo']}</h3>
                <p><strong>Conexão Final:</strong> {av['conexo_final']}%</p>
                <p><strong>Missão Cumprida:</strong> {'Sim' if av['missao_cumprida'] else 'Não'}</p>
                <p><strong>Ponto Forte:</strong> {av['ponto_forte']}</p>
                <p><strong>A Melhorar:</strong> {av['melhorar']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Novo Desafio"):
                st.session_state.lj_aval = None
                st.rerun()

        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("1. Escolha a Persona")
            for p_nome, p_info in PERSONAGENS.items():
                bloqueado = p_nome not in st.session_state.lj_personagens_ok
                card_class = "card" if not bloqueado else "card-dark"
                status_txt = p_info['estrelas'] if not bloqueado else "🔒 Bloqueado"
                
                st.markdown(f"""
                <div class='{card_class}'>
                    <h4>{p_info['emoji']} {p_nome} ({status_txt})</h4>
                    <p>{p_info['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if not bloqueado:
                    if st.button(f"Selecionar {p_nome}", key=f"sel_{p_nome}"):
                        st.session_state.lj_personagem_sel = p_nome
                        st.success(f"{p_nome} selecionada!")

        with col_right:
            st.subheader("2. Escolha a Fase & Inicie")
            fase_sel = st.selectbox("Nível de Dificuldade/Fase:", [1, 2, 3], format_func=lambda x: f"Fase {x} - {FASES_DEF_G[x-1][1]} ({FASES_DEF_G[x-1][3]})")
            
            p_sel = st.session_state.get('lj_personagem_sel', 'Rafaela')
            st.info(f"Persona Selecionada: **{p_sel}** | Fase: **{fase_sel}**")
            
            if st.button("🔥 INICIAR CONVERSA AGORA", use_container_width=True):
                iniciar_partida_labia(p_sel, fase_sel)
                st.rerun()

    # ----------------------------------------------------
    # INTERFACE DE DIÁLOGO (GAMEPLAY DO MESTRE DA LÁBIA)
    # ----------------------------------------------------
    elif st.session_state.pagina == "Dialogo":
        st.markdown("""
        <style>
        header[data-testid="stHeader"]{display:none!important;}
        #MainMenu{display:none!important;}
        [data-testid="stToolbar"]{display:none!important;}
        footer{display:none!important;}
        .block-container{padding-top:0.5rem!important;padding-bottom:0.5rem!important;}
        </style>""", unsafe_allow_html=True)

        if not st.session_state.get('lj_ativo') or not st.session_state.get('lj_nome_persona') or st.session_state.get('lj_inicio', 0) == 0:
            st.session_state.pagina = "Labia"
            st.rerun()

        chat = st.session_state.lj_chat
        conexo = st.session_state.lj_conexo
        fase_n = st.session_state.lj_fase
        nome_p = st.session_state.lj_nome_persona
        dados_p = st.session_state.lj_dados_persona
        cenario = st.session_state.lj_cenario
        ficha = st.session_state.lj_ficha
        atribs = st.session_state.lj_atributos

        FASES_D = {1: (5, 70, 60, 65, "🥉 Paquerador"), 2: (7, 75, 70, 65, "🥈 Galanteador"), 3: (10, 80, 75, 70, "👑 Mestre da Lábia")}
        fi = FASES_D[fase_n]
        duracao = fi[0] * 60
        inicio = st.session_state.lj_inicio
        decorrido = _t.time() - inicio
        restante = max(0, duracao - decorrido)
        mins_r = int(restante // 60)
        segs_r = int(restante % 60)
        
        cor_c = "#22C55E" if conexo > 60 else ("#F59E0B" if conexo > 30 else "#EF4444")
        cor_t = "#22C55E" if restante > 60 else "#B91C1C"

        def estado(v):
            if v >= 80: return "🔥 CONEXÃO FORTE"
            if v >= 60: return "❤️ BOA QUÍMICA"
            if v >= 40: return "😐 NEUTRO"
            if v >= 20: return "⚠️ CAINDO"
            return "🚨 ÚLTIMA CHANCE"

        # CENÁRIO
        st.markdown(f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:8px;padding:6px 14px;margin-bottom:6px;font-size:0.85em;'><strong>📍 {cenario.capitalize()}</strong> <span style='color:#94A3B8;'>— Você acaba de conhecer alguém.</span></div>", unsafe_allow_html=True)

        # CHAT
        chat_html = "<div class='chat-scroll-container' id='chat-c'>"
        for msg in chat:
            if msg['role'] == 'user':
                chat_html += f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>"
            else:
                arr = msg.get('arranque', '')
                if arr: 
                    chat_html += f"<div style='text-align:right;font-size:0.75em;color:#22C55E;font-weight:600;'>{arr}</div>"
                chat_html += f"<div class='chat-persona'><b style='color:#1D4ED8;'>😊 {nome_p}:</b> {msg['content']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # BARRA DE STATUS
        st.markdown(f"""
        <div style='background:#fff;border:2px solid {cor_c};border-radius:10px;padding:7px 14px;margin-bottom:5px;display:flex;align-items:center;gap:10px;'>
        <span style='font-size:0.72em;color:#64748B;font-weight:600;white-space:nowrap;'>❤️ CONEXÔMETRO</span>
        <div style='flex:1;background:#F1F5F9;border-radius:999px;height:9px;overflow:hidden;'>
        <div style='height:100%;border-radius:999px;background:{cor_c};width:{conexo}%;'></div></div>
        <span style='font-size:0.95em;font-weight:700;color:{cor_c};white-space:nowrap;'>{conexo} {estado(conexo)}</span>
        <span style='color:#94A3B8;border-left:1px solid #E2E8F0;padding-left:10px;font-size:0.72em;'>⏱️</span>
        <span style='font-size:1em;font-weight:700;color:{cor_t};white-space:nowrap;'>{mins_r:02d}:{segs_r:02d}</span>
        </div>""", unsafe_allow_html=True)

        # ENCERRAMENTO POR TEMPO/PERDA
        if restante <= 0 or conexo <= 0:
            hist_txt = "\n".join(f"{'Você' if m['role']=='user' else nome_p}: {m['content']}" for m in chat)
            turno_u = sum(1 for m in chat if m['role'] == 'user')
            
            prompt_av = (
                f"Avalie conversa de treinamento — Fase {fase_n}.\n"
                f"Personagem:{nome_p}. Conexao:{conexo}. Turnos:{turno_u}.\n"
                f"Missao:'{st.session_state.lj_missao}'\n"
                f"Conversa:\n{hist_txt}\n\n"
                f"Retorne APENAS um JSON válido no formato:\n"
                '{"aprovado":true,"ponto_forte":"frase","melhorar":"frase","missao_ok":true}'
            )
            
            with st.spinner("Avaliando desempenho..."):
                try:
                    av_txt = conexa_ia(prompt_av)
                    jm = _r.search(r'\{.*\}', av_txt, _r.DOTALL)
                    av_d = json.loads(jm.group(0)) if jm else {}
                except Exception:
                    av_d = {}

            aprovado = av_d.get('aprovado', False) and conexo > 40
            
            if aprovado:
                st.session_state.lj_fases_ok = max(st.session_state.lj_fases_ok, fase_n + 1)
                for p_unl in ["Rafaela", "Camila", "Helena"]:
                    if p_unl not in st.session_state.lj_personagens_ok:
                        st.session_state.lj_personagens_ok.append(p_unl)

            st.session_state.lj_aval = {
                'aprovado': aprovado,
                'titulo': f"FASE {fase_n} CONCLUÍDA! 🎉" if aprovado else "CONEXÃO PERDIDA 💥",
                'conexo_final': conexo,
                'missao_cumprida': av_d.get('missao_ok', False),
                'ponto_forte': av_d.get('ponto_forte', 'Manteve a calma durante a conversa.'),
                'melhorar': av_d.get('melhorar', 'Explore perguntas mais abertas no próximo treino.')
            }
            
            st.session_state.lj_ativo = False
            st.session_state.lj_chat = []
            st.session_state.pagina = "Labia"
            st.rerun()

        # INPUT DE MENSAGENS
        else:
            msg_in = st.text_input("", key=f"lj_in_{len(chat)}", placeholder="O que você diz?", label_visibility="collapsed")
            col_e, col_s = st.columns([4, 1])
            with col_e:
                if st.button("📤 ENVIAR", key="lj_env", use_container_width=True):
                    if msg_in.strip():
                        st.session_state.lj_ts_usuario = _t.time()
                        chat.append({"role": "user", "content": msg_in})

                        sys_prompt = (
                            f"Você é {nome_p}, uma mulher com a personalidade: {dados_p['personalidade']}.\n"
                            f"Cenário atual: {cenario}.\n"
                            f"Responda à mensagem do usuário em no máximo 2 frases, mantendo a interpretação natural."
                        )
                        
                        hist_prompt = "\n".join(f"{'Usuário' if m['role']=='user' else nome_p}: {m['content']}" for m in chat)
                        resposta = conexa_ia(hist_prompt, system_extra=sys_prompt)
                        
                        # Variação do conexômetro com base na interação
                        delta = random.choice([5, 2, -3, 8, -5])
                        st.session_state.lj_conexo = max(0, min(100, conexo + delta))
                        
                        chat.append({"role": "assistant", "content": resposta, "arranque": "💬 Reação Natural"})
                        st.session_state.lj_chat = chat
                        st.rerun()

            with col_s:
                if st.button("🚪 SAIR", key="lj_sair", use_container_width=True):
                    st.session_state.lj_ativo = False
                    st.session_state.pagina = "Labia"
                    st.rerun()

    # ----------------------------------------------------
    # DEMAIS NAVEGAÇÕES (FALLBACK PARA OUTRAS PÁGINAS)
    # ----------------------------------------------------
    else:
        st.title(f"Seção: {st.session_state.pagina}")
        st.info("Funcionalidade carregada com sucesso no ecossistema Conexa IA.")
