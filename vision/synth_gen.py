"""
ODBARS Sentetik Veri Üretici (v2 — Şartnameye Uyumlu)
=======================================================
Şartname referansları:
  - Tabela: "Arial Black" yazı tipi, dış çapı 60cm, siyah zemin, beyaz kenarlık  (s.13)
  - STOP:   Rampa yüzeyi üzerine boyanmış yazı (levha değil)                      (s.15)
  - Hedef:  A3 boyutunda, çerçeveli, Şekil 5 benzeri atış hedefi                  (s.15)

Kullanım:
    python synth_gen.py --n 200
    python synth_gen.py --n 200 --bg_dir backgrounds/ --preview
"""

import cv2
import numpy as np
import os
import random
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Pillow kurulu değil. 'pip install Pillow' ile kurun (Arial Black için gerekli).")

IMG_W, IMG_H  = 640, 640
DATASET_ROOT  = Path(__file__).parent / "dataset"

# Şartnamede geçen parkur aşaması isimleri (tabela metinleri)
TABELA_TEXTS = [
    "SU GEÇİŞİ", "TAŞLI YOL", "KAYAR ENGEL",
    "TABELA", "DİK EĞİM", "YAN EĞİM", "ATIŞ",
    "1", "2", "3", "4", "5", "6", "7",
]

# ─────────────────────────────────────────────
# Arial Black font yükleyici (PIL)
# ─────────────────────────────────────────────

def get_font(size=24):
    """Arial Black fontunu yükler. Bulunamazsa en yakın alternatifi döner."""
    if not PIL_AVAILABLE:
        return None

    # macOS / Linux / Windows için olası font yolları
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",  # macOS
        "/usr/share/fonts/truetype/msttcorefonts/Arial_Black.ttf",  # Linux
        "C:/Windows/Fonts/ariblk.ttf",  # Windows
        # Alternatifler (Arial Black yoksa)
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def pil_to_cv(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def cv_to_pil(cv_img):
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))


# ─────────────────────────────────────────────
# Nesne çiziciler
# ─────────────────────────────────────────────

