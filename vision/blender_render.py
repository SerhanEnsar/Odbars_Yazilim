"""
ODBARS Blender Dataset Renderer
================================
Blender Script Konsolu'ndan veya terminalden çalıştırın:
    blender --background --python blender_render.py

Yapılanlar:
  - Sahneyi sıfırlar
  - Zemin düzlemi oluşturur (isteğe bağlı arazi görseli)
  - Tabela, STOP, Hedef nesnelerini kodla üretir
  - Kamerayı ve ışığı rastgele konumlandırır
  - N adet render alır ve YOLO formatında label yazar
"""

import bpy
import bmesh
import mathutils
import math
import random
import os
import json
from pathlib import Path

# ─────────────────────────────────────────────
# AYARLAR — ihtiyaca göre değiştirin
# ─────────────────────────────────────────────
CONFIG = {
    "n_renders":      200,           # ← istediğin sayıyı gir
    "output_dir":     "/Users/serhanensar/Desktop/Renders",
    "terrain_dir":    "",            # ← PNG/JPG'lerin bulunduğu klasör yolu (boş = düz renk)
    "font_path":      "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "render_w":       1920,
    "render_h":       1080,
    "class_weights":  [0.4, 0.3, 0.3],
    "camera_distance_range": (1.5, 8.0),
    "camera_height_range":   (0.3, 2.5),
}

TABELA_TEXTS = ["SU GECISI", "TASLI YOL", "KAYAR ENGEL",
                "DIK EGIM", "YAN EGIM", "ATIS",
                "1", "2", "3", "4", "5", "6", "7"]

OUT = Path(CONFIG["output_dir"])
(OUT / "images" / "train").mkdir(parents=True, exist_ok=True)
(OUT / "labels" / "train").mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# Yardımcı: sahneyi temizle
# ─────────────────────────────────────────────
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in list(bpy.data.meshes) + list(bpy.data.materials) + list(bpy.data.curves):
        bpy.data.batch_remove(ids=[block]) if hasattr(bpy.data, 'batch_remove') else None


def purge():
    for attr in ['meshes', 'materials', 'curves', 'lights', 'cameras']:
        col = getattr(bpy.data, attr)
        for item in list(col):
            try:
                col.remove(item)
            except Exception:
                pass


# ─────────────────────────────────────────────
# Materyal oluşturucu (basit renk)
# ─────────────────────────────────────────────
def make_material(name, color_rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color_rgba
        bsdf.inputs["Roughness"].default_value = 0.7
    return mat


def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


# ─────────────────────────────────────────────
# Zemin düzlemi
# ─────────────────────────────────────────────
def _pick_terrain():
    """terrain_dir klasöründen rastgele bir PNG/JPG seçer."""
    td = CONFIG.get("terrain_dir", "")
    if not td:
        return None
    td_path = Path(td)
    if not td_path.is_dir():
        return None
    images = (list(td_path.glob("*.jpg")) + list(td_path.glob("*.png"))
              + list(td_path.glob("*.jpeg")))
    return str(random.choice(images)) if images else None


def create_ground():
    """Zemin düzlemi. terrain_dir klasöründen her seferinde rastgele doku seçer."""
    terrain_path = _pick_terrain()
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"

    mat = bpy.data.materials.new("GroundMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    if terrain_path:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(terrain_path)
        coord = nodes.new("ShaderNodeTexCoord")
        links.new(coord.outputs["UV"], tex_node.inputs["Vector"])
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        print(f"  Terrain: {Path(terrain_path).name}")
    else:
        bsdf.inputs["Base Color"].default_value = (0.35, 0.30, 0.22, 1.0)
        bsdf.inputs["Roughness"].default_value = 1.0

    assign_material(ground, mat)
    return ground


# ─────────────────────────────────────────────
# TABELA (class 0)
# ─────────────────────────────────────────────
def create_tabela(text_str, border_color=(0.9, 0.9, 0.9, 1.0), label_class=0):
    objs = []

    # Disk (60cm çap = 0.3m yarıçap)
    bpy.ops.mesh.primitive_circle_add(vertices=64, radius=0.30, fill_type='NGON', location=(0, 0, 0))
    disk = bpy.context.active_object
    disk.name = f"Sign_Disk_{label_class}"
    assign_material(disk, make_material(f"DiskMat_{label_class}", (0.02, 0.02, 0.02, 1.0)))
    objs.append(disk)

    # Dış kenarlık halkası
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0.001),
        major_radius=0.30,
        minor_radius=0.025,
        major_segments=64,
        minor_segments=12,
    )
    ring = bpy.context.active_object
    ring.name = f"Sign_Ring_{label_class}"
    assign_material(ring, make_material(f"RingMat_{label_class}", border_color))
    objs.append(ring)

    # İç ince halka
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0.001),
        major_radius=0.25,
        minor_radius=0.008,
        major_segments=64,
        minor_segments=8,
    )
    inner = bpy.context.active_object
    inner.name = f"Sign_InnerRing_{label_class}"
    assign_material(inner, make_material(f"InnerRingMat_{label_class}", border_color))
    objs.append(inner)

    # Metin
    bpy.ops.object.text_add(location=(0, 0, 0.002))
    txt_obj = bpy.context.active_object
    txt_obj.name = f"Sign_Text_{label_class}"
    txt_obj.data.body = text_str
    txt_obj.data.align_x = 'CENTER'
    txt_obj.data.align_y = 'CENTER'
    txt_obj.data.size = 0.06  # yazı boyutu (metre)
    txt_obj.data.extrude = 0.002

    # Font yükle
    font_path = CONFIG["font_path"]
    if Path(font_path).exists():
        font = bpy.data.fonts.load(font_path)
        txt_obj.data.font = font

    txt_mat = make_material(f"TextMat_{label_class}", (0.92, 0.92, 0.92, 1.0))
    if txt_obj.data.materials:
        txt_obj.data.materials[0] = txt_mat
    else:
        txt_obj.data.materials.append(txt_mat)
    objs.append(txt_obj)

    # Hepsini parent'la → Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = f"Sign_Parent_{label_class}"
    for o in objs:
        o.parent = parent

    return parent


