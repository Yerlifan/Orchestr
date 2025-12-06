# 🇹🇷 ORCHESTR AI

**ORCHESTR AI**, Microsoft AutoGen ve Streamlit kullanılarak geliştirilmiş, **çok kullanıcılı ve kalıcı hafızaya sahip** profesyonel bir Yapay Zeka Takım Yönetim Platformudur.

Kullanıcıların kendi sanal AI çalışanlarını (ajanlarını) oluşturmasına, bu ajanları bir ekip gibi yönetmesine ve karmaşık görevleri otonom olarak çözdürmesine olanak tanır.

## 🌟 Temel Özellikler

  * **🔐 Çoklu Kullanıcı Sistemi:** Güvenli giriş ve kayıt sistemi (SHA-256 şifreleme). Her kullanıcının verisi izoledir.
  * **👥 Dinamik Takım Kurulumu:** İstediğiniz rol ve yetenekte (Yazılımcı, Analist, Tasarımcı vb.) sınırsız ajan oluşturun.
  * **🧠 Çoklu Model Desteği:** GPT-4o, GPT-4.1, Gemini 2.5 Pro ve Flash modellerini aynı ekip içinde hibrit olarak kullanın.
  * **📺 Canlı Terminal İzleme:** Ajanların arka planda birbirleriyle nasıl konuştuğunu, yazdıkları kodları ve hata düzeltmelerini Matrix tarzı terminalden canlı izleyin.
  * **💾 Kalıcı Hafıza (JSON DB):** Sohbetleriniz, kurduğunuz ekipler ve ayarlarınız JSON tabanlı veritabanında saklanır. Tarayıcıyı kapatsanız bile verileriniz kaybolmaz.
  * **🔄 Dinamik Akış Kontrolü:** Sohbet sırasında "Yaratıcılık" (Temperature) ayarını değiştirin veya konuşma sırasına (Otomatik/Sıralı) müdahale edin.
  * **📁 Sohbet Arşivi:** Geçmiş projelerinize tek tıkla geri dönün, kaldığınız yerden devam edin.

-----

# 📘 ORCHESTR AI - Kullanım ve Kurulum Rehberi

**ORCHESTR AI**, birden fazla Yapay Zeka ajanını (Agent) bir araya getirerek sanal bir çalışma ekibi kurmanızı, onları yönetmenizi ve karmaşık görevleri otonom olarak çözdürmenizi sağlayan profesyonel bir platformdur.

-----

## 🛠️ Bölüm 1: Kurulum (Yönetici İçin)

Bu sistemi kendi bilgisayarınızda veya sunucunuzda çalıştırmak için aşağıdaki adımları izleyin.

### 1\. Gereksinimler

  * Python 3.10 veya üzeri
  * OpenAI veya Google Gemini API Anahtarı

### 2\. Dosya Yapısı

Proje klasörünüzde şu iki dosyanın olduğundan emin olun:

  * `orchestr_streamlit.py` (Ana uygulama)
  * `utils.py` (Yardımcı fonksiyonlar ve veritabanı)

### 3\. Kütüphanelerin Yüklenmesi

Terminali açın ve gerekli paketleri yükleyin:

```bash
pip install streamlit ag2 pyautogen
```

### 4\. Uygulamayı Başlatma

Terminalden şu komutu girin:

