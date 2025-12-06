import os
import json
import hashlib
import base64
import PyPDF2
from datetime import datetime
import config

# --- ŞİFRELEME ---
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# --- JSON İŞLEMLERİ ---
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

# --- DOSYA OKUMA ---
def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        else:
            return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Error: {e}"

# --- KULLANICI YÖNETİMİ ---
def register_user(u, p, a):
    users = load_json(config.USERS_FILE)
    if u in users: return False, "Username Taken"
    users[u] = {"password": hash_password(p), "avatar": a, "created_at": str(datetime.now())}
    save_json(config.USERS_FILE, users)
    return True, "Kayıt Başarılı"

def login_user(u, p):
    users = load_json(config.USERS_FILE)
    if u not in users: return False, None
    if users[u]["password"] == hash_password(p):
        return True, users[u].get("avatar", "👤")
    return False, None

def get_all_users():
    users = load_json(config.USERS_FILE)
    return [{"name": k, "avatar": v.get("avatar", "👤")} for k, v in users.items()]

# --- VERİ YÖNETİMİ ---
def get_user_files(u):
    return {
        "sessions": os.path.join(config.DB_FOLDER, f"{u}_sessions.json"),
        "team": os.path.join(config.DB_FOLDER, f"{u}_team.json")
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

# --- AJAN TRANSFERİ ---
def get_all_past_agents(u):
    sessions = get_user_data(u, "sessions")
    unique_agents = {}
    for s_id, s_data in sessions.items():
        if "agents" in s_data and s_data["agents"]:
            for ag in s_data["agents"]:
                key = f"{ag['name']} ({ag['role'][:15]}...)"
                ag['source_project'] = s_data.get('title', 'Bilinmeyen')
                unique_agents[key] = ag
    return unique_agents