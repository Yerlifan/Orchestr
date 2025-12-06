import streamlit as st
import streamlit.components.v1 as components
import autogen
import uuid
import time
from datetime import datetime
import os

# MODÜLLER
import config
import data_handler as db
import styles

st.set_page_config(page_title="ORCHESTR", page_icon="🛡️", layout="wide")

# JS SCROLL FIX
components.html("""<script>function scrollToEnd(){const m=window.parent.document.querySelector(".main");if(m){m.scrollTo({top:m.scrollHeight,behavior:'smooth'});}}</script>""", height=0, width=0)

# INIT
defaults = {
    "logged_in": False, "username": None, "avatar": "👤",
    "current_session_id": str(uuid.uuid4()), "chat_history": [],
    "terminal_logs": "", "is_running": False, "agents_config": [],
    "manager": None, "user_proxy": None, "admin_access": False,
    "rag_content": "", "language": "TR", "theme": "Kızıl", "bg_color": "#0E1117"
}
for k, v in defaults.items(): 
    if k not in st.session_state: st.session_state[k] = v

T = config.LANG[st.session_state.language]
if st.session_state.theme not in config.THEMES: st.session_state.theme = "Kızıl"
theme_hex = config.THEMES[st.session_state.theme]
styles.load_css(theme_hex, st.session_state.bg_color)

# ==============================================================================
# GİRİŞ EKRANI
# ==============================================================================
if not st.session_state.logged_in:
    st.markdown(f"<div style='text-align: center; margin-top: 20px; color: #888; font-size: 0.8rem; letter-spacing: 2px;'>{T['our_team']}</div>", unsafe_allow_html=True)
    usrs = db.get_all_users()
    if usrs:
        html = '<div class="team-showcase">'
        for u in usrs:
            html += f'<div class="team-card"><div class="team-avatar">{u["avatar"]}</div><div class="team-name">{u["name"]}</div></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    else: st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown(f"""<div class="login-container"><div class="login-logo">🛡️</div><div class="login-title">{T['login_header']}</div><div class="login-sub">{T['login_sub']}</div></div>""", unsafe_allow_html=True)
        t1, t2 = st.tabs([T["login_title"], T["reg_title"]])
        with t1:
            with st.form("login_form"):
                u = st.text_input(T["username"], key="l_u")
                p = st.text_input(T["pass"], type="password", key="l_p")
                rem = st.checkbox(T["remember"])
                if st.form_submit_button(T["login_btn"], use_container_width=True, type="primary"):
                    ok, av = db.login_user(u, p)
                    if ok:
                        st.session_state.logged_in = True; st.session_state.username = u; st.session_state.avatar = av
                        st.session_state.agents_config = []
                        st.session_state.current_session_id = str(uuid.uuid4()); st.session_state.chat_history = []; st.session_state.terminal_logs = ""; st.session_state.is_running = False; st.session_state.rag_content = ""
                        st.rerun()
                    else: st.error("Hatalı")
        with t2:
            with st.form("reg_form"):
                nu = st.text_input(T["username"], key="r_u"); np = st.text_input(T["pass"], type="password", key="r_p"); nav = st.selectbox("Avatar", config.AVATARS)
                if st.form_submit_button(T["reg_btn"], use_container_width=True):
                    ok, msg = db.register_user(nu, np, nav)
                    if ok: st.success(msg)
                    else: st.error(msg)
    st.markdown('<div class="mugendai-footer">Designed by Mugendai (aka Yerlifan) ⚡</div>', unsafe_allow_html=True)
    st.stop()

# ==============================================================================
# ANA UYGULAMA
# ==============================================================================
u = st.session_state.username; av = st.session_state.avatar

