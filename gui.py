import customtkinter as ctk
import threading
import ears
import brain
import hands
import mouth
import memory

# Arayüzün Ana Sınıfı
class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pencere Ayarları
        self.title("J.A.R.V.I.S. Kontrol Paneli")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")  # Karanlık tema
        ctk.set_default_color_theme("blue")
        
        # Ekrana bir Başlık Ekle
        self.baslik = ctk.CTkLabel(self, text="J.A.R.V.I.S. YEREL ASİSTAN", font=("Arial", 20, "bold"), text_color="#00FFFF")
        self.baslik.pack(pady=10)

        # Konuşmaların akacağı siyah ekran (Konsol görünümü)
        self.konsol = ctk.CTkTextbox(self, width=650, height=350, font=("Consolas", 14), text_color="#00FFFF", fg_color="#0d0d0d")
        self.konsol.pack(pady=10)
        
        # Sistemi başlatacak buton
        self.basla_btn = ctk.CTkButton(self, text="Sistemi Ateşle", command=self.sistemi_baslat, font=("Arial", 14, "bold"), fg_color="#8B0000", hover_color="#5C0000")
        self.basla_btn.pack(pady=10)

        self.calisiyor = False

    def ekrana_yaz(self, metin):
        """Yazıları arayüzdeki konsola ekler ve en alta kaydırır."""
        self.konsol.insert(ctk.END, metin + "\n")
        self.konsol.see(ctk.END)

    def sistemi_baslat(self):
        """Butona basıldığında arka planda Jarvis'i çalıştıracak ayrı bir işlem (Thread) başlatır."""
        if not self.calisiyor:
            self.calisiyor = True
            self.basla_btn.configure(state="disabled", text="Sistem Aktif (Dinleniyor)", fg_color="#005500")
            
            # Asistanı arka plana atıyoruz ki arayüz donmasın!
            t = threading.Thread(target=self.jarvis_dongusu)
            t.daemon = True # Arayüz kapanırsa bu da kapansın
            t.start()

    def jarvis_dongusu(self):
            self.ekrana_yaz("[SİSTEM] J.A.R.V.I.S. modülleri yüklendi.")
            self.ekrana_yaz("[SİSTEM] Uyku modunda... (Uyandırmak için 'Jarvis' deyin)\n" + "-"*50)
            
            while self.calisiyor:
                try:
                    # 1. Wake word dinle
                    ears.uyandirma_bekle()
                    self.ekrana_yaz("\n>>> [AKTİF] Sesiniz algılandı, dinliyorum...")
                    
                    # 2. Asıl komutu dinle
                    kullanici_mesaji = ears.beni_dinle(saniye=5)
                    
                    if not kullanici_mesaji:
                        # ANLAŞILAMADI DURUMUNDA EKLENEN KISIM
                        self.ekrana_yaz(">>> Anlaşılamadı, uyku moduna dönülüyor.")
                        self.ekrana_yaz("-" * 50 + "\n[SİSTEM] Uyku modunda... (Uyandırmak için 'Jarvis' deyin)")
                        continue
                        
                    self.ekrana_yaz(f"\nSen: {kullanici_mesaji}")
                    
                    # 3. Aksiyon (Eller) kontrolü
                    aksiyon_cevabi = hands.komut_islet(kullanici_mesaji)
                    
                    if aksiyon_cevabi:
                        cevap = aksiyon_cevabi
                        memory.mesaj_kaydet('user', kullanici_mesaji)
                        memory.mesaj_kaydet('assistant', aksiyon_cevabi)
                    else:
                        self.ekrana_yaz("Jarvis düşünüyor...")
                        cevap = brain.jarvis_ile_konus(kullanici_mesaji)
                        
                    self.ekrana_yaz(f"Jarvis: {cevap}\n" + "-"*50)
                    
                    # 4. Sesi oynat
                    mouth.konus(cevap)
                    
                    # BAŞARILI CEVAPTAN SONRA DÖNGÜ BAŞA SARMADAN EKLENEN KISIM
                    self.ekrana_yaz("[SİSTEM] Uyku modunda... (Uyandırmak için 'Jarvis' deyin)")
                    
                except Exception as e:
                    self.ekrana_yaz(f"[HATA]: {e}")

# Programı Çalıştır
if __name__ == "__main__":
    uygulama = JarvisGUI()
    uygulama.mainloop()