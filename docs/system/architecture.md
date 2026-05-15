# TEKNOFEST İnsansız Kara Aracı (İKA) - Sistem Mimarisi

## Genel Bakış
Proje, otonom ve uzaktan kumandalı sürüş yeteneklerine sahip bir İnsansız Kara Aracı (İKA) sistemini içermektedir. İki ana yazılım modülü bulunmaktadır:
1. **Araç Üzeri Yazılım & Otonomi (Vision & Control)**: Aracın üzerindeki işlemcide çalışan, kameralardan gelen verileri işleyip (şerit takibi, koni tespiti, hareketli engel tespiti, hedef panosu tespiti) aracı yönlendiren ve otonom atış kararını veren otonomi/görüntü işleme sistemi.
2. **Yer Kontrol İstasyonu (GCS Panel)**: Operatörün aracı manuel koşuda uzaktan kontrol edeceği (RF/Wi-Fi), 3 farklı kameranın (ön, arka, nişan) canlı görüntülerini izleyeceği, telemetri verilerini göreceği ve acil durdurma (E-Stop) komutunu verebileceği modern arayüz.

## İletişim ve Veri Akışı
- **GCS Panel <-> Araç (İKA)**: Araç ve yer istasyonu arasında düşük gecikmeli bir haberleşme protokolü (WebRTC üzerinden video akışı ve WebSocket/UDP üzerinden telemetri/kontrol komutları) kullanılacaktır.
- Araç üzerinde ROS (Robot Operating System) veya benzer modüler bir middleware kullanılması durumunda, GCS Paneli ROSBridge (veya özel bir API) aracılığıyla araca bağlanacaktır.

## Modüler Yapı
- `/vision`: Otonom sürüş algoritmaları, engel tanıma, atış hedefini hizalama ve 3 kameranın verilerini işleyen modüller.
- `/panel`: Aracı manuel olarak yönlendirme arayüzünü, sensör okumalarını ve kamera yayınlarını barındıran kontrol paneli.
- `/docs`: Sistematik geliştirme ve proje takibi dokümantasyonu.
