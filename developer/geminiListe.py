import os
import google.generativeai as genai

# API Key'i ortam değişkenlerinden al
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("❌ HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı.")
else:
    print("🔍 Google Sunucularına Bağlanılıyor...\n")
    
    try:
        # Kütüphaneyi yapılandır
        genai.configure(api_key=api_key)
        
        print(f"{'MODEL ADI':<40} | {'AÇIKLAMA'}")
        print("-" * 70)
        
        # Modelleri listele
        for m in genai.list_models():
            # Sadece sohbet/metin üretebilen modelleri filtrele
            if 'generateContent' in m.supported_generation_methods:
                # model isminin başındaki 'models/' kısmını temizle
                clean_name = m.name.replace("models/", "")
                print(f"{clean_name:<40} | {m.display_name}")
                
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        print("\nÖNERİ: Eğer 'google.generativeai' modülü bulunamadı derse,")
        print("Terminalden şu komutu çalıştır: pip install google-generativeai")