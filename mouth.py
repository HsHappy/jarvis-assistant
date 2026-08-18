import pyttsx3

def konus(metin):
    print("Seslendiriliyor...")
    
    try:
        motor = pyttsx3.init()
        motor.setProperty('rate', 160) # Konuşma hızı
        
        # Sistemdeki tüm sesleri çekiyoruz
        sesler = motor.getProperty('voices')
        
        # Türkçe sesi (Tolga) bul ve ayarla
        for ses in sesler:
            if "Turkish" in ses.name or "Tolga" in ses.name:
                motor.setProperty('voice', ses.id)
                break # Sesi bulunca aramayı bırak
                
        motor.say(metin)
        motor.runAndWait()
        
    except Exception as e:
        print(f"Seslendirme hatası: {e}")

if __name__ == "__main__":
    konus("Merhaba efendim. Ses sistemlerim güncellendi. Artık düzgün bir Türkçe ile konuşabiliyorum.")