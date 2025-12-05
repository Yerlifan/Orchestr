import os
from openai import OpenAI

# 1. API Anahtarını Kontrol Et
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ HATA: OPENAI_API_KEY ortam değişkeni bulunamadı.")
else:
    print("🔍 OpenAI Sunucularına Bağlanılıyor...\n")
    
    try:
        # 2. İstemciyi (Client) Başlat
        client = OpenAI()
        
        # 3. Modelleri Listele
        response = client.models.list()
        
        # Modelleri isme göre sıralayalım ki okuması kolay olsun
        sorted_models = sorted(response.data, key=lambda x: x.id)

        print(f"{'MODEL ID (KODDA KULLANILACAK)':<40} | {'OLUŞTURULMA TARİHİ'}")
        print("-" * 70)
        
        # 4. Listeyi Ekrana Bas
        for model in sorted_models:
            # Sadece bizim işimize yarayacak 'gpt' modellerini öne çıkaralım
            # (Dall-e, tts, whisper gibi modelleri filtreleyebilirsin)
            if "gpt" in model.id:
                # Unix zaman damgasını basitçe göstermek yerine olduğu gibi bırakıyoruz veya
                # datetime ile çevirebiliriz ama ID'yi görmek yeterli.
                print(f"{model.id:<40} | {model.created}")

        print("\n--- Diğer Modeller (Embeddings, TTS, vs.) ---")
        # İstersen diğerlerini de görebilirsin
        count = 0
        for model in sorted_models:
            if "gpt" not in model.id and count < 5: # Örnek olarak ilk 5 tanesini göster
                print(f"{model.id:<40}")
                count += 1
        if count >= 5: print("... ve daha fazlası.")

    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")