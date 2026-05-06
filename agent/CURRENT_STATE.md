# Projenin Güncel Durumu (Current State)

*Her tamamlanan görevden veya önemli karardan sonra bu dosyayı güncelleyin.*

## Son Güncelleme: 7 Mayıs 2026
**Branch**: `feature/panel-init`  
**Durum**: Panel (GCS) arayüzü + Vision Core temeli tamamlandı. Donanım entegrasyonu bekleniyor.

---

## Tamamlananlar

### Panel (GCS Arayüzü)
- Electron + Vite + React altyapısı kuruldu, `npm run dev` ile çalışıyor.
- "Çöl Kamuflajı / Taktik Askeri" temasıyla tam HUD tasarımı tamamlandı.
- **Telemetri**: 20Hz hızında smooth "Random Walk" simülasyon verisi akıyor (main.js).
- **Sürüş Modu**: `O` tuşu ile OTONOM ↔ MANUEL geçişi.
- **Klavye Kontrolü**: WASD + SPACE tuş göstergesi (sadece MANUEL modda).
- **Görev Navigasyonu**: Manuel modda ↑↓ ok tuşları + Enter ile popup + Esc ile iptal.
- **Görev Durumları**: Aynı anda yalnızca 1 AKTİF görev, OTONOM modda değişiklik kilitli.
- **Dinamik Action Log**: Toast bildirimleri + genişletilebilir floating panel (sağ altta).
  - AKTİF: Turuncu, TAMAM: Yeşil, BEKLEME: Gri, ACİL: Kırmızı yanıp söner.
  - Panel açıkken toastlar gizlenir, yeni log gelince auto-scroll.
- **Kamera Altyapısı**: 3 kamera slotu (CAM_FWD, CAM_REAR, CAM_AIM) MJPEG stream alacak şekilde hazırlandı. `http://127.0.0.1:8765/cam_*` adreslerini dinliyor. Sinyal yokken animasyonlu "Sinyal Aranıyor" ekranı.
- **Animasyon**: Atış Görevi AKTİF olunca CAM_AIM büyüyüp ön plana geçiyor (Picture-in-Picture).

### Vision Core (Python)
- `vision/main.py`: Flask tabanlı MJPEG streaming sunucusu kuruldu.
- Port: **8765** (macOS AirPlay 5000'i kullandığından çakışmaması için).
- Kamera açılamazsa siyah dummy frame akışı yapıyor, uygulama çökmüyor.
- YOLO / OpenCV entegrasyonu için yer açık bırakıldı (`# GORUNTU ISLEME ALANI`).
- `vision/requirements.txt`: flask, opencv-python, numpy, ultralytics.

### Dokümantasyon
- `vision/KOMUTLAR.md`: Vision sunucusu için tüm terminal komutları.
- `panel/KOMUTLAR.md`: Panel için tüm terminal komutları + klavye kısayolları.

---

## Sıradaki Adımlar (To-Do)

1. **YOLO Entegrasyonu**: `vision/main.py` içindeki `# GORUNTU ISLEME ALANI` bölümüne YOLOv8/v11 ile nesne tespiti + bounding box çizimi eklenmesi.
2. **Kamera Erişim İzni**: macOS Gizlilik → Kamera izninin terminale verilmesi (ilk çalıştırmada çıkabilir).
3. **Donanım Telemetri**: `panel/electron/main.js` içindeki simülasyon kodunun yerine gerçek SerialPort/UDP veri okuma altyapısının kurulması.
4. **Gamepad API**: `navigator.getGamepads()` ile joystick/gamepad desteği (yarışma öncesinde).
5. **Jetson Geçişi**: Vision sunucusu `host='0.0.0.0'` ile zaten ağa açık. Panel URL'lerinde `127.0.0.1` → `<JETSON_IP>` değiştirilmesi yeterli.

---

## Bloke Eden Durumlar (Blockers)

- Diğer araç sistemleri (STM32, ROS vb.) henüz hazır değil → Telemetri entegrasyonu beklemede.
- Gerçek kamera donanımı mevcut değil → Vision simülasyon modunda çalışıyor.

---

## Komut Özeti

```bash
# Vision Core başlat (Control Panel kök dizininden)
cd vision && source venv/bin/activate && python main.py

# Panel başlat
cd panel && npm run dev
```
