import cv2

def yuz_taramasi_yap():
    try:
        kamera = cv2.VideoCapture(0)
        ret, kare = kamera.read()
        if not ret:
            kamera.release()
            return "Kameraya erişim sağlayamadım efendim."

        yuz_casc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Eğittiğimiz kişisel modeli yüklüyoruz
        taniyici = cv2.face.LBPHFaceRecognizer_create()
        taniyici.read('patron_yuzu.yml')
        
        gri_kare = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        yuzler = yuz_casc.detectMultiScale(gri_kare, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        kamera.release()
        
        if len(yuzler) == 0:
            return "Kamera taraması tamamlandı. Ortamda kimseyi göremiyorum."
            
        for (x, y, w, h) in yuzler:
            # Kırpılan yüzü modele soruyoruz: "Bu kim?"
            id, hata_payi = taniyici.predict(gri_kare[y:y+h, x:x+w])
            
            # LBPH modelinde hata payı (confidence) 0'a yaklaştıkça eşleşme mükemmel demektir.
            # Genellikle 70'in altındaki değerler güvenli bir eşleşmedir.
            if hata_payi < 70 and id == 1:
                return "Hoş geldiniz efendim. Sizi görmek ne güzel."
                
        return f"Tarama tamamlandı. Karşımda {len(yuzler)} kişi görüyorum ama kim olduklarını çıkaramadım."
            
    except Exception as e:
        print(f"\n[OPENCV HATASI]: {e}\n")
        return f"Görme sistemlerimde teknik bir arıza meydana geldi. Hata kodu: {str(e)}"