# TEKNOFEST Havacılıkta Yapay Zeka - Sistem Mimarisi

## Genel Bakış
Proje iki ana modülden oluşmaktadır:
1. **Görüntü İşleme Modülü (Vision System)**: Sunucudan görüntüleri alan, üzerinde yapay zeka modelleri (nesne tespiti, pozisyon kestirimi, görüntü eşleme) koşturan ve sonuçları üreten sistem.
2. **Yer Kontrol İstasyonu (GCS Panel)**: Operatörün sistemi takip edeceği, kamera görüntülerini canlı olarak bounding-box'lar (sınır kutuları) ile göreceği, bağlantı durumlarını ve telemetri bilgilerini anlık izleyebileceği modern arayüz.

## İletişim ve Veri Akışı
- **Yarışma Sunucusu**: `http://IP:5000` üzerinden JSON API sunar. Görüntüleri ve telemetriyi verir, sonuçları alır.
- **Vision Core**: Yarışma sunucusu ile API haberleşmesini yönetir. Görüntüleri işler.
- **GCS Panel <-> Vision Core**: Panel, vision core üzerinden websocket veya yerel bir REST API ile beslenir. GCS Panel sadece bir "Front-end" olarak çalışırken, Vision System "Back-end" işlevini de üstlenir.

## Modüler Yapı
- `/vision`: Görüntü işleme modellerinin eğitimi, test edilmesi ve inferance (çıkarım) kodlarını barındırır.
- `/panel`: React, Vue, Next.js veya saf HTML/JS tabanlı modern GCS arayüzünü barındırır.
- `/docs`: Projenin planlamasını ve dökümantasyonunu tutar.