def draw_tabela(canvas, x, y, radius):
    """
    Şartnameye göre:
    - Siyah dolu daire, beyaz kenarlık halkası
    - İçinde Arial Black ile aşama ismi/numarası
    x, y → merkez piksel | radius → piksel yarıçap
    """
    # ─ OpenCV ile zemin şeklini çiz ─
    cv2.circle(canvas, (x, y), radius, (8, 8, 8), -1)           # siyah dolgu
    border_t = max(3, radius // 8)
    cv2.circle(canvas, (x, y), radius, (240, 240, 240), border_t)  # beyaz kenarlık
    # İçte ince beyaz halka
    inner_r = int(radius * 0.82)
    cv2.circle(canvas, (x, y), inner_r, (220, 220, 220), max(1, border_t // 2))

    # ─ PIL ile Arial Black yazısı ─
    text = random.choice(TABELA_TEXTS)
    if PIL_AVAILABLE:
        font_size = max(12, radius // 2)
        font = get_font(font_size)
        pil_img = cv_to_pil(canvas)
        draw   = ImageDraw.Draw(pil_img)

        # Metin boyutunu al ve ortala
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = x - tw // 2
        ty = y - th // 2

        # Beyaz gölge + beyaz metin
        draw.text((tx + 1, ty + 1), text, font=font, fill=(60, 60, 60))
        draw.text((tx, ty), text, font=font, fill=(235, 235, 235))
        canvas = pil_to_cv(pil_img)
    else:
        # Fallback: OpenCV font
        fs = radius / 60.0
        th = max(1, radius // 18)
        (tw, _), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, fs, th)
        cv2.putText(canvas, text, (x - tw // 2, y + int(radius * 0.18)),
                    cv2.FONT_HERSHEY_DUPLEX, fs, (225, 225, 225), th, cv2.LINE_AA)
    return canvas


def draw_stop(canvas, x, y, radius):
    """
    STOP tabelası: Tabela ile aynı dairesel levha formatı.
    Şartneme parkur görselinde de dairesel levha olarak gösterilmiş.
    Siyah dolu daire, beyaz kenarlık, Arial Black ile 'STOP' yazısı.
    """
    # Dış daire — kırmızı gölgeli siyah (stop renk vurgusu)
    cv2.circle(canvas, (x, y), radius, (8, 8, 8), -1)
    border_t = max(3, radius // 8)
    # Kırmızı dış kenarlık (STOP levhası vurgusu)
    cv2.circle(canvas, (x, y), radius, (30, 30, 200), border_t)
    # İç beyaz halka
    inner_r = int(radius * 0.82)
    cv2.circle(canvas, (x, y), inner_r, (200, 200, 200), max(1, border_t // 2))

    if PIL_AVAILABLE:
        font_size = max(12, radius // 2)
        font = get_font(font_size)
        pil_img = cv_to_pil(canvas)
        draw   = ImageDraw.Draw(pil_img)

        bbox = draw.textbbox((0, 0), "STOP", font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = x - tw // 2
        ty = y - th // 2

        # Gölge + beyaz metin
        draw.text((tx + 1, ty + 1), "STOP", font=font, fill=(40, 40, 40))
        draw.text((tx, ty), "STOP", font=font, fill=(230, 230, 230))
        canvas = pil_to_cv(pil_img)
    else:
        fs = radius / 50.0
        th = max(1, radius // 16)
        (tw, _), _ = cv2.getTextSize("STOP", cv2.FONT_HERSHEY_DUPLEX, fs, th)
        cv2.putText(canvas, "STOP", (x - tw // 2, y + int(radius * 0.15)),
                    cv2.FONT_HERSHEY_DUPLEX, fs, (225, 225, 225), th, cv2.LINE_AA)
    return canvas


def draw_hedef(canvas, x, y, w, h):
    """
    Şekil 5 — A3 boyutunda atış hedefi, çerçeveli.
    Eşmerkezli daireler: dıştan içe kırmızı→beyaz→siyah→beyaz→kırmızı.
    Merkez: siyah nokta.
    """
    cx, cy = x + w // 2, y + h // 2
    max_r  = min(w, h) // 2 - 4

    # Beyaz çerçeve arkaplan
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (245, 245, 245), -1)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (30, 30, 30), 2)

    # Eşmerkezli halkalar (Şekil 5'e uygun)
    rings = [
        (1.00, (30,  30,  30)),   # dış → siyah
        (0.80, (220, 220, 220)),  # beyaz
        (0.60, (20,  20,  180)), # mavi/kırmızı
        (0.40, (220, 220, 220)),  # beyaz
        (0.20, (20,  20,  180)), # iç kırmızı/mavi
    ]
    for ratio, color in rings:
        r = int(max_r * ratio)
        if r > 1:
            cv2.circle(canvas, (cx, cy), r, color, -1)

    # Artı (crosshair) çizgileri
    line_color = (60, 60, 60)
    cv2.line(canvas, (cx - max_r, cy), (cx + max_r, cy), line_color, 1)
    cv2.line(canvas, (cx, cy - max_r), (cx, cy + max_r), line_color, 1)

    # Merkez nokta
    cv2.circle(canvas, (cx, cy), max(2, max_r // 8), (255, 255, 255), -1)
    return canvas


# ─────────────────────────────────────────────
# Arka plan yükleyici
# ─────────────────────────────────────────────

def load_backgrounds(bg_dir):
    bgs = []
    if bg_dir and Path(bg_dir).exists():
        for ext in ["*.jpg", "*.png", "*.jpeg"]:
            for p in Path(bg_dir).glob(ext):
                img = cv2.imread(str(p))
                if img is not None:
                    bgs.append(cv2.resize(img, (IMG_W, IMG_H)))

    if not bgs:
        print("⚠️  Arka plan bulunamadı → düz renkli arka planlar kullanılıyor.")
        terrains = [
            (90, 85, 75),   # kum/toprak
            (110, 115, 108),# kaya/beton
            (70, 90, 65),   # çimen
            (130, 125, 115),# çakıl
        ]
        for color in terrains:
            for _ in range(5):
                bg = np.full((IMG_H, IMG_W, 3), color, dtype=np.uint8)
                noise = np.random.randint(0, 25, (IMG_H, IMG_W, 3), dtype=np.uint8)
                bgs.append(cv2.add(bg, noise))
    return bgs


# ─────────────────────────────────────────────
# YOLO label yazar
# ─────────────────────────────────────────────

def write_label(label_path, class_id, x, y, w, h):
    cx = (x + w / 2) / IMG_W
    cy = (y + h / 2) / IMG_H
    nw = w / IMG_W
    nh = h / IMG_H
    with open(label_path, 'a') as f:
        f.write(f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")


# ─────────────────────────────────────────────
# Ana üretim döngüsü
# ─────────────────────────────────────────────

def generate(n_images, bg_dir, split="train"):
    out_img = DATASET_ROOT / "images" / split
    out_lbl = DATASET_ROOT / "labels" / split
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    bgs = load_backgrounds(bg_dir)
    count = 0

    for i in range(n_images):
        canvas = random.choice(bgs).copy()
        lbl_path = out_lbl / f"synth_{i:05d}.txt"

        n_objects = random.randint(1, 3)

        for _ in range(n_objects):
            class_id = random.choice([0, 1, 2])

            if class_id == 0:  # tabela
                radius = random.randint(35, 110)
                x = random.randint(radius + 5, IMG_W - radius - 5)
                y = random.randint(radius + 5, IMG_H - radius - 5)
                canvas = draw_tabela(canvas, x, y, radius)
                write_label(lbl_path, 0, x - radius, y - radius, radius * 2, radius * 2)

            elif class_id == 1:  # stop levhası (tabela formatında, kırmızı kenarlık)
                radius = random.randint(35, 110)
                x = random.randint(radius + 5, IMG_W - radius - 5)
                y = random.randint(radius + 5, IMG_H - radius - 5)
                canvas = draw_stop(canvas, x, y, radius)
                write_label(lbl_path, 1, x - radius, y - radius, radius * 2, radius * 2)

            elif class_id == 2:  # hedef
                w = random.randint(60, 200)
                h = int(w * 1.41)
                if y + h > IMG_H: h = IMG_H - 20
                x = random.randint(0, IMG_W - w)
                y = random.randint(0, IMG_H - h)
                canvas = draw_hedef(canvas, x, y, w, h)
                write_label(lbl_path, 2, x, y, w, h)

        # Hafif blur (hareket + odak simülasyonu)
        if random.random() > 0.6:
            k = random.choice([3, 5])
            canvas = cv2.GaussianBlur(canvas, (k, k), 0)

        cv2.imwrite(str(out_img / f"synth_{i:05d}.jpg"), canvas,
                    [cv2.IMWRITE_JPEG_QUALITY, 92])
        count += 1
        if count % 50 == 0:
            print(f"  {count}/{n_images} üretildi...")

    print(f"✅ {count} görüntü → {out_img}")
    print(f"   Etiketler   → {out_lbl}")


def preview(n=6, split="train"):
    img_dir = DATASET_ROOT / "images" / split
    images  = sorted(img_dir.glob("*.jpg"))[:n]
    for p in images:
        img = cv2.imread(str(p))
        if img is not None:
            cv2.imshow(p.name, img)
    print("Herhangi bir tuşa basın...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n",       type=int,  default=200)
    parser.add_argument("--bg_dir",  type=str,  default=None)
    parser.add_argument("--split",   type=str,  default="train",
                        choices=["train", "val", "test"])
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()

    generate(args.n, args.bg_dir, args.split)
    if args.preview:
        preview(6, args.split)
