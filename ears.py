import sounddevice as sd
import speech_recognition as sr
import numpy as np
import wave
import os
import winsound

def beni_dinle(saniye=5):
    r = sr.Recognizer()
    ornekleme_hizi = 44100
    dosya_adi = "test_sesi.wav"
    
    print(f"\n{saniye} saniye boyunca sizi dinliyorum (Lütfen yüksek sesle konuşun)...")
    
    # Mikrofondan kayıt alıyoruz
    ses_verisi = sd.rec(int(saniye * ornekleme_hizi), samplerate=ornekleme_hizi, channels=1, dtype='int16')
    sd.wait()
    
    print("Kayıt bitti, ses dosyaya kaydediliyor...")
    
    # Sesi klasöre kaydediyoruz ki ne duyduğunu kontrol edebilelim
    with wave.open(dosya_adi, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2) # 16-bit
        f.setframerate(ornekleme_hizi)
        f.writeframes(ses_verisi.tobytes())
        
    print("Ses işleniyor...")
    
    # Kaydettiğimiz bu dosyayı okutup Google'a gönderiyoruz
    with sr.AudioFile(dosya_adi) as kaynak:
        audio_data = r.record(kaynak)
        
    try:
        metin = r.recognize_google(audio_data, language="tr-TR")
        return metin
    except sr.UnknownValueError:
        print("Ne dediğinizi anlayamadım.")
        return ""
    except sr.RequestError:
        print("Ses servisine ulaşılamadı.")
        return ""

if __name__ == "__main__":
    soylenen = beni_dinle()
    if soylenen:
        print(f"\nJarvis duydu: {soylenen}")
    else:
        print("\n!!! LÜTFEN KONTROL EDİN !!!")
        print(f"Proje klasörünüzde 'test_sesi.wav' adında bir dosya oluştu.")
        print("Lütfen o dosyayı açıp dinleyin. Kendi sesinizi duyabiliyor musunuz?")

def uyandirma_bekle():
    r = sr.Recognizer()
    ornekleme_hizi = 44100
    dosya_adi = "wake_word.wav"
    
    print("\n[Uyku Modu] Jarvis dinliyor... (Uyandırmak için 'Jarvis' deyin)")
    
    while True:
        # Sadece 2.5 saniyelik kısa bir ortam dinlemesi yapıyoruz
        ses_verisi = sd.rec(int(2.5 * ornekleme_hizi), samplerate=ornekleme_hizi, channels=1, dtype='int16')
        sd.wait()
        
        with wave.open(dosya_adi, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(ornekleme_hizi)
            f.writeframes(ses_verisi.tobytes())
            
        with sr.AudioFile(dosya_adi) as kaynak:
            audio_data = r.record(kaynak)
            
        try:
            # Sesi hızlıca Google'a sor
            metin = r.recognize_google(audio_data, language="tr-TR").lower()
            
            # Eğer duyduğu 2.5 saniyelik sesin içinde 'jarvis' kelimesi geçiyorsa uyandır!
            if "jarvis" in metin or "carvis" in metin:  # Türkçe okunuş ihtimalini de ekledik
                print("\nJarvis uyandı!")
                # Siri gibi uyandığını belli etmek için kısa bir BİP sesi çıkar
                winsound.Beep(1000, 300) 
                return True
        except:
            # Sessizlik veya anlamsız gürültü varsa hiçbir şey yapma, uyumaya devam et
            pass