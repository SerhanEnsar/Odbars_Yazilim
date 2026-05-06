"""
ODBARS Veri Hazırlama Aracı
============================
Bu script iki görevi yerine getirir:
1. Görüntü toplama: Kameradan video kaydederek frame'leri dataset'e ekler.
2. Label doğrulama: Etiketlenmiş dosyaların format kontrolünü yapar.

Kullanım:
    python data_prep.py --mode capture --cam 0 --class tabela
    python data_prep.py --mode validate
"""

import cv2
import os
import argparse
import random
import shutil
from pathlib import Path

# Sınıf tanımları (dataset.yaml ile aynı sıra olmalı)
CLASSES = {
    0: "tabela",
    1: "stop",
    2: "engel",
    3: "hedef",
    4: "koni",
}

DATASET_ROOT = Path(__file__).parent / "dataset"
IMAGES_DIR = DATASET_ROOT / "images"
LABELS_DIR = DATASET_ROOT / "labels"


def capture_frames(cam_index: int, class_name: str, max_frames: int = 300):
    """
    Kameradan canlı görüntü alarak belirlenen sınıf için ham görüntü toplar.
    Görüntüler dataset/images/train ve val klasörlerine 80/20 oranında bölünür.
    Etiketleme sonradan Roboflow veya LabelImg ile yapılacak.

    Args:
        cam_index: Kamera index numarası (0, 1, 2...)
        class_name: Çekilen nesnenin sınıf adı (klasör isimlendirme için)
        max_frames: Kaç frame kaydedileceği
    """
    class_id = next((k for k, v in CLASSES.items() if v == class_name), None)
    if class_id is None:
        print(f"HATA: '{class_name}' geçerli bir sınıf değil. Geçerliler: {list(CLASSES.values())}")
        return

    save_dir = IMAGES_DIR / "train" / class_name
    save_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"HATA: Kamera {cam_index} açılamadı.")
        return

    count = 0
    print(f"[{class_name}] Kayıt başladı. 'S' ile kaydet, 'Q' ile çık.")

    while count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, f"Sinif: {class_name} | Kaydedilen: {count}/{max_frames}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display, "S: Kaydet | Q: Cik",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        cv2.imshow("ODBARS - Frame Toplama", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            filename = save_dir / f"{class_name}_{count:04d}.jpg"
            cv2.imwrite(str(filename), frame)
            count += 1
            print(f"  Kaydedildi: {filename}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n✅ {count} frame kaydedildi → {save_dir}")


def split_dataset(train_ratio: float = 0.8):
    """
    images/train içindeki görüntüleri train/val olarak böler.
    Etiketleme bittikten sonra çalıştırılır.
    """
    train_img = IMAGES_DIR / "train"
    val_img   = IMAGES_DIR / "val"
    train_lbl = LABELS_DIR / "train"
    val_lbl   = LABELS_DIR / "val"

    all_images = list(train_img.glob("*.jpg")) + list(train_img.glob("*.png"))
    random.shuffle(all_images)

    split_idx = int(len(all_images) * train_ratio)
    val_images = all_images[split_idx:]

    for img_path in val_images:
        label_path = train_lbl / img_path.with_suffix(".txt").name
        shutil.move(str(img_path), str(val_img / img_path.name))
        if label_path.exists():
            shutil.move(str(label_path), str(val_lbl / label_path.name))

    print(f"✅ Split tamamlandı: {split_idx} train / {len(val_images)} val")


def validate_labels():
    """
    Mevcut label dosyalarının YOLO formatına uygunluğunu kontrol eder.
    Format: <class_id> <x_center> <y_center> <width> <height>
    Tüm değerler 0-1 arasında normalize edilmiş olmalıdır.
    """
    errors = []
    n_classes = len(CLASSES)

    for split in ["train", "val", "test"]:
        label_dir = LABELS_DIR / split
        if not label_dir.exists():
            continue
        for label_file in label_dir.glob("*.txt"):
            with open(label_file) as f:
                for line_no, line in enumerate(f, 1):
                    parts = line.strip().split()
                    if len(parts) != 5:
                        errors.append(f"{label_file}:{line_no} → 5 değer olmalı, {len(parts)} var")
                        continue
                    class_id, x, y, w, h = parts
                    if int(class_id) >= n_classes:
                        errors.append(f"{label_file}:{line_no} → Geçersiz class_id: {class_id}")
                    for val in [x, y, w, h]:
                        if not (0.0 <= float(val) <= 1.0):
                            errors.append(f"{label_file}:{line_no} → Değer aralık dışı: {val}")

    if errors:
        print(f"❌ {len(errors)} hata bulundu:")
        for e in errors:
            print(f"   {e}")
    else:
        print("✅ Tüm label dosyaları geçerli YOLO formatında.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ODBARS Dataset Hazırlama")
    parser.add_argument("--mode", choices=["capture", "split", "validate"], required=True)
    parser.add_argument("--cam", type=int, default=0, help="Kamera index")
    parser.add_argument("--class", dest="class_name", help="Çekilecek sınıf adı")
    parser.add_argument("--frames", type=int, default=300)
    args = parser.parse_args()

    if args.mode == "capture":
        capture_frames(args.cam, args.class_name, args.frames)
    elif args.mode == "split":
        split_dataset()
    elif args.mode == "validate":
        validate_labels()
