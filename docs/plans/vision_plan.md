# Görüntü İşleme ve Otonomi (Vision System) Planlaması

## 1. Algılama ve Görevler
Şartnamedeki zorlu parkur ve atış görevlerini tamamlamak üzere aşağıdaki otonomi yetenekleri geliştirilecektir:
1. **Parkur ve Engel Tespiti**:
   - Parkuru sınırlayan bariyerlerin tespiti ile şerit takip algoritması.
   - Trafik Konisi (Kırmızı-beyaz/Turuncu-beyaz) tespiti ve kaçınma.
   - Kayar Engel (sürekli git-gel yapan 1 metrelik engel) tespiti ve hız ayarı ile zamanlamalı geçiş.
2. **Atış ve Hedef Tespiti**:
   - Nişan kamerası kullanılarak, 10 metre mesafedeki A3 boyutundaki hedef panosunun tespiti.
   - Hedef panosundaki iç içe geçmiş halkaların algılanması ve lazerin tam orta noktaya otonom olarak hizalanması.

## 2. Kamera Konfigürasyonu
- Araçta Şartname gereği **en az 3 kamera** bulunacaktır:
  - Ön (İleri Sürüş) Kamerası
  - Arka (Geri Sürüş) Kamerası
  - Nişan Kamerası (Atış hizalama için yüksek zoom veya dar açılı özel kamera)

## 3. Optimizasyon
- Nesne tanıma işlemleri (YOLOv8 vb. modeller ile koni ve hedef tespiti) edge cihazda (ör. Jetson Nano/Orin) çalışacak şekilde optimize edilecektir (TensorRT).
- Sensör ve kontrol döngüsü gerçek zamanlı (düşük gecikmeli) çalışmalıdır.
