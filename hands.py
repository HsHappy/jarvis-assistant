import subprocess
import webbrowser
import requests
import re
from ddgs import DDGS
import eyes

def hava_durumu_getir():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.0138&longitude=28.9497¤t_weather=true"
        cevap = requests.get(url).json()
        derece = cevap['current_weather']['temperature']
        return f"İstanbul için anlık hava durumu {derece} derece efendim."
    except Exception:
        return "Şu anda hava durumu servisine ulaşılamıyor."

def dolar_kuru_getir():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        cevap = requests.get(url).json()
        tl_karsiligi = cevap['rates']['TRY']
        return f"Güncel verilere göre 1 Amerikan Doları, {tl_karsiligi} Türk Lirası işlem görüyor."
    except Exception:
        return "Şu anda döviz kurlarına ulaşılamıyor."

def sorguyu_temizle(mesaj):
    # Noktalama işaretlerini sil
    mesaj = re.sub(r'[^\w\s]', '', mesaj.lower())
    
    # Arama motoruna gönderilmemesi gereken gereksiz kelimeler
    gereksiz_kelimeler = ["jarvis", "bana", "nedir", "kimdir", "araştır", "bilgi", "ver", "öğretir", "misin", "lütfen", "hakkında", "durumu", "ne", "anlat"]
    
    kelimeler = mesaj.split()
    temiz_kelimeler = [k for k in kelimeler if k not in gereksiz_kelimeler]
    
    # Kalan kelimeleri birleştirip geri döndür
    return " ".join(temiz_kelimeler)

def internette_ara(sorgu):
    temiz_sorgu = sorguyu_temizle(sorgu)
    print(f"Jarvis internette şunu arıyor: '{temiz_sorgu}'")
    
    if not temiz_sorgu:
        return "Neyi araştırmamı istediğinizi tam anlayamadım efendim."
        
    try:
        with DDGS() as ddgs:
            sonuclar = list(ddgs.text(temiz_sorgu, region='tr-tr', safesearch='moderate', max_results=2))
            if sonuclar:
                ozet = sonuclar[0]['body']
                return f"İnternetten bulduğum verilere göre: {ozet}"
            else:
                return "Bu konu hakkında güncel bir bilgi bulamadım efendim."
    except Exception as e:
        return "İnternete erişirken bir sorun yaşadım."

def komut_islet(mesaj):
    mesaj = mesaj.lower()
    
    # --- KAMERA VE GÖRÜŞ KOMUTLARI ---
    if "ortama bak" in mesaj or "kimse var mı" in mesaj or "taraması yap" in mesaj:
        return eyes.yuz_taramasi_yap()
    
    # --- 1. CANLI VERİ KOMUTLARI ---
    if "hava" in mesaj:
        return hava_durumu_getir()
        
    # Şartı çok basitleştirdik: Cümlede "dolar" ve "kur" geçmesi yeterli
    elif "dolar" in mesaj or "kur" in mesaj:
        return dolar_kuru_getir()

    # --- 2. TARAYICI VE UYGULAMA KOMUTLARI ---
    elif "youtube aç" in mesaj:
        webbrowser.open("https://www.youtube.com")
        return "Hemen YouTube'u açıyorum efendim."
        
    elif "google" in mesaj and "aç" in mesaj:
        webbrowser.open("https://www.google.com")
        return "Google arama motorunu başlattım."
        
    elif "hesap makinesi" in mesaj and "aç" in mesaj:
        subprocess.Popen('calc.exe')
        return "Hesap makinesi ekrana getirildi."

    # --- 3. DİNAMİK İNTERNET ARAMASI ---
    elif any(kelime in mesaj for kelime in ["kimdir", "nedir", "araştır", "bilgi", "öğret", "nasıl", "durum"]):
        return internette_ara(mesaj)

    return False