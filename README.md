# 🇹🇷 ORCHESTR AI

**ORCHESTR AI**, Microsoft AutoGen ve Streamlit kullanılarak geliştirilmiş, **çok kullanıcılı ve kalıcı hafızaya sahip** profesyonel bir Yapay Zeka Takım Yönetim Platformudur.

Kullanıcıların kendi sanal AI çalışanlarını (ajanlarını) oluşturmasına, bu ajanları bir ekip gibi yönetmesine ve karmaşık görevleri otonom olarak çözdürmesine olanak tanır.

## 🌟 Temel Özellikler

  * **🔐 Çoklu Kullanıcı Sistemi:** Güvenli giriş ve kayıt sistemi (SHA-256 şifreleme). Her kullanıcının verisi izoledir.
  * **👥 Dinamik Takım Kurulumu:** İstediğiniz rol ve yetenekte (Yazılımcı, Analist, Tasarımcı vb.) sınırsız ajan oluşturun.
  * **🧠 Çoklu Model Desteği:** GPT-4o, GPT-4.1, Gemini 1.5 Pro ve Flash modellerini aynı ekip içinde hibrit olarak kullanın.
  * **📺 Canlı Terminal İzleme:** Ajanların arka planda birbirleriyle nasıl konuştuğunu, yazdıkları kodları ve hata düzeltmelerini Matrix tarzı terminalden canlı izleyin.
  * **💾 Kalıcı Hafıza (JSON DB):** Sohbetleriniz, kurduğunuz ekipler ve ayarlarınız JSON tabanlı veritabanında saklanır. Tarayıcıyı kapatsanız bile verileriniz kaybolmaz.
  * **🔄 Dinamik Akış Kontrolü:** Sohbet sırasında "Yaratıcılık" (Temperature) ayarını değiştirin veya konuşma sırasına (Otomatik/Sıralı) müdahale edin.
  * **📁 Sohbet Arşivi:** Geçmiş projelerinize tek tıkla geri dönün, kaldığınız yerden devam edin.

## 🛠️ Kurulum

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1\. Repoyu Klonlayın

```bash
git clone https://github.com/KULLANICI_ADIN/orchestr-ai.git
cd orchestr-ai
```

### 2\. Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# Mac/Linux için:
source venv/bin/activate
```

### 3\. Gereksinimleri Yükleyin

```bash
pip install -r requirements.txt
```

*(Eğer requirements.txt dosyan yoksa şu komutu çalıştır: `pip install streamlit autogen pyautogen`)*

### 4\. Uygulamayı Başlatın

```bash
streamlit run main.py
```

## 🔑 API Anahtarları

Sistemi kullanmak için OpenAI veya Google Gemini API anahtarlarına ihtiyacınız vardır.

  * Uygulama arayüzündeki **Sol Menü (Sidebar) -\> API Anahtarları** bölümünden anahtarlarınızı girebilirsiniz.
  * Anahtarlarınız sadece yerel oturumunuzda kullanılır.

## 📂 Proje Yapısı

```
orchestr-ai/
├── main.py              # Uygulamanın ana giriş noktası (Arayüz)
├── utils.py             # Veritabanı, Güvenlik ve Yardımcı Fonksiyonlar
├── orchestr_db/         # Kullanıcı verilerinin tutulduğu JSON klasörü
│   ├── users.json       # Kullanıcı hesapları
│   └── ...              # Kullanıcıya özel sohbet ve takım dosyaları
├── requirements.txt     # Gerekli kütüphaneler
└── README.md            # Dokümantasyon
```

## 🚀 Kullanım Senaryoları

1.  **Yazılım Geliştirme:** Bir "Senior Developer", bir "Code Reviewer" ve bir "Tester" ajanı oluşturup onlara bir Python scripti yazdırın.
2.  **İçerik Üretimi:** Bir "SEO Uzmanı", bir "Metin Yazarı" ve bir "Editör" oluşturup blog yazısı hazırlatın.
3.  **Veri Analizi:** Bir "Veri Bilimci" ve bir "İş Analisti" oluşturup elinizdeki verileri yorumlatın.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz\! Lütfen önce bir "Issue" açarak tartışın, ardından "Pull Request" gönderin.

1.  Fork'layın.
2.  Yeni bir branch oluşturun (`git checkout -b ozellik/YeniOzellik`).
3.  Commit yapın (`git commit -m 'Yeni özellik eklendi'`).
4.  Push yapın (`git push origin ozellik/YeniOzellik`).
5.  Pull Request açın.

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

-----

**⚡ Made by Mugendai(aka Yerlifan)**
