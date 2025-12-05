import autogen
import os
import sys
import time

# --- 1. API GİRİŞLERİ ---
openai_key = os.environ.get("OPENAI_API_KEY")
google_key = os.environ.get("GOOGLE_API_KEY")

if not openai_key and not google_key:
    print("❌ HATA: API Anahtarları eksik! Lütfen ortam değişkenlerini kontrol edin.")

# --- 2. MODEL LİSTESİ ---
available_models = [
    {"label": "GPT-4.1", "model": "gpt-4.1", "api_key": openai_key, "api_type": "openai"},
    {"label": "GPT-4o", "model": "gpt-4o", "api_key": openai_key, "api_type": "openai"},
    {"label": "Gemini 2.5 Pro", "model": "gemini-2.5-pro", "api_key": google_key, "api_type": "google"},
    {"label": "Gemini 2.5 Flash", "model": "gemini-2.5-flash", "api_key": google_key, "api_type": "google"},
    {"label": "Gemini Pro Latest", "model": "gemini-pro-latest", "api_key": google_key, "api_type": "google"},
]

def print_header():
    """ORCHESTR Logosu ve Açılış Ekranı"""
    print("\n" + "="*50)
    print("          O R C H E S T R   ")
    print("   Yapay Zeka Takım Orkestrasyon Sistemi")
    print("="*50 + "\n")

def save_conversation(groupchat, filename="toplanti_kaydi.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- ORCHESTR LOG: {time.strftime('%Y-%m-%d %H:%M')} ---\n\n")
            for message in groupchat.messages:
                sender = message.get('name', 'Bilinmiyor')
                content = message.get('content', '')
                f.write(f"[{sender}]:\n{content}\n")
                f.write("-" * 50 + "\n")
        print(f"\n✅ Kayıt Başarılı: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"❌ Kayıt hatası: {e}")

def select_model(agent_name):
    print(f"\n🧠 {agent_name} için MODEL seçin:")
    valid_models = [m for m in available_models if m["api_key"]]
    
    if not valid_models:
        print("❌ HİÇBİR MODEL İÇİN API KEY BULUNAMADI!")
        sys.exit()

    for idx, m in enumerate(valid_models):
        print(f"  [{idx + 1}] {m['label']}")
    
    while True:
        try:
            sel_input = input("Model No: ")
            sel = int(sel_input)
            if 1 <= sel <= len(valid_models):
                m = valid_models[sel-1]
                return {
                    "model": m["model"], 
                    "api_key": m["api_key"],
                    "api_type": m["api_type"]
                }
            print("Lütfen listedeki numaralardan birini girin.")
        except ValueError: 
            print("Lütfen sayı girin.")

def create_team(temp):
    agents = []
    print("\n--- EKİBİ OLUŞTURUYORUZ ---")
    while True:
        try:
            num = int(input("Kaç ajan olsun? (Örn: 2): "))
            break
        except: pass

    for i in range(num):
        name = input(f"\n{i+1}. Ajan İsmi: ").replace(" ", "_")
        role = input("Rol Tanımı: ")
        
        system_msg = f"{role}. Diğer uzmanlarla tartış. Hemen kabul etme, en iyiyi bulana kadar sorgula. Sonuç mükemmel olunca 'TERMINATE' de."
        
        cfg = select_model(name)
        
        if "o1-" in cfg["model"]:
            agent_llm_config = {"config_list": [cfg]} 
        else:
            agent_llm_config = {"config_list": [cfg], "temperature": temp}

        agent = autogen.AssistantAgent(
            name=name,
            system_message=system_msg,
            llm_config=agent_llm_config
        )
        agents.append(agent)
    return agents

def start_system():
    print_header() # Logoyu Bas
    
    print("--- PROJE TİPİ ---")
    print("1: Teknik (Düşük Yaratıcılık - 0.2)")
    print("2: Yaratıcı (Yüksek Yaratıcılık - 0.8)")
    temp = 0.2 if input("Seçim: ") == "1" else 0.8
    
    team = create_team(temp)
    
    manager_cfg_list = []
    for m in available_models:
        if m["api_key"]:
            manager_cfg_list.append({
                "model": m["model"],
                "api_key": m["api_key"],
                "api_type": m["api_type"]
            })

    manager_llm_config = {"config_list": manager_cfg_list, "temperature": temp}

    user_proxy = autogen.UserProxyAgent(
        name="Patron",
        human_input_mode="NEVER", 
        code_execution_config={"use_docker": False, "work_dir": "output"},
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
    )
    team.insert(0, user_proxy)

    groupchat = autogen.GroupChat(
        agents=team, messages=[], max_round=15, speaker_selection_method="auto"
    )
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat, 
        llm_config=manager_llm_config
    )

    first_msg = input("\n🚀 İlk Görev Nedir?\n> ")
    user_proxy.initiate_chat(manager, message=first_msg)

    while True:
        print("\n" + "="*40)
        print("⏸️  ORCHESTR BEKLEMEDE - TALİMATINIZ NEDİR?")
        print("="*40)
        print("1. 💬 Feedback Ver / Devam Ettir")
        print("2. 💾 Kaydet (.txt)")
        print("3. 🚪 Çıkış")
        
        choice = input("\nSeçiminiz (1/2/3): ")

        if choice == "1":
            feedback = input("\nFeedback/Yeni Emir: ")
            
            formatted_feedback = f"""
            **************************************************
            ⚠️  DİKKAT: PATRON TALİMATI GÜNCELLENDİ ⚠️
            **************************************************
            GEÇMİŞ KONUŞMALARI HATIRLA AMA ARTIK ŞUNA ODAKLAN:
            {feedback}
            """
            
            print("\n🔄 ORCHESTR Ekibi Çalışıyor...")
            user_proxy.initiate_chat(manager, message=formatted_feedback, clear_history=False)
            
        elif choice == "2":
            fname = input("Dosya adı: ") or "orchestr_log.txt"
            if not fname.endswith(".txt"): fname += ".txt"
            save_conversation(groupchat, fname)
            if input("Çıkış? (e/h): ").lower() == 'e': break
        elif choice == "3":
            print("👋 ORCHESTR Kapatılıyor...")
            break

if __name__ == "__main__":
    start_system()