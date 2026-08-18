import sqlite3

def baglanti_al():
    # Veritabanı dosyasına bağlan (yoksa otomatik oluşturur)
    conn = sqlite3.connect('jarvis_memory.db')
    
    # Sohbet geçmişi tablosunu oluştur (eğer yoksa)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sohbet_gecmisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT,
            icerik TEXT
        )
    ''')
    return conn

def mesaj_kaydet(rol, icerik):
    """Kullanıcının veya asistanın mesajını veritabanına ekler."""
    conn = baglanti_al()
    conn.execute("INSERT INTO sohbet_gecmisi (rol, icerik) VALUES (?, ?)", (rol, icerik))
    conn.commit()
    conn.close()

def gecmisi_getir(limit=10):
    """Modelin hatırlaması için son X mesajı SQL'den çeker."""
    conn = baglanti_al()
    
    # Son 'limit' kadar mesajı id'ye göre tersten alıp, sonra tekrar kronolojik sıraya diziyoruz
    sorgu = f"""
        SELECT rol, icerik FROM (
            SELECT * FROM sohbet_gecmisi ORDER BY id DESC LIMIT {limit}
        ) ORDER BY id ASC
    """
    cursor = conn.execute(sorgu)
    
    # Ollama API'sinin beklediği JSON / Sözlük formatına çeviriyoruz
    gecmis = [{'role': satir[0], 'content': satir[1]} for satir in cursor.fetchall()]
    
    conn.close()
    return gecmis