# HELPERLAR
def create_new(): st.session_state.current_session_id = str(uuid.uuid4()); st.session_state.chat_history = []; st.session_state.terminal_logs = ""; st.session_state.is_running = False; st.session_state.manager = None; st.session_state.agents_config = []; st.session_state.rag_content = ""; st.rerun()
def save_chat():
    s = db.get_user_data(u, "sessions"); sid = st.session_state.current_session_id
    t = s.get(sid, {}).get("title", T["new_chat"])
    if t == T["new_chat"] and st.session_state.chat_history:
        for m in st.session_state.chat_history:
            if m["name"] == u: t = m["content"][:30] + "..."; break
    s[sid] = {"id": sid, "title": t, "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "history": st.session_state.chat_history, "logs": st.session_state.terminal_logs, "agents": st.session_state.agents_config}
    db.save_user_data(u, "sessions", s)
def load_chat(sid):
    d = db.get_user_data(st.session_state.username, "sessions").get(sid)
    if d: st.session_state.current_session_id = d["id"]; st.session_state.chat_history = d["history"]; st.session_state.terminal_logs = d.get("logs", ""); st.session_state.agents_config = d.get("agents", []); st.session_state.is_running = False; st.session_state.rag_content = ""; st.rerun()
def del_chat(sid):
    s = db.get_user_data(u, "sessions"); 
    if sid in s: del s[sid]
    db.save_user_data(u, "sessions", s)
    if st.session_state.current_session_id == sid: create_new()
    else: st.rerun()
def upd_title(nt): s = db.get_user_data(u, "sessions"); sid = st.session_state.current_session_id; s[sid]["title"] = nt if sid in s else None; db.save_user_data(u, "sessions", s); st.rerun()
def move_agent(i, d): l = st.session_state.agents_config; l[i], l[i+d] = l[i+d], l[i]; db.save_user_data(u, "team", l); save_chat(); st.rerun()
def del_agent(i): st.session_state.agents_config.pop(i); db.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.rerun()

# HEADER
ct = db.get_user_data(u, "sessions").get(st.session_state.current_session_id, {}).get("title", T["new_chat"])
st.markdown(f"""<div class="header-container"><div><p class="header-title">ORCHESTR</p><p class="header-sub">{T['active_project']}: {ct}</p></div><div class="user-badge">{av} {u}</div></div>""", unsafe_allow_html=True)
with st.popover(f"✏️ {T['edit_title']}"):
    nt = st.text_input("Name", value=ct)
    if st.button(T["save"], type="primary"): upd_title(nt)

# SIDEBAR
with st.sidebar:
    c1, c2 = st.columns(2)
    with c1:
        k = list(config.THEMES.keys()); c = st.session_state.theme if st.session_state.theme in k else "Kızıl"
        sel_t = st.selectbox(T["theme_sel"], k, index=k.index(c))
        if sel_t != st.session_state.theme: st.session_state.theme = sel_t; st.rerun()
    with c2:
        st.session_state.bg_color = st.color_picker(T["bg_sel"], value=st.session_state.bg_color)
    st.session_state.language = st.selectbox(T["lang_sel"], ["TR", "EN"], index=0 if st.session_state.language=="TR" else 1)
    
    st.divider()
    st.subheader(f"🗂️ {T['my_chats']}")
    if st.button(f"➕ {T['new_chat']}", use_container_width=True): create_new()
    srt = sorted(db.get_user_data(u, "sessions").items(), key=lambda x: x[1]['date'], reverse=True)
    with st.container(height=250):
        if not srt: st.caption("-")
        for sid, sd in srt:
            c1, c2 = st.columns([5, 1])
            act = "🟢" if sid == st.session_state.current_session_id else "⚫"
            if c1.button(f"{act} {sd['title'][:18]}", key=sid, use_container_width=True): load_chat(sid)
            if c2.button("✖", key=f"d_{sid}"): del_chat(sid)

    with st.expander(f"🎛️ {T['settings']}", expanded=True):
        tmp = st.slider(T["creativity"], 0.0, 1.0, 0.2)
        fr = st.slider(T["first_turn"], 3, 50, 5) # Default 5
        fbr = st.slider(T["fb_turn"], 1, 30, 2)   # Default 2
        meth = st.radio(T["order"], [T["auto"], T["seq"]]); smeth = "round_robin" if meth == T["seq"] else "auto"
        if st.session_state.is_running and st.session_state.manager:
            try: st.session_state.manager.llm_config["temperature"] = tmp; st.session_state.groupchat.speaker_selection_method = smeth
            except: pass

    curr_okey = st.session_state.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
    curr_gkey = st.session_state.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    with st.expander(f"🔑 {T['api_access']}", expanded=False):
        if not st.session_state.admin_access:
            if st.text_input(T["admin_pass"], type="password") == config.ADMIN_PASSWORD: st.session_state.admin_access = True; st.rerun()
        else:
            n1 = st.text_input("OpenAI Key", value=curr_okey, type="password"); n2 = st.text_input("Google Key", value=curr_gkey, type="password")
            if n1 != curr_okey: st.session_state["OPENAI_API_KEY"] = n1
            if n2 != curr_gkey: st.session_state["GOOGLE_API_KEY"] = n2
    
    st.markdown('<div class="mugendai-footer">Made by Mugendai ⚡</div>', unsafe_allow_html=True)
    st.divider()
    if st.button(f"🚪 {T['logout']}", use_container_width=True): st.session_state.clear(); st.rerun()

# LOGIC
def start_orc():
    if not st.session_state.agents_config: st.error("Empty!"); return
    k1 = st.session_state.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))
    k2 = st.session_state.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY"))
    if not k1 and not k2: st.error(T["no_api"]); return
    lst = []; cfgs = []
    
    rag_info = "" 
    if st.session_state.rag_content: rag_info = f"\n\n[FILE CONTEXT]:\n{st.session_state.rag_content[:15000]}..."

    # --- TAKIM BİLGİSİNİ HAZIRLA ---
    team_members = st.session_state.agents_config
    team_size = len(team_members)
    roster_text = "EKİP ÜYELERİ:\n"
    for member in team_members:
        roster_text += f"- {member['name']} ({member['role']})\n"

    for ag in st.session_state.agents_config:
        k = k1 if ag["model_config"]["api_type"] == "openai" else k2
        cfg = [{"model": ag["model_config"]["model"], "api_key": k, "api_type": ag["model_config"]["api_type"]}]
        lc = {"config_list": cfg}
        if "o1-" not in ag["model_config"]["model"]: lc["temperature"] = tmp
        
        msg = f"""Sen {ag['name']}. Rolün: {ag['role']}.
        
        [TAKIM BİLGİSİ]:
        Bu ekip toplam {team_size} kişiden oluşuyor.
        {roster_text}
        
        [GÖREV KURALLARI]:
        1. Diğer ekip üyelerinin (ajanların) yazdıklarını dikkatle oku ve anladığını belli et.
        2. Kendi aranızda tartışın.
        3. Bu görev için toplam {fr} tur (döngü) hakkınız var. Zamanı iyi kullan.
        4. "Sıra sende", "Ne düşünüyorsun?" deme. İşi yap.
        5. Kod yaz ama çalıştırma.
        6. Kullanıcı (Patron) sadece izliyor, ona soru sorma.
        
        {rag_info}"""
        
        lst.append(autogen.AssistantAgent(name=ag["name"], system_message=msg, llm_config=lc))
        cfgs.append(cfg[0])
    
    # USER PROXY FIX
    up = autogen.UserProxyAgent(
        name=u, 
        human_input_mode="NEVER", 
        code_execution_config=False, 
        is_termination_msg=lambda x: False, # Sürekli konuşması için False
        default_auto_reply="Devam edin. İlerleyin."
    )
    lst.insert(0, up)
    
    h_msgs = [{"role": "user" if m["name"]==u else "assistant", "content": m["content"], "name": m["name"]} for m in st.session_state.chat_history]
    
    # MATEMATİK (Döngü Sayısı * Ajan Sayısı)
    # fr = Döngü Sayısı (Kullanıcının seçtiği tur)
    # num_agents = Ajan sayısı
    num_agents = len(st.session_state.agents_config)
    start_round = (fr * num_agents) + len(h_msgs) + 2

    gc = autogen.GroupChat(agents=lst, messages=h_msgs, max_round=start_round, speaker_selection_method=smeth)
    mgr = autogen.GroupChatManager(groupchat=gc, llm_config={"config_list": cfgs, "temperature": tmp})
    st.session_state.manager = mgr; st.session_state.user_proxy = up; st.session_state.groupchat = gc; st.session_state.is_running = True

