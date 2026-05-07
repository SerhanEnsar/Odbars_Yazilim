# ODBARS — Otonom Dinamik Bölge Analiz ve Rehberlik Sistemi

![ODBARS Banner](https://img.shields.io/badge/TEKNOFEST-2026-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Development-green?style=for-the-badge)

ODBARS, TEKNOFEST 2026 İnsansız Kara Aracı (İKA) yarışması için geliştirilmiş, yüksek doğruluklu nesne tespiti, otonom sürüş rehberliği ve kapsamlı bir Yer Kontrol İstasyonu (GCS) sunan bir ekosistemdir.

## 📂 Proje Mimarisi

Proje iki ana modülden oluşmaktadır:

### 1. [Vision Core (Görüntü İşleme)](./vision)
Yapay zeka modellerinin eğitimi için sentetik veri üretimi ve gerçek zamanlı nesne tespiti birimidir.
- **Blender 3D Render**: Trafik levhaları, engeller ve hedefler için fotogerçekçi veri üretimi.
- **SynthGUI**: Sentetik veri üretim sürecini yöneten ve verileri kontrol eden arayüz.
- **YOLOv8/v11 Entegrasyonu**: Görev nesnelerinin (tabela, koni, stop) yüksek performanslı tespiti.

### 2. [GCS Panel (Kontrol Paneli)](./panel)
Operatörün aracı izlediği, görevleri yönettiği ve manuel müdahale edebildiği Electron tabanlı modern arayüzdür.
- **React + Vite + Electron**: Hızlı ve akıcı kullanıcı deneyimi.
- **Telemetri İzleme**: Hız, batarya, konum ve görev durumu takibi.
- **Video Stream**: Araç üzerindeki kameralardan gelen görüntülerin düşük gecikmeli aktarımı.

## 🚀 Kurulum ve Başlatma

### Gereksinimler
- **Python 3.10+** (Vision birimi için)
- **Node.js 18+** (Panel birimi için)
- **Blender 4.0+** (3D Render işlemleri için)

### Adımlar

1. **Depoyu Klonlayın:**
   ```bash
   git clone https://github.com/SerhanEnsar/Odbars_Yazilim.git
   cd "Control Panel"
   ```

2. **Vision Birimini Hazırlayın:**
   ```bash
   cd vision
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **GCS Paneli Başlatın:**
   ```bash
   cd ../panel
   npm install
   npm run dev
   ```

## 🔍 Sentetik Veri Üretimi
Eğitim verisi üretmek için geliştirilen özel arayüzü kullanabilirsiniz:
```bash
python3 vision/synth_gui.py
```
*Bu panel üzerinden mesafe ayarları, tabela çeşitleri ve zemin tipleri seçilerek YOLO formatında otomatik etiketli veri üretilebilir.*

## 📜 Lisans
Bu proje TEKNOFEST 2026 İKA yarışması kapsamında geliştirilmektedir. Tüm hakları ODBARS ekibine aittir.

---
**ODBARS — Geleceğin Otonom Sistemleri Üzerinde Tam Kontrol.**
