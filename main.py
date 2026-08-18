import ears
import brain
import mouth
import hands

def asistan_dongusu():
    print("="*50)
    print("Jarvis Sistemi Başlatılıyor...")
    print("="*50)
    
    # Kullanıcıdan mod seçimi alıyoruz
    print("Hangi modda kullanmak istersiniz?")
    print("1 - Yazılı Sohbet (Chat)")
    print("2 - Sesli Sohbet (Mikrofon)")
    mod = input("Seçiminiz (1 veya 2): ")
    
    print("\nAsistanı kapatmak için 'kapat' veya 'çıkış' komutunu kullanabilirsiniz.")
    print("-" * 50)
    
    while True:
        kullanici_mesaji = ""
        
        # Seçilen moda göre girdiyi al
        if mod == '1':
            kullanici_mesaji = input("\nSen: ")
        else:
            kullanici_mesaji = ears.beni_dinle(saniye=5)
            # Mikrofon boş ses duyduysa döngüyü başa sar
            if not kullanici_mesaji:
                continue
            print(f"\nSen: {kullanici_mesaji}")
        
        # Boş mesaj (sadece Enter'a basılmışsa) gönderilmesini engelle
        if not kullanici_mesaji.strip():
            continue
            
        # Çıkış kontrolü
        if "kapat" in kullanici_mesaji.lower() or "çıkış" in kullanici_mesaji.lower():
            print("Jarvis: Sistem kapatılıyor. Görüşmek üzere, efendim!")
            break
            
        # --- YENİ EKLENEN KISIM ---
        # 1. Önce 'Eller' modülüne sor: Bu bir bilgisayar komutu mu?
        aksiyon_cevabi = hands.komut_islet(kullanici_mesaji)
        
        if aksiyon_cevabi:
            # Eğer bir aksiyon alındıysa, beyni yormaya gerek yok. Doğrudan aksiyon cevabını ver.
            cevap = aksiyon_cevabi
            
            # İsteğe bağlı: Asistanın yaptığı bu işlemi de hafızaya ekleyebiliriz 
            # ki sonradan ne yaptığını hatırlasın (Bunun için import memory ekli olmalıdır)
            import memory
            memory.mesaj_kaydet('user', kullanici_mesaji)
            memory.mesaj_kaydet('assistant', aksiyon_cevabi)
        else:
            # 2. Eğer bir komut yoksa (False döndüyse), normal sohbet için Beyin'e gönder
            cevap = brain.jarvis_ile_konus(kullanici_mesaji)
        # --- YENİ EKLENEN KISIM SONU ---
        
        # Önce ekrana yazdır
        print(f"Jarvis: {cevap}\n")
        
        # Sonra sesli olarak oku!
        mouth.konus(cevap)

if __name__ == "__main__":
    asistan_dongusu()