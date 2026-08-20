import streamlit as st
from groq import Groq
from datetime import datetime, date
import json
import random
import time as _t
import re as _r

st.set_page_config(page_title="CONEXA IA", page_icon="🧠", layout="wide")

# ============================================================
# MODELO GROQ — Atualizado para os modelos suportados pela API
# ============================================================
GROQ_MODEL = "llama-3.3-70b-versatile"

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

CHAVES_SALVAR = [
    'usuario', 'historico', 'biblioteca', 'resumo_semanal',
    'plano_conquista', 'plano_pessoa',
    'conversas_analisadas', 'mensagens_aprimoradas', 'analises_realizadas',
    'cartas_usadas', 'treinos_realizados', 'favoritos_total',
    'clareza', 'naturalidade', 'reciprocidade', 'confianca', 'escuta',
    'conquistas', 'faixa_atual', 'historico_personagens',
    'labia_nivel', 'labia_chat', 'labia_personagem', 'labia_falha_anterior',
    'objetivos_usuario',
    'lj_hist_cenarios', 'lj_hist_aberturas', 'lj_hist_partidas',
    'lj_fases_ok', 'lj_personagens_ok', 'lj_titulo', 'lj_desbloqueado',
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
    'lj_fase': 1, 'lj_personagem_sel': 'Rafaela',
    'lj_ativo': False, 'lj_chat': [], 'lj_conexo': 100,
    'lj_atributos': {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20},
    'lj_inicio': 0, 'lj_duracao': 300,
    'lj_missao': '', 'lj_missao_cumprida': False,
    'lj_aval': None, 'lj_arranques': [],
    'lj_hist_cenarios': [], 'lj_hist_aberturas': [],
    'lj_ts_persona': 0, 'lj_ts_usuario': 0,
    'lj_combo': 0, 'lj_fases_ok': 0,
    'lj_titulo': '🥉 Paquerador',
    'lj_personagens_ok': ['Rafaela'],
    'lj_hist_partidas': [], 'lj_desbloqueado': False,
    'lj_ficha': {}, 'lj_ficha_resumo': '',
    'lj_nome_persona': '', 'lj_dados_persona': {},
    'lj_cenario': '',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── MOTOR DE IA APRIMORADO ───
def conexa_ia(prompt, system_extra=""):
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = (
            "Você é o CONEXA IA — motor de inteligência avançado para dinâmica social e sedução. "
            "Sua análise deve ser afiada, realista e baseada em linguagem corporal, subtexto emocional e psicologia da atração. "
            "Se estiver interpretando um personagem em um roleplay de sedução, seja EXTREMAMENTE realista: reaja com frieza ou desinteresse a respostas monossilábicas ou necessitadas, e reaja com charme e curiosidade a respostas confiantes e autênticas. "
            "Português do Brasil natural e contemporâneo. " + system_extra
        )
        resp = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model=GROQ_MODEL,
            temperature=0.75,
        )
        st.session_state['lj_last_err'] = None
        return resp.choices[0].message.content
    except Exception as e:
        st.session_state['lj_last_err'] = str(e)
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

# ─── PERSONAGENS E REGRAS ───
PERSONAGENS = {
    "Rafaela": {
        "emoji": "😊", "dificuldade": 2, "estrelas": "⭐⭐",
        "desc": "Simpática, bem-humorada, comunicativa. Curiosa sobre a vida, mas nota quando a pessoa força a barra.",
        "personalidade": "simpática, expressiva, de riso fácil, fala sobre hobbies, gosta de respostas autênticas e inteligentes.",
        "comportamento_baixo": "dá respostas educadas porém curtas, muda de assunto.",
        "comportamento_alto": "faz perguntas espontâneas, ri, demonstra forte curiosidade e joga ganchos de conversa.",
    },
    "Camila": {
        "emoji": "😏", "dificuldade": 4, "estrelas": "⭐⭐⭐⭐",
        "desc": "Segura, sarcástica, confiante. Testa os limites e prefere caras que não se abalam fácil.",
        "personalidade": "desafiadora, irônica, direta, sarcástica, nota fraqueza imediatamente.",
        "comportamento_baixo": "responde com uma palavra só, é irônica, mostra tédio explícito.",
        "comportamento_alto": "recompensa confiança com elogios sutis, flerta provocando, sorri provocativa.",
    },
    "Helena": {
        "emoji": "🧐", "dificuldade": 5, "estrelas": "⭐⭐⭐⭐⭐",
        "desc": "Sofisticada, inteligente, reservada. Detesta clichês ou cantadas prontas.",
        "personalidade": "intelectual, elegante, analítica, exigente, valoriza repertório e conversa fluida.",
        "comportamento_baixo": "fica distante, responde formalmente, encerra o papo.",
        "comportamento_alto": "se engaja em debates profundos, compartilha detalhes da vida, sorri com elegância.",
    },
}

