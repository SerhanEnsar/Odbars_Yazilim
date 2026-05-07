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
    "n_renders":      5,           # ← istediğin sayıyı gir
    "output_dir":     "/Users/serhanensar/Desktop/Renders",
    "terrain_dir":    "/Users/serhanensar/Desktop/Terrains",            # ← PNG/JPG'lerin bulunduğu klasör yolu (boş = düz renk)
    "font_path":      "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "render_w":       1920,
    "render_h":       1080,
    "class_weights":  [0.4, 0.3, 0.3],
    "camera_distance_range": (1.5, 8.0),
    "camera_height_range":   (0.2, 0.5),    # Araç kamerası yüksekliği (metre)
}

# Şartname: tabelada sadece görev numarası yazıyor
TABELA_TEXTS = ["1", "2", "3", "4", "5", "6", "7"]

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
    """Zemin düzlemi. Subdivide edilir ve doku kullanılarak 3D displacement uygulanır."""
    terrain_path = _pick_terrain()
    
    # 1. Mesh oluştur ve subdivide et (3D derinlik için)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Ground"
    
    # Edit moduna geçip bölüyoruz
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=60) # 60x60 = 3600 yüzey (hız için makul)
    bpy.ops.object.mode_set(mode='OBJECT')

    mat = bpy.data.materials.new("GroundMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    if terrain_path:
        img = bpy.data.images.load(terrain_path)
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = img
        
        # Base Color
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        
        # 2. Displacement Uygula (Gerçek 3D kabartma)
        # Modifier kullanarak yapmak daha kontrollü
        tex = bpy.data.textures.new("GroundTex", type='IMAGE')
        tex.image = img
        
        disp_mod = ground.modifiers.new(name="Displace", type='DISPLACE')
        disp_mod.texture = tex
        disp_mod.strength = 0.4 # Kabarıklık şiddeti
        disp_mod.mid_level = 0.5
        
        # Yumuşatma
        bpy.ops.object.modifier_add(type='SUBSURF')
        ground.modifiers["Subdivision"].levels = 1
        bpy.ops.object.shade_smooth()
        
        print(f"  3D Terrain: {Path(terrain_path).name}")
    else:
        bsdf.inputs["Base Color"].default_value = (0.35, 0.30, 0.22, 1.0)
        bsdf.inputs["Roughness"].default_value = 1.0

    assign_material(ground, mat)
    return ground


# ─────────────────────────────────────────────
# TABELA (class 0)
# ─────────────────────────────────────────────
def create_tabela(text_str, border_color=(0.9, 0.9, 0.9, 1.0), label_class=0):
    """Şartnameye uygun tabela: dikey metal direk + karşıya bakan disk."""
    objs = []

    # 1. Direk (Sign Post) - Z ekseninde dikey
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=1.5, location=(0, 0, 0.75))
    post = bpy.context.active_object
    post.name = f"Sign_Post_{label_class}"
    post_mat = make_material(f"PostMat_{label_class}", (0.5, 0.5, 0.5, 1.0))
    post_mat.node_tree.nodes.get("Principled BSDF").inputs["Metallic"].default_value = 1.0
    post_mat.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.3
    assign_material(post, post_mat)
    objs.append(post)

    # Tabela yüksekliği (z=1.2m civarı)
    tz = 1.2

    # 2. Disk - X ekseninde 90 derece dönük (karşıya bakıyor)
    bpy.ops.mesh.primitive_circle_add(vertices=64, radius=0.30, fill_type='NGON', 
                                     location=(0, -0.02, tz), rotation=(math.radians(90), 0, 0))
    disk = bpy.context.active_object
    disk.name = f"Sign_Disk_{label_class}"
    disk_mat = make_material(f"DiskMat_{label_class}", (0.01, 0.01, 0.01, 1.0))
    disk_mat.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = 0.5
    assign_material(disk, disk_mat)
    objs.append(disk)

    # 3. Dış kenarlık halkası (Torus) - disk ile aynı rotasyon
    bpy.ops.mesh.primitive_torus_add(
        location=(0, -0.025, tz),
        rotation=(math.radians(90), 0, 0),
        major_radius=0.30,
        minor_radius=0.02,
        major_segments=64,
        minor_segments=12,
    )
    ring = bpy.context.active_object
    ring.name = f"Sign_Ring_{label_class}"
    assign_material(ring, make_material(f"RingMat_{label_class}", border_color))
    objs.append(ring)

    # 4. Metin (Görev Numarası) - önde
    bpy.ops.object.text_add(location=(0, -0.03, tz), rotation=(math.radians(90), 0, 0))
    txt_obj = bpy.context.active_object
    txt_obj.name = f"Sign_Text_{label_class}"
    txt_obj.data.body = text_str
    txt_obj.data.align_x = 'CENTER'
    txt_obj.data.align_y = 'CENTER'
    txt_obj.data.size = 0.20
    txt_obj.data.extrude = 0.01

    font_path = CONFIG["font_path"]
    if Path(font_path).exists():
        txt_obj.data.font = bpy.data.fonts.load(font_path)

    txt_mat = make_material(f"TextMat_{label_class}", (0.95, 0.95, 0.95, 1.0))
    assign_material(txt_obj, txt_mat)
    objs.append(txt_obj)

    # 5. Parent & Empty
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
    """A3 levha + metal direk + hedef dokusu."""
    objs = []
    
    # 1. Direk
    bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=1.5, location=(0, 0, 0.75))
    post = bpy.context.active_object
    post.name = "Hedef_Post"
    assign_material(post, make_material("PostMat_Hedef", (0.5, 0.5, 0.5, 1.0)))
    post.data.materials[0].node_tree.nodes.get("Principled BSDF").inputs["Metallic"].default_value = 1.0
    objs.append(post)

    hz = 1.0 # Hedef merkezi yüksekliği

    # 2. A3 Levha - Karşıya bakan (X rotasyon 90)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.02, hz), rotation=(math.radians(90), 0, 0))
    plane = bpy.context.active_object
    plane.name = "Hedef_Board"
    plane.scale = (0.297, 0.42, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Materyal & Doku
    mat = bpy.data.materials.new("HedefMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1.0)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    mapping = nodes.new("ShaderNodeMapping")
    # UV düzeltme: hedef dokusunu ortalamak için mapping ayarı gerekebilir
    gradient = nodes.new("ShaderNodeTexGradient")
    gradient.gradient_type = 'RADIAL'
    color_ramp = nodes.new("ShaderNodeValToRGB")

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
    objs.append(plane)

    # 3. Çerçeve (Backing)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.015, hz), rotation=(math.radians(90), 0, 0))
    frame = bpy.context.active_object
    frame.name = "Hedef_Frame"
    frame.scale = (0.31, 0.44, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    assign_material(frame, make_material("FrameMat", (0.05, 0.05, 0.05, 1.0)))
    objs.append(frame)

    # Parent & Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = "Hedef_Parent"
    for o in objs:
        o.parent = parent
        
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
def get_2d_bbox(parent_obj, cam, render_w, render_h):
    """
    Empty (parent) nesnenin içindeki tüm mesh çocuklarını bulur 
    ve hepsini kapsayan bir 2D bounding box hesaplar.
    """
    scene = bpy.context.scene
    mat = cam.matrix_world.normalized().inverted()
    cam_data = cam.data

    def project(co_world):
        co_cam = mat @ co_world
        if co_cam.z >= 0: return None
        fov_x = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
        fov_y = 2 * math.atan(cam_data.sensor_height / (2 * cam_data.lens))
        nx = -co_cam.x / (-co_cam.z * math.tan(fov_x / 2))
        ny =  co_cam.y / (-co_cam.z * math.tan(fov_y / 2))
        px = (nx + 1) / 2 * render_w
        py = (1 - (ny + 1) / 2) * render_h
        return (px, py)

    all_points = []
    
    # Parent ve tüm alt nesnelerin (direk, disk, metin) köşelerini topla
    # Sadece mesh olanları veya text olanları al
    to_check = [parent_obj] + list(parent_obj.children_recursive)
    
    for obj in to_check:
        if obj.type in ['MESH', 'CURVE', 'FONT']:
            # bound_box yerel koordinattadır, dünya koordinatına çevir
            corners = [obj.matrix_world @ mathutils.Vector(c) for c in obj.bound_box]
            for c in corners:
                p = project(c)
                if p: all_points.append(p)

    if not all_points:
        return None

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    
    x1, x2 = max(0, min(xs)), min(render_w, max(xs))
    y1, y2 = max(0, min(ys)), min(render_h, max(ys))

    if (x2 - x1) < 1 or (y2 - y1) < 1: return None

    cx = ((x1 + x2) / 2) / render_w
    cy = ((y1 + y2) / 2) / render_h
    bw = (x2 - x1) / render_w
    bh = (y2 - y1) / render_h
    
    return (cx, cy, bw, bh)


# ─────────────────────────────────────────────
# Kamerayı rastgele konumlandır, nesneye baktır
# ─────────────────────────────────────────────
def aim_camera_at(cam, target_loc):
    """
    Araç kamerası perspektifi:
    - Kamera zemine yakın (20-50cm), sabit öne bakan açıda
    - Nesne kameranın önünde, parkur kenarında dikey duruyor
    - Uzaklık 2-8m arası rastgele
    """
    d_min, d_max = CONFIG["camera_distance_range"]
    h_min, h_max = CONFIG["camera_height_range"]

    dist   = random.uniform(d_min, d_max)
    # Yalnızca kameranın önünden (120° yatay açı) bakış
    angle  = random.uniform(-math.pi * 0.33, math.pi * 0.33)
    # Kamera zemin seviyesinde
    cam_h  = random.uniform(h_min, h_max)

    cam.location = mathutils.Vector((
        target_loc.x - dist * math.sin(angle),  # nesnenin önünde
        target_loc.y - dist * math.cos(angle),
        cam_h,                                   # zemine yakın sabit yükseklik
    ))

    # Kamera nesnenin merkezine doğrudan baktırılır
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
        create_ground()  # terrain_dir'den otomatik rastgele seçer

        # Sınıf seç (1–3 nesne arası)
        n_objects = random.randint(1, 3)
        class_ids = random.choices([0, 1, 2], weights=weights, k=n_objects)

        # Kamera ve ışık kur
        cam = setup_camera()
        setup_lights()

        created_pairs = []  # (class_id, obj)
        for cls_id in class_ids:
            obj = creators[cls_id]()
            # Artık içerde dikey yapılıyor, burada ek rotasyona gerek yok
            ox = random.uniform(-4, 4)
            oy = random.uniform(-4, 4)
            obj.location = mathutils.Vector((ox, oy, 0)) # Zemin üzerinde (z=0)
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
    import sys
    # Komut satırı argümanlarını kontrol et: blender --python script.py -- --config path.json
    if "--" in sys.argv:
        args = sys.argv[sys.argv.index("--") + 1:]
        if args and args[0].endswith(".json"):
            config_path = Path(args[0])
            if config_path.exists():
                with open(config_path, 'r') as f:
                    new_cfg = json.load(f)
                    CONFIG.update(new_cfg)
                    print(f"✅ Harici konfigürasyon yüklendi: {config_path.name}")

    main()
