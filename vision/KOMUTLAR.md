# ODBARS Vision Core — Komut Referansı

## İlk Kurulum (Bir kez yapılır)

```bash
# Control Panel klasörüne git
cd "/Users/serhanensar/Documents/Proje/Control Panel/vision"

# Python sanal ortamı oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate

# Gerekli kütüphaneleri yükle
pip install -r requirements.txt
```

---

## Sunucuyu Başlatma (Her seferinde)

```bash
# Control Panel klasöründeyken:
cd vision && source venv/bin/activate && python main.py

# Veya vision klasörünün içindeyseniz:
source venv/bin/activate && python main.py
```

Başarılı çıktı:
```
✅ Kamera 0 (FWD) başarıyla açıldı.
🚀 ODBARS Vision Core başlatılıyor...
 * Running on http://127.0.0.1:8765
```

---

## Stream URL'leri

| Kamera       | URL                                  |
|--------------|--------------------------------------|
| Ön Kamera    | http://127.0.0.1:8765/cam_fwd        |
| Arka Kamera  | http://127.0.0.1:8765/cam_rear       |
| Nişan Kamera | http://127.0.0.1:8765/cam_aim        |
| Durum API    | http://127.0.0.1:8765/api/status     |

---

## Jetson Nano'ya Geçince

```bash
# Jetson'da IP adresini öğren
hostname -I

# Ana bilgisayardan bağlanmak için URL'leri şöyle değiştir:
# http://<JETSON_IP>:8765/cam_fwd
# Örnek: http://192.168.1.42:8765/cam_fwd
```

---

## Sunucuyu Durdurma

```bash
CTRL + C
```

---

## Sorun Giderme

| Hata | Çözüm |
|------|-------|
| `Port 5000 is in use` | macOS AirPlay kullanıyor, biz 8765 kullanıyoruz — sorun yok |
| `camera failed to initialize` | macOS kamera izni ver: Sistem Ayarları → Gizlilik → Kamera |
| `Address already in use (8765)` | `lsof -ti:8765 \| xargs kill -9` |
| `ModuleNotFoundError` | `source venv/bin/activate` yapıldığından emin ol |
