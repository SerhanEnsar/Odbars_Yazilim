# ODBARS Vision — Blender Render Komutları

## Gereksinimler

| Araç | Nereden | Notlar |
|------|---------|--------|
| Blender 4.x | [blender.org](https://www.blender.org/download/) | macOS DMG olarak indir |
| Polyhaven Terrain | [polyhaven.com/textures](https://polyhaven.com/textures) | Aşağıya bak |

---

## Polyhaven'dan Terrain İndirme

1. [polyhaven.com/textures](https://polyhaven.com/textures) → **Ground** veya **Rock** kategorisi
2. Bir texture seç → sağ panelde format: **JPG** (BLEND değil!), çözünürlük: **4K**
3. `diffuse` veya `color` adlı görseli indir (örn: `rocky_terrain_01_diff_4k.jpg`)
4. Hepsini tek bir klasöre koy, örneğin:

```
/Users/serhanensar/Documents/Terrains/
├── rocky_terrain_01_diff_4k.jpg
├── sandy_ground_02_diff_4k.jpg
├── gravel_03_diff_4k.jpg
└── ...
```

> **Not:** Blender dosyası (`.blend`) değil, sadece `diffuse/color` JPG dosyasını indir.  
> HDR formatına gerek yok, düz JPG yeterli.

---

## CONFIG Ayarları (`blender_render.py` üstü)

```python
CONFIG = {
    "n_renders":    200,   # ← İstediğin sayıyı yaz (100, 500, 1000 olabilir)
    "output_dir":   "/Users/serhanensar/Desktop/Renders",  # ← Çıkış klasörü
    "terrain_dir":  "/Users/serhanensar/Documents/Terrains",  # ← Terrain klasörü
    "font_path":    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "render_w":     1920,  # 1080p
    "render_h":     1080,
    "class_weights": [0.4, 0.3, 0.3],  # tabela / stop / hedef olasılıkları
    "camera_distance_range": (1.5, 8.0),  # kamera mesafesi (metre)
    "camera_height_range":   (0.3, 2.5),  # kamera yüksekliği (metre)
}
```

| Parametre | Açıklama |
|-----------|----------|
| `n_renders` | Toplam kaç render alınacak. İstediğin sayıyı yazabilirsin. |
| `output_dir` | Görseller ve YOLO label dosyaları buraya kaydedilir. |
| `terrain_dir` | Bu klasördeki JPG/PNG dosyalarından her render'da biri rastgele seçilir. |
| `render_w/h` | 1920×1080 (1080p). Değiştirebilirsin: 640×640, 1280×720 vb. |
| `class_weights` | 3 sınıfın seçilme olasılığı: `[tabela, stop, hedef]` toplamı 1.0 olmalı. |

---

## Render Başlatma

```bash
# Terminal'den (Blender'ı uygulama olarak açmadan, arka planda çalışır):
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python "/Users/serhanensar/Documents/Proje/Control Panel/vision/blender_render.py"
```

```bash
# Kısa alias (opsiyonel, ~/.zshrc içine ekle):
alias blender-render='/Applications/Blender.app/Contents/MacOS/Blender --background --python'
# Kullanımı:
blender-render "/Users/serhanensar/Documents/Proje/Control Panel/vision/blender_render.py"
```

---

## Çıkış Klasörü Yapısı

Render bittikten sonra şu yapı oluşur:

```
Desktop/Renders/
├── images/
│   └── train/
│       ├── render_00000.jpg
│       ├── render_00001.jpg
│       └── ...
└── labels/
    └── train/
        ├── render_00000.txt    ← YOLO formatı
        ├── render_00001.txt
        └── ...
```

---

## Roboflow'a Yükleme (Render Sonrası)

1. Roboflow → `odbars-vision` projesi → **Upload Data**
2. `images/train/` klasörünü sürükle-bırak
3. "Upload Labels" seçeneğinde `labels/train/` klasörünü seç  
   *(Roboflow, YOLO `.txt` etiketlerini otomatik tanır)*
4. Dataset Version oluştur → Augmentation ekle → Export

---

## Render Süre Tahmini

| Samples | 1 Render | 200 Render | Açıklama |
|---------|----------|------------|----------|
| 64 (varsayılan) | ~15–30 sn | ~1–2 saat | Hızlı, yeterince kaliteli |
| 128 | ~30–60 sn | ~3–4 saat | Daha temiz gölgeler |

> Hız/kalite dengesini `sc.cycles.samples = 64` satırından ayarlayabilirsin.

---

## Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|-------|-------|
| `ModuleNotFoundError: bpy` | Bu script doğrudan Python ile değil, Blender içinden çalışır. |
| Font bulunamadı | `font_path`'i kontrol et. macOS'ta: `/System/Library/Fonts/Supplemental/Arial Black.ttf` |
| Terrain yüklenmedi | `terrain_dir` içinde `.jpg` veya `.png` dosyası olduğundan emin ol. |
| Render boş/siyah | Cycles engine seçili mi? `sc.render.engine = 'CYCLES'` satırını kontrol et. |
| Çok yavaş | `sc.cycles.samples` değerini düşür (32 veya 64). |
