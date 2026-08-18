import ollama
import memory

def jarvis_ile_konus(kullanici_mesaji):
    print("Jarvis geçmişi tarıyor ve düşünüyor...")

    # 1. Senin yazdığın yeni mesajı veritabanına kaydet (rol: user)
    memory.mesaj_kaydet('user', kullanici_mesaji)

    # 2. Veritabanından eski konuşmaları çek (Token sınırını aşmamak için son 10 mesajı alıyoruz)
    eski_mesajlar = memory.gecmisi_getir(limit=10)
    
    # Modele önce kim olduğunu ve nasıl davranması gerektiğini söylüyoruz
    sistem_mesaji = {
        'role': 'system', 
        'content': 'Senin adın Jarvis. Sen son derece zeki, saygılı ve yardımsever bir yapay zeka asistanısın. Kullanıcıya her zaman, istisnasız olarak sadece düzgün, gramer kurallarına uygun, doğal bir Türkçe ile yanıt vermelisin. İngilizce kelimeler kullanmaktan kaçın ve yanıtlarını kısa, öz ve anlaşılır tut.'
    }
    
    # 4. Sistemin kafasındaki asıl mesaj paketi (Sistem Komutu + Eski Konuşmalar)
    # Eski konuşmaların en sonunda zaten senin az önce SQL'e kaydettiğimiz yeni mesajın da var.
    gonderilecek_mesajlar = [sistem_mesaji] + eski_mesajlar
    
    # 5. Tüm bu paketi Ollama'ya gönder
    cevap = ollama.chat(
        model='llama3', 
        messages=gonderilecek_mesajlar,
        options={'temperature': 0.2}
    )
    
    asistanin_cevabi = cevap['message']['content']
    
    # 6. Jarvis'in ürettiği cevabı da SQL'e kaydet (rol: assistant) ki bir sonraki sefer onu da hatırlasın
    memory.mesaj_kaydet('assistant', asistanin_cevabi)
    
    return asistanin_cevabi