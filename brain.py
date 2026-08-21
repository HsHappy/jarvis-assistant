from openai import OpenAI
import memory

# OpenRouter API yapılandırması
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="BURAYA_API_ANAHTARI_GELECEK" 
)

def jarvis_ile_konus(kullanici_mesaji):
    print("Jarvis buluttaki nöral ağlara bağlanıyor...")
    
    # 1. Mesajı hafızaya kaydet ve geçmişi çek
    memory.mesaj_kaydet('user', kullanici_mesaji)
    eski_mesajlar = memory.gecmisi_getir(limit=10)
    
    # 2. Jarvis'in sistem karakteri
    sistem_mesaji = {
        'role': 'system', 
        'content': '''Senin adın Jarvis. Sadece düzgün, gramer kurallarına uygun, doğal bir Türkçe kullan. 
        Asla uydurma kelimeler üretme. Yanıtların kısa, öz ve profesyonel olsun. 
        Sen kıdemli bir yazılım mimarı ve mühendislik mentorusun. 
        Bana sadece çalışan kodu verme; kodun arkasındaki mühendislik kararlarını, kurumsal güvenlik standartlarını 
        ve performans optimizasyonlarını da kısaca açıkla. 
        Kodlarımın modüler, bakımı kolay ve profesyonel standartlarda olmasını sağla.'''
    }
    
    gonderilecek_mesajlar = [sistem_mesaji] + eski_mesajlar
    
    try:
        # 3. OpenRouter üzerinden devasa bir model çağırıyoruz
        # Not: 'meta-llama/llama-3.1-8b-instruct:free' modeli test için tamamen ücretsizdir. 
        # İstersen burayı 'meta-llama/llama-3.1-70b-instruct' ile değiştirebilirsin.
        response = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=gonderilecek_mesajlar,
            temperature=0.3
        )
        
        asistanin_cevabi = response.choices[0].message.content
        
        # 4. Gelen zekice cevabı hafızaya yaz ve döndür
        memory.mesaj_kaydet('assistant', asistanin_cevabi)
        return asistanin_cevabi
        
    except Exception as e:
        print(f"[API HATASI]: {e}")
        return "Beyin sunucularına bağlanırken bir ağ hatası oluştu."