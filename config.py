import os

# --- KLASÖR VE DOSYA YOLLARI ---
DB_FOLDER = "orchestr_db"
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

USERS_FILE = os.path.join(DB_FOLDER, "users.json")

# --- GÜVENLİK ---
ADMIN_PASSWORD = "yerlifan123"

# --- AVATARLAR ---
AVATARS = ["👨‍💻", "👩‍💻", "🚀", "🧠", "🦁", "🦉", "🦄", "🎨", "⚡", "🤖", "🔥", "💎", "🛡️", "👑", "👽", "👻", "🐯"]

# --- TEMA RENKLERİ ---
THEMES = {
    "Kızıl": "#FF4B4B", 
    "Mavi": "#2196F3", 
    "Yesil": "#4CAF50", 
    "Mor": "#9C27B0", 
    "Turuncu": "#FF9800", 
    "Turkuaz": "#00BCD4"
}

# --- AI MODELLERİ (EKSİK OLAN KISIM EKLENDİ) ---
MODELS = [
    {"label": "GPT-4.1", "model": "gpt-4.1", "api_type": "openai"},
    {"label": "GPT-4o", "model": "gpt-4o", "api_type": "openai"},
    {"label": "Gemini 2.5 Pro", "model": "gemini-2.5-pro", "api_type": "google"},
    {"label": "Gemini 2.5 Flash", "model": "gemini-2.5-flash", "api_type": "google"},
    {"label": "Gemini Pro Latest", "model": "gemini-pro-latest", "api_type": "google"}
]
# Hata veren MLABS buraya tanımlandı:
MLABS = [m["label"] for m in MODELS]

# --- DİL PAKETİ ---
LANG = {
    "TR": {
        "login_header": "GİRİŞ", 
        "login_sub": "Yapay Zeka Takım Orkestrasyonu",
        "login_title": "Giriş Yap", 
        "reg_title": "Kayıt Ol",
        "username": "Kullanıcı Adı", 
        "pass": "Şifre", 
        "login_btn": "Giriş Yap", 
        "reg_btn": "Kayıt Ol",
        "welcome": "Hoşgeldin", 
        "remember": "Beni Hatırla",
        "new_chat": "Yeni Ekip", 
        "my_chats": "Projelerim", 
        "settings": "Sistem Ayarları",
        "api_access": "API Erişimi", 
        "start_btn": "Ekibi Kur ve Başlat ", 
        "stop_task": "Görevi Durdur", 
        "stop_icon": "🛑",
        "logout": "Çıkış", 
        "chat_input": "Görev ver veya feedback yaz...", 
        "feedback_label": "Yönlendirme:",
        "team_setup": "Ekip Kurulumu", 
        "add_agent": "Üye Ekle", 
        "name": "İsim", 
        "role": "Rol", 
        "model": "Model",
        "save": "Kaydet", 
        "delete": "Sil", 
        "active_team": "Çalışan Ekip",
        "attach": "Dosya Ekle", 
        "file_help": "Analiz için PDF/TXT yükle.",
        "upload_doc": "Döküman Yükle", 
        "upload_img": "Resim Yükle",
        "theme_sel": "Tema Rengi", 
        "bg_sel": "Arka Plan", 
        "lang_sel": "Dil",
        "creativity": "Yaratıcılık", 
        "first_turn": "İlk Tur Limiti", 
        "fb_turn": "Feedback Turu Limiti", 
        "order": "Sıra",
        "auto": "Otomatik", 
        "seq": "Sıralı", 
        "active_project": "Proje", 
        "edit_title": "Başlığı Düzenle",
        "admin_pass": "Admin Şifresi", 
        "lock": "Kilitle", 
        "unlock": "Kilit Açıldı",
        "wrong_pass": "Hatalı Şifre", 
        "no_api": "API Anahtarı Yok", 
        "terminal": "Canlı Terminal", 
        "working": "Çalışıyor...",
        "our_team": "TAKIM ARKADAŞLARIMIZ", 
        "import_title": "♻️ Geçmişten Ajan Transfer Et", 
        "import_btn": "Transfer Et", 
        "no_past_agent": "Geçmiş kayıt bulunamadı."
    },
    "EN": {
        "login_header": "LOGIN", 
        "login_sub": "AI Team Orchestration",
        "login_title": "Login", 
        "reg_title": "Register",
        "username": "Username", 
        "pass": "Password", 
        "login_btn": "Login", 
        "reg_btn": "Register", 
        "welcome": "Welcome", 
        "remember": "Remember Me",
        "new_chat": "New Team", 
        "my_chats": "Projects", 
        "settings": "System Settings",
        "api_access": "API Access", 
        "start_btn": "Setup & Start", 
        "stop_task": "Stop Task", 
        "stop_icon": "🛑",
        "logout": "Logout", 
        "chat_input": "Enter task...", 
        "feedback_label": "Feedback:",
        "team_setup": "Team Setup", 
        "add_agent": "Add Member", 
        "name": "Name", 
        "role": "Role", 
        "model": "Model",
        "save": "Save", 
        "delete": "Delete", 
        "active_team": "Active Team",
        "attach": "Attach File", 
        "file_help": "Upload PDF/TXT Analysis",
        "upload_doc": "Upload Doc", 
        "upload_img": "Upload Image",
        "theme_sel": "Accent Color", 
        "bg_sel": "Background", 
        "lang_sel": "Language",
        "creativity": "Creativity", 
        "first_turn": "First Round Limit", 
        "fb_turn": "Feedback Round", 
        "order": "Order", 
        "auto": "Auto", 
        "seq": "Sequential", 
        "active_project": "Active Project", 
        "edit_title": "Edit Title", 
        "admin_pass": "Admin Password", 
        "lock": "Lock", 
        "unlock": "Unlocked", 
        "wrong_pass": "Wrong Password", 
        "no_api": "No API Keys", 
        "terminal": "Live Terminal", 
        "working": "Working...", 
        "our_team": "OUR TEAM", 
        "import_title": "♻️ Import Agent", 
        "import_btn": "Import", 
        "no_past_agent": "No history found."
    }
}