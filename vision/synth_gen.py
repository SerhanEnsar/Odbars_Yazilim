"""
ODBARS Sentetik Veri Üretici
==============================
Şartnamede tanımlanan 3 nesne sınıfını programatik olarak üretir:
  0: tabela  - 60cm çaplı daire, siyah zemin, beyaz metin
  1: stop    - "STOP" yazısı (dik eğim üzerindeki işaret)
  2: hedef   - A3 boyutunda atış hedefi

Kullanım:
    python synth_gen.py --n 200 --bg_dir backgrounds/

Çıktı:
    dataset/images/train/*.jpg
    dataset/labels/train/*.txt   (YOLO formatı)
"""

import cv2
import numpy as np
import os
import random
import argparse
from pathlib import Path

# --- Ayarlar ---
IMG_W, IMG_H = 640, 640
DATASET_ROOT  = Path(__file__).parent / "dataset"
CLASSES       = {0: "tabela", 1: "stop", 2: "hedef"}


# ─────────────────────────────────────────────
# Nesne çiziciler
# ─────────────────────────────────────────────

def draw_tabela(canvas, x, y, radius):
    """
    Şartnameye göre: dış çapı 60cm, siyah zemin, beyaz kenarlık + metin.
    x, y → merkez piksel koordinatı
    radius → piksel cinsinden yarıçap
    """
    # Dış daire (siyah dolgu)
    cv2.circle(canvas, (x, y), radius, (10, 10, 10), -1)
    # Beyaz kenarlık halkası
    cv2.circle(canvas, (x, y), radius, (240, 240, 240), max(3, radius // 10))
    # Merkezdeki metin (parkur adı placeholder)
    label_text = random.choice(["SU", "TAS", "EGIM", "ATIS", "1", "2", "3"])
    font_scale = radius / 40.0
    thickness  = max(1, int(radius / 20))
    (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    cv2.putText(canvas, label_text,
                (x - tw // 2, y + th // 2),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                (230, 230, 230), thickness, cv2.LINE_AA)
    return canvas


def draw_stop(canvas, x, y, w, h):
    """
    STOP yazısı: Sarı/beyaz zemin üzerine koyu kırmızı kalın yazı.
    Rampa üzerinde çarpık (perspective) görünebilir — augmentation ile halledilecek.
    """
    # Zemin dikdörtgen
    bg_color = random.choice([(240, 240, 200), (255, 255, 255), (200, 200, 180)])
    cv2.rectangle(canvas, (x, y), (x + w, y + h), bg_color, -1)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (60, 60, 60), 2)

    # STOP metni
    font_scale = w / 120.0
    thickness  = max(2, int(w / 40))
    text = "STOP"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness)
    tx = x + (w - tw) // 2
    ty = y + (h + th) // 2
    cv2.putText(canvas, text, (tx, ty),
                cv2.FONT_HERSHEY_DUPLEX, font_scale,
                (20, 20, 180), thickness, cv2.LINE_AA)
    return canvas


def draw_hedef(canvas, x, y, w, h):
    """
    Atış hedefi: Şekil 5'e göre çerçeveli A3 poster.
    Eşmerkezli daireler (kırmızı/siyah/beyaz) + merkez nokta.
    """
    cx, cy = x + w // 2, y + h // 2
    max_r  = min(w, h) // 2

    # Dış çerçeve
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (40, 40, 40), 2)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (220, 220, 220), -1)

    # Eşmerkezli halkalar (dıştan içe: kırmızı, beyaz, siyah, beyaz, kırmızı)
    colors = [(0, 0, 200), (220, 220, 220), (30, 30, 30), (220, 220, 220), (0, 0, 200)]
    for i, color in enumerate(colors):
        r = int(max_r * (1.0 - i * 0.18))
        if r > 2:
            cv2.circle(canvas, (cx, cy), r, color, -1)

    # Merkez nokta
    cv2.circle(canvas, (cx, cy), max(2, max_r // 10), (0, 0, 0), -1)
    return canvas


# ─────────────────────────────────────────────
# Arka plan yükleyici
# ─────────────────────────────────────────────

def load_backgrounds(bg_dir):
    """Arka plan görüntülerini yükler. Yoksa düz renkli arka planlar üretir."""
    bgs = []
    if bg_dir and Path(bg_dir).exists():
        for ext in ["*.jpg", "*.png", "*.jpeg"]:
            for p in Path(bg_dir).glob(ext):
                img = cv2.imread(str(p))
                if img is not None:
                    bgs.append(cv2.resize(img, (IMG_W, IMG_H)))
    
    if not bgs:
        print("⚠️  Arka plan klasörü bulunamadı, düz renkli arka planlar kullanılıyor.")
        for _ in range(20):
            color = [random.randint(60, 180) for _ in range(3)]
            bg = np.full((IMG_H, IMG_W, 3), color, dtype=np.uint8)
            # Hafif gürültü ekle (daha gerçekçi)
            noise = np.random.randint(0, 15, (IMG_H, IMG_W, 3), dtype=np.uint8)
            bgs.append(cv2.add(bg, noise))
    
    return bgs


# ─────────────────────────────────────────────
# YOLO label yazar
# ─────────────────────────────────────────────

def write_label(label_path, class_id, x, y, w, h, img_w=IMG_W, img_h=IMG_H):
    """YOLO normalize formatında label dosyası yazar."""
    cx = (x + w / 2) / img_w
    cy = (y + h / 2) / img_h
    nw = w / img_w
    nh = h / img_h
    with open(label_path, 'a') as f:
        f.write(f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")


# ─────────────────────────────────────────────
# Ana üretim döngüsü
# ─────────────────────────────────────────────

def generate(n_images, bg_dir, split="train"):
    out_img_dir = DATASET_ROOT / "images" / split
    out_lbl_dir = DATASET_ROOT / "labels" / split
    out_img_dir.mkdir(parents=True, exist_ok=True)
    out_lbl_dir.mkdir(parents=True, exist_ok=True)

    backgrounds = load_backgrounds(bg_dir)
    count = 0

    for i in range(n_images):
        # Rastgele arka plan seç ve kopyala
        canvas = random.choice(backgrounds).copy()
        label_path = out_lbl_dir / f"synth_{i:05d}.txt"

        # Her görüntüde 1-3 rastgele nesne yerleştir
        n_objects = random.randint(1, 3)
        placed    = []

        for _ in range(n_objects):
            class_id = random.choice(list(CLASSES.keys()))

            if class_id == 0:  # tabela
                radius = random.randint(30, 100)
                x = random.randint(radius, IMG_W - radius)
                y = random.randint(radius, IMG_H - radius)
                draw_tabela(canvas, x, y, radius)
                bx, by = x - radius, y - radius
                bw = bh = radius * 2
                write_label(label_path, class_id, bx, by, bw, bh)

            elif class_id == 1:  # stop
                w = random.randint(80, 220)
                h = random.randint(40, 100)
                x = random.randint(0, IMG_W - w)
                y = random.randint(0, IMG_H - h)
                draw_stop(canvas, x, y, w, h)
                write_label(label_path, class_id, x, y, w, h)

            elif class_id == 2:  # hedef
                w = random.randint(60, 180)
                h = int(w * 1.41)  # A3 en-boy oranı
                if h > IMG_H: h = IMG_H - 20
                x = random.randint(0, IMG_W - w)
                y = random.randint(0, IMG_H - h)
                draw_hedef(canvas, x, y, w, h)
                write_label(label_path, class_id, x, y, w, h)

        # Hafif gaussian blur (gerçekçilik)
        if random.random() > 0.5:
            canvas = cv2.GaussianBlur(canvas, (3, 3), 0)

        img_path = out_img_dir / f"synth_{i:05d}.jpg"
        cv2.imwrite(str(img_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])
        count += 1

    print(f"✅ {count} sentetik görüntü üretildi → {out_img_dir}")
    print(f"   Etiketler                      → {out_lbl_dir}")


# ─────────────────────────────────────────────
# Önizleme: ilk N görüntüyü göster
# ─────────────────────────────────────────────

def preview(n=5, split="train"):
    img_dir = DATASET_ROOT / "images" / split
    images  = list(img_dir.glob("*.jpg"))[:n]
    for img_path in images:
        img = cv2.imread(str(img_path))
        cv2.imshow(img_path.name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ODBARS Sentetik Veri Üretici")
    parser.add_argument("--n",      type=int, default=200,  help="Üretilecek görüntü sayısı")
    parser.add_argument("--bg_dir", type=str, default=None, help="Arka plan görüntü klasörü")
    parser.add_argument("--split",  type=str, default="train", choices=["train", "val", "test"])
    parser.add_argument("--preview",action="store_true",    help="Üretilen görüntüleri önizle")
    args = parser.parse_args()

    generate(args.n, args.bg_dir, args.split)

    if args.preview:
        preview(5, args.split)
