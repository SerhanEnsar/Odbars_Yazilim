# 02 - Görüntü İşleme Çıktı Formatları

Bu dokümanda algoritma seçimi yapılmamıştır. Sadece her görüntü işleme görevinin sistem tarafından üretmesi gereken çıktı tanımlanmıştır.

## 1. Tabela tanıma çıktısı

```yaml
detected: true/false
stage_id: görev numarası
confidence: güven skoru
bbox: [x, y, width, height]
center_px: [x, y]
```

Alan açıklamaları:
- `detected`: Parkur aşama tabelası algılandı mı?
- `stage_id`: Tabeladan okunan parkur/görev numarası.
- `confidence`: Algılamanın güven skoru.
- `bbox`: Tabelanın görüntüdeki sınırlayıcı kutusu.
- `center_px`: Tabela merkezinin piksel koordinatı.

## 2. Hedef tespiti çıktısı

```yaml
target_detected: true/false
target_center_px: [x, y]
crosshair_center_px: [x, y]
error_px: [dx, dy]
fire_permission: true/false
```

Alan açıklamaları:
- `target_detected`: Atış hedefi algılandı mı?
- `target_center_px`: Hedef merkezinin piksel koordinatı.
- `crosshair_center_px`: Nişan merkezinin piksel koordinatı.
- `error_px`: Nişan merkezi ile hedef merkezi arasındaki piksel hatası.
- `fire_permission`: Atış için görsel hizalama uygun mu?

## 3. Koni tespiti çıktısı

```yaml
detected: true/false
cones:
  - bbox: [x, y, width, height]
    center_px: [x, y]
    relative_position: left/center/right
    distance_estimate: yakın/orta/uzak
safe_path_center_px: [x, y]
```

Alan açıklamaları:
- `detected`: Trafik konisi algılandı mı?
- `cones`: Algılanan konilerin listesi.
- `bbox`: Her koninin görüntüdeki sınırlayıcı kutusu.
- `center_px`: Her koninin merkez piksel koordinatı.
- `relative_position`: Koninin görüntü/araç eksenine göre konumu.
- `distance_estimate`: Görüntüye dayalı yaklaşık mesafe sınıfı.
- `safe_path_center_px`: Konilere temas etmeden izlenecek güvenli geçiş merkez noktası.

## 4. Kayar engel çıktısı

```yaml
detected: true/false
center_px: [x, y]
motion_direction: left/right/stationary/unknown
safe_to_pass: true/false
```

Alan açıklamaları:
- `detected`: Kayar engel algılandı mı?
- `center_px`: Kayar engelin merkez piksel koordinatı.
- `motion_direction`: Engelin hareket yönü.
- `safe_to_pass`: Engel konumu ve yönüne göre geçiş güvenli mi?

## 5. Yol/bariyer takibi çıktısı

```yaml
detected: true/false
left_boundary_px: [[x1, y1], [x2, y2]]
right_boundary_px: [[x1, y1], [x2, y2]]
road_center_px: [x, y]
heading_error_px: dx
```

Alan açıklamaları:
- `detected`: Parkur sınırları/bariyerleri algılandı mı?
- `left_boundary_px`: Sol parkur sınırı veya bariyer çizgisi.
- `right_boundary_px`: Sağ parkur sınırı veya bariyer çizgisi.
- `road_center_px`: Parkurun görüntüdeki merkez noktası.
- `heading_error_px`: Araç görüntü ekseni ile yol merkezi arasındaki piksel hatası.

## 6. Stop algılama çıktısı

```yaml
detected: true/false
stop_center_px: [x, y]
stop_zone_reached: true/false
required_wait_s: 2
stop_command: true/false
```

Alan açıklamaları:
- `detected`: Stop noktası/işareti algılandı mı?
- `stop_center_px`: Stop işaretinin veya stop bölgesinin merkez piksel koordinatı.
- `stop_zone_reached`: Araç stop bölgesine ulaştı mı?
- `required_wait_s`: Şartnamedeki bekleme süresi.
- `stop_command`: Araca dur komutu üretilmeli mi?

## 7. Geri görüş çıktısı

```yaml
obstacle_detected: true/false
obstacle_center_px: [x, y]
obstacle_relative_position: left/center/right
reverse_safe: true/false
```

Alan açıklamaları:
- `obstacle_detected`: Geri kamera görüntüsünde engel var mı?
- `obstacle_center_px`: Arkadaki engelin merkez piksel koordinatı.
- `obstacle_relative_position`: Engelin görüntü/araç eksenine göre konumu.
- `reverse_safe`: Geri hareket güvenli mi?
