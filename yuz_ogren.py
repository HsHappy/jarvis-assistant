import cv2
import numpy as np
import time

kamera = cv2.VideoCapture(0)
# Daha önce klasörümüze indirdiğimiz yüz bulma şablonu
yuz_casc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

yuz_verileri = []
idler = []

print("Kameraya bakın ve başınızı hafifçe sağa sola çevirin...")
time.sleep(2) # Hazırlanman için 2 saniye bekleme süresi

sayac = 0
while True:
    ret, kare = kamera.read()
    if not ret: continue
    
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
    yuzler = yuz_casc.detectMultiScale(gri, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in yuzler:
        sayac += 1
        # Sadece yüzün olduğu bölgeyi kırpıp hafızaya alıyoruz
        yuz_verileri.append(gri[y:y+h, x:x+w])
        idler.append(1) # 1 ID'si patronu (seni) temsil eder
        
        cv2.rectangle(kare, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.imshow('Jarvis - Yuzunuzu Ogreniyor', kare)
        
    cv2.waitKey(100) # Her kare arası 100ms bekle
    
    # 30 farklı açıdan fotoğraf yeterlidir
    if sayac >= 30: 
        break

kamera.release()
cv2.destroyAllWindows()

print("Yüz verileri toplandı. Yapay Zeka modeli eğitiliyor...")

# LBPH algoritması ile modeli eğit
taniyici = cv2.face.LBPHFaceRecognizer_create()
taniyici.train(yuz_verileri, np.array(idler))

# Öğrenilmiş yüz bilgisini projeye kaydet
taniyici.write('patron_yuzu.yml')
print("İşlem Başarılı! Jarvis artık yüzünüzü tanıyor (patron_yuzu.yml oluşturuldu).")