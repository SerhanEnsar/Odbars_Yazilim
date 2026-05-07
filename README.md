# TEKNOFEST 2026 AI in Aviation Project (ODBARS)

Bu depo, ODBARS otonom kara aracı projesinin kontrol paneli ve görüntü işleme birimlerini içerir.

## 📂 Proje Yapısı
- **[/vision](file:///Users/serhanensar/Documents/Proje/Control%20Panel/vision)**: Sentetik veri üretim hattı ve görüntüleme araçları.
  - [Sentetik Veri Kullanım Kılavuzu](file:///Users/serhanensar/Documents/Proje/Control%20Panel/vision/SYNTH_DATA_GUIDE.md)
- **[/panel](file:///Users/serhanensar/Documents/Proje/Control%20Panel/panel)**: GCS (Yer Kontrol İstasyonu) arayüzü ve Electron uygulaması.
  - [Panel Komut Referansı](file:///Users/serhanensar/Documents/Proje/Control%20Panel/panel/KOMUTLAR.md)

## 🚀 Başlatma
Sentetik veri panelini başlatmak için:
```bash
python3 vision/synth_gui.py
```
