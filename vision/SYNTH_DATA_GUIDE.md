# ODBARS — Sentetik Veri Üretim Hattı (3D & 2D)

Bu dizin, TEKNOFEST 2026 İKA yarışması için gerekli olan sentetik eğitim verilerinin (tabelalar, engeller, hedefler) otomatik üretimi ve kontrolü için geliştirilen araçları içerir.

## 🚀 Hızlı Başlangıç

Sistemi başlatmak için ana dizinde şu komutu çalıştırın:

```bash
python3 "/Users/serhanensar/Documents/Proje/Control Panel/vision/synth_gui.py"
```

## 🛠 Özellikler

### 1. Blender (3D) Render Hattı
*   **Trafik Levhası Standartları**: Kırmızı çerçeveli, beyaz zeminli ve siyah metinli gerçekçi modeller.
*   **Görünürlük Garantisi**: Nesne kadraja girmeyene kadar (10 deneme) kamera açısı otomatik optimize edilir.
*   **Mesafe Kontrolü**: Panel üzerinden belirlenen min-max mesafelerde (örn: 2m-10m) üretim.
*   **Otomatik Etiketleme**: Sadece levha kısmını kapsayan hassas YOLO formatında Bounding Box üretimi.

### 2. Veri Kontrol Paneli (Dataset Viewer)
*   **Anlık İzleme**: Üretilen görselleri ve üzerine çizilmiş Bbox'ları yan yana görebilme.
*   **Etiket Doğrulama**: `.txt` içeriğini ve sınıfları (Tabela, STOP, Hedef) görsel üzerinden denetleme.
*   **Esnek Tarama**: `.jpg`, `.png`, `.JPG` formatlarındaki tüm verileri otomatik bulma.

## 📊 Sınıf Listesi (YOLO IDs)

| ID | Sınıf Adı | Açıklama |
|----|-----------|----------|
| 0  | Tabela 1  | 1 numaralı görev levhası |
| 1  | Tabela 2  | 2 numaralı görev levhası |
| ...| ...       | ... |
| 6  | Tabela 7  | 7 numaralı görev levhası |
| 7  | STOP      | Dur levhası |
| 8  | Hedef     | A3 boyutlu hedef levhası |

## 📁 Klasör Yapısı
*   `blender_render.py`: Blender motoru ve 3D sahne yönetim betiği.
*   `synth_gui.py`: Tüm süreci yöneten Tkinter tabanlı kontrol arayüzü.
*   `dataset/`: Üretilen görsellerin ve etiketlerin kaydedildiği varsayılan dizin.

---
*Geliştirici: Antigravity AI — ODBARS Projesi*
