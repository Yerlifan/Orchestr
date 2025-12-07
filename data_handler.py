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
    if default is None: default = {}
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

# --- MODEL YÖNETİMİ ---
def get_models():
    if not os.path.exists(config.MODELS_FILE):
        save_json(config.MODELS_FILE, config.DEFAULT_MODELS)
        return config.DEFAULT_MODELS
    models = load_json(config.MODELS_FILE)
    if not models: return config.DEFAULT_MODELS
    return models

def add_new_model(label, model_id, api_type, base_url=None):
    models = get_models()
    for m in models:
        if m["label"] == label or m["model"] == model_id:
            return False, "Model already exists"
    new_model = {"label": label, "model": model_id, "api_type": api_type}
    if base_url: new_model["base_url"] = base_url
    models.append(new_model)
    save_json(config.MODELS_FILE, models)
    return True, "Model added"

def delete_model(index):
    models = get_models()
    if 0 <= index < len(models):
        models.pop(index)
        save_json(config.MODELS_FILE, models)
        return True
    return False

def reset_models_to_default():
    save_json(config.MODELS_FILE, config.DEFAULT_MODELS)

# --- DOSYA OKUMA ---
def read_uploaded_file(uploaded_file):
    if uploaded_file is None: return ""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages: text += page.extract_text() + "\n"
            return text
        else: return uploaded_file.getvalue().decode("utf-8")
    except Exception as e: return f"Error: {e}"

# --- KULLANICI ---
def register_user(u, p, a):
    users = load_json(config.USERS_FILE)
    if u in users: return False, "Username Taken"
    users[u] = {"password": hash_password(p), "avatar": a, "created_at": str(datetime.now())}
    save_json(config.USERS_FILE, users)
    return True, "OK"

def login_user(u, p):
    users = load_json(config.USERS_FILE)
    if u not in users: return False, None
    if users[u]["password"] == hash_password(p): return True, users[u].get("avatar", "👤")
    return False, None

def get_all_users():
    users = load_json(config.USERS_FILE)
    return [{"name": k, "avatar": v.get("avatar", "👤")} for k, v in users.items()]

def get_user_files(u): return {"sessions": os.path.join(config.DB_FOLDER, f"{u}_sessions.json"), "team": os.path.join(config.DB_FOLDER, f"{u}_team.json")}
def get_user_data(u, t): p = get_user_files(u); return load_json(p["sessions"], {}) if t=="sessions" else load_json(p["team"], [])
def save_user_data(u, t, d): p = get_user_files(u); save_json(p["sessions"] if t=="sessions" else p["team"], d)

def get_all_past_agents(u):
    sessions = get_user_data(u, "sessions")
    unique_agents = {}
    for s_id, s_data in sessions.items():
        if "agents" in s_data and s_data["agents"]:
            for ag in s_data["agents"]:
                key = f"{ag['name']} ({ag['role'][:15]}..)"
                ag['source_project'] = s_data.get('title', '?')
                unique_agents[key] = ag
    return unique_agents