# ODBARS Panel (GCS Arayüzü) — Komut Referansı

## İlk Kurulum (Bir kez yapılır)

```bash
# Panel klasörüne git
cd "/Users/serhanensar/Documents/Proje/Control Panel/panel"

# Node bağımlılıklarını yükle
npm install
```

---

## Geliştirme Sunucusunu Başlatma

```bash
# Panel klasöründeyken:
npm run dev
```

Electron uygulaması açılır. Arayüz `http://localhost:5173` üzerinden de erişilebilir.

---

## Hem Vision hem Panel Aynı Anda

İki ayrı terminal sekmesi aç:

**Terminal 1 — Vision Core:**
```bash
cd "/Users/serhanensar/Documents/Proje/Control Panel"
cd vision && source venv/bin/activate && python main.py
```

**Terminal 2 — GCS Panel:**
```bash
cd "/Users/serhanensar/Documents/Proje/Control Panel/panel"
npm run dev
```

---

## Klavye Kısayolları

| Tuş | Fonksiyon |
|-----|-----------|
| `O` | Otonom ↔ Manuel mod geçişi |
| `↑ / ↓` | Manuel modda görevler arası geçiş |
| `Enter` | Seçili görevin durum popup'ını aç / onayla |
| `Esc` | Popup'ı kapat (değişiklik yapma) |
| `W A S D` | Manuel sürüş tuşları (görsel gösterge) |
| `Space` | Fren (görsel gösterge) |

---

## Git İş Akışı

```bash
# Değişiklikleri kaydet ve pushla
git add -A
git commit -m "feat/fix/refactor: açıklama"
git push origin feature/panel-init

# Son commitleri gör
git log --oneline -10

# Durumu kontrol et
git status
```

---

## Sorun Giderme

| Hata | Çözüm |
|------|-------|
| `npm run dev` açılmıyor | `npm install` yaptığından emin ol |
| Electron GPU hatası | Uygulamayı tamamen kapat, tekrar `npm run dev` |
| Kamera görünmüyor | Vision sunucusunun 8765'te çalıştığından emin ol |
| `render frame disposed` hatası | `ps aux \| grep electron \| awk '{print $2}' \| xargs kill -9` |
