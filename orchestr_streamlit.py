import streamlit as st
import autogen
import os
import time
import json
import sys
import re
import uuid
import hashlib
from contextlib import contextmanager
from datetime import datetime

# --- 1. AYARLAR VE KLASÖR YAPISI ---
DB_FOLDER = "orchestr_db"
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)
USERS_FILE = os.path.join(DB_FOLDER, "users.json")

# --- AVATAR LİSTESİ ---
AVATARS = ["👨‍💻", "👩‍💻", "🚀", "🧠", "🦁", "🦉", "🦄", "🎨", "⚡", "🤖", "🔥", "💎", "🛡️", "👑", "👽", "👻", "🐯"]

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="ORCHESTR AI", page_icon="👤", layout="wide")

# --- CSS (GÖRSELLİK) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    
    /* Header */
    .header-container {
        padding: 20px; background: linear-gradient(90deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 15px; border-left: 5px solid #FF4B4B; margin-bottom: 20px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .header-title { font-size: 32px; font-weight: bold; color: white; margin: 0; }
    .header-subtitle { font-size: 14px; color: #BBB; margin: 0; }
    .user-badge { background-color: #333; padding: 5px 15px; border-radius: 20px; border: 1px solid #555; font-weight: bold; }
    
    /* Üye Kartları */
    .member-grid { display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 30px; }
    .member-card {
        background-color: #262730; border: 1px solid #444; border-radius: 12px;
        padding: 15px; width: 110px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s, border-color 0.2s;
    }
    .member-card:hover { transform: translateY(-5px); border-color: #FF4B4B; }
    .member-avatar { font-size: 45px; margin-bottom: 8px; }
    .member-name { font-size: 13px; color: #EEE; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    
    /* Sohbet ve Terminal */
    .stChatMessage { background-color: #262730; border-radius: 10px; border: 1px solid #444; }
    .stCodeBlock { border: 1px solid #00FF00 !important; }
</style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def load_json(path, default=None):
    if default is None:
        default = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- KULLANICI FONKSİYONLARI ---
def register_user(username, password, avatar):
    users = load_json(USERS_FILE)
    if username in users:
        return False, "Kullanıcı adı alınmış."
    users[username] = {
        "password": hash_password(password),
        "avatar": avatar,
        "created_at": str(datetime.now())
    }
    save_json(USERS_FILE, users)
    return True, "Kayıt başarılı! Giriş yapın."

def login_user(username, password):
    users = load_json(USERS_FILE)
    if username not in users:
        return False, None
    if users[username]["password"] == hash_password(password):
        return True, users[username].get("avatar", "👤")
    return False, None

def get_all_users():
    users = load_json(USERS_FILE)
    return [{"name": k, "avatar": v.get("avatar", "👤")} for k, v in users.items()]

# --- DOSYA YÖNETİMİ ---
def get_user_files(u):
    return {
        "sessions": os.path.join(DB_FOLDER, f"{u}_sessions.json"),
        "team": os.path.join(DB_FOLDER, f"{u}_team.json")
    }

def get_user_data(u, t):
    p = get_user_files(u)
    if t == "sessions":
        return load_json(p["sessions"], {})
    else:
        return load_json(p["team"], [])

def save_user_data(u, t, d):
    p = get_user_files(u)
    if t == "sessions":
        save_json(p["sessions"], d)
    else:
        save_json(p["team"], d)

# --- CANLI AKIŞ ---
class StreamlitOutputStream:
    def __init__(self, c):
        self.c = c
        self.ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    def write(self, d):
        st.session_state.terminal_logs += self.ansi.sub('', d)
        self.c.code(st.session_state.terminal_logs, language="yaml")
    def flush(self):
        pass

@contextmanager
def capture_output(c):
    new = StreamlitOutputStream(c)
    old = sys.stdout
    sys.stdout = new
    try:
        yield
    finally:
        sys.stdout = old

# --- SESSION BAŞLATMA ---
def init_state():
    defaults = {
        "logged_in": False, "username": None, "avatar": "👤",
        "current_session_id": str(uuid.uuid4()), "chat_history": [],
        "terminal_logs": "", "is_running": False, "agents_config": [],
        "manager": None, "user_proxy": None
    }
    for k, v in defaults.items(): 
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# ==============================================================================
# GİRİŞ EKRANI
# ==============================================================================
if not st.session_state.logged_in:
    st.markdown("<div style='text-align: center; margin-top: 30px;'><h1>O R C H E S T R</h1><p>Profesyonel AI Takım Orkestrasyonu</p></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        tab1, tab2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        with tab1:
            with st.form("login"):
                u = st.text_input("Kullanıcı Adı")
                p = st.text_input("Şifre", type="password")
                if st.form_submit_button("Giriş Yap", use_container_width=True):
                    ok, av = login_user(u, p)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.session_state.avatar = av
                        st.session_state.agents_config = get_user_data(u, "team")
                        # GİRİŞTE YENİ SOHBET BAŞLAT (TEMİZLİK)
                        st.session_state.current_session_id = str(uuid.uuid4())
                        st.session_state.chat_history = []
                        st.session_state.terminal_logs = ""
                        st.session_state.is_running = False
                        st.rerun()
                    else:
                        st.error("Hatalı bilgi.")
        with tab2:
            with st.form("reg"):
                nu = st.text_input("Kullanıcı Adı")
                np = st.text_input("Şifre", type="password")
                nav = st.selectbox("Avatar Seçin", AVATARS)
                if st.form_submit_button("Kayıt Ol", use_container_width=True):
                    if nu and np:
                        ok, msg = register_user(nu, np, nav)
                        if ok: st.success(msg)
                        else: st.error(msg)
                    else:
                        st.warning("Bilgileri doldurun.")

    # Üye Vitrini
    st.markdown("---")
    st.markdown("<h5 style='text-align: center; color: #666;'>🚀 Takım Arkadaşlarımız</h5>", unsafe_allow_html=True)
    users = get_all_users()
    if users:
        html = '<div class="member-grid">'
        for usr in users:
            html += f'<div class="member-card"><div class="member-avatar">{usr["avatar"]}</div><div class="member-name">{usr["name"]}</div></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    st.stop()
    # ==============================================================================
# ANA UYGULAMA
# ==============================================================================

# --- YARDIMCI FONKSİYONLAR ---
def create_new_chat():
    st.session_state.current_session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.terminal_logs = ""
    st.session_state.is_running = False
    st.session_state.manager = None
    st.rerun()

def save_current_chat():
    u = st.session_state.username
    sessions = get_user_data(u, "sessions")
    sid = st.session_state.current_session_id
    
    curr_t = sessions.get(sid, {}).get("title", "Yeni AI Ekibi")
    if curr_t == "Yeni AI Ekibi" and st.session_state.chat_history:
        for m in st.session_state.chat_history:
            if m["name"] == u:
                curr_t = m["content"][:30] + "..."
                break
                
    sessions[sid] = {
        "id": sid,
        "title": curr_t,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "history": st.session_state.chat_history,
        "logs": st.session_state.terminal_logs,
        "agents": st.session_state.agents_config
    }
    save_user_data(u, "sessions", sessions)

def load_chat(sid):
    s = get_user_data(st.session_state.username, "sessions").get(sid)
    if s:
        st.session_state.current_session_id = s["id"]
        st.session_state.chat_history = s["history"]
        st.session_state.terminal_logs = s.get("logs", "")
        st.session_state.agents_config = s.get("agents", [])
        st.session_state.is_running = False
        st.rerun()

def delete_chat(sid):
    u = st.session_state.username
    s = get_user_data(u, "sessions")
    if sid in s:
        del s[sid]
        save_user_data(u, "sessions", s)
        if st.session_state.current_session_id == sid:
            create_new_chat()
        else:
            st.rerun()

def update_title(nt):
    u = st.session_state.username
    s = get_user_data(u, "sessions")
    sid = st.session_state.current_session_id
    if sid not in s:
        save_current_chat()
        s = get_user_data(u, "sessions")
    s[sid]["title"] = nt
    save_user_data(u, "sessions", s)
    st.rerun()

# --- HEADER ---
u = st.session_state.username
av = st.session_state.avatar
ct = get_user_data(u, "sessions").get(st.session_state.current_session_id, {}).get("title", "Yeni AI Ekibi")

with st.container():
    st.markdown(f"""
    <div class="header-container">
        <div><p class="header-title">O R C H E S T R</p><p class="header-subtitle">Aktif Ekip: <b>{ct}</b></p></div>
        <div class="user-badge">{av} {u}</div>
    </div>""", unsafe_allow_html=True)
    
    with st.popover("✏️"):
        nt = st.text_input("Ekip Adı", value=ct)
        if st.button("Kaydet", type="primary"):
            update_title(nt)

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("🗂️ AI Ekiplerim")
    if st.button("➕ Yeni Ekip", use_container_width=True):
        create_new_chat()
    
    srt = sorted(get_user_data(u, "sessions").items(), key=lambda x: x[1]['date'], reverse=True)
    with st.container(height=250):
        if not srt:
            st.caption("Liste boş.")
        for sid, sd in srt:
            c1, c2 = st.columns([5, 1])
            act = "🟢" if sid == st.session_state.current_session_id else "⚫"
            if c1.button(f"{act} {sd['title'][:18]}", key=sid, use_container_width=True):
                load_chat(sid)
            if c2.button("✖", key=f"d_{sid}"):
                delete_chat(sid)

    st.divider()
    with st.expander("🎛️ Canlı Ayarlar", expanded=True):
        tmp = st.slider("Yaratıcılık", 0.0, 1.0, 0.2)
        fr = st.slider("İlk Tur", 5, 50, 15)
        fbr = st.slider("Feedback Turu", 3, 30, 8)
        meth = st.radio("Sıra:", ["Otomatik", "Sıralı"])
        smeth = "round_robin" if meth == "auto" else "Sıralı"
        
        # Canlı Güncelleme
        if st.session_state.is_running and st.session_state.manager:
            try:
                st.session_state.manager.llm_config["temperature"] = tmp
                st.session_state.groupchat.speaker_selection_method = smeth
                for ag in st.session_state.groupchat.agents:
                    if hasattr(ag, 'llm_config') and "config_list" in ag.llm_config:
                        if "o1-" not in ag.llm_config["config_list"][0].get("model", ""):
                            ag.llm_config["temperature"] = tmp
            except: pass

    with st.expander("🔑 API"):
        okey = st.text_input("OpenAI", value=os.environ.get("OPENAI_API_KEY", ""), type="password")
        gkey = st.text_input("Google", value=os.environ.get("GOOGLE_API_KEY", ""), type="password")

    st.divider()
    if st.button("🚪 Çıkış", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- MANTIK ---
MODELS = [{"label": "GPT-4.1", "model": "gpt-4.1", "api_type": "openai"}, {"label": "GPT-4o", "model": "gpt-4o", "api_type": "openai"}, {"label": "Gemini 2.5 Pro", "model": "gemini-2.5-pro", "api_type": "google"}, {"label": "Gemini 2.5 Flash", "model": "gemini-2.5-flash", "api_type": "google"}, {"label": "Gemini Pro Latest", "model": "gemini-pro-latest", "api_type": "google"}]
MLABS = [m["label"] for m in MODELS]

def start_orc():
    if not st.session_state.agents_config:
        st.error("Ekip boş!")
        return
    lst = []; cfgs = []
    for ag in st.session_state.agents_config:
        k = okey if ag["model_config"]["api_type"] == "openai" else gkey
        cfg = [{"model": ag["model_config"]["model"], "api_key": k, "api_type": ag["model_config"]["api_type"]}]
        lc = {"config_list": cfg}
        if "o1-" not in ag["model_config"]["model"]:
            lc["temperature"] = tmp
        
        msg = f"{ag['role']}. Takım olarak tartışın. Ben (Patron) izliyorum. Sıra sana gelince susma."
        lst.append(autogen.AssistantAgent(name=ag["name"], system_message=msg, llm_config=lc))
        cfgs.append(cfg[0])
    
    # Auto-Reply Fix
    up = autogen.UserProxyAgent(
        name=u, human_input_mode="NEVER", code_execution_config={"use_docker": False},
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        default_auto_reply="Devam edin, izliyorum."
    )
    lst.insert(0, up)
    
    h_msgs = []
    if st.session_state.chat_history:
        for m in st.session_state.chat_history:
            r = "user" if m["name"] == u else "assistant"
            h_msgs.append({"role": r, "content": m["content"], "name": m["name"]})

    gc = autogen.GroupChat(agents=lst, messages=h_msgs, max_round=fr, speaker_selection_method=smeth)
    mgr = autogen.GroupChatManager(groupchat=gc, llm_config={"config_list": cfgs, "temperature": tmp})
    st.session_state.manager = mgr; st.session_state.user_proxy = up; st.session_state.groupchat = gc; st.session_state.is_running = True

# --- KURULUM EKRANI ---
if not st.session_state.is_running:
    if not st.session_state.agents_config:
        st.info("👋 Yeni ekip kur.")
    with st.expander("➕ Üye Ekle", expanded=True):
        c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
        n = c1.text_input("İsim", placeholder="Örn. Yazılımcı, Felsefe")
        r = c2.text_input("Rol", placeholder="Fizik Motoru Uzmanı")
        m = c3.selectbox("Model", MLABS)
        if c4.button("Ekle", use_container_width=True):
            if n and r:
                sel = next(x for x in MODELS if x["label"] == m)
                st.session_state.agents_config.append({"name": n.replace(" ","_"), "role": r, "model_config": sel})
                save_user_data(u, "team", st.session_state.agents_config)
                save_current_chat()
                st.rerun()

    if st.session_state.agents_config:
        st.write("---")
        for i, ag in enumerate(st.session_state.agents_config):
            with st.expander(f"👤 {ag['name']} ({ag['model_config']['label']})"):
                c_up, c_dw, _ = st.columns([1,1,8])
                if c_up.button("⬆️", key=f"u{i}") and i>0:
                    l = st.session_state.agents_config
                    l[i], l[i-1] = l[i-1], l[i]
                    save_user_data(u, "team", l)
                    save_current_chat()
                    st.rerun()
                if c_dw.button("⬇️", key=f"d{i}") and i<len(st.session_state.agents_config)-1:
                    l = st.session_state.agents_config
                    l[i], l[i+1] = l[i+1], l[i]
                    save_user_data(u, "team", l)
                    save_current_chat()
                    st.rerun()
                
                nn = st.text_input("Ad", ag['name'], key=f"nm{i}")
                rr = st.text_area("Rol", ag['role'], key=f"rl{i}")
                try: idx = MLABS.index(ag['model_config']['label'])
                except: idx = 0
                mm = st.selectbox("Model", MLABS, index=idx, key=f"md{i}")
                
                c1, c2 = st.columns(2)
                if c1.button("💾", key=f"sv{i}"):
                    ns = next(x for x in MODELS if x["label"] == mm)
                    st.session_state.agents_config[i] = {"name": nn, "role": rr, "model_config": ns}
                    save_user_data(u, "team", st.session_state.agents_config)
                    save_current_chat()
                    st.success("OK")
                    time.sleep(0.5)
                    st.rerun()
                if c2.button("🗑️", key=f"dl{i}"):
                    st.session_state.agents_config.pop(i)
                    save_user_data(u, "team", st.session_state.agents_config)
                    save_current_chat()
                    st.rerun()

    if st.button("🚀 BAŞLAT", type="primary", use_container_width=True):
        start_orc()
        save_current_chat()
        st.rerun()

# --- SOHBET EKRANI ---
else:
    with st.expander("🔒 Ekip"):
        for ag in st.session_state.agents_config:
            st.write(f"**{ag['name']}**: {ag['role']}")
        if st.button("🔴 Düzenle"):
            st.session_state.is_running = False
            st.rerun()

    cc = st.container()
    with cc:
        for m in st.session_state.chat_history:
            avt = av if m["name"] == u else "🤖"
            with st.chat_message(m["name"], avatar=avt):
                st.markdown(f"**{m['name']}**: {m['content']}")

    st.write("---")
    tph = st.empty()

    pr = st.chat_input("Görev...")
    if pr:
        with tph.expander("📺 Terminal (Çalışıyor...)", expanded=True):
            lb = st.empty()
            if st.session_state.terminal_logs:
                lb.code(st.session_state.terminal_logs, language="yaml")
            
            st.session_state.chat_history.append({"name": u, "content": pr})
            with cc:
                with st.chat_message(u, avatar=av):
                    st.markdown(f"**{u}**: {pr}")
            save_current_chat()
            
            msg = f"FEEDBACK: {pr}" if len(st.session_state.chat_history) > 1 else pr
            cl = len(st.session_state.groupchat.messages)
            tgt = (cl + fbr) if len(st.session_state.chat_history) > 1 else fr
            st.session_state.groupchat.max_round = tgt
            
            with capture_output(lb):
                with st.spinner("Ekip çalışıyor..."):
                    try:
                        st.session_state.user_proxy.initiate_chat(st.session_state.manager, message=msg, clear_history=False)
                    except Exception as e:
                        st.error(str(e))
            
            raw = st.session_state.groupchat.messages
            nh = []
            for m in raw:
                if m.get("content") and m.get("role") != "function":
                    nh.append({"name": m.get("name", "Asistan"), "content": m["content"]})
            st.session_state.chat_history = nh
            save_current_chat()
            st.rerun()