def create_stop():
    return create_tabela("STOP", border_color=(0.85, 0.08, 0.08, 1.0), label_class=1)


# ─────────────────────────────────────────────
# HEdef (class 2) — A3 levha + halka dokusu
# ─────────────────────────────────────────────
def create_hedef():
    # A3: 297x420mm → 0.297 x 0.42m
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = "Hedef_Board"
    plane.scale = (0.297, 0.42, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Beyaz zemin
    mat = bpy.data.materials.new("HedefMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)

    # Eşmerkezli halka dokusu — Gradient + ColorRamp ile
    tex_coord = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    gradient = nodes.new("ShaderNodeTexGradient")
    gradient.gradient_type = 'RADIAL'
    color_ramp = nodes.new("ShaderNodeValToRGB")

    # Halka renkleri: siyah-beyaz-mavi-beyaz-mavi
    cr = color_ramp.color_ramp
    cr.elements[0].position = 0.0;  cr.elements[0].color = (0.05, 0.05, 0.05, 1)
    cr.elements[1].position = 1.0;  cr.elements[1].color = (1.0, 1.0, 1.0, 1)
    for pos, col in [(0.2, (0.0, 0.0, 0.8, 1)), (0.38, (1,1,1,1)),
                     (0.56, (0.0,0.0,0.8,1)), (0.74, (1,1,1,1))]:
        el = cr.elements.new(pos)
        el.color = col

    links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], gradient.inputs["Vector"])
    links.new(gradient.outputs["Color"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])

    assign_material(plane, mat)

    # Çerçeve
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, -0.001))
    frame = bpy.context.active_object
    frame.name = "Hedef_Frame"
    frame.scale = (0.31, 0.44, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(frame, make_material("FrameMat", (0.05, 0.05, 0.05, 1.0)))

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    parent = bpy.context.active_object
    parent.name = "Hedef_Parent"
    plane.parent = parent
    frame.parent = parent
    return parent


# ─────────────────────────────────────────────
# Kamera + Işık
# ─────────────────────────────────────────────
def setup_camera():
    bpy.ops.object.camera_add(location=(0, -3, 1.5))
    cam = bpy.context.active_object
    cam.name = "RenderCam"
    bpy.context.scene.camera = cam
    cam.data.lens = 35  # mm
    return cam


def setup_lights():
    # Ana ışık (güneş)
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    sun.data.energy = random.uniform(2.0, 6.0)
    sun.rotation_euler = (
        math.radians(random.uniform(30, 70)),
        math.radians(random.uniform(-30, 30)),
        math.radians(random.uniform(0, 360)),
    )
    # Dolgu ışığı
    bpy.ops.object.light_add(type='AREA', location=(-3, 3, 4))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = random.uniform(100, 400)
    return sun, fill


# ─────────────────────────────────────────────
# 3D → 2D projeksiyon (YOLO bbox için)
# ─────────────────────────────────────────────
def get_2d_bbox(obj, cam, render_w, render_h):
    """
    Nesnenin 3D bounding box köşelerini 2D'ye projekte eder.
    Normalize edilmiş YOLO koordinatları döner: (cx, cy, w, h)
    """
    scene = bpy.context.scene
    mat = cam.matrix_world.normalized().inverted()
    cam_data = cam.data

    def project(co_world):
        co_cam = mat @ co_world
        # Kamera koordinat sistemi: z negatif ileriye bakar
        if co_cam.z >= 0:
            return None
        fov_x = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
        fov_y = 2 * math.atan(cam_data.sensor_height / (2 * cam_data.lens))
        # Normalize [-1, 1]
        nx = -co_cam.x / (-co_cam.z * math.tan(fov_x / 2))
        ny =  co_cam.y / (-co_cam.z * math.tan(fov_y / 2))
        # Pixel
        px = (nx + 1) / 2 * render_w
        py = (1 - (ny + 1) / 2) * render_h
        return (px, py)

    corners = [mathutils.Vector(c) for c in obj.bound_box]
    world_corners = [obj.matrix_world @ c for c in corners]

    points_2d = [project(c) for c in world_corners]
    points_2d = [p for p in points_2d if p is not None]
    if not points_2d:
        return None

    xs = [p[0] for p in points_2d]
    ys = [p[1] for p in points_2d]
    x1, x2 = max(0, min(xs)), min(render_w, max(xs))
    y1, y2 = max(0, min(ys)), min(render_h, max(ys))

    if x2 <= x1 or y2 <= y1:
        return None

    cx = ((x1 + x2) / 2) / render_w
    cy = ((y1 + y2) / 2) / render_h
    bw = (x2 - x1) / render_w
    bh = (y2 - y1) / render_h
    return (cx, cy, bw, bh)


# ─────────────────────────────────────────────
# Kamerayı rastgele konumlandır, nesneye baktır
# ─────────────────────────────────────────────
def aim_camera_at(cam, target_loc):
    d_min, d_max = CONFIG["camera_distance_range"]
    h_min, h_max = CONFIG["camera_height_range"]
    dist = random.uniform(d_min, d_max)
    angle = random.uniform(0, 2 * math.pi)
    height = random.uniform(h_min, h_max)

    cam.location = mathutils.Vector((
        target_loc.x + dist * math.cos(angle),
        target_loc.y + dist * math.sin(angle),
        target_loc.z + height,
    ))
    # Nesneye baktır
    direction = target_loc - cam.location
    rot = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot.to_euler()


# ─────────────────────────────────────────────
# Render ayarları
# ─────────────────────────────────────────────
def setup_render(w, h):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 64          # hız/kalite dengesi (128 daha iyi ama yavaş)
    sc.cycles.use_denoising = True
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 92


# ─────────────────────────────────────────────
# ANA DÖNGÜ
# ─────────────────────────────────────────────
def main():
    random.seed(42)
    setup_render(CONFIG["render_w"], CONFIG["render_h"])

    # Sınıf → üretici fonksiyon
    creators = {
        0: lambda: create_tabela(random.choice(TABELA_TEXTS)),
        1: lambda: create_stop(),
        2: lambda: create_hedef(),
    }
    weights = CONFIG["class_weights"]
    n = CONFIG["n_renders"]
    img_w = CONFIG["render_w"]
    img_h = CONFIG["render_h"]
    out_imgs = OUT / "images" / "train"
    out_lbls = OUT / "labels" / "train"

    for i in range(n):
        print(f"[{i+1}/{n}] Render alınıyor...")

        # Sahneyi sıfırla
        purge()
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Zemin
        create_ground(CONFIG["terrain_image"])

        # Sınıf seç (1–3 nesne arası)
        n_objects = random.randint(1, 3)
        class_ids = random.choices([0, 1, 2], weights=weights, k=n_objects)

        # Kamera ve ışık kur
        cam = setup_camera()
        setup_lights()

        created_pairs = []  # (class_id, obj)
        for cls_id in class_ids:
            obj = creators[cls_id]()
            # Tabela / hedef sahneye dik durur (X ekseninde 90° döndür)
            obj.rotation_euler.x = math.radians(90)
            # Rastgele konum (zemin düzlemi üzerinde dikey)
            ox = random.uniform(-4, 4)
            oy = random.uniform(-4, 4)
            oz = random.uniform(0.4, 1.6)   # yerden yükseklik
            obj.location = mathutils.Vector((ox, oy, oz))
            created_pairs.append((cls_id, obj))

        # Kamerayı ilk nesneye yönelt (ya da rastgele bir noktaya)
        target = created_pairs[0][1].location if created_pairs else mathutils.Vector((0,0,1))
        aim_camera_at(cam, target)

        # Render
        img_path = str(out_imgs / f"render_{i:05d}.jpg")
        bpy.context.scene.render.filepath = img_path
        bpy.ops.render.render(write_still=True)

        # YOLO label yaz
        lbl_path = out_lbls / f"render_{i:05d}.txt"
        with open(lbl_path, 'w') as f:
            for cls_id, obj in created_pairs:
                bbox = get_2d_bbox(obj, cam, img_w, img_h)
                if bbox:
                    cx, cy, bw, bh = bbox
                    f.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

    print(f"\n✅ {n} render tamamlandı → {OUT}")


if __name__ == "__main__":
    main()
