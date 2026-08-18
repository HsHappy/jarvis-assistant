import sounddevice as sd
import speech_recognition as sr
import numpy as np
import wave
import os

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