if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🧠 CONEXA IA")
        st.markdown("**Inteligência para conversas, comunicação e conexões.**")
        
        perfis = perfis_salvos()
        if perfis:
            chave_r = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for np in perfis:
                dp = carregar_cache(np)
                if st.button(f"🧠 Entrar como {np}", key=f"perfil_{np}", use_container_width=True):
                    if chave_r.strip():
                        st.session_state.usuario = np
                        st.session_state.api_key = chave_r
                        carregar_json(dp)
                        st.session_state.etapa = "App"
                        st.rerun()

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")
        if st.button("🧠 ENTRAR NO CONEXA"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()

elif st.session_state.etapa == "App":

    em_partida = st.session_state.get('pagina') == 'Dialogo'

    if not em_partida:
        barra_salvar()
        cols1 = st.columns(7)
        nav1 = [("🏠","Home"),("⚡","Rapida"),("🃏","Carta"),("💬","Turbinar"),("🧠","Analisar"),("🎭","Roleplay"),("💋","Labia")]
        for i,(ic,pg) in enumerate(nav1):
            if cols1[i].button(f"{ic} {pg}", key=f"nav1_{pg}"):
                st.session_state.pagina = pg; st.rerun()

    if st.session_state.pagina == "Dialogo":
        # Redireciona se sem sessão ativa
        if not st.session_state.get('lj_ativo') or not st.session_state.get('lj_nome_persona'):
            st.session_state.pagina="Labia"; st.rerun()

        chat     = st.session_state.lj_chat
        conexo   = st.session_state.lj_conexo
        fase_n   = st.session_state.lj_fase
        nome_p   = st.session_state.lj_nome_persona
        cenario  = st.session_state.lj_cenario
        
        st.markdown(f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:8px;padding:6px 14px;margin-bottom:6px;font-size:0.85em;'><strong>📍 {cenario.capitalize()}</strong> — Conversa em andamento com {nome_p}</div>", unsafe_allow_html=True)

        # RENDER DO CHAT
        chat_html = "<div class='chat-scroll-container' id='chat-c'>"
        for msg in chat:
            if msg['role'] == 'user':
                chat_html += f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>"
            else:
                arr = msg.get('arranque','')
                if arr: 
                    chat_html += f"<div style='text-align:right;font-size:0.75em;color:#22C55E;font-weight:600;'>{arr}</div>"
                chat_html += f"<div class='chat-persona'><b style='color:#1D4ED8;'>😊 {nome_p}:</b> {msg['content']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # ENTRADA DE TEXTO DO USUÁRIO
        with st.form("form_resposta", clear_on_submit=True):
            user_input = st.text_input("Sua resposta:", key="input_usuario_chat")
            btn_enviar = st.form_submit_button("Enviar Mensagem 💬")

        if btn_enviar and user_input.strip():
            # 1. Adiciona a resposta do usuário
            st.session_state.lj_chat.append({"role": "user", "content": user_input})
            st.session_state.lj_ts_usuario = _t.time()

            # 2. PROMPT DE RESPOSTA INTELIGENTE (MESTRE DA LÁBIA)
            dados_p = PERSONAGENS.get(nome_p, PERSONAGENS["Rafaela"])
            
            prompt_ia = f"""
            Você está interpretando {nome_p} em um RPG realista de sedução e comunicação interpessoal.
            - Perfil: {dados_p['personalidade']}
            - Nível de conexão atual do usuário com você: {conexo}/100
            - Comportamento esperado se Conexão < 40: {dados_p['comportamento_baixo']}
            - Comportamento esperado se Conexão > 70: {dados_p['comportamento_alto']}
            - Cenário local: {cenario}

            Sua tarefa:
            1. Responda o usuário mantendo TOTALMENTE o papel de {nome_p}. Seja humana, viva, use linguagem coloquial brasileira. Jamais aja como um assistente de IA.
            2. Avalie a mensagem do usuário ("{user_input}"):
               - Se foi ruim (genérica, insegura, entediante, forçada): diminua a conexão em 5 a 15 pontos.
               - Se foi boa (espirituosa, autêntica, charmosa, prestou atenção no que você falou): aumente a conexão em 5 a 15 pontos.
            3. Verifique se o usuário cumpriu a missão atual: "{st.session_state.lj_missao}".

            Retorne estritamente um JSON no seguinte formato:
            {{
                "resposta": "Sua fala no personagem aqui",
                "delta_conexao": 10 ou -10,
                "motivo_mudanca": "Breve justificativa técnica do porque a conexão subiu ou desceu",
                "missao_cumprida": true ou false
            }}
            """

            # Chamada de API com JSON seguro
            res_raw = conexa_ia(prompt_ia, system_extra="Responda EXCLUSIVAMENTE no formato JSON exigido.")
            
            try:
                # Trata blocos de código se a IA mandar ```json ... ```
                json_clean = _r.sub(r'```json\s*|\s*```', '', res_raw).strip()
                dados_resp = json.loads(json_clean)
                
                # Atualiza Conexômetro
                delta = dados_resp.get("delta_conexao", 0)
                st.session_state.lj_conexo = max(0, min(100, st.session_state.lj_conexo + delta))
                
                # Adiciona resposta da IA no Chat
                arranque_txt = f"{'+' if delta>0 else ''}{delta} Conexão: {dados_resp.get('motivo_mudanca','')}"
                st.session_state.lj_chat.append({
                    "role": "assistant",
                    "content": dados_resp.get("resposta", "..."),
                    "arranque": arranque_txt
                })
                st.session_state.lj_ts_persona = _t.time()
                
                if dados_resp.get("missao_cumprida"):
                    st.session_state.lj_missao_cumprida = True

            except Exception as e:
                # Fallback inteligente se o JSON falhar
                st.session_state.lj_chat.append({
                    "role": "assistant",
                    "content": f"Hum, entendi... mas me conta mais sobre isso.",
                    "arranque": "Conexão Inalterada"
                })

            st.rerun()

    elif st.session_state.pagina == "Labia":
        st.title("💋 Mestre da Lábia")
        st.markdown("Escolha um personagem e teste suas habilidades de comunicação em tempo real.")

        col1, col2 = st.columns(2)
        with col1:
            nome_sel = st.selectbox("Escolha a Persona:", list(PERSONAGENS.keys()))
            pers = PERSONAGENS[nome_sel]
            st.markdown(f"**Dificuldade:** {pers['estrelas']}")
            st.markdown(f"**Estilo:** {pers['desc']}")

        with col2:
            cenario_sel = st.selectbox("Cenário:", ["Cafeteria", "Livraria", "Festa de Aniversário", "Academia", "Parque"])
            missao_sel = "Conseguir criar um clima descontraído e fazer ela rir ou se interessar espontaneamente."

        if st.button("🔥 Iniciar Conversa", use_container_width=True):
            st.session_state.lj_ativo = True
            st.session_state.lj_nome_persona = nome_sel
            st.session_state.lj_dados_persona = pers
            st.session_state.lj_cenario = cenario_sel
            st.session_state.lj_missao = missao_sel
            st.session_state.lj_conexo = 50
            st.session_state.lj_inicio = _t.time()
            st.session_state.lj_duracao = 300
            
            # Mensagem de abertura da IA baseada na persona
            prompt_abertura = f"Gere uma fala de abertura realista para {nome_sel} estando em um(a) {cenario_sel}. Seja natural."
            abertura = conexa_ia(prompt_abertura)

            st.session_state.lj_chat = [{"role": "assistant", "content": abertura}]
            st.session_state.pagina = "Dialogo"
            st.rerun()
