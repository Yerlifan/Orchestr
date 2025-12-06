import streamlit as st
import autogen
import uuid
import time
from datetime import datetime
import os
import utils 

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="ORCHESTR AI", page_icon="🛡", layout="wide")
utils.load_css()

# --- STATE BAŞLATMA ---
defaults = {"logged_in": False, "username": None, "avatar": "👤", "current_session_id": str(uuid.uuid4()), "chat_history": [], "terminal_logs": "", "is_running": False, "agents_config": [], "manager": None, "user_proxy": None, "admin_access": False}
for k,v in defaults.items(): 
    if k not in st.session_state: st.session_state[k] = v

# ==============================================================================
# GİRİŞ EKRANI
# ==============================================================================
if not st.session_state.logged_in:
    st.markdown("<div style='text-align: center; margin-top: 30px;'><h1>O R C H E S T R</h1><p>Profesyonel AI Takım Orkestrasyonu</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        t1, t2 = st.tabs(["Giriş Yap", "Kayıt Ol"])
        with t1:
            with st.form("l"):
                u = st.text_input("Kullanıcı Adı"); p = st.text_input("Şifre", type="password")
                if st.form_submit_button("Giriş", use_container_width=True):
                    ok, av = utils.login_user(u, p)
                    if ok:
                        st.session_state.logged_in = True; st.session_state.username = u; st.session_state.avatar = av
                        st.session_state.agents_config = utils.get_user_data(u, "team")
                        st.session_state.current_session_id = str(uuid.uuid4())
                        st.session_state.chat_history = []; st.session_state.terminal_logs = ""; st.session_state.is_running = False
                        st.rerun()
                    else: st.error("Hatalı!")
        with t2:
            with st.form("r"):
                nu = st.text_input("Kullanıcı Adı"); np = st.text_input("Şifre", type="password")
                nav = st.selectbox("Avatar", utils.AVATARS)
                if st.form_submit_button("Kayıt Ol", use_container_width=True):
                    ok, msg = utils.register_user(nu, np, nav)
                    if ok: st.success(msg)
                    else: st.error(msg)

    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #888;'>🏆 Ekip Üyelerimiz</h4>", unsafe_allow_html=True)
    usrs = utils.get_all_users()
    if usrs:
        h = '<div class="member-grid">' + "".join([f'<div class="member-card"><div class="member-avatar">{x["avatar"]}</div><div class="member-name">{x["name"]}</div></div>' for x in usrs]) + '</div>'
        st.markdown(h, unsafe_allow_html=True)
    
    st.markdown('<center><div class="mugendai-footer">⚡ Made by Mugendai ⚡</div></center>', unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# ANA UYGULAMA
# ==============================================================================

def create_new(): st.session_state.current_session_id = str(uuid.uuid4()); st.session_state.chat_history = []; st.session_state.terminal_logs = ""; st.session_state.is_running = False; st.session_state.manager = None; st.session_state.agents_config = []; st.rerun()

def save_chat():
    u = st.session_state.username; s = utils.get_user_data(u, "sessions"); sid = st.session_state.current_session_id
    t = s.get(sid, {}).get("title", "Yeni Ekip")
    if t == "Yeni Ekip" and st.session_state.chat_history:
        for m in st.session_state.chat_history:
            if m["name"] == u: t = m["content"][:30] + "..."; break
    s[sid] = {"id": sid, "title": t, "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "history": st.session_state.chat_history, "logs": st.session_state.terminal_logs, "agents": st.session_state.agents_config}
    utils.save_user_data(u, "sessions", s)

def load_chat(sid):
    d = utils.get_user_data(st.session_state.username, "sessions").get(sid)
    if d: st.session_state.current_session_id = d["id"]; st.session_state.chat_history = d["history"]; st.session_state.terminal_logs = d.get("logs", ""); st.session_state.agents_config = d.get("agents", []); st.session_state.is_running = False; st.rerun()

def del_chat(sid):
    u = st.session_state.username; s = utils.get_user_data(u, "sessions")
    if sid in s: del s[sid]; utils.save_user_data(u, "sessions", s); st.rerun() if st.session_state.current_session_id != sid else create_new()

def upd_title(nt):
    u = st.session_state.username; s = utils.get_user_data(u, "sessions"); sid = st.session_state.current_session_id
    if sid not in s: save_chat(); s = utils.get_user_data(u, "sessions")
    s[sid]["title"] = nt; utils.save_user_data(u, "sessions", s); st.rerun()

# HEADER
u = st.session_state.username; av = st.session_state.avatar
ct = utils.get_user_data(u, "sessions").get(st.session_state.current_session_id, {}).get("title", "Yeni Ekip")

with st.container():
    st.markdown(f"""<div class="header-container"><div><p class="header-title">O R C H E S T R</p><p class="header-subtitle">Aktif Ekip: <b>{ct}</b></p></div><div class="user-badge">{av} {u}</div></div>""", unsafe_allow_html=True)
    with st.popover("✏️"):
        nt = st.text_input("Ad", value=ct)
        if st.button("Kaydet", type="primary"): upd_title(nt)

# SIDEBAR
with st.sidebar:
    st.markdown('<marquee><H1>ORCHESTR</H1></marquee>', unsafe_allow_html=True)
    st.subheader("🗂️ AI Ekiplerim")
    if st.button("➕ Yeni Ekip", use_container_width=True): create_new()
    srt = sorted(utils.get_user_data(u, "sessions").items(), key=lambda x: x[1]['date'], reverse=True)
    with st.container(height=250):
        if not srt: st.caption("Yok.")
        for sid, sd in srt:
            c1, c2 = st.columns([5, 1])
            act = "🟢" if sid == st.session_state.current_session_id else "⚫"
            if c1.button(f"{act} {sd['title'][:15]}", key=sid, use_container_width=True): load_chat(sid)
            if c2.button("✖", key=f"d_{sid}"): del_chat(sid)
    
    st.divider()
    with st.expander("🎛️ Canlı Ayarlar", expanded=True):
        tmp = st.slider("Yaratıcılık", 0.0, 1.0, 0.2)
        fr = st.slider("İlk Tur", 5, 50, 8)
        fbr = st.slider("Feedback Turu", 1, 30, 5)
        meth = st.radio("Sıra:", ["Otomatik", "Sıralı"])
        smeth = "round_robin" if meth == "Sıralı" else "auto"
        if st.session_state.is_running and st.session_state.manager:
            try:
                st.session_state.manager.llm_config["temperature"] = tmp
                st.session_state.groupchat.speaker_selection_method = smeth
                for ag in st.session_state.groupchat.agents:
                    if "o1-" not in ag.llm_config["config_list"][0].get("model", ""): ag.llm_config["temperature"] = tmp
            except: pass

    # API YÖNETİMİ
    current_okey = st.session_state.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    current_gkey = st.session_state.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

    with st.expander("🔑 API Erişimi", expanded=False):
        if not st.session_state.admin_access:
            admin_input = st.text_input("Admin Şifresi", type="password")
            if admin_input:
                if admin_input == utils.ADMIN_PASSWORD:
                    st.session_state.admin_access = True
                    st.success("Açıldı 🔓"); time.sleep(0.5); st.rerun()
                else: st.error("Yanlış ❌")
        else:
            new_okey = st.text_input("OpenAI Key", value=current_okey, type="password")
            new_gkey = st.text_input("Google Key", value=current_gkey, type="password")
            if new_okey != current_okey: st.session_state["OPENAI_API_KEY"] = new_okey
            if new_gkey != current_gkey: st.session_state["GOOGLE_API_KEY"] = new_gkey
            current_okey = new_okey; current_gkey = new_gkey
            if st.button("🔒 Kilitle"): st.session_state.admin_access = False; st.rerun()
    
    st.divider()
    if st.button("🚪 Çıkış", use_container_width=True): st.session_state.clear(); st.rerun()

# MANTIK
MODELS = [{"label": "GPT-4.1", "model": "gpt-4.1", "api_type": "openai"}, {"label": "GPT-4o", "model": "gpt-4o", "api_type": "openai"}, {"label": "Gemini 2.5 Pro", "model": "gemini-2.5-pro", "api_type": "google"}, {"label": "Gemini 2.5 Flash", "model": "gemini-2.5-flash", "api_type": "google"}, {"label": "Gemini Pro Latest", "model": "gemini-pro-latest", "api_type": "google"}]
MLABS = [m["label"] for m in MODELS]

def start_orc():
    if not st.session_state.agents_config: st.error("Ekip boş!"); return
    if not current_okey and not current_gkey: st.error("API Anahtarı yok! Sol menüden ekleyin."); return
    
    lst = []; cfgs = []
    for ag in st.session_state.agents_config:
        k = current_okey if ag["model_config"]["api_type"] == "openai" else current_gkey
        cfg = [{"model": ag["model_config"]["model"], "api_key": k, "api_type": ag["model_config"]["api_type"]}]
        lc = {"config_list": cfg}
        if "o1-" not in ag["model_config"]["model"]: lc["temperature"] = tmp
        # Prompt güncellemesi: Kodları yaz ama çalıştırmaya çalışma
        msg = f"{ag['role']}. Takım olarak tartışın. Kodları markdown formatında yazın ama çalıştırmayı denemeyin (UserProxy çalıştıramaz). Ben (Patron) izliyorum. Sıra sana gelince susma."
        lst.append(autogen.AssistantAgent(name=ag["name"], system_message=msg, llm_config=lc))
        cfgs.append(cfg[0])
    
    # FIX: code_execution_config=False (HATA ÇÖZÜMÜ)
    up = autogen.UserProxyAgent(
        name=u, 
        human_input_mode="NEVER", 
        code_execution_config=False,
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""), 
        default_auto_reply="Harika gidiyor. Tartışmaya devam edin. Ben izliyorum."
    )
    lst.insert(0, up)
    
    h_msgs = [{"role": "user" if m["name"]==u else "assistant", "content": m["content"], "name": m["name"]} for m in st.session_state.chat_history]
    gc = autogen.GroupChat(agents=lst, messages=h_msgs, max_round=fr, speaker_selection_method=smeth)
    mgr = autogen.GroupChatManager(groupchat=gc, llm_config={"config_list": cfgs, "temperature": tmp})
    st.session_state.manager = mgr; st.session_state.user_proxy = up; st.session_state.groupchat = gc; st.session_state.is_running = True

# --- KURULUM ---
if not st.session_state.is_running:
    if not st.session_state.agents_config: st.info("👋 Yeni ekip kur.")
    with st.expander("➕ Üye Ekle", expanded=True):
        c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
        n = c1.text_input("İsim", placeholder="Dev"); r = c2.text_input("Rol"); m = c3.selectbox("Model", MLABS)
        if c4.button("Ekle", use_container_width=True):
            if n and r:
                sel = next(x for x in MODELS if x["label"] == m)
                st.session_state.agents_config.append({"name": n.replace(" ","_"), "role": r, "model_config": sel})
                utils.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.rerun()

    if st.session_state.agents_config:
        st.write("---")
        for i, ag in enumerate(st.session_state.agents_config):
            with st.expander(f"👤 {ag['name']} ({ag['model_config']['label']})"):
                c_up, c_dw, _ = st.columns([1,1,8])
                if c_up.button("⬆️", key=f"u{i}") and i>0:
                    l = st.session_state.agents_config; l[i], l[i-1] = l[i-1], l[i]
                    utils.save_user_data(u, "team", l); save_chat(); st.rerun()
                if c_dw.button("⬇️", key=f"d{i}") and i<len(st.session_state.agents_config)-1:
                    l = st.session_state.agents_config; l[i], l[i+1] = l[i+1], l[i]
                    utils.save_user_data(u, "team", l); save_chat(); st.rerun()
                
                nn = st.text_input("Ad", ag['name'], key=f"n{i}"); rr = st.text_area("Rol", ag['role'], key=f"r{i}")
                try: idx = MLABS.index(ag['model_config']['label'])
                except: idx = 0
                mm = st.selectbox("Model", MLABS, index=idx, key=f"md{i}")
                
                c1, c2 = st.columns(2)
                if c1.button("💾", key=f"sv{i}"):
                    ns = next(x for x in MODELS if x["label"] == mm)
                    st.session_state.agents_config[i] = {"name": nn, "role": rr, "model_config": ns}
                    utils.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.success("OK"); time.sleep(0.5); st.rerun()
                if c2.button("🗑️", key=f"dl{i}"):
                    st.session_state.agents_config.pop(i)
                    utils.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.rerun()

    if st.button("🚀 BAŞLAT", type="primary", use_container_width=True): start_orc(); save_chat(); st.rerun()

# --- SOHBET ---
else:
    with st.expander("🔒 Ekip"):
        for ag in st.session_state.agents_config: st.write(f"**{ag['name']}**: {ag['role']}")
        if st.button("🔴 Düzenle"): st.session_state.is_running = False; st.rerun()

    cc = st.container()
    with cc:
        for m in st.session_state.chat_history:
            avt = av if m["name"] == u else "🤖"
            with st.chat_message(m["name"], avatar=avt): st.markdown(f"**{m['name']}**: {m['content']}")

    st.write("---")
    tph = st.empty()

    pr = st.chat_input("Görev...")
    if pr:
        # Terminal ÇALIŞIYORKEN AÇIK
        with tph.expander("📺 Terminal (Çalışıyor...)", expanded=True):
            lb = st.empty()
            if st.session_state.terminal_logs: lb.code(st.session_state.terminal_logs, language="yaml")
            
            st.session_state.chat_history.append({"name": u, "content": pr})
            with cc:
                with st.chat_message(u, avatar=av): st.markdown(f"**{u}**: {pr}")
            save_chat()
            
            msg = f"FEEDBACK: {pr}" if len(st.session_state.chat_history) > 1 else pr
            cl = len(st.session_state.groupchat.messages)
            tgt = (cl + fbr) if len(st.session_state.chat_history) > 1 else fr
            st.session_state.groupchat.max_round = tgt
            
            with utils.capture_output(lb):
                with st.spinner("Ekip çalışıyor..."):
                    try: st.session_state.user_proxy.initiate_chat(st.session_state.manager, message=msg, clear_history=False)
                    except Exception as e: st.error(str(e))
            
            raw = st.session_state.groupchat.messages
            nh = []
            for m in raw:
                if m.get("content") and m.get("role") != "function":
                    nh.append({"name": m.get("name", "Asistan"), "content": m["content"]})
            st.session_state.chat_history = nh
            save_chat()
            st.rerun()