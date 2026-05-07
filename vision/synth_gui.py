"""
ODBARS Sentetik Veri Üretici — GUI Panel
Çalıştırma: python synth_gui.py
Gereksinimler: pip install Pillow opencv-python
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import cv2
import numpy as np
import random
import os
import json
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ─────────────────────────────────────────────
# Font yükleyici
# ─────────────────────────────────────────────

def get_font(size=24):
    if not PIL_AVAILABLE:
        return None
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial_Black.ttf",
        "C:/Windows/Fonts/ariblk.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def pil_to_cv(img): return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
def cv_to_pil(img): return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# ─────────────────────────────────────────────
# Perspektif bozucu
# ─────────────────────────────────────────────

def apply_perspective(canvas, x1, y1, w, h, strength=0.18):
    """Nesnenin bounding box bölgesine hafif perspektif dönüşümü uygular."""
    x2, y2 = x1 + w, y1 + h
    roi = canvas[y1:y2, x1:x2].copy()
    if roi.shape[0] < 10 or roi.shape[1] < 10:
        return canvas
    rw, rh = roi.shape[1], roi.shape[0]
    dx = int(rw * strength * random.uniform(0.3, 1.0))
    dy = int(rh * strength * random.uniform(0.3, 1.0))
    side = random.choice(["left", "right", "top", "bottom"])
    src = np.float32([[0,0],[rw,0],[rw,rh],[0,rh]])
    if side == "left":
        dst = np.float32([[dx,dy],[rw,0],[rw,rh],[dx,rh-dy]])
    elif side == "right":
        dst = np.float32([[0,0],[rw-dx,dy],[rw-dx,rh-dy],[0,rh]])
    elif side == "top":
        dst = np.float32([[dx,dy],[rw-dx,dy],[rw,rh],[0,rh]])
    else:
        dst = np.float32([[0,0],[rw,0],[rw-dx,rh-dy],[dx,rh-dy]])
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(roi, M, (rw, rh), borderMode=cv2.BORDER_REPLICATE)
    canvas[y1:y2, x1:x2] = warped
    return canvas


# ─────────────────────────────────────────────
# Nesne çiziciler
# ─────────────────────────────────────────────

TABELA_TEXTS = ["SU GECİSİ","TASLI YOL","KAYAR ENGEL","DİK EGİM","YAN EGİM","ATIS","1","2","3","4","5","6","7"]


def _draw_text_centered(pil_img, cx, cy, text, font, fill=(235,235,235), shadow=(30,30,30)):
    """PIL üzerinde metni (cx, cy) noktasına tam ortalı yazar."""
    d = ImageDraw.Draw(pil_img)
    bb = d.textbbox((0, 0), text, font=font)   # (left, top, right, bottom)
    # offset'i çıkar → gerçek boyut
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    tx = cx - tw // 2 - bb[0]   # bb[0] = sol offset
    ty = cy - th // 2 - bb[1]   # bb[1] = üst offset
    # Gölge
    d.text((tx + 1, ty + 1), text, font=font, fill=shadow)
    # Asıl metin
    d.text((tx, ty), text, font=font, fill=fill)
    return pil_img


def draw_tabela(canvas, x, y, radius, persp_strength=0.15):
    """Şartname: Arial Black, siyah dolgu daire, beyaz dış kenarlık halkası."""
    # Dış siyah daire
    cv2.circle(canvas, (x, y), radius, (10, 10, 10), -1)
    # Beyaz dış kenarlık
    bt = max(4, radius // 7)
    cv2.circle(canvas, (x, y), radius, (240, 240, 240), bt, lineType=cv2.LINE_AA)
    # İç beyaz ince çember çizgisi (şartneme tabelasındaki gibi)
    inner_r = int(radius * 0.84)
    cv2.circle(canvas, (x, y), inner_r, (180, 180, 180), max(1, bt // 3), lineType=cv2.LINE_AA)

    text = random.choice(TABELA_TEXTS)
    if PIL_AVAILABLE:
        # Yazı boyutunu yarıçapa göre otomatik ayarla
        font_size = max(10, int(radius * 0.55))
        font = get_font(font_size)
        pil = cv_to_pil(canvas)
        pil = _draw_text_centered(pil, x, y, text, font)
        canvas = pil_to_cv(pil)

    if persp_strength > 0:
        canvas = apply_perspective(canvas, x - radius, y - radius, radius * 2, radius * 2, persp_strength)
    return canvas, (x - radius, y - radius, radius * 2, radius * 2)


def draw_stop(canvas, x, y, radius, persp_strength=0.15):
    """STOP levhası: tabela formatında, kırmızı kenarlık farkıyla ayrışır."""
    cv2.circle(canvas, (x, y), radius, (10, 10, 10), -1)
    bt = max(4, radius // 7)
    cv2.circle(canvas, (x, y), radius, (40, 40, 210), bt, lineType=cv2.LINE_AA)
    inner_r = int(radius * 0.84)
    cv2.circle(canvas, (x, y), inner_r, (160, 160, 200), max(1, bt // 3), lineType=cv2.LINE_AA)
    if PIL_AVAILABLE:
        font_size = max(10, int(radius * 0.55))
        font = get_font(font_size)
        pil = cv_to_pil(canvas)
        pil = _draw_text_centered(pil, x, y, "STOP", font, fill=(230, 230, 230))
        canvas = pil_to_cv(pil)
    if persp_strength > 0:
        canvas = apply_perspective(canvas, x - radius, y - radius, radius * 2, radius * 2, persp_strength)
    return canvas, (x - radius, y - radius, radius * 2, radius * 2)


def draw_hedef(canvas, x, y, w, h, persp_strength=0.12):
    """A3 oranlı atış hedefi: eşmerkezli halkalar + crosshair + merkez nokta."""
    cx, cy = x + w // 2, y + h // 2
    max_r  = min(w, h) // 2 - 4

    # Beyaz arka zemin
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (245, 245, 245), -1)

    # Eşmerkezli halkalar (dıştan içe)
    ring_defs = [
        (1.00, (30,  30,  30)),    # siyah dış
        (0.78, (255, 255, 255)),   # beyaz
        (0.58, (0,   0,  200)),   # mavi/kırmızı
        (0.38, (255, 255, 255)),   # beyaz
        (0.20, (0,   0,  200)),   # iç mavi/kırmızı
    ]
    for ratio, color in ring_defs:
        r = int(max_r * ratio)
        if r > 2:
            cv2.circle(canvas, (cx, cy), r, color, -1, lineType=cv2.LINE_AA)

    # Crosshair çizgileri
    lc = (80, 80, 80)
    cv2.line(canvas, (cx - max_r, cy), (cx + max_r, cy), lc, 1, lineType=cv2.LINE_AA)
    cv2.line(canvas, (cx, cy - max_r), (cx, cy + max_r), lc, 1, lineType=cv2.LINE_AA)

    # Kare dış çerçeve
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (30, 30, 30), 2)

    # Merkez beyaz nokta
    cv2.circle(canvas, (cx, cy), max(3, max_r // 7), (255, 255, 255), -1, lineType=cv2.LINE_AA)

    if persp_strength > 0:
        canvas = apply_perspective(canvas, x, y, w, h, persp_strength)
    return canvas, (x, y, w, h)


def load_backgrounds(bg_dir, img_w=640, img_h=640):
    bgs = []
    if bg_dir and Path(bg_dir).exists():
        for ext in ["*.jpg","*.png","*.jpeg"]:
            for p in Path(bg_dir).glob(ext):
                img = cv2.imread(str(p))
                if img is not None:
                    bgs.append(cv2.resize(img, (img_w, img_h)))
    if not bgs:
        for color in [(90,85,75),(110,115,108),(70,90,65),(130,125,115)]:
            for _ in range(5):
                bg = np.full((img_h, img_w, 3), color, dtype=np.uint8)
                noise = np.random.randint(0, 25, (img_h, img_w, 3), dtype=np.uint8)
                bgs.append(cv2.add(bg, noise))
    return bgs


def write_label(label_path, class_id, bx, by, bw, bh, img_w=640, img_h=640):
    cx = (bx + bw/2) / img_w
    cy = (by + bh/2) / img_h
    nw = bw / img_w
    nh = bh / img_h
    with open(label_path, 'a') as f:
        f.write(f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")


def generate_dataset(cfg, progress_cb=None, log_cb=None):
    """Ana üretim fonksiyonu. cfg: dict."""
    img_w = cfg["img_w"]
    img_h = cfg["img_h"]
    out_img = Path(cfg["out_dir"]) / "images" / cfg["split"]
    out_lbl = Path(cfg["out_dir"]) / "labels" / cfg["split"]
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    bgs = load_backgrounds(cfg["bg_dir"], img_w, img_h)
    persp = cfg["persp_strength"]
    counts = {0: cfg["n_tabela"], 1: cfg["n_stop"], 2: cfg["n_hedef"]}
    r_min, r_max = cfg["radius_min"], cfg["radius_max"]

    # Tüm örnekleri karıştır
    samples = []
    for cls_id, n in counts.items():
        samples.extend([cls_id] * n)
    random.shuffle(samples)

    total = len(samples)
    i = 0
    for idx, cls_id in enumerate(samples):
        canvas = random.choice(bgs).copy()
        lbl_path = out_lbl / f"synth_{idx:05d}.txt"

        margin = r_max + 5
        radius = random.randint(r_min, r_max)
        x = random.randint(margin, img_w - margin)
        y = random.randint(margin, img_h - margin)

        if cls_id == 0:
            canvas, bbox = draw_tabela(canvas, x, y, radius, persp)
        elif cls_id == 1:
            canvas, bbox = draw_stop(canvas, x, y, radius, persp)
        elif cls_id == 2:
            w = radius * 2
            h = int(w * 1.41)
            bx = random.randint(0, img_w - w)
            by = random.randint(0, img_h - h)
            canvas, bbox = draw_hedef(canvas, bx, by, w, h, persp)

        if cfg.get("blur") and random.random() > 0.55:
            canvas = cv2.GaussianBlur(canvas, (3,3), 0)

        write_label(lbl_path, cls_id, *bbox, img_w, img_h)
        cv2.imwrite(str(out_img / f"synth_{idx:05d}.jpg"), canvas, [cv2.IMWRITE_JPEG_QUALITY, 92])

        if progress_cb:
            progress_cb(idx + 1, total)
        if log_cb and (idx + 1) % 50 == 0:
            log_cb(f"{idx+1}/{total} üretildi...")

    if log_cb:
        log_cb(f"✅ Tamamlandı! {total} görüntü → {out_img}")


# ─────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────

class SynthGUI:
    def __init__(self, root):
        self.root = root
        root.title("ODBARS — GUNCEL VERSION")
        root.resizable(False, False)
        root.configure(bg="#1a1a1a")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1a1a1a")
        style.configure("TLabel", background="#1a1a1a", foreground="#d4c5a0", font=("Helvetica", 11))
        style.configure("TLabelframe", background="#1a1a1a", foreground="#f59e0b", font=("Helvetica", 11, "bold"))
        style.configure("TLabelframe.Label", background="#1a1a1a", foreground="#f59e0b")
        style.configure("TButton", background="#2a241c", foreground="#d4c5a0", font=("Helvetica", 11, "bold"))
        style.configure("TScale", background="#1a1a1a")
        style.configure("TCombobox", fieldbackground="#2a241c", foreground="#d4c5a0")
        style.configure("Horizontal.TProgressbar", troughcolor="#2a241c", background="#f59e0b")

        self.notebook = ttk.Notebook(self.root)

        self.tab_2d = ttk.Frame(self.notebook)
        self.tab_3d = ttk.Frame(self.notebook)
        self.tab_view = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_2d, text="  🖼️  2D Sentetik  ")
        self.notebook.add(self.tab_3d, text="  🧊  Blender (3D)  ")
        self.notebook.add(self.tab_view, text="  🔍  Veri Kontrolü  ")

        self.blender_status = "idle" # idle, running, paused
        self.blender_queue = []
        self.blender_done_count = 0
        self.blender_total_count = 0

        self._build_2d_ui()
        self._build_3d_ui()
        self._build_viewer_ui(self.tab_view)
        self._build_status_ui()
        
        # En son notebook'u paketle ki alt panel ezilmesin
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def _build_status_ui(self):
        # Durum ve İlerleme Paneli (En altta sabit)
        f_stat = ttk.Frame(self.root, padding=5)
        f_stat.pack(side="bottom", fill="x")

        self.progress = ttk.Progressbar(f_stat, orient="horizontal", length=460,
                                        mode="determinate", style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=10, pady=5)

        self.log_text = tk.Text(f_stat, height=6, bg="#0f0f0f", fg="#a3b59a",
                                font=("Courier", 10), bd=0, relief="flat")
        self.log_text.pack(fill="x", padx=10, pady=5)

    def _build_2d_ui(self):
        pad = {"padx": 12, "pady": 6}
        parent = self.tab_2d

        # ── Klasör Seçimi ──
        f_dir = ttk.LabelFrame(parent, text=" 📁  Klasörler ", padding=8)
        f_dir.grid(row=0, column=0, columnspan=2, sticky="ew", **pad)

        self.bg_dir   = tk.StringVar(value="")
        self.out_dir  = tk.StringVar(value=str(Path(__file__).parent / "dataset"))

        self._lbl(f_dir, "Arka Plan Klasörü:", 0, 0)
        ttk.Entry(f_dir, textvariable=self.bg_dir, width=38, font=("Helvetica", 10)).grid(row=0, column=1, padx=4)
        ttk.Button(f_dir, text="Seç", command=lambda: self._pick_dir(self.bg_dir)).grid(row=0, column=2, padx=4)

        self._lbl(f_dir, "Çıkış Klasörü:", 0, 1)
        ttk.Entry(f_dir, textvariable=self.out_dir, width=38, font=("Helvetica", 10)).grid(row=1, column=1, padx=4)
        ttk.Button(f_dir, text="Seç", command=lambda: self._pick_dir(self.out_dir)).grid(row=1, column=2, padx=4)

        # ── Sınıf Sayıları ──
        f_cnt = ttk.LabelFrame(parent, text=" 🎯  Sınıf Başına Görüntü Sayısı ", padding=8)
        f_cnt.grid(row=1, column=0, sticky="nsew", **pad)

        self.n_tabela = tk.IntVar(value=150)
        self.n_stop   = tk.IntVar(value=100)
        self.n_hedef  = tk.IntVar(value=100)

        for row, (label, var) in enumerate([
            ("🔵  Tabela :", self.n_tabela),
            ("🔴  STOP   :", self.n_stop),
            ("🎯  Hedef  :", self.n_hedef),
        ]):
            self._lbl(f_cnt, label, 0, row)
            ttk.Spinbox(f_cnt, from_=10, to=2000, textvariable=var,
                        width=8, font=("Helvetica", 11)).grid(row=row, column=1, padx=8, pady=3)

        # ── Boyut ve Perspektif ──
        f_opt = ttk.LabelFrame(parent, text=" ⚙️  Boyut & Perspektif ", padding=8)
        f_opt.grid(row=1, column=1, sticky="nsew", **pad)

        self.r_min   = tk.IntVar(value=35)
        self.r_max   = tk.IntVar(value=120)
        self.persp   = tk.DoubleVar(value=0.15)
        self.img_w   = tk.IntVar(value=640)
        self.img_h   = tk.IntVar(value=640)
        self.do_blur = tk.BooleanVar(value=True)
        self.split   = tk.StringVar(value="train")

        for row, (label, var, lo, hi) in enumerate([
            ("Min. Yarıçap (px):", self.r_min, 20, 200),
            ("Max. Yarıçap (px):", self.r_max, 40, 300),
            ("Görüntü Genişliği:", self.img_w, 320, 1280),
            ("Görüntü Yüksekliği:", self.img_h, 320, 1280),
        ]):
            self._lbl(f_opt, label, 0, row)
            ttk.Spinbox(f_opt, from_=lo, to=hi, textvariable=var,
                        width=7, font=("Helvetica", 11)).grid(row=row, column=1, padx=8, pady=3)

        self._lbl(f_opt, "Perspektif Gücü:", 0, 4)
        pslider = ttk.Scale(f_opt, from_=0.0, to=0.40, variable=self.persp, orient="horizontal", length=130)
        pslider.grid(row=4, column=1, padx=8, pady=3)
        self.persp_lbl = ttk.Label(f_opt, text="0.15")
        self.persp_lbl.grid(row=4, column=2)
        self.persp.trace_add("write", lambda *_: self.persp_lbl.config(text=f"{self.persp.get():.2f}"))

        self._lbl(f_opt, "Bulanıklık:", 0, 5)
        ttk.Checkbutton(f_opt, variable=self.do_blur).grid(row=5, column=1, sticky="w", padx=8)

        self._lbl(f_opt, "Bölüm:", 0, 6)
        ttk.Combobox(f_opt, textvariable=self.split, values=["train","val","test"],
                     width=8, state="readonly").grid(row=6, column=1, padx=8, pady=3)

        # ── Üretimi Başlat ──
        f_btns = ttk.Frame(parent)
        f_btns.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(f_btns, text="🔍  Önizle (5 görüntü)", command=self._preview).grid(row=0, column=0, padx=10)
        ttk.Button(f_btns, text="▶  Üretimi Başlat",      command=self._start_2d).grid(row=0, column=1, padx=10)

    def _build_3d_ui(self):
        parent = self.tab_3d
        pad = {"padx": 12, "pady": 6}

        f_top = ttk.Frame(parent, padding=5)
        f_top.pack(fill="x")

        self.blender_terrain_dir = tk.StringVar(value="")
        self.blender_output_dir  = tk.StringVar(value=str(Path(__file__).parent / "dataset_blender"))
        self.blender_path = tk.StringVar(value="/Applications/Blender.app/Contents/MacOS/Blender")

        ttk.Label(f_top, text="Terrain Klasörü:").grid(row=0, column=0, sticky="w")
        ttk.Entry(f_top, textvariable=self.blender_terrain_dir, width=35).grid(row=0, column=1, padx=5)
        ttk.Button(f_top, text="Seç", command=self._pick_blender_terrain).grid(row=0, column=2)

        ttk.Label(f_top, text="Çıkış Klasörü:").grid(row=1, column=0, sticky="w")
        ttk.Entry(f_top, textvariable=self.blender_output_dir, width=35).grid(row=1, column=1, padx=5)
        ttk.Button(f_top, text="Seç", command=lambda: self._pick_dir(self.blender_output_dir)).grid(row=1, column=2)

        # Terrain Listesi
        lbl_f = ttk.LabelFrame(parent, text=" 🏔️  Zemin Seçimi ve Sayı Ayarı ", padding=8)
        lbl_f.pack(fill="both", expand=True, padx=10, pady=5)

        self.terrain_canvas = tk.Canvas(lbl_f, bg="#1a1a1a", highlightthickness=0)
        self.terrain_scroll = ttk.Scrollbar(lbl_f, orient="vertical", command=self.terrain_canvas.yview)
        self.terrain_list_frame = ttk.Frame(self.terrain_canvas)

        self.terrain_canvas.create_window((0, 0), window=self.terrain_list_frame, anchor="nw")
        self.terrain_canvas.configure(yscrollcommand=self.terrain_scroll.set)

        self.terrain_canvas.pack(side="left", fill="both", expand=True)
        self.terrain_scroll.pack(side="right", fill="y")

        self.terrain_vars = {} # {filename: (bool_var, count_var)}

        self.f_blender_controls = ttk.Frame(parent, padding=10)
        self.f_blender_controls.pack(fill="x")
        
        self.btn_blender_start = ttk.Button(self.f_blender_controls, text="🧊  Başlat", command=self._start_blender)
        self.btn_blender_start.pack(side="left", padx=5)
        
        self.btn_blender_stop = ttk.Button(self.f_blender_controls, text="⏹  Durdur", command=self._stop_blender, state="disabled")
        self.btn_blender_stop.pack(side="left", padx=5)
        
        self.blender_use_steps = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.f_blender_controls, text="Mesafe Adımları", variable=self.blender_use_steps).pack(side="left", padx=5)
        
        self.blender_dist_min = tk.DoubleVar(value=2.0)
        self.blender_dist_max = tk.DoubleVar(value=8.0)
        ttk.Label(self.f_blender_controls, text="Mesafe (m):").pack(side="left", padx=(10,2))
        ttk.Entry(self.f_blender_controls, textvariable=self.blender_dist_min, width=4).pack(side="left")
        ttk.Label(self.f_blender_controls, text="-").pack(side="left")
        ttk.Entry(self.f_blender_controls, textvariable=self.blender_dist_max, width=4).pack(side="left")
        
        ttk.Button(self.f_blender_controls, text="🔄  Listeyi Yenile", command=self._refresh_terrain_list).pack(side="right")

    def _build_viewer_ui(self, parent):
        self.view_img_dir = tk.StringVar()
        self.view_lbl_dir = tk.StringVar()

        # Üst Panel: Klasör Seçimi
        f_top = ttk.Frame(parent, padding=10)
        f_top.pack(fill="x")
        
        ttk.Label(f_top, text="Images:").grid(row=0, column=0)
        ttk.Entry(f_top, textvariable=self.view_img_dir, width=30).grid(row=0, column=1)
        ttk.Button(f_top, text="Seç", command=lambda: self._pick_dir(self.view_img_dir)).grid(row=0, column=2)

        ttk.Label(f_top, text="Labels:").grid(row=0, column=3)
        ttk.Entry(f_top, textvariable=self.view_lbl_dir, width=30).grid(row=0, column=4)
        ttk.Button(f_top, text="Seç", command=lambda: self._pick_dir(self.view_lbl_dir)).grid(row=0, column=5)
        
        ttk.Button(f_top, text="🔄 Yükle", command=self._load_viewer_data).grid(row=0, column=6, padx=10)

        # Ana İçerik Alanı
        f_main = ttk.Frame(parent, padding=5)
        f_main.pack(fill="both", expand=True)
        
        f_main.columnconfigure(1, weight=3)
        f_main.columnconfigure(2, weight=1)
        f_main.rowconfigure(0, weight=1)

        # 1. SOL: Liste
        f_list = ttk.Frame(f_main, padding=5)
        f_list.grid(row=0, column=0, sticky="nsw")

        ttk.Label(f_list, text="Dosya Listesi").pack(pady=2)
        self.view_list = tk.Listbox(f_list, width=25, height=25, bg="#1a1a1a", fg="#d4c5a0", selectbackground="#f59e0b")
        self.view_list.pack(fill="both", expand=True)
        self.view_list.bind("<<ListboxSelect>>", self._on_view_select)
        self.view_list.bind("<Double-1>", self._on_view_select) # Çift tıklama desteği
        
        ttk.Button(f_list, text="👁️ Seçiliyi Görüntüle", command=lambda: self._on_view_select(None)).pack(fill="x", pady=5)

        # 2. ORTA: Görsel Alanı
        self.f_view_imgs = ttk.Frame(f_main, padding=5)
        self.f_view_imgs.grid(row=0, column=1, sticky="nsew")
        self.f_view_imgs.columnconfigure(0, weight=1)
        self.f_view_imgs.columnconfigure(1, weight=1)

        ttk.Label(self.f_view_imgs, text="Orijinal Görüntü").grid(row=0, column=0, pady=2)
        self.canvas_raw = tk.Label(self.f_view_imgs, bg="#000", width=400, height=400)
        self.canvas_raw.grid(row=1, column=0, padx=2, pady=2)

        ttk.Label(self.f_view_imgs, text="Etiketli (BBox)").grid(row=0, column=1, pady=2)
        self.canvas_bbox = tk.Label(self.f_view_imgs, bg="#000", width=400, height=400)
        self.canvas_bbox.grid(row=1, column=1, padx=2, pady=2)

        # 3. SAĞ: Metin Alanı
        f_text = ttk.Frame(f_main, padding=5)
        f_text.grid(row=0, column=2, sticky="nsew")
        ttk.Label(f_text, text="Etiket İçeriği").pack(pady=2)
        self.txt_view_label = tk.Text(f_text, width=20, bg="#0f0f0f", fg="#f59e0b", font=("Courier", 11))
        self.txt_view_label.pack(fill="both", expand=True)


    def _load_viewer_data(self):
        # Yolları temizle (tırnak ve boşlukları at)
        raw_idat = self.view_img_dir.get().strip().strip("'").strip('"')
        raw_ldat = self.view_lbl_dir.get().strip().strip("'").strip('"')
        
        idat = Path(raw_idat)
        ldat = Path(raw_ldat)
        
        print(f"DEBUG: Loading from {idat}", flush=True)
        
        if not idat.is_dir():
            messagebox.showerror("Hata", f"Görsel klasörü bulunamadı:\n{idat}")
            return
        
        self.view_list.delete(0, "end")
        
        # Tüm varyasyonları tara
        exts = ["*.jpg", "*.JPG", "*.jpeg", "*.PNG", "*.png"]
        files = []
        for e in exts:
            files.extend(list(idat.glob(e)))
        
        self.viewer_files = sorted(list(set([f.stem for f in files])))
        print(f"FOUND: {len(self.viewer_files)} files.", flush=True)
        
        for f in self.viewer_files:
            self.view_list.insert("end", f)
        
        if not self.viewer_files:
            self._log(f"⚠️ {idat.name} klasöründe resim bulunamadı!", "yellow")
            print(f"DEBUG: No files found in {idat}")
        
        # Hata kontrolü
        missing_lbl = [f for f in self.viewer_files if not (ldat / f"{f}.txt").exists()]
        missing_img = [f.stem for f in ldat.glob("*.txt") if not (idat / f"{f.stem}.jpg").exists()]

        if missing_lbl:
            self._log(f"❌ HATA: {len(missing_lbl)} görselin etiketi eksik!", color="red")
        if missing_img:
            self._log(f"❌ HATA: {len(missing_img)} etiketin görseli eksik!", color="red")
        
        if self.viewer_files and not missing_lbl and not missing_img:
            self._log("✅ Tüm dosyalar eşleşiyor.", color="green")

        if missing_lbl:
            self._log(f"❌ HATA: {len(missing_lbl)} görselin etiketi eksik!", color="red")
        if missing_img:
            self._log(f"❌ HATA: {len(missing_img)} etiketin görseli eksik!", color="red")
        
        if not missing_lbl and not missing_img:
            self._log("✅ Tüm dosyalar eşleşiyor.", color="green")

    def _on_view_select(self, event):
        print("\n--- EVENT TRIGGERED ---", flush=True)
        idx = self.view_list.curselection()
        if not idx: return
        fname = self.viewer_files[idx[0]]
        
        img_dir = Path(self.view_img_dir.get().strip().strip("'").strip('"'))
        lbl_dir = Path(self.view_lbl_dir.get().strip().strip("'").strip('"'))
        
        # Olası tüm uzantıları dene
        img_p = None
        for ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]:
            p = img_dir / f"{fname}{ext}"
            if p.exists():
                img_p = p
                break
        
        if not img_p:
            print(f"❌ Dosya bulunamadı: {fname}", flush=True)
            return

        lbl_p = lbl_dir / f"{fname}.txt"
        print(f"✅ Yükleniyor: {img_p.name}", flush=True)

        print(f"\n--- Görüntüleniyor: {fname} ---")

        if not img_p.exists():
            self._log(f"Dosya bulunamadı: {fname}", "red")
            return

        try:
            # 1. Orijinal Görüntü
            pil_img = Image.open(str(img_p)).convert("RGB")
            orig_w, orig_h = pil_img.size
            
            ratio = min(450 / orig_w, 450 / orig_h)
            new_size = (int(orig_w * ratio), int(orig_h * ratio))
            
            pil_disp = pil_img.resize(new_size, Image.Resampling.LANCZOS)
            tk_img_raw = ImageTk.PhotoImage(pil_disp)
            
            self.canvas_raw.config(image=tk_img_raw)
            self.canvas_raw.image = tk_img_raw
            print("✅ Orijinal görüntülendi.")

            # 2. Bbox Çizimi
            pil_bbox = pil_img.copy()
            draw = ImageDraw.Draw(pil_bbox)
            lbl_content = ""

            if lbl_p.exists():
                with open(lbl_p, "r") as f:
                    lbl_content = f.read()
                    f.seek(0)
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) == 5:
                            cid, cx, cy, bw, bh = map(float, parts)
                            x1 = (cx - bw/2) * orig_w
                            y1 = (cy - bh/2) * orig_h
                            x2 = (cx + bw/2) * orig_w
                            y2 = (cy + bh/2) * orig_h
                            class_names = ["Tabela", "STOP", "Hedef"]
                            cname = class_names[int(cid)] if int(cid) < len(class_names) else f"ID {int(cid)}"
                            
                            draw.rectangle([x1, y1, x2, y2], outline="red", width=5)
                            draw.text((x1, y1-20), cname, fill="red")

            pil_disp_bbox = pil_bbox.resize(new_size, Image.Resampling.LANCZOS)
            tk_img_bbox = ImageTk.PhotoImage(pil_disp_bbox)
            
            self.canvas_bbox.config(image=tk_img_bbox)
            self.canvas_bbox.image = tk_img_bbox
            
            self.txt_view_label.delete("1.0", "end")
            self.txt_view_label.insert("end", lbl_content)
            
            self.root.update_idletasks()
            
        except Exception as e:
            print(f"❌ HATA: {str(e)}")
            self._log(f"Yükleme hatası: {str(e)}", "red")

    def _stop_blender(self):
        self.blender_status = "stopping"
        self._log("⏹ Durduruluyor... (Mevcut render bitince duracak)")

    def _start_blender(self):
        if self.blender_status == "running": return
        
        td = self.blender_terrain_dir.get()
        od = self.blender_output_dir.get()
        if not td: return messagebox.showerror("Hata", "Terrain klasörü seçilmedi.")

        if self.blender_status != "paused":
            selected = [(name, var[1].get()) for name, var in self.terrain_vars.items() if var[0].get()]
            if not selected: return messagebox.showwarning("Uyarı", "Hiç zemin seçilmedi.")
            self.blender_queue = selected
            self.blender_done_count = 0
            self.blender_total_count = sum(n for _, n in selected)
            self.progress["maximum"] = self.blender_total_count
        
        self.blender_status = "running"
        self.btn_blender_start.config(text="🧊  Devam Et", state="disabled")
        self.btn_blender_stop.config(state="normal")
        self._log(f"🧊 Blender Render Başlıyor...")

        def run():
            cfg_path = Path(od) / "temp_gui_config.json"
            cfg_path.parent.mkdir(parents=True, exist_ok=True)

            while self.blender_queue and self.blender_status == "running":
                fname, n = self.blender_queue.pop(0)
                temp_cfg = {
                    "n_renders": n, "output_dir": od, "terrain_dir": td,
                    "render_w": 1920, "render_h": 1080, "file_prefix": fname.split(".")[0],
                    "use_distance_steps": self.blender_use_steps.get(),
                    "camera_distance_range": (self.blender_dist_min.get(), self.blender_dist_max.get())
                }
                
                import tempfile, shutil
                with tempfile.TemporaryDirectory() as tmp_td:
                    shutil.copy(Path(td)/fname, Path(tmp_td)/fname)
                    temp_cfg["terrain_dir"] = tmp_td
                    with open(cfg_path, 'w') as f: json.dump(temp_cfg, f)
                    
                    cmd = [self.blender_path.get(), "--background", "--python", 
                           str(Path(__file__).parent / "blender_render.py"), "--", str(cfg_path)]
                    
                    self.root.after(0, lambda f=fname: self._log(f"🚀 Render: {f}..."))
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    for line in process.stdout:
                        if "Saved:" in line:
                            self.blender_done_count += 1
                            pct = (self.blender_done_count / self.blender_total_count) * 100
                            self.root.after(0, lambda c=self.blender_done_count, p=pct: self._update_progress(c, p))
                    process.wait()

            if self.blender_status == "stopping":
                self.blender_status = "paused"
                self.root.after(0, lambda: self._log("⏸ Duraklatıldı."))
            elif not self.blender_queue:
                self.blender_status = "idle"
                self.root.after(0, lambda: self._log("✅ Blender üretimi TAMAMLANDI!"))
                self.root.after(0, self._show_blender_report)

            self.root.after(0, lambda: self.btn_blender_start.config(state="normal"))
            self.root.after(0, lambda: self.btn_blender_stop.config(state="disabled"))

        threading.Thread(target=run, daemon=True).start()

    def _update_progress(self, val, pct):
        self.progress["value"] = val
        # Progress bar üzerinde yazı göstermek Tkinter'da zordur, label'ı güncelleyelim
        self.root.title(f"ODBARS — %{int(pct)} Tamamlandı")

    def _show_blender_report(self):
        od = Path(self.blender_output_dir.get())
        imgs = list((od / "images" / "train").glob("*.jpg"))
        report = f"\n--- ÜRETİM RAPORU ---\n"
        report += f"Toplam Görsel: {len(imgs)}\n"
        report += f"Çıkış Dizini: {od}\n"
        report += "---------------------\n"
        self._log(report)
        messagebox.showinfo("Rapor", f"Üretim bitti. {len(imgs)} görsel hazır.")
        # Viewer dizinlerini otomatik ayarla
        self.view_img_dir.set(str(od / "images" / "train"))
        self.view_lbl_dir.set(str(od / "labels" / "train"))
        self._load_viewer_data()

    def _lbl(self, parent, text, col, row, **kw):
        ttk.Label(parent, text=text).grid(column=col, row=row, sticky="w", padx=8, pady=3, **kw)

    def _pick_dir(self, var):
        d = filedialog.askdirectory()
        if d: var.set(d)

    def _pick_blender_terrain(self):
        d = filedialog.askdirectory()
        if d:
            self.blender_terrain_dir.set(d)
            self._refresh_terrain_list()

    def _refresh_terrain_list(self):
        for child in self.terrain_list_frame.winfo_children():
            child.destroy()
        
        self.terrain_vars = {}
        td = Path(self.blender_terrain_dir.get())
        if not td.is_dir(): return

        files = sorted(list(td.glob("*.jpg")) + list(td.glob("*.png")) + list(td.glob("*.jpeg")))
        for i, f in enumerate(files):
            b_var = tk.BooleanVar(value=True)
            c_var = tk.IntVar(value=10)
            self.terrain_vars[f.name] = (b_var, c_var)

            f_row = ttk.Frame(self.terrain_list_frame)
            f_row.pack(fill="x", pady=2)
            ttk.Checkbutton(f_row, variable=b_var).pack(side="left")
            ttk.Label(f_row, text=f.name, width=25).pack(side="left", padx=5)
            ttk.Label(f_row, text="Adet:").pack(side="left")
            ttk.Entry(f_row, textvariable=c_var, width=5).pack(side="left", padx=5)

        self.terrain_list_frame.update_idletasks()
        self.terrain_canvas.config(scrollregion=self.terrain_canvas.bbox("all"))

    def _log(self, msg, color=None):
        tags = {"red": "#ff4d4d", "green": "#4dff88", "yellow": "#ffff4d"}
        self.log_text.insert("end", msg + "\n")
        if color in tags:
            # Satır sonu indeksini bul
            end_idx = self.log_text.index("end-1c")
            start_idx = self.log_text.index(f"{end_idx} linestart")
            self.log_text.tag_add(color, start_idx, end_idx)
            self.log_text.tag_config(color, foreground=tags[color])
        self.log_text.see("end")

    def _get_cfg(self):
        return {
            "bg_dir":       self.bg_dir.get() or None,
            "out_dir":      self.out_dir.get(),
            "n_tabela":     self.n_tabela.get(),
            "n_stop":       self.n_stop.get(),
            "n_hedef":      self.n_hedef.get(),
            "radius_min":   self.r_min.get(),
            "radius_max":   self.r_max.get(),
            "persp_strength": self.persp.get(),
            "img_w":        self.img_w.get(),
            "img_h":        self.img_h.get(),
            "blur":         self.do_blur.get(),
            "split":        self.split.get(),
        }

    def _preview(self):
        cfg = self._get_cfg()
        cfg["n_tabela"] = 2
        cfg["n_stop"]   = 2
        cfg["n_hedef"]  = 1
        import tempfile
        cfg["out_dir"] = tempfile.mkdtemp()
        cfg["split"]   = "preview"
        self._log("Önizleme oluşturuluyor...")
        generate_dataset(cfg)
        img_dir = Path(cfg["out_dir"]) / "images" / "preview"
        imgs = sorted(img_dir.glob("*.jpg"))
        for p in imgs[:5]:
            img = cv2.imread(str(p))
            cv2.imshow(f"Önizleme: {p.name}", img)
        self._log("Önizleme pencerelerini kapatmak için bir tuşa basın veya pencereyi kapatın.")
        
        while True:
            # Pencerelerin hala açık olup olmadığını kontrol et
            active_windows = False
            for p in imgs[:5]:
                title = f"Önizleme: {p.name}"
                try:
                    if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) >= 1:
                        active_windows = True
                        break
                except: pass
            
            if not active_windows: break
            if cv2.waitKey(30) & 0xFF == ord('q'): break
            self.root.update()

        cv2.destroyAllWindows()

    def _start_2d(self):
        cfg = self._get_cfg()
        total = cfg["n_tabela"] + cfg["n_stop"] + cfg["n_hedef"]
        self.progress["maximum"] = total
        self.progress["value"] = 0
        self._log(f"2D Üretim başlatılıyor... Toplam: {total} görüntü")
        def run():
            def prog_cb(done, tot): self.root.after(0, lambda: self.progress.configure(value=done))
            generate_dataset(cfg, prog_cb, lambda m: self.root.after(0, lambda msg=m: self._log(msg)))
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app  = SynthGUI(root)
    root.mainloop()
