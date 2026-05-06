# Yer Kontrol İstasyonu (GCS Panel) Planlaması

## 1. Temel Bileşenler
- **Bağlantı Paneli**: Yarışma sunucusunun IP ve Port bilgilerinin girileceği, API bağlantı durumunun (Ping/Gecikme) gösterileceği alan.
- **Canlı Görüntü Ekranı (Video Feed)**: Uçaktan veya sunucudan gelen canlı yayının izleneceği ana ekran.
- **Algılama Çıktıları (Bounding Boxes)**: Modelin tespit ettiği İnsan, Taşıt, UAP, UAİ alanlarının canlı ekran üzerine bindirilmesi.
- **Telemetri ve Pozisyon**: İHA'nın güncel konumu, tespit edilen hedefin hesaplanan GPS koordinatları.
- **Log ve Debug Ekranı**: Gönderilen JSON paketlerinin ve alınan yanıtların/hataların gerçek zamanlı takibi.

## 2. Tasarım Prensipleri
- **Karanlık Mod (Dark Mode)**: Göz yormaması ve modern bir havacılık arayüzü görünümü sunması için.
- **Tepkisellik (Responsive)**: Ekrana farklı widget'ların eklenebileceği grid tabanlı bir yerleşim düzeni.
- **Aesthetic**: Canlı, fütüristik renkler. Verilerin okunabilirliğini artırmak için temiz tipografi (Örn: Inter veya Roboto font).

## 3. Kullanılacak Teknolojiler
- HTML5 / Vanilla CSS ve JS (Performans ve modülerlik odaklı).
- İhtiyaç halinde Chart.js veya harita entegrasyonu için Leaflet.js.
