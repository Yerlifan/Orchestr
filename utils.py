import os
import json
import hashlib
import sys
import re
import streamlit as st
from datetime import datetime
from contextlib import contextmanager

# --- AYARLAR ---
DB_FOLDER = "orchestr_db"
if not os.path.exists(DB_FOLDER): os.makedirs(DB_FOLDER)
USERS_FILE = os.path.join(DB_FOLDER, "users.json")

# Admin Şifresi
ADMIN_PASSWORD = "yerlifan123"

AVATARS = ["👨‍💻", "👩‍💻", "🚀", "🧠", "🦁", "🦉", "🦄", "🎨", "⚡", "🤖", "🔥", "💎", "🛡️", "👑", "👽", "👻", "🐯"]

# --- CSS STİLLERİ ---
def load_css():
    st.markdown("""
    <style>
        .stApp { background-color: #0E1117; }
        .header-container {
            padding: 20px; background: linear-gradient(90deg, #1E1E1E 0%, #2D2D2D 100%);
            border-radius: 15px; border-left: 5px solid #FF4B4B; margin-bottom: 20px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .header-title { font-size: 32px; font-weight: bold; color: white; margin: 0; }
        .header-subtitle { font-size: 14px; color: #BBB; margin: 0; }
        .user-badge { background-color: #333; padding: 5px 15px; border-radius: 20px; border: 1px solid #555; font-weight: bold; }
        .member-grid { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 20px; }
        .member-card {
            background-color: #262730; border: 1px solid #444; border-radius: 10px;
            padding: 15px; width: 100px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        .member-card:hover { transform: scale(1.05); border-color: #FF4B4B; }
        .member-avatar { font-size: 40px; margin-bottom: 5px; }
        .member-name { font-size: 12px; color: #EEE; font-weight: bold; overflow: hidden; text-overflow: ellipsis; }
        .stCodeBlock { border: 1px solid #00FF00 !important; }
        .stChatMessage { background-color: #262730; border-radius: 10px; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİTABANI YARDIMCILARI ---
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def load_json(path, default=None):
    """Güvenli JSON yükleme (Hata Düzeltildi)"""
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

# --- KULLANICI İŞLEMLERİ ---
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

def get_user_data(username, type):
    f = os.path.join(DB_FOLDER, f"{username}_{type}.json")
    if type == "sessions":
        return load_json(f, {})
    else:
        return load_json(f, [])

def save_user_data(username, type, data):
    f = os.path.join(DB_FOLDER, f"{username}_{type}.json")
    save_json(f, data)

# --- CANLI TERMİNAL SINIFI ---
class StreamlitOutputStream:
    def __init__(self, c):
        self.c = c
        self.ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    
    def write(self, d): 
        # Session state kontrolü
        if "terminal_logs" not in st.session_state:
            st.session_state.terminal_logs = ""
            
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