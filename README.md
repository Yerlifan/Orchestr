# 🛡️ ORCHESTR AI

**ORCHESTR AI**, Microsoft AutoGen ve Streamlit tabanlı, gelişmiş bir **Çoklu Ajan (Multi-Agent) Orkestrasyon Platformudur**. 

Bu araç, kullanıcıların karmaşık görevleri çözmek için özelleştirilmiş yapay zeka ekipleri kurmasına, yönetmesine ve bu ekiplerin birbiriyle işbirliği yapmasını izlemesine olanak tanır. OpenAI (GPT-4), Google (Gemini) ve Yerel LLM'leri (Ollama, Deepseek) destekler.

---

### 🧠 Akıllı Ajan Yönetimi
* **Ajan Kütüphanesi (Public):** Sık kullandığınız ajan şablonlarını (Örn: "Kıdemli Yazılımcı") kütüphaneye kaydedin ve dilediğiniz projeye tek tıkla dahil edin.
* **Proje Ekibi (Private):** Her sohbet oturumu için özelleştirilmiş, izole edilmiş ajan ekipleri kurun.
* **Karma Model Desteği:** Aynı ekipte GPT-4, Gemini Pro ve Local Llama modellerini aynı anda çalıştırın.

### 🛡️ Güvenlik ve Kontrol
* **API Kilidi:** Sunumlar veya ekran paylaşımları sırasında API anahtarlarınızı gizlemek için paneli kilitleyin.
* **Sınırlandırmalar:** Kaynak tüketimini kontrol altında tutmak için Maksimum Ajan Sınırı (10) ve Karakter Limiti (25.000).
* **Anti-Echo Döngüsü:** Ajanların birbirini sürekli tekrar etmesini engelleyen özel sistem mesajları (Prompt Engineering).

### 💾 Veri ve Süreklilik
* **Sistemi Dışa Aktar (Export):** Tüm ajan kütüphanenizi, ayarlarınızı ve aktif sohbet geçmişinizi tek bir `.json` dosyası olarak yedekleyin.
* **Kalıcı Hafıza:** Sohbet geçmişi ve ajan yapılandırmaları yerel veritabanında saklanır.
* **Akıllı Tur Hesaplama:** Kullanıcı müdahalesine gerek kalmadan ajanlar arası konuşma turlarını otomatik yönetir.

### 🎨 Gelişmiş UI/UX
* **Dinamik Sidebar:** Proje, Ajan Yönetimi ve Sistem Ayarları olarak gruplandırılmış profesyonel menü.
* **Tema:** Görünümü kullanıcıya özel ayarlanabilen keyifli bir deneyim.
* **Çoklu Dil Desteği:** Tamamen özelleştirilebilir TR/EN dil seçenekleri.

---

## 🛠️ Kurulum

Proje Python 3.8+ gerektirir.

1.  **Repoyu Klonlayın:**
    ```bash
    git clone https://github.com/Yerlifan/orchestr-ai.git
    cd orchestr-ai
    ```

2.  **Sanal Ortam Oluşturun (Önerilen):**
    ```bash
    python -m venv venv
    # Windows için:
    venv\Scripts\activate
    # Mac/Linux için:
    source venv/bin/activate
    ```

3.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı Başlatın:**
    ```bash
    streamlit run main.py
    ```

---

## ⚙️ Yapılandırma

`config.py` dosyası üzerinden sistemin temel davranışlarını değiştirebilirsiniz:

* **MAX_AGENT_LIMIT:** Bir projeye eklenebilecek maksimum ajan sayısı.
* **MAX_CHAR_LIMIT:** Kullanıcı giriş kutusunun karakter sınırı.
* **THEMES:** Arayüz renk temaları.
* **DEFAULT_MODELS:** Sistem sıfırlandığında geri yüklenecek varsayılan modeller.

---

## 🤝 Katkıda Bulunma

1.  Bu repoyu Forklayın.
2.  Yeni bir Branch oluşturun (`git checkout -b feature/YeniOzellik`).
3.  Değişikliklerinizi Commit edin (`git commit -m 'Yeni özellik eklendi'`).
4.  Branch'i Pushlayın (`git push origin feature/YeniOzellik`).
5.  Bir Pull Request açın.

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.

---