# --- UI STATES ---
if not st.session_state.is_running:
    if not st.session_state.agents_config: st.info(f"👋 {T['welcome']} {u}")
    
    with st.expander(f"{T['import_title']}", expanded=False):
        past = db.get_all_past_agents(u)
        if past:
            sel = st.selectbox("Seç:", list(past.keys()))
            if st.button(T["import_btn"]):
                st.session_state.agents_config.append(past[sel]); db.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.rerun()
        else: st.caption(T["no_past_agent"])

    with st.expander(f"➕ {T['add_agent']}", expanded=True):
        c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
        n = c1.text_input(T["name"], placeholder="Scientist, Guide, Programmer"); r = c2.text_input(T["role"]); m = c3.selectbox(T["model"], config.MLABS)
        if c4.button(T["add_agent"], use_container_width=True):
            if n and r:
                sl = next(x for x in config.MODELS if x["label"] == m)
                st.session_state.agents_config.append({"name": n.replace(" ","_"), "role": r, "model_config": sl})
                db.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.rerun()

    if st.session_state.agents_config:
        st.write("---")
        for i, ag in enumerate(st.session_state.agents_config):
            m_label = ag['model_config']['label'] if isinstance(ag.get('model_config'), dict) else "Unknown"
            with st.expander(f"👤 {ag['name']} ({m_label})"):
                c_up, c_dw, _ = st.columns([1, 1, 8])
                if c_up.button("⬆️", key=f"u{i}") and i>0: move_agent(i, -1)
                if c_dw.button("⬇️", key=f"d{i}") and i<len(st.session_state.agents_config)-1: move_agent(i, 1)
                nn = st.text_input(T["name"], value=ag['name'], key=f"nm{i}"); rr = st.text_area(T["role"], value=ag['role'], key=f"rl{i}")
                try: idx = config.MLABS.index(m_label)
                except: idx = 0
                mm = st.selectbox(T["model"], config.MLABS, index=idx, key=f"md{i}")
                c_sv, c_del = st.columns(2)
                if c_sv.button("💾 " + T["save"], key=f"sv{i}"):
                    ns = next(x for x in config.MODELS if x["label"] == mm)
                    st.session_state.agents_config[i] = {"name": nn.replace(" ", "_"), "role": rr, "model_config": ns}
                    db.save_user_data(u, "team", st.session_state.agents_config); save_chat(); st.success("OK"); time.sleep(0.5); st.rerun()
                if c_del.button("🗑️ " + T["delete"], key=f"dl{i}"): del_agent(i)

    if st.button(f"🚀 {T['start_btn']}", type="primary", use_container_width=True): start_orc(); save_chat(); st.rerun()

