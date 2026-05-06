# Görüntü İşleme (Vision System) Planlaması

## 1. Görevler ve Algoritmalar
1. **Nesne Tespiti (Object Detection)**: 
   - İnsan, Taşıt, UAP (Uçuşa Uygun Alan Personel), UAİ (Uçuşa Uygun Alan İniş).
   - Hareket durumlarının takibi (Optical Flow veya ardışık kare analizi).
   - *Planlanan Model*: YOLOv8 / YOLOv10 (Hızlı çıkarım süresi ve yüksek isabet oranları sebebiyle).
2. **Pozisyon Kestirimi (Position Estimation)**:
   - Referans konum verileri kullanılarak ekrandaki objelerin dünya koordinatlarına dönüştürülmesi.
   - Kamera matriksi (Intrinsic) ve duruş (Extrinsic/Pose) kestirimi (PnP, homography vb.).
3. **Görüntü Eşleme (Image Matching)**:
   - SIFT / ORB veya derin öğrenme tabanlı eşleştirici algoritmalar (SuperGlue/LightGlue) kullanılarak referans görüntü ile hedefi bulma.

## 2. Optimizasyon ve Süre
- Yarışmada yaklaşık 5 dakika içerisinde 2250 kare işlenmesi gerekiyor (Yani ortalama 7.5 FPS).
- Modelin GPU veya TensorRT üzerinde optimize çalışması şart.

## 3. Haberleşme
- Sunucudan `GET` / `POST` metotları ile JSON istekleri çekilecek. İşlem tamamlandıktan sonra sonuç paketi oluşturulup tekrar sunucuya iletilecek.
- Ayrıca Panel modülüne anlık veri akışı sağlamak için sistem `FastAPI` / `Flask` ile bir websocket veya lokal API ayağa kaldıracak.