```bash
streamlit run orchestr_streamlit.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

-----

## 🚀 Bölüm 2: Kullanıcı Rehberi

### 1\. Giriş ve Kayıt

Sistem çok kullanıcılıdır. Her kullanıcının verisi (sohbetleri, takımları) tamamen izoledir.

  * **Kayıt Ol:** "Kayıt Ol" sekmesine gelin. Kullanıcı adı, şifre belirleyin ve sizi temsil edecek bir **Avatar** (🦁, 🚀 vb.) seçin.
  * **Giriş Yap:** Bilgilerinizle sisteme giriş yapın.

### 2\. API Anahtarlarını Tanımlama (Admin Yetkisi)

Sistemin çalışması için beyin gücüne (LLM) ihtiyacı vardır.

1.  Sol menüde (Sidebar) en altta **"🔑 API Erişimi"** kutusunu açın.
2.  **Admin Şifresini** girin. (Varsayılan: `yerlifan123`)
3.  Açılan kutulara **OpenAI API Key** veya **Google Gemini API Key** yapıştırın.
4.  Bu işlem bir kez yapılır, sistem anahtarları hatırlar.

### 3\. Ekip Kurulumu (Install Phase)

Giriş yaptıktan sonra sizi boş bir ekran karşılar. Sol menüdeki **"➕ Üye Ekle"** panelini kullanın:

  * **İsim:** Sanal çalışana bir isim verin (Örn: *Yazılımcı, Editör, Hukukçu*).
  * **Rol:** Ona ne yapması gerektiğini söyleyin (Örn: *"Sen kıdemli bir Python uzmanısın. Hatalı kodları affetmezsin."*).
  * **Model:** Bu ajanın hangi zekayı kullanacağını seçin (GPT-4o, Gemini 2.5 Pro vb.).
  * **Ekle:** Butona basın.

> **İpucu:** Eklediğiniz ajanları "Yukarı/Aşağı" oklarıyla sıralayabilir veya kalem ikonuna basarak özelliklerini değiştirebilirsiniz.

### 4\. Sistemi Başlatma ve Sohbet

Ekibiniz hazırsa sol alttaki **"🚀 BAŞLAT"** butonuna basın.

  * Ajanlar kilitlenir ve "Çalışma Modu"na geçilir.
  * Alttaki sohbet kutusuna görevinizi yazın (Örn: *"Bana Snake oyunu yapan bir Python kodu yazın."*).

### 5\. 📺 Canlı Terminal (The Matrix)

Siz görevi verdiğinizde, sohbet kutusunun üzerinde siyah bir **Terminal Ekranı** açılır.

  * Burada ajanların arka planda birbirleriyle nasıl konuştuğunu, denedikleri kodları ve aldıkları hataları **anlık olarak** izleyebilirsiniz.
  * İşlem bittiğinde bu ekran kapanır ve temiz sonuç sohbet balonları olarak aşağıya düşer.

### 6\. Feedback (Yönlendirme)

Ajanlar çalışırken veya durduklarında müdahale edebilirsiniz.

  * Sohbet kutusuna yazdığınız her yeni mesaj, sisteme bir **"Feedback" (Geri Bildirim)** olarak gider.
  * Örn: *"Renkler çok koyu olmuş, daha açık tonlar kullanın"* derseniz, ekip kaldığı yerden devam ederek kodu düzeltir.

### 7\. Çoklu Proje Yönetimi

Sol menüdeki **"🗂️ AI Ekiplerim"** başlığı altından:

  * **➕ Yeni Ekip:** Sıfırdan temiz bir sayfa açar.
  * **Geçmiş Listesi:** Eski projelerinize tıklayarak o anki ekibi ve konuşma geçmişini geri yüklersiniz.
  * **Kalem İkonu:** Projenizin ismini (Örn: "Yeni Sohbet" yerine "Web Sitesi Projesi") değiştirebilirsiniz.

### 8\. Canlı Ayarlar (Hot-Swap)

Sistem çalışırken bile **"🎛️ Canlı Ayarlar"** panelinden:

  * **Yaratıcılık (Temperature):** Ajanların ne kadar yaratıcı veya tutarlı olacağını ayarlayın.
  * **Tur Sayısı:** Tartışmanın ne kadar süreceğini belirleyin.
  * **Sıralama:** "Otomatik" (Yapay zeka kimin konuşacağına karar verir) veya "Sıralı" (Listeye göre sırayla konuşurlar) modunu seçin.

-----

## ❓ Sıkça Sorulan Sorular

**S: Bilgisayarımı kapatırsam ne olur?**
C: Sistem yerel bilgisayarınızda çalışıyorsa işlem durur. Eğer bir sunucuya (Streamlit Cloud vb.) kurduysanız arka planda çalışmaya devam eder.

**S: Ajanlar yazdıkları kodu çalıştırabilir mi?**
C: Güvenlik nedeniyle ajanların yazdığı kodlar sadece ekranda gösterilir, otomatik çalıştırılmaz (Execution: False). Kodu kopyalayıp kendi ortamınızda çalıştırmalısınız.

**S: Sohbet geçmişim kaybolur mu?**
C: Hayır. Tüm veriler `orchestr_db` klasöründe JSON formatında güvenle saklanır.

-----

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz\! Lütfen önce bir "Issue" açarak tartışın, ardından "Pull Request" gönderin.

1.  Fork'layın.
2.  Yeni bir branch oluşturun (`git checkout -b ozellik/YeniOzellik`).
3.  Commit yapın (`git commit -m 'Yeni özellik eklendi'`).
4.  Push yapın (`git push origin ozellik/YeniOzellik`).
5.  Pull Request açın.

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

**⚡ Made by Mugendai (aka Yerlifan)**

