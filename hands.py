import subprocess
import webbrowser

def komut_islet(mesaj):
    mesaj = mesaj.lower()
    
    # 1. Tarayıcı İşlemleri (Web siteleri)
    if "youtube aç" in mesaj:
        webbrowser.open("https://www.youtube.com")
        return "Hemen YouTube'u açıyorum efendim."
        
    elif "google" in mesaj and "aç" in mesaj:
        webbrowser.open("https://www.google.com")
        return "Google arama motorunu tarayıcıda başlattım."
        
    # 2. İşletim Sistemi İşlemleri (Yerel Uygulamalar)
    elif "hesap makinesi" in mesaj and "aç" in mesaj:
        # Windows'un kendi hesap makinesi uygulaması
        subprocess.Popen('calc.exe')
        return "Hesap makinesi ekrana getirildi."
        
    elif "not defteri" in mesaj and "aç" in mesaj:
        subprocess.Popen('notepad.exe')
        return "Yeni bir not defteri açtım."
        
    # 3. İsteğe Bağlı: Kendi kullandığın programlar (Örn: VS Code)
    elif "vs code" in mesaj and "aç" in mesaj:
        # Windows'ta code komutu VS Code'u başlatır
        subprocess.Popen('code', shell=True)
        return "Visual Studio Code başlatılıyor. İyi kodlamalar!"

    # Eğer mesajda bir aksiyon kelimesi yoksa, False dönüyoruz
    # Böylece sistem bunun normal bir sohbet olduğunu anlar ve Beyin'e (LLM'e) gönderir.
    return False