else:
    with st.expander(f"🔒 {T['active_team']}"):
        for ag in st.session_state.agents_config: st.write(f"**{ag['name']}**: {ag['role']}")

    cc = st.container()
    with cc:
        for idx, m in enumerate(st.session_state.chat_history):
            avt = av if m["name"] == u else "🤖"
            disp = f"**{m['name']}**" if m["name"] == u else f"**{m['name']}** (Msg #{idx+1})"
            with st.chat_message(m["name"], avatar=avt): st.write(disp); st.markdown(f"{m['content']}")

    st.write("---")
   
    c_att, c_stop, c_in = st.columns([0.5, 0.5, 5])
    with c_att:
        with st.popover(f"📎"):
            st.caption(T['file_help'])
            ud = st.file_uploader(T["upload_doc"], type=['pdf', 'txt'], key="cdoc")
            if ud: st.session_state.rag_content = db.read_uploaded_file(ud); st.success("OK")
    with c_stop:
        if st.button(T["stop_icon"], help=T["stop_task"]): st.session_state.is_running = False; st.rerun()
    with c_in:
        pr = st.chat_input(T["chat_input"], key="main_chat_unique")

    tph = st.empty()
    if st.session_state.terminal_logs and not st.session_state.get("processing", False):
        with tph.container():
             with st.expander(f"📺 {T['terminal']}", expanded=False): st.code(st.session_state.terminal_logs, language="yaml")

    if pr:
        st.session_state.processing = True
        with tph.container():
            with st.expander(f"📺 {T['terminal']} ({T['working']})", expanded=False):
                lb = st.empty()
                if st.session_state.terminal_logs: lb.code(st.session_state.terminal_logs, language="yaml")
                st.session_state.chat_history.append({"name": u, "content": pr})
                with cc: 
                    with st.chat_message(u, avatar=av): 
                        st.write(f"**{u}** (Msg #{len(st.session_state.chat_history)})")
                        st.markdown(pr)
                save_chat()
                
                rag_app = f"\n\n--- FILE ---\n{st.session_state.rag_content[:20000]}\n--- END ---" if st.session_state.rag_content else ""
                
                current_msgs = len(st.session_state.groupchat.messages)
                num_agents = len(st.session_state.agents_config)
                if num_agents == 0: num_agents = 1
                
                if len(st.session_state.chat_history) <= 2:
                    # İlk tur
                    tgt = (fr * num_agents) + 2
                    msg = f"{pr} {rag_app}"
                else:
                    # Feedback turu
                    tgt = (fbr * num_agents) + 2
                    msg = f"{T['feedback_label']} {pr}"
                
                st.session_state.groupchat.max_round = tgt
                
                with styles.capture_output(lb):
                    with st.spinner(T["working"]):
                        try: st.session_state.user_proxy.initiate_chat(st.session_state.manager, message=msg, clear_history=False)
                        except Exception as e: st.error(str(e))
        
        raw = st.session_state.groupchat.messages
        nh = []
        for m in raw:
            if m.get("content") and m.get("role") != "function":
                nh.append({"name": m.get("name", "Asistan"), "content": m["content"]})
        st.session_state.chat_history = nh
        save_chat()
        st.session_state.processing = False
        st.